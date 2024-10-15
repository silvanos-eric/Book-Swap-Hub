from faker import Faker
import random
from datetime import datetime
from app import app, db, User, Book, Review, Transaction 

# Initialize Faker
fake = Faker()

with app.app_context():  
    # Delete existing data
    try:
        print("Deleting existing data...")
        Review.query.delete()
        Transaction.query.delete()
        Book.query.delete()
        User.query.delete()
        db.session.commit()  # Commit deletions
        print("Deleted all records.")
    except Exception as e:
        db.session.rollback()
        print(f"Error while deleting records: {e}")

    # The seed function
    def seed_database():
        try:
            # Generate Users
            users = []
            print("Creating users...")
            for _ in range(10):  # create 10 users
                user = User(
                    username=fake.user_name(),
                    email=fake.email(),
                    password=fake.password(),
                    profile_picture=fake.image_url()
                )
                users.append(user)
                db.session.add(user)
            db.session.commit()  # Commit all users
            print(f"Created {len(users)} users.")
            
            # Generate Books
            books = []
            print("Creating books...")
            for _ in range(10):  # create 10 books
                book = Book(
                    title=fake.sentence(nb_words=3),
                    author=fake.name(),
                    price=random.randint(10, 100),  # price between 10 and 100
                    condition=random.choice([True, False]),  # True for new, False for used
                    status=random.choice(["available", "sold"]),
                    user_id=random.choice([user.id for user in users])  # random user owns the book
                )
                books.append(book)
                db.session.add(book)
            db.session.commit()  # Commit all books
            print(f"Created {len(books)} books.")

            # Generate Reviews
            reviews = []
            print("Creating reviews...")
            for _ in range(20):  # create 20 reviews
                review = Review(
                    rating=random.randint(1, 5),  # rating between 1 and 5
                    comment=fake.text(),
                    user_id=random.choice([user.id for user in users]),
                    book_id=random.choice([book.id for book in books])
                )
                reviews.append(review)
                db.session.add(review)
            db.session.commit()  # Commit all reviews
            print(f"Created {len(reviews)} reviews.")

            # Generate Transactions
            transactions = []
            print("Creating transactions...")
            for _ in range(10):  # create 10 transactions
                transaction = Transaction(
                    transaction_date=fake.date_time_this_year(),
                    transaction_type=random.choice(["purchase", "sale"]),
                    user_id=random.choice([user.id for user in users]),
                    book_id=random.choice([book.id for book in books])
                )
                transactions.append(transaction)
                db.session.add(transaction)
            db.session.commit()  # Commit all transactions
            print(f"Created {len(transactions)} transactions.")
            
            print("Successfully updated bookshub database.")
        
        except Exception as e:
            db.session.rollback()
            print(f"Error while seeding database: {e}")

    # Call seed function
    seed_database()
