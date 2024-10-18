import random
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
    no_of_products = 20
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
    role_list = Role.query.all()
    print(f'Creating {no_of_users} users...')
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


if __name__ == '__main__':
    with app.app_context():
        seed()
        print('Done.')
