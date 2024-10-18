from app import app
from models import Book, Review, Role, Transaction, User

if __name__ == '__main__':
    with app.app_context():
        import ipdb
        ipdb.set_trace()
