from sqlalchemy import Enum, func
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


class Transactions(db.Model, SerializerMixin):
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
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False,
                        ondelete='CASCADE')  # Foreign key to User model
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id'),
                        nullable=False,
                        ondelete='CASCADE')  # Foreign key to Book model
    returned = db.Column(
        db.Boolean, default=False, nullable=False
    )  # Status to track if the book is returned (applicable for rentals)

    # ORM-level validation for transaction_type
    @validates('transaction_type')
    def validate_transaction_type(self, _, transaction_type):
        if transaction_type not in ['rent', 'buy']:
            raise ValueError(
                "Invalid transaction type. Must be either 'rent' or 'buy'.")
        return transaction_type

    def __repr__(self):
        return f"<Transaction {self.id} for Book {self.book_id}>"
