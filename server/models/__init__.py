from flask_sqlalchemy import SQLAlchemy

from .book import Book
from .review import Reviews
from .role import Role
from .transaction import Transactions
from .user import User
from .user_roles import user_roles as user_roles

db = SQLAlchemy()

__all__ = ['Book', 'Review', 'Role', 'Transactions', 'User']
