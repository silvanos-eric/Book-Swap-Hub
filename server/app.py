from config import Config
# Books API
from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, User, Book, Review, Transaction
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Create a Flask instance
app = Flask(__name__)
app.config.from_object(Config)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookshub.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

api = Api(app)

# GET /books: Retrieve all books.
class Books(Resource):
    def get(self):
        all_books = [book.to_dict() for book in Book.query.all()]
        return make_response(jsonify(all_books), 200)
    
    def post(self):
        title = request.json.get('title')
        author = request.json.get('author')
        price = request.json.get('price')
        condition = request.json.get('condition')
        status = request.json.get('status')
        user_id = request.json.get('user_id')

        new_book = Book(
            title=title, author=author, price=price, condition=condition, status=status, user_id=user_id
        )
        db.session.add(new_book)
        db.session.commit()
        return make_response(new_book.to_dict(), 201)

class BookId(Resource):
    def get(self, id):
        book = Book.query.filter_by(id=id).first()
        if book:
            return make_response(jsonify(book.to_dict()), 200)
        return {'error': "Book not found"}, 404    

    def patch(self, id):
        book = Book.query.filter_by(id=id).first()
        if not book:
            return {'error': "Book not found"}, 404
        
        title = request.json.get('title', book.title)
        author = request.json.get('author', book.author)
        price = request.json.get('price', book.price)
        condition = request.json.get('condition', book.condition)
        status = request.json.get('status', book.status)

        book.title = title
        book.author = author
        book.price = price
        book.condition = condition
        book.status = status

        db.session.commit()
        return make_response(book.to_dict(), 200)

    def delete(self, id):
        book = Book.query.filter_by(id=id).first()
        if not book:
            return {'error': "Book not found"}, 404
        
        db.session.delete(book)
        db.session.commit()
        return {'message': "Book deleted successfully"}, 200

class ReviewResource(Resource):
    def post(self, book_id):
        content = request.json.get('content')
        user_id = request.json.get('user_id')

        new_review = Review(content=content, book_id=book_id, user_id=user_id)
        db.session.add(new_review)
        db.session.commit()
        return make_response(new_review.to_dict(), 201)

    def get(self, book_id):
        reviews = [review.to_dict() for review in Review.query.filter_by(book_id=book_id).all()]
        return make_response(jsonify(reviews), 200)

class TransactionResource(Resource):
    def get(self):
        try:
            transactions = [transaction.to_dict() for transaction in Transaction.query.all()]
            return make_response(jsonify(transactions), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    def post(self):
        # Extract and validate JSON request body
        transaction_data = request.get_json()
        transaction_date_str = transaction_data.get('transaction_date')
        transaction_type = transaction_data.get('transaction_type')
        user_id = transaction_data.get('user_id')
        book_id = transaction_data.get('book_id')

        # Validation for required fields
        if not all([transaction_date_str, transaction_type, user_id, book_id]):
            return make_response(jsonify({"error": "Missing required fields"}), 400)

        # Check if transaction_type is valid
        if transaction_type not in ['purchase', 'sale', 'rent']:
            return make_response(jsonify({"error": "Invalid transaction_type, select either: 'purchase', 'sale', 'rent'"}), 400)

        # Convert transaction_date to a datetime object
        try:
            transaction_date = datetime.strptime(transaction_date_str, "%Y-%m-%d")
        except ValueError:
            return make_response(jsonify({"error": "Invalid date format. Expected YYYY-MM-DD."}), 400)
        
        # Verify if the user exists
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User with ID {} does not exist.".format(user_id)}), 404)

        # Verify if the book exists
        book = Book.query.get(book_id)
        if not book:
            return make_response(jsonify({"error": "Book with ID {} does not exist.".format(book_id)}), 404)


        # Attempt to create and save the new transaction
        try:
            new_transaction = Transaction(
                transaction_date=transaction_date, 
                transaction_type=transaction_type,
                user_id=user_id,
                book_id=book_id
            )
            db.session.add(new_transaction)
            db.session.commit()

            return make_response(jsonify({
                'message': "Transaction successful",
                'transaction_details': new_transaction.to_dict()
            }), 201)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)

api.add_resource(TransactionResource, '/transactions')
    

class UserResource(Resource):
    def post(self):
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')  # Ensure this is fetched
        profile_picture = request.json.get('profile_picture')

        print(f"Request data: {request.json}")  # Debug logging

        if not username or not email or not password:
            return {'error': 'Username, email, and password must be provided.'}, 400
        
        if len(password) < 8:
            return {'error': "Password must be at least 8 characters long."},400
        

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        try:
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                profile_picture=profile_picture
            )
            db.session.add(new_user)
            db.session.commit()
            return make_response(new_user.to_dict(), 201)
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Username or email already exists'}, 400
        except Exception as exc:
            db.session.rollback()
            return {'error': 'Error creating account', 'details': str(exc)}, 500

class AuthResource(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user.password is None:
            return {'error': 'Password not found for this user.'}, 500
        
        if bcrypt.check_password_hash(user.password, password):
            return {'message': 'Login successful'}, 200
            
        return {'error': 'Invalid credentials'}, 401

api.add_resource(Books, '/books')
api.add_resource(BookId, '/books/<int:id>')
api.add_resource(ReviewResource, '/books/<int:book_id>/reviews')
api.add_resource(UserResource, '/users/signup')
api.add_resource(AuthResource, '/users/login')

@app.route('/')
def index():
    return "<h1> Hello, Welcome to Books Swap Hub<h1>"

if __name__ == '__main__':
    app.run(debug=True, port=5555)
