from db import db

# This a model --> Our internal representation of entity
# It is a helper
class UserModel(db.Model) :
    # Because we use users in our query
    # We need to tell sqlAlch the table name where 
    # This models are gonna be stored
    __tablename__ = 'users'

    # Tel what col we want the table to contain

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password) :
        self.username = username
        self.password = password

    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username) :
        """
            This method is used to retrieve a user in the db
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id) :
        """
            This method is used to retrieve a user in the db
        """
        return cls.query.filter_by(id=_id).first()