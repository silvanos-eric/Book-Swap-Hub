import random as rc
from datetime import datetime

from app import app
from faker import Faker
from models import Book, Review, Role, Transaction, User, db, user_roles


def seed():
    # Initialize Faker
    fake = Faker()

    # Reset database
    print('Resetting database...')
    db.session.query(user_roles).delete()
    Review.query.delete()
    Transaction.query.delete()
    Book.query.delete()
    User.query.delete()
    Role.query.delete()
    db.session.commit()

    # Number of records
    no_of_users = 20
    no_of_books = 100
    no_of_transactions = 15
    no_of_reviews = 5

    try:
        # Creating roles
        print('Creating roles...')
        role_name_list = ['vendor', 'customer']
        roles = []
        for role_name in role_name_list:
            role = Role(name=role_name)
            db.session.add(role)
            roles.append(role)
        db.session.commit()

        # Creating users
        print(f'Creating {no_of_users} users...')
        for _ in range(no_of_users):
            username = fake.unique.user_name()
            email = f'{username}@student.moringaschool.com'
            book_img = fake.image_url()
            role = rc.choice(roles)

            new_user = User(username=username,
                            email=email,
                            profile_picture=book_img)
            new_user.roles.append(role)
            db.session.add(new_user)
        db.session.commit()

        # Creating Books
        print(f'Creating {no_of_books} books...')
        vendors = User.get_users_by_role(
            'vendor')  # Fetch vendors after users are created
        for _ in range(no_of_books):
            title = fake.sentence(nb_words=5)
            author = fake.name()
            price = fake.random_int(min=20, max=500)
            condition = rc.choice(['new', 'used'])
            image_url = fake.image_url()

            new_book = Book(
                title=title,
                author=author,
                price=price,
                condition=condition,
                status='available',
                image_url=image_url,
                user=rc.choice(vendors)  # Assign random vendor as the owner
            )
            db.session.add(new_book)
        db.session.commit()

        # Creating transactions
        print(f'Creating {no_of_transactions} transactions...')
        customers = User.get_users_by_role('customer')  # Fetch customers
        for _ in range(no_of_transactions):
            available_books = Book.get_books_by_status('available')
            if not available_books:
                break  # Stop if no available books left

            customer = rc.choice(customers)
            available_book = rc.choice(available_books)
            transaction_type = rc.choice(['rent', 'buy'])

            new_transaction = Transaction(transaction_type=transaction_type,
                                          user=customer,
                                          book=available_book)
            db.session.add(new_transaction)

        db.session.commit()

        # Creating reviews
        print(f'Creating {no_of_reviews} reviews...')
        customers_with_transactions = [
            customer for customer in customers if customer.transactions
        ]
        for _ in range(no_of_reviews):
            if not customers_with_transactions:
                break  # Stop if no customers with transactions are left

            customer = rc.choice(customers_with_transactions)
            transaction = rc.choice(customer.transactions)

            if not transaction:
                break

            # Create review for the selected transaction's book
            rating = rc.choice(range(1, 6))
            comment = fake.sentence(nb_words=10)

            new_review = Review(
                rating=rating,
                comment=comment,
                user_id=customer.id,  # Explicitly assign user_id
                book_id=transaction.book.id  # Explicitly assign book_id
            )
            db.session.add(new_review)

        db.session.commit()
        print("Seeding completed successfully.")

    except Exception as e:
        db.session.rollback()  # Rollback session in case of error
        print(f"Error during seeding: {e}")


if __name__ == '__main__':
    with app.app_context():
        print('Starting...')
        seed()
        print('Done.')
