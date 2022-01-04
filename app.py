from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

# This is our app
app = Flask(__name__)
# In order to know when an object as changed but not in the db
# It will track it if True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # The db is a the root
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = "Secret"
api = Api(app)


@app.before_first_request
def create_tables() :
    db.create_all()

# This JWT object uses the app (The block above), authenticate and identity
# To allow the login feature
# It create a new endpoint (/auth)
jwt = JWT(app, authenticate, identity)

# Let the Student resource accessible via our API
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')


if __name__ == '__main__' :
    db.init_app(app)
    app.run(port=4000, debug=True)