from functools import update_wrapper

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel

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
    parser.add_argument('store_id',
        type=float,
        required=True,
        help='Every item needs a store id'
    )

    @jwt_required()
    def get(self, name) :
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
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
        if ItemModel.find_by_name(name) :
            return {'message' : "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        
        item = ItemModel(name, **data)

        try :
            item.save_to_db()
        except :
            return {'message' : "An error ocurred inserting the item."}, 500 #Internal server error

        return item.json(), 201 # WHEN CREATED

    def delete(self,name) :
        """
            This method delete an item
        """
        item = ItemModel.find_by_name(name)

        if item :
            item.delete_from_db()

        return {'message' : 'Item deleted'}

    def put(self,name) :
        """
            This method can update an item or create it
        """
        
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None :
            item = ItemModel.find_by_name(name, **data)
        else : 
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource) :
    """
        This class return a list of items
    """
    def get(self) :
        # We get all the items
        #return {'item' : list(map(lambda x: x.json(), ItemModel.query.all()))} --> Only if not all python
        return {'items' : [item.json() for item in ItemModel.query.all()]}
        """ connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        results = cursor.execute(query)
        items = []

        for row in results :
            items.append({'name' : row[0], 'price' : row[1]})

        connection.close()

        return {'items' : items} """