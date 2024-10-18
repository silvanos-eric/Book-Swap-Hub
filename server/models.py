from config import bcrypt
from email_validator import EmailNotValidError, validate_email
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, event, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

VALID_ROLES = ['seller', 'customer']

# Association table for many-to-many relationship between User and Role
user_roles = db.Table(
    'user_roles',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('users.id', ondelete='CASCADE'),
              primary_key=True),
    db.Column('role_id',
              db.Integer,
              db.ForeignKey('roles.id', ondelete='CASCADE'),
              primary_key=True))


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)  # Auto-incrementing primary key
    username = db.Column(
        db.String(50), nullable=False, unique=True
    )  # Username with max length of 50 characters, must be unique
    email = db.Column(
        db.String(255), nullable=False,
        unique=True)  # Email with max length of 255 characters, must be unique
    _password_hash = db.Column(
        db.String(255), )  # Password hash with max length of 255 characters
    profile_picture = db.Column(db.Text)  # Profile picture (optional)
    created_at = db.Column(db.DateTime, default=func.now(
    ))  # Use func.now() to set the current timestamp for creation
    updated_at = db.Column(
        db.DateTime, default=func.now(),
        onupdate=func.now())  # Automatically updated on record modification

    # Relationships
    books_for_sale = db.relationship('Book',
                                     backref='user',
                                     cascade='all, delete-orphan')
    purchased_books = association_proxy('transactions', 'book')
    reviews = db.relationship('Review',
                              backref='user',
                              cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user')

    # Many-to-many relationship with Role, using backref to implicitly define the reverse relationship in Role
    roles = db.relationship('Role',
                            secondary=user_roles,
                            backref=db.backref('users', lazy='dynamic'))

    # ORM level constraint for email column. Flexible and more robust
    @validates('email')
    def validate_email(self, _, email):
        """
        Validate the email address provided by the user and return the
        normalized email if valid, or raise a ValueError if invalid.
        """
        try:
            # Validate the email using the email-validator library
            valid = validate_email(email)
            # Return the normalized email (e.g., lowercase and trimmed)
            return valid.email
        except EmailNotValidError as e:
            # Raise an exception for invalid emails
            raise ValueError(f'Invalid email address: {e}')

    # Utility to add a role to a user
    def add_role(self, role_name):
        self.roles.append(Role.query.filter_by(name=role_name))

    # Check if the user has a specifc role
    def has_role(self, role_name):
        return any(role_name == role.name for role in self.roles)

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Private field, _password is not accessible')

    @password_hash.setter
    def password_has(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode(
            'utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    @classmethod
    def get_users_by_role(cls, role_name):
        """
        Return all users who have the specified role.
        """
        if role_name not in VALID_ROLES:
            raise ValueError(
                f'Invalid role. Role must be one of: {", ".join(VALID_ROLES)}')
        return cls.query.join(user_roles).join(Role).filter(
            Role.name == role_name).all()

    def __repr__(self):
        return f"<User {self.username}>"


class Book(db.Model, SerializerMixin):
    __tablename__ = 'books'

    id = db.Column(db.Integer,
                   primary_key=True)  # Auto-incrementing primary key
    title = db.Column(db.String(255),
                      nullable=False)  # Title of the book (required)
    author = db.Column(db.String(255),
                       nullable=False)  # Author's name (required)
    price = db.Column(db.Numeric(10, 2), nullable=False,
                      default=0.00)  # Price of the book, default is 0.00
    condition = db.Column(
        Enum('new', 'used', name='book_condition'),
        nullable=False,
        default='new'
    )  # Book condition, either 'new' or 'used', default is 'new'
    status = db.Column(
        Enum('available', 'rented', 'sold', name='book_status'),
        nullable=False,
        default='available')  # Book status, default is 'available'
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )  # Foreign key to the users table

    # Relationships
    reviews = db.relationship('Review', backref='book')
    transactions = db.relationship('Transaction', backref='_book')

    @classmethod
    def get_books_by_status(cls, status):
        return cls.query.filter_by(status=status).all()

    def __repr__(self):
        return f"<Book {self.id} : {self.title}>"


class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'

    id = db.Column(
        db.Integer,
        primary_key=True)  # Auto-incrementing ID for each transaction
    transaction_date = db.Column(
        db.DateTime, default=func.now(),
        nullable=False)  # Date of transaction, defaults to current time
    transaction_type = db.Column(
        Enum('rent', 'buy', name='transaction_type'),
        nullable=False)  # Type of transaction (rent or buy)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )  # Foreign key to User model
    book_id = db.Column(
        db.Integer,
        db.ForeignKey('books.id', ondelete='CASCADE'),
        nullable=False,
    )  # Foreign key to Book model
    returned = db.Column(
        db.Boolean, default=False, nullable=False
    )  # Status to track if the book is returned (applicable for rentals)

    @property
    def book(self):
        return self._book

    @book.setter
    def book(self, value):
        if value.status in ['sold', 'rented']:
            raise ValueError(
                f"Book '{value.title}' is already '{value.status}' and cannot be added to the transaction."
            )
        if self.transaction_type == 'buy':
            value.status = 'sold'
        elif self.transaction_type == 'rent':
            value.status = 'rented'

        self._book = value

    # ORM-level validation for transaction_type
    @validates('transaction_type')
    def validate_transaction_type(self, _, transaction_type):
        if transaction_type not in ['rent', 'buy']:
            raise ValueError(
                "Invalid transaction type. Must be either 'rent' or 'buy'.")
        return transaction_type

    def __repr__(self):
        return f"<Transaction {self.id} for Book {self.book_id}>"


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer,
                   primary_key=True)  # Auto-incrementing ID for each review
    rating = db.Column(db.Integer, nullable=False)  # Rating between 1 and 5
    comment = db.Column(db.Text, nullable=True)  # Optional review comment
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )  # Foreign key to User model
    book_id = db.Column(
        db.Integer,
        db.ForeignKey('books.id', ondelete='CASCADE'),
        nullable=False,
    )  # Foreign key to Book model

    # Database-level constraint to ensure rating is between 1 and 5
    __table_args__ = (db.CheckConstraint('rating >= 1 AND rating <= 5',
                                         name='check_rating_range'), )

    # ORM-level validation for rating
    @validates('rating')
    def validate_rating(self, _, rating):
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating

    def __repr__(self):
        return f"<Review {self.id} {self.comment}>"


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(Enum('seller', 'customer'), nullable=False, unique=True)

    def __repr__(self):
        return f'<Role {self.name}>'
