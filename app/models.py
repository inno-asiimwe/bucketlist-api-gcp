from app import db
from flask_bcrypt import Bcrypt 

class User(db.Model):
    """Class to define the users table"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(256), nullable=False)
    lastname = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    bucketlists = db.relationship('Bucketlist', backref='User')

    def __init__(self, firstname, lastname, username, password, email):
        """Initialising the user"""
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = Bcrypt.generate_password_hash(password).decode()
        self.email = email

    def password_is_valid(self, password):
        """Method validates password against its harsh"""
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Method saves user to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Method deletes user from database"""
        db.session.remove(self)
        db.commit()

    def __repr__(self):
        """ """
        return '<User %r>' %(self.name)

class Bucketlist(db.Model):
    """Class to define the bucketlists table"""
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    description = db.Column(db.Text)
    owner = db.Column(db.Integer, db.ForeignKey(User.id))
    items = db.relationship('Item', backref='Bucketlist')

    def __init__(self, name, description, owner):
        """Initialising the bucketlist"""
        self.name = name
        self.description = description
        self.owner = owner

    def save(self):
        """Method to save bucketlist to database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Method to delete bucketlist from database"""
        db.session.remove(self)
        db.seession.commit()

    @staticmethod
    def get_all_bucketlists(owner_id):
        """Method returns all bucketlists owned by a given user"""
        return Bucketlist.query.filter_by(owner=owner_id)

    def __repr__(self):
        """A representation for an instance of a bucketlist"""
        return '<Bucketlist: %r>' %(self.name)

class Item(db.Model):
    """Class to define the Items table"""
    __tablename__ = 'items'
    id = db.Column(db.Integr, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    description = db.Column(db.Text)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('Bucketlist.id'))

    def __init__(self, name, description, bucketlist_id):
        """Initialising an item"""
        self.name = name
        self.description = description
        self.bucketlist_id = bucketlist_id

    def __repr__(self):
        """Method to represent an instance of the item"""
        return '<Item: %r>' %(self.name)

    def save(self):
        """Method to save item to database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Method to delete item from database"""
        db.session.remove(self)
        db.seession.commit()
    
    @staticmethod
    def get_all_items(bucketlist_id):
        """Method returns all items in a given bucketlist"""
        return Item.query.filter_by(bucketlist_id=bucketlist_id)


