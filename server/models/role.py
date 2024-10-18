from models import db
from sqlalchemy import Enum


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(Enum('seller', 'buyer'), nullable=False, unique=True)

    def __repr__(self):
        return f'<Role {self.name}>'
