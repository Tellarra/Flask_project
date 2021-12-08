import sqlite3
from flask_restful import Resource, reqparse

class User :

    def __init__(self, _id, username, password) :
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username) :
        """
            This method is used to retrieve a user in the db
        """
        # First -> Set up connection
        connection = sqlite3.connect('data.db')
        # Then cursor
        cursor = connection.cursor()
        # Then query
        # Where = filter and ? = parameter
        query = "SELECT * FROM users WHERE username=?" 
        # parameter always need to be a tuple, the comma is used to render the brackets not useless
        result = cursor.execute(query, (username,))
        # Get first row
        row =result.fetchone()

        if row :
            user = cls(*row) #first, second and third col
        else :
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id) :
        """
            This method is used to retrieve a user in the db
        """
        # First -> Set up connection
        connection = sqlite3.connect('data.db')
        # Then cursor
        cursor = connection.cursor()
        # Then query
        # Where = filter and ? = parameter
        query = "SELECT * FROM users WHERE id=?" 
        # parameter always need to be a tuple, the comma is used to render the brackets not useless
        result = cursor.execute(query, (_id,))
        # Get first row
        row =result.fetchone()

        if row :
            user = cls(*row) #first, second and third col
        else :
            user = None

        connection.close()
        return user

class UserRegister(Resource) :
    # Better to use Resource as of endpoint
    # Because it allows us to do only post

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help='This field cannot be blank'
    )

    parser.add_argument('password',
        type=str,
        required=True,
        help='This field cannot be blank'
    )

    def post(self) :
        data = UserRegister.parser.parse_args()
        
        # Check if user exists before establishing connection
        if User.find_by_username(data['username']) :
            return {'message' : 'A user with that username already exists'}, 400
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message' : 'User created successfully'}
