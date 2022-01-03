from db import db

class ItemModel(db.Model) :
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # Adding a store col
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # Linking store / store_id to the different items
    store = db.relationship('StoreModel')


    def __init__(self, name, price, store_id) :
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) :
        """
            Return a representation of the model
        """
        return {'name' : self.name, 'price' : self.price}

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