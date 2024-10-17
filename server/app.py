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
    """GETs all books, POSTs a new book"""
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

        if not all (['title', 'author', 'price', 'condition', 'status', 'user_id']):
            return make_response({'error': "Missing required fields"}, 400)

        if not isinstance(title, str) or len(title) <= 0:
            return make_response(jsonify({"error": "Title must be a string and cannot be empty!"}), 400)

        if condition not in ['new', 'used']:
            return {'error': "Book condition is either 'new' or 'used'"}, 400

        if status not in ['rent', 'sale']:
            return {'error': "Book status is either 'rent' or 'sale'"}, 400

        # Verify if the user exists
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User with ID {} does not exist.".format(user_id)}), 404)


        new_book = Book(
            title=title, author=author, price=price, condition=condition, status=status, user_id=user_id
        )
        db.session.add(new_book)
        db.session.commit()
        return make_response(new_book.to_dict(), 201)

class BookId(Resource):
    """GETs a book by id, PATCHes and DELETEs a book"""

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
        return {'message': "You have successfully deleted the '{}' book".format(book.title)}, 200

class BookReviews(Resource):
    """GETs all reviews of a book, POSTs a new review for a book"""
    def get(self, book_id):
        reviews = [review.to_dict() for review in Review.query.filter_by(book_id=book_id).all()]
        return make_response(jsonify(reviews), 200)

    def post(self, book_id):
        rating = request.json.get('rating')
        comment = request.json.get('comment')
        user_id = request.json.get('user_id')
        book_id = request.json.get('book_id')

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {'error': "Rating must be an integer within 1 to 5"}, 400

        new_review = Review(rating=rating, comment=comment, book_id=book_id, user_id=user_id)
        db.session.add(new_review)
        db.session.commit()
        return make_response(new_review.to_dict(), 201)


class Transactions(Resource):
    """GETs all existing transactions, POSTs a new transaction for a book"""
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


class TransactionId(Resource):
    """GETs details for a single transaction, DELETEs a transaction"""
    def get(self, id):
        try:
            transaction = Transaction.query.filter(Transaction.id == id).first().to_dict()
            return make_response(jsonify(transaction), 200)
        except Exception as e:
            return make_response(jsonify({'error': "str(e)"})), 500

    def delete(self, id):
        transaction = Transaction.query.get(id)
        if not transaction:
            return {'error': "Transaction not found"}, 404
        
        db.session.delete(transaction)
        db.session.commit()
        return {'message': "You have successfully deleted the transaction for book {}".format(transaction.book_id)}, 200
   

class UserSignUp(Resource):
    """Authenticates and creates a new user"""
    def post(self):
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        profile_picture = request.json.get('profile_picture')

        #verifies all user sign up credentials are valid
        if not username or not email or not password:
            return {'error': 'Username, email, and password must be provided.'}, 400
        
        user = User.query.filter_by(email=email).first()
        if user:
            return make_response({'error': "Email already in use"})

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
            return make_response({"message": "Account created successfully", "details": new_user.to_dict()}, 201)

        except Exception as exc:
            db.session.rollback()
            return {'error': 'Error creating account', 'details': str(exc)}, 400

class UserLogin(Resource):
    """validates an existing user's credential"""
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return make_response({'error': 'User account for _{}_ not found'.format(username)}, 404)
        
        if not bcrypt.check_password_hash(user.password, password):
            return make_response({'error': "Password is incorrect"}, 401)

        return {'message': 'Welcome back {}. Glad to see you again.'.format(user.username)}, 200

  #hover over the class names to see what each route does    
api.add_resource(Books, '/books')
api.add_resource(BookId, '/books/<int:id>')
api.add_resource(BookReviews, '/books/<int:book_id>/reviews')
api.add_resource(Transactions, '/books/transactions')
api.add_resource(TransactionId, '/books/transactions/<int:id>')
api.add_resource(UserSignUp, '/user/signup') 
api.add_resource(UserLogin, '/user/login')

@app.route('/')
def index():
    return "<h1> Hello, Welcome to Books Swap Hub<h1>"

if __name__ == '__main__':
    app.run(debug=True, port=5555)
