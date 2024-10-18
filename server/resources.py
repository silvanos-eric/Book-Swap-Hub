from flask import request, session
from flask_restful import Resource
from models import Book, db


class Books(Resource):

    def get(self):
        book_list = Book.query.all()
        book_dict_list = [book.to_dict() for book in book_list]

        return book_dict_list

    def post(self):
        try:
            user_id = session.get('user_id')

            if not user_id:
                return {'error': 'Authentication required'}, 401

            data = request.json
            title = data['title']
            author = data['author']
            price = data['price']
            condition = data['condition']

            new_book = Book(title=title,
                            author=author,
                            price=price,
                            condition=condition)
            db.session.add(new_book)
            db.session.commit()

            # TODO: Complete logic after building auth routes
        except (KeyError, ValueError) as e:

            if isinstance(e, KeyError):
                error = f'Missing required field: {e}'

            return {'error': error}, 400
