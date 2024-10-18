from email_validator import EmailNotValidError, validate_email
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin


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
        db.String(255),
        nullable=False)  # Password hash with max length of 255 characters
    profile_picture = db.Column(db.Text)  # Profile picture (optional)
    created_at = db.Column(db.DateTime, default=func.now(
    ))  # Use func.now() to set the current timestamp for creation
    updated_at = db.Column(
        db.DateTime, default=func.now(),
        onupdate=func.now())  # Automatically updated on record modification

    # Basic database constraint for email column
    __table_args__ = (db.CheckConstraint(
        "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'",
        name='check_email_format'), )

    # Relationships
    books = db.relationship('Book',
                            backref='user',
                            cascade='all, delete-orpan')
    reviews = db.relationship('Review',
                              backref='user',
                              cascade='all, delete-orpan')
    transactions = db.relationship('Transaction', backref='user')

    # Many-to-many relationship with Role, using backref to implicitly define the reverse relationship in Role
    roles = db.relationship('Role',
                            secondary=user_roles,
                            backref=db.backref('users', lazy='dynamic'))

    # Serialization config

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
        role = Role.query.filter_by(name=role_name)

    # Check if the user has a specifc role
    def has_role(self, role_name):
        return any(role_name == role.name for role in self.roles)

    def __repr__(self):
        return f"<User {self.username}>"
