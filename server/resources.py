from flask import request, session
from flask_restful import Resource
from models import Book, Review, User, db


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
            if isinstance(e, KeyError) and 'Auth' in str(e):
                return {'error': str(e)}, 401

            if isinstance(e, KeyError):
                error = f'Missing required field: {e}'

            return {'error': error}, 400


class BookByID(Resource):

    def get(self, id):
        book = db.session.get(Book, id)

        try:
            if not book:
                return {'error': f'Book with ID {id} not found'}, 404

            book_dict = book.to_dict()
            return book_dict
        except:
            return {'error': 'An unkown error occurred'}, 500

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
        except (ValueError) as e:
            if isinstance(e, ValueError) and 'Auth' in str(e):
                return {'error': str(e)}, 401
        except:
            return {'error': 'An unkown error occurred'}, 500


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
        except (KeyError, ValueError) as e:
            if isinstance(e, KeyError):
                return {'error': f'Missing required field: {e}'}
            if isinstance(e, ValueError) and 'Auth' in str(e):
                return {'error': str(e)}, 401
        except:
            return {'error', 'An unknown error occurred'}, 500


def validate_login():
    user_id = session.get('user_id')

    if not user_id:
        raise ValueError('Authentication Required')

    print(user_id)

    user = db.session.get(User, user_id)

    if not user:
        raise ValueError('Authentication Required')

    return user_id
