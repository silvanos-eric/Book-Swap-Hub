from flask import request, session
from flask_restful import Resource
from models import Book, Review, Role, Transaction, User, db
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

authError = 'Authentication Required.'
credentialsError = "Invalid email/password"


def validate_login():
    user_id = session.get('user_id')

    if not user_id:
        raise ValueError('Authentication Required.')

    print(user_id)

    user = db.session.get(User, user_id)

    if not user:
        raise ValueError('Authentication Required.')

    return user_id


def handleException(e):
    if isinstance(e, ValueError) and 'Auth' in str(e):
        return {'error': 'Bad Request', 'message': str(e)}, 401
    if isinstance(e, ValueError) and 'not found' in str(e).lower():
        return {'error': 'Bad Request', 'message': str(e)}, 404
    if isinstance(e, ValueError):
        return {'error': 'Bad Request', 'message': str(e)}, 400
    if isinstance(e, KeyError):
        return {
            'error': 'Bad Request',
            'message': f'Missing required field: {e}.'
        }, 400
    if isinstance(e, BadRequest):
        return {
            'error':
            'Bad Request',
            'message':
            'Malformed JSON body. Please ensure the properties provided are well formatted.'
        }, 400
    if isinstance(e, IntegrityError) and 'UNIQUE' in str(
            e) and 'users.username' in str(e):
        return {
            'error': 'Account creation failed',
            'message': 'Username already taken.'
        }, 400
    if isinstance(
            e,
            IntegrityError) and 'UNIQUE' in str(e) and 'users.email' in str(e):
        return {
            "error": "Account creation failed",
            "message": "Email already taken. Log in or reset password"
        }, 400

    print(f'***{type(e)}***')
    print(f'***{(e)}***')
    return {'error': 'An uknown error occurred'}, 500


def createUser(data):
    username = data['username']
    email = data['email']
    profile_picture = data.get('profile_picture')
    password = data['password']
    password_confirmation = data['confirm_password']

    if password != password_confirmation:
        raise ValueError('Passwords do not match')

    new_user = User(username=username,
                    email=email,
                    profile_picture=profile_picture)
    new_user.password_hash = password

    role_name = data.get('role')

    if role_name is None:
        role_name = 'customer'

    role = Role.query.filter_by(name=role_name).first()

    new_user.roles.append(role)

    return new_user


class Books(Resource):

    def get(self):
        book_list = Book.query.all()
        book_dict_list = [book.to_dict() for book in book_list]

        return book_dict_list

    def post(self):
        try:
            _, user_id = validate_login()

            data = request.json
            title = data['title']
            author = data['author']
            price = data['price']
            condition = data['condition']

            new_book = Book(title=title,
                            author=author,
                            price=price,
                            condition=condition,
                            user_id=user_id)

            db.session.add(new_book)
            db.session.commit()

            return new_book.to_dict, 201

            # TODO: Complete logic after building auth routes
        except (KeyError, ValueError) as e:
            error = handleException(e)
            return error


class BookByID(Resource):

    def get(self, id):
        book = db.session.get(Book, id)

        try:
            if not book:
                raise ValueError(f'Book with ID {id} not found')

            book_dict = book.to_dict()
            return book_dict
        except Exception as e:
            error = handleException(e)
            return error

    def patch(self, id):
        try:
            validate_login()
            data = request.json

            book = db.session.get(Book, id)

            for attr in data:
                setattr(book, attr, data[attr])

            db.session.add(book)
            db.session.commit(book)

            # TODO: Complete logic after implementing auth routes
        except Exception as e:
            error = handleException(e)
            return error


class Reviews(Resource):

    def get(self):
        review_list = Review.query.all()

        review_dict_list = [review.to_dict() for review in review_list]

        return review_dict_list

    def post(self):
        try:
            user_id = validate_login()
            data = request.json

            rating = data['rating']
            comment = data.get('comment')
            book_id = data['book_id']

            new_review = Review(rating=rating,
                                comment=comment,
                                user_id=user_id,
                                book_id=book_id)

            db.session.add(new_review)
            db.session.commit()

            return new_review.to_dict(), 201
        except Exception as e:
            errors = handleException(e)
            return errors


class ReviewByID(Resource):

    def get(self, id):
        review = db.session.get(Review, id)

        return review.to_dict()

    def patch(self, id):
        try:
            validate_login()

            data = request.json

            review = db.session.get(Review, id)

            for attr in data:
                setattr(review, attr, data[attr])

            db.session.add(review)
            db.session.commit()

            #TODO: Complete logic after implementing auth routes
        except Exception as e:
            error = handleException(e)
            return error


class Users(Resource):

    def get(self):
        try:
            validate_login()
            user_list = User.query.all()
            user_dict_list = [
                user.to_dict(rules=('-transactions', )) for user in user_list
            ]
            return user_dict_list
        except Exception as e:
            error = handleException(e)
            return error

    def post(self):
        try:
            validate_login()
            data = request.snake_case_data

            new_user = createUser(data)

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id

            return new_user.to_dict, 201
        except Exception as e:
            error = handleException(e)
            return error


class UserByID(Resource):

    def get(self, id):
        try:
            # validate_login()

            user = db.session.get(User, id)

            if not user:
                raise ValueError(authError)

            return user.to_dict()
        except Exception as e:
            error = handleException(e)
            return error

    def patch(self, id):
        try:
            validate_login()

            user = db.session.get(User, id)

            if not user:
                raise ValueError(authError)

            data = request.json
            for attr in data:
                setattr(user, attr, data[attr])

            db.session.add(user)
            db.session.commit()

            return user.to_dict()
        except Exception as e:
            error = handleException(e)
            return error


class SignUp(Resource):

    def post(self):
        try:
            data = request.snake_case_data

            new_user = createUser(data)

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id

            return new_user.to_dict(), 201

        except Exception as e:
            error = handleException(e)
            return error


class CheckSession(Resource):

    def get(self):
        try:
            user_id = validate_login()

            user = db.session.get(User, user_id)

            if not user:
                raise ValueError(authError)

            return user.to_dict()
        except Exception as e:
            error = handleException(e)
            return error


class ClearSession(Resource):

    def delete(self):
        session.pop('user_id', None)

        return {}, 200


class Logout(Resource):

    def delete(self):
        try:
            validate_login()
            session.pop('user_id', None)
        except Exception as e:
            error = handleException(e)
            return error

        return {}


class Login(Resource):

    def post(self):
        try:
            data = request.json

            email = data.get('email')
            username = data.get('username')

            if not email and not username:
                raise ValueError('Please provide a username or email.')

            password = data['password']

            # Check is user exists
            user = None
            if email:
                user = User.query.filter_by(email=email).first()
            if username:
                user = User.query.filter_by(username=username).first()

            if not user:
                raise ValueError(credentialsError)

            # Check the password
            if not user.authenticate(password):
                raise ValueError(credentialsError)

            # Log in the user
            session['user_id'] = user.id

            return user.to_dict()
        except Exception as e:
            error = handleException(e)
            return error


class Transactions(Resource):

    def get(self):
        try:
            validate_login()

            transaction_list = Transaction.query.all()

            transaction_dict_list = [
                transaction.to_dict() for transaction in transaction_list
            ]

            return transaction_dict_list
        except Exception as e:
            error = handleException(e)
            return error

    def post(self):
        try:
            user_id = validate_login()

            data = request.snake_case_data

            transaction_type = data['transaction_type']
            book_id = data['book_id']

            book = db.session.get(Book, book_id)

            if not book:
                raise ValueError(f'Book with ID {book_id} not found.')

            new_transaction = Transaction(transaction_type=transaction_type,
                                          user_id=user_id)

            new_transaction.book = book

            db.session.add(new_transaction)
            db.session.commit()

            return new_transaction.to_dict(), 201
        except Exception as e:
            error = handleException(e)
            return error
