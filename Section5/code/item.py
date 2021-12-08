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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        cursor.close()

        if row :
            return {'item' : {'name' : row[0], 'price' : row[1]}}
        return {'message' : 'Item not found'}, 404
        """
            # The next allows us to return the first time an item is found
            item = next(filter(lambda x: x['name'] == name, items), None)
            return {'item' : item}, 200 if item else 404 # NOT FOUND
        """

    def post(self,name) :
        """
            This is how you use JSON payload
            If there is no payload or the request does not have the proper content-type header
            There will be an error 
            force = True --> this allow us to only look at content and skip header if None
            silent = True --> Return None
        """
        # We want to check for errors first
        if next(filter(lambda x: x['name'] == name, items), None) :
            return {'message' : 'An item with name "{}" already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name' : name, 'price' : data['price']}
        items.append(item)
        return item, 201 # WHEN CREATED

    def delete(self,name) :
        """
            This method delete an item
        """
        global items
        items = list(filter(lambda x : x['name'] != name, items))
        return {'message' : 'Item deleted'}

    def put(self,name) :
        """
            This method can update an item or create it
        """
        
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None :
            item = {'name' : name, 'price' : data['price']}
            items.append(item)
        else :
            item.update(data)

        return item

class ItemList(Resource) :
    """
        This class return a list of items
    """
    def get(self) :
        return {'items' : items}