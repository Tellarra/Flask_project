from flask import Flask, jsonify, request, render_template

# Create an object of Flask
app = Flask(__name__)
stores = [
    {
        'name': 'My wonderful store',
        'items': [
            {
            'name' : 'My item',
            'price' : 15.99
            }
        ]
    }
]

@app.route('/')
def home() :
    return render_template('index.html')

# POST - used to receive data
# GET - used to send data back only

# POST /store data: {name:} --> Create new store with name
# Create route
# app.route - by default is a get request
# THIS IS AN ENDPOINT
@app.route('/store', methods=['POST'])
def create_store() :
    """
        Must retunr a response back to the browser
    """
    request_data = request.get_json() 
    new_store = {
        'name' : request_data['name'],
        'items' : []
    }

    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name> --> Return data about it
@app.route('/store/<string:name>')
def get_store(name) :
    # Iterate over stores
    # If store name match, return it
    # If none match, return error
    for store in stores :
        if store['name'] == name :
            return jsonify(store)
    return jsonify({'message' : 'Store not found'})

# GET /store --> Return list of the store 
@app.route('/store')
def get_stores() :
    # Convert store variables into json
    return jsonify({'stores' : stores})

# POST /store/<string:name>/item {name:, price:} --> Create an item inside a specific store with a name
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name) :
    """
        Create a new item and return it
    """

    request_data = request.get_json()
    for store in stores :
        if store['name'] == name :
            new_item = {
                'name' : request_data['name'],
                'price' : request_data['price']

            }
            store['items'].append(new_item)
            return jsonify(new_item)
    
    return jsonify({'message' : 'Store not found'})

# GET /store/<string:name>/item --> Get all items in a specific store
@app.route('/store/<string:name>/item')
def get_item_in_store(name) :
    """ 
        Iterate over stores
        If store name match, return the items
        If none match, return error
    """
    for store in stores :
        if store['name'] == name :
            return jsonify({'items' : store['items']})

    return jsonify({'message' : 'Store not found'})


# Port - Area of computer where it will receive the request + return response
app.run(port=4000)

