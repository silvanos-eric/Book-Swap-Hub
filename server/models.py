from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Enum
from sqlalchemy.orm import validates
import re

db = SQLAlchemy() #initializes the database

class Review(db.Model, SerializerMixin): #association table
    __tablename__ = 'reviews'
    
    #serialize rules
    # serialize_rules = ('-book.reviews', '-user.reviews', '-book.users', '-user.books')
    serialize_only = ('id', 'rating', 'comment', 'user_id', 'book_id')

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))

    # relationships
    book = db.relationship('Book', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    #serialize rules
    serialize_rules = ('-reviews.user', '-books.users', 'reviews.book', '-transactions.user')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String)

    # relationships
    reviews = db.relationship('Review', back_populates='user')
    books = association_proxy('reviews', 'book', creator=lambda bookObj: Review(book=bookObj))
    transactions = db.relationship('Transaction', back_populates='user')
    
    @validates('email')
    def validate_email(self, key, email):
        if not self.is_valid_email(email):
            raise ValueError("Invalid email format")
        return email
    
    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return password   
          
    @validates('username')
    def validate_username(self, key, username):
        user = User.query.filter_by(username=username).first()    

        if user:
            raise ValueError("Username already exists")
        return username
    
    @staticmethod
    def is_valid_email(email):
        """Checks if the email format is valid using regex."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

class Book(db.Model, SerializerMixin):
    __tablename__ = 'books'

    #serialize rules
    serialize_rules = ('-reviews.book', '-users.books', '-reviews.user', '-transactions.book')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    condition = db.Column(Enum('new', 'used', name='book_condition'), nullable=False, default='new') #used or new
    status = db.Column(Enum('rent', 'sale', name='book_status'), nullable=False, default='rent') #rent or sale
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationships
    reviews = db.relationship('Review', back_populates='book')
    users = association_proxy('reviews', 'user', creator=lambda userObj: Review(user=userObj))
    transactions = db.relationship('Transaction', back_populates='book')

class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'

    #serialize rules
    serialize_rules = ('-book.transactions', 'user.transactions', '-book.reviews', '-user.reviews')

    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime)
    transaction_type = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))

    #relationships
    book = db.relationship('Book', back_populates='transactions')
    user = db.relationship('User', back_populates='transactions')