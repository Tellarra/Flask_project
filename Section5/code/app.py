from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList
# This is our app
app = Flask(__name__)
app.secret_key = "Secret"
api = Api(app)

# This JWT object uses the app (The block above), authenticate and identity
# To allow the login feature
# It create a new endpoint (/auth)
jwt = JWT(app, authenticate, identity)

# Let the Student resource accessible via our API
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=4000, debug=True)