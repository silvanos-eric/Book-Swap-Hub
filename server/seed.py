import random as rc
from datetime import datetime

from app import app
from faker import Faker
from models import Book, Review, Role, Transaction, User, db, user_roles


def seed():
    # Initialize Faker
    fake = Faker()

    # Reset database
    db.session.query(user_roles).delete()
    Role.query.delete()
    User.query.delete()
    Book.query.delete()
    Transaction.query.delete()
    Review.query.delete()

    # Number of records
    no_of_users = 5
    no_of_books = 30
    no_of_transactions = 10
    no_of_reviews = 8

    # Creating roles
    print('Creating roles...')
    role_name_list = ['seller', 'buyer']
    for role in role_name_list:
        new_role = Role(name=role)
        db.session.add(new_role)
        db.session.commit()

    # Creating users
    print(f'Creating {no_of_users} users...')
    role_list = Role.query.all()
    for _ in range(no_of_users):
        username = fake.unique.user_name()
        email = f'{username}@student.moringaschool.com'
        profile_picture = fake.image_url()
        role = rc.choice(role_list)

        new_user = User(username=username,
                        email=email,
                        profile_picture=profile_picture)
        new_user.roles.append(role)
        db.session.add(new_user)
        db.session.commit()

    # Creating Books
    print(f'Creating {no_of_books} books...')
    for _ in range(no_of_books):
        # Create book
        title = fake.sentence(nb_words=3)
        author = fake.name()
        price = fake.random_int(min=20, max=500)
        condition = rc.choice(['new', 'used'])
        status = 'available'

        new_book = Book(title=title,
                        author=author,
                        price=price,
                        condition=condition,
                        status=status)

        # Select a random seller
        sellers = User.get_users_by_role('seller')
        seller = rc.choice(sellers)

        # Set seller as owner
        new_book.user = seller

        # Save to database
        db.session.add(new_book)
        db.session.commit()

    # Create transactions
    print(f'Creating {no_of_transactions} transactions...')
    for _ in range(no_of_transactions):
        # Select a random buyer
        buyers = User.get_users_by_role('buyer')
        buyer = rc.choice(buyers)

        # Select a random available book
        available_books = Book.get_books_by_status('available')
        # Out of available books quit loop
        if not available_books:
            break
        available_book = rc.choice(available_books)

        transaction_type = rc.choice(['rent', 'buy'])

        new_transaction = Transaction(transaction_type=transaction_type)
        new_transaction.user = buyer
        new_transaction.book = available_book

        db.session.add(new_transaction)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        seed()
        print('Done.')
