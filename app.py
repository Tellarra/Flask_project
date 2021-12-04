from flask import Flask

# Create an object of Flask
app = Flask(__name__)

# POST - used to receive data
# GET - used to send data back only

# POST /store data: {name:} --> Create new store with name
# GET /store/<string:name> --> Return data about it
# GET /store --> Return list of the store 
# POST /store/<string:name>/item {name:, price:} --> Create an item inside a specific store with a name
# GET /store/<string:name>/item --> Get all items in a specific store

# Create route
# app.route - by default is a get request
@app.route('/store', methods=['POST'])

def home() :
    """
        Must retunr a response back to the browser
    """
    return "Hello, world!"

# Port - Area of computer where it will receive the request + return response
app.run(port=4000)

