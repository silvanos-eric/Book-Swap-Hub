import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from models import db
from sqlalchemy import MetaData
from utils import generate_secret_key

SECRET_KEY = os.environ.get('SECRET_KEY') or generate_secret_key()
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URI') or 'sqlite:///bookshub.db'

# Create a Flask instance
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialize extensions
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    })

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

api = Api(app)
