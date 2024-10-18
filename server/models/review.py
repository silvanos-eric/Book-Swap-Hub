from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer,
                   primary_key=True)  # Auto-incrementing ID for each review
    rating = db.Column(db.Integer, nullable=False)  # Rating between 1 and 5
    comment = db.Column(db.Text, nullable=True)  # Optional review comment
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False,
                        ondelete='CASCADE')  # Foreign key to User model
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id'),
                        nullable=False,
                        ondelete='CASCADE')  # Foreign key to Book model

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
