from db import db

class StoreModel(db.Model) :
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # It is a query builder that has the ability to look in the items
    # This architecture is a bit low because it needs to access the items tables everytime
    # Without the lazy and the all it is faster but can trigger errors in our case
    items = db.relationship('ItemModel', lazy='dynamic') 

    def __init__(self, name) :
        self.name = name

    def json(self) :
        """
            Return a representation of the model
        """
        return {'name' : self.name, 'items' : [item.json() for item in self.items.all()]}

    @classmethod # Because return an object as opposed to a dict
    def find_by_name(cls, name) :
        """
            This method will return the first item
            that matches the name
        """
        # We are doing a query user the SQLAlch
        # This query will use our model
        return cls.query.filter_by(name=name).first() # SELECT * FROM item WHERE name=name LIMIT 1
        """
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "SELECT * FROM items WHERE name=?"
            result = cursor.execute(query, (name,))
            row = result.fetchone()
            cursor.close()

            if row :
                # cls calls the __init__
                return cls(*row) # Argument unpacking row[0], row[1]
        """
    def save_to_db(self) :
        """
            Saving the model to the db
        """
        # A collection of object that we will add to our db
        db.session.add(self)
        db.session.commit()

        """
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "INSERT INTO items VALUES (?, ?)"
            cursor.execute(query, (self.name, self.price))

            connection.commit()
            connection.close()
        """
        
    def delete_from_db(self) :
        db.session.delete(self)
        db.session.commit()