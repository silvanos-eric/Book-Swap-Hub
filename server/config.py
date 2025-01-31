import os

from flask import Flask
from flask_bcrypt import Bcrypt
from utils import generate_secret_key

SECRET_KEY = os.getenv('SECRET_KEY') or generate_secret_key()
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or 'sqlite:///bookshub.db'

print('SECRET_KEY', SECRET_KEY)
print('DATABASE_URI', SQLALCHEMY_DATABASE_URI)

# Create a Flask instance
app = Flask(__name__, static_folder='../client/dist', static_url_path='')
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialize bcrypt
bcrypt = Bcrypt(app)
