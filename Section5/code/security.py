from werkzeug.security import safe_str_cmp
from user import User

"""
    # Table of users
    users = [
        User(1, 'Bob', 'test')
    ]

    # Have an index on user
    # This is a mapping to retrieve users by username and id
    username_mapping = { u.username : u for u in users }
    userid_mapping = { u.id : u for u in users }
"""
def authenticate(username, password) :
    """
        This method is used when the user authenticate
        i.e sends in the auth endpoint
        user = Create a user object
    """
    user = User.find_by_username(username)

    # Compare a user to the mapping password
    # If match then return user and generate JWT token
    if user and safe_str_cmp(user.password, password) :
        return user

def identity(payload) :
    """
        This method is used when user request an endpoint, 
        where they need to be authenticated
        We get a payload comming from request
        user_id = the identity from the payload which is the user id
    """
    user_id = payload['identity']
    return User.find_by_id(user_id)