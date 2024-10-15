from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy() #initializes the database

class Review(db.Model, SerializerMixin): #association table
    __tablename__ = 'reviews'
    
    #serialize rules
    serialize_rules = ('-book.reviews', '-user.reviews',)

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
    serialize_rules = ('-reviews.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    profile_picture = db.Column(db.String)

    # relationships
    reviews = db.relationship('Review', back_populates='user')
    books = association_proxy('reviews', 'book', creator=lambda bookObj: Review(book=bookObj))
    transactions = db.relationship('Transaction', back_populates='user')

class Book(db.Model, SerializerMixin):
    __tablename__ = 'books'

    #serialize rules
    serialize_rules = ('-reviews.book',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    price = db.Column(db.Integer)
    condition = db.Column(db.Boolean)
    status = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # relationships
    reviews = db.relationship('Review', back_populates='book')
    users = association_proxy('reviews', 'user', creator=lambda userObj: Review(user=userObj))
    transactions = db.relationship('Transaction', back_populates='book')

class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'

    #serialize rules
    serialize_rules = ('-book.transactions', 'user.transactions')

    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime)
    transaction_type = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))

    #relationships
    book = db.relationship('Book', back_populates='transactions')
    user = db.relationship('User', back_populates='transactions')