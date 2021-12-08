import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource) :
    """
        This classcan :
        - Get an item which is in the memory
        - Create a new item or return a message
    """
    #Implement a decorator
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )
    @jwt_required()
    def get(self, name) :
        item = self.find_by_name(name)

        if item:
            return item
        return {'message' : 'Item not found'}, 404
        """
            # The next allows us to return the first time an item is found
            item = next(filter(lambda x: x['name'] == name, items), None)
            return {'item' : item}, 200 if item else 404 # NOT FOUND
        """

    @classmethod
    def find_by_name(cls, name) :
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        cursor.close()

        if row :
            return {'item' : {'name' : row[0], 'price' : row[1]}}

    def post(self,name) :
        """
            This is how you use JSON payload
            If there is no payload or the request does not have the proper content-type header
            There will be an error 
            force = True --> this allow us to only look at content and skip header if None
            silent = True --> Return None
        """
        # We want to check for errors first
        if self.find_by_name(name) :
            return {'message' : 'An item with name "{}" already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name' : name, 'price' : data['price']}

        try :
            self.insert(item)
        except :
            return {'message' : "An error ocurred inserting the item."}, 500 #Internal server error

        return item, 201 # WHEN CREATED

    @classmethod
    def insert(cls,item) :
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self,name) :
        """
            This method delete an item
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message' : 'Item deleted'}

    def put(self,name) :
        """
            This method can update an item or create it
        """
        
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name' : name, 'price' : data['price']}

        if item is None :
            try :
                self.insert(updated_item)
            except :
                return {'message' : "An error ocurred inserting the item."}, 500 #Internal server error
        else : 
            try :
                self.update(updated_item)
            except :
                return {'message' : "An error ocurred updating the item."}, 500 #Internal server error

        return updated_item

    @classmethod
    def update(cls, item) :
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

class ItemList(Resource) :
    """
        This class return a list of items
    """
    def get(self) :
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        results = cursor.execute(query)
        items = []

        for row in results :
            items.append({'name' : row[0], 'price' : row[1]})

        connection.close()

        return {'items' : items}