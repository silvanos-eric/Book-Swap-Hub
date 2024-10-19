from flask import request, session
from flask_restful import Resource
from models import Book, Review, Role, User, db, user_roles

authError = 'Authentication Required', 401
roleError = 'Invalid role. Role must be either: seller or customer', 400


def validate_login():
    user_id = session.get('user_id')

    if not user_id:
        raise ValueError('Authentication Required')

    print(user_id)

    user = db.session.get(User, user_id)

    if not user:
        raise ValueError('Authentication Required')

    return user_id


def handleErrors(e):
    if isinstance(e, ValueError) and 'Auth' in str(e):
        return {'error': str(e)}, 401
    if isinstance(e, KeyError):
        return {'error': f'Missing required field: {e}'}, 400
    print(e)
    return {'error': 'An uknown error occurred'}, 500


def createUser(data):
    username = data['username']
    email = data['email']
    profile_picture = data.get('profile_picture')
    password = data['password']
    password_confirmation = data['password_confirmation']

    if password != password_confirmation:
        raise ValueError('Passwords do not match')

    new_user = User(username=username,
                    password=password,
                    email=email,
                    profile_picture=profile_picture)

    role_name = data.get('role')

    if not role_name:
        role = Role.query.filter(name='customer')

    role = Role.query.filter_by(name=role_name)
    if not role:
        raise ValueError('Invalid role. Role must be one of: seller ,customer')

    new_user.roles.append(role)


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
            error = handleErrors(e)
            return error


class BookByID(Resource):

    def get(self, id):
        book = db.session.get(Book, id)

        try:
            if not book:
                return {'error': f'Book with ID {id} not found'}, 404

            book_dict = book.to_dict()
            return book_dict
        except Exception as e:
            error = handleErrors(e)

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
            error = handleErrors(e)
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
            errors = handleErrors(e)
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
            error = handleErrors(e)
            return error


class Users(Resource):

    def get(self):
        user_list = User.query.all()
        user_dict_list = [user.to_dict() for user in user_list]

        return user_dict_list

    def post(self):
        try:
            validate_login()
            data = request.json

            new_user = createUser(data)

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id

            return new_user.to_dict, 201
        except Exception as e:
            error = handleErrors(e)
            return error


class UserByID(Resource):

    def get(self, id):
        try:
            validate_login()

            user = db.session.query(User, id)

            if not user:
                return authError

            return user.to_dict()
        except Exception as e:
            error = handleErrors(e)
            return error

    def patch(self, id):
        try:
            validate_login()

            user = db.session.get(User, id)

            if not user:
                return authError

            data = request.json
            for attr in data:
                setattr(user, attr, data[attr])

            db.session.add(user)
            db.session.commit()

            return user.to_dict()
        except Exception as e:
            error = handleErrors(e)
            return error
