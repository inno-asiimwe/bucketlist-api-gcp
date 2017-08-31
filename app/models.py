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

    def __init__(self, firstname, lastname, username, password, email):
        """Initialising the user"""
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = Bcrypt.generate_password_hash(password).decode()