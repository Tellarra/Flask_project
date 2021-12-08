import sqlite3
from sqlite3.dbapi2 import connect

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