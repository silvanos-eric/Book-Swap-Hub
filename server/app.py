from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, User, Book, Review, Transaction

# Create a Flask instance
app = Flask(__name__)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookshub.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app) # Add extensions to use with flask

# GET /books: Retrieve all books.
class Books(Resource):

    def get(self):
        all_books = [book.to_dict() for book in Book.query.all()]
        return make_response(jsonify(all_books), 200)

api.add_resource(Books, '/books')


@app.route('/')
def index():
    return "<h1> Hello, Welcome to Books Swap Hub<h1>"

if __name__ == '__main__':
    app.run(debug=True, port=5555)
