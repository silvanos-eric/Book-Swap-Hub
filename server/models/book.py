from sqlalchemy import Enum
from sqlalchemy_serializer import SerializerMixin


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
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False,
                        ondelete='CASCADE')  # Foreign key to the users table

    # Relationships
    reviews = db.relationship('Review', backref='book')
    transactions = db.relationship('Tranasction', backref='book')

    def __repr__(self):
        return f"<Book {self.id} : {self.title}>"
