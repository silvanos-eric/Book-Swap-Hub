from config import app
from flask import send_file
from flask_migrate import Migrate
from flask_restful import Api
from models import db
from resources import (BookByID, Books, CheckSession, ClearSession, Login,
                       Logout, ReviewByID, Reviews, SignUp, Transactions,
                       UserByID, Users)

# Initialize extensions
db.init_app(app)

migrate = Migrate(app, db)

api = Api(app)

# Register resources
api.add_resource(Books, '/api/books')
api.add_resource(BookByID, '/api/books/<int:id>')
api.add_resource(Reviews, '/api/reviews')
api.add_resource(ReviewByID, '/api/reviews/<int:id>')
api.add_resource(Users, '/api/users')
api.add_resource(UserByID, '/api/users/<int:id>')
api.add_resource(SignUp, '/api/signup')
api.add_resource(Login, '/api/login')
api.add_resource(CheckSession, '/api/check_session')
api.add_resource(ClearSession, '/api/clear_session')
api.add_resource(Logout, '/api/logout')
api.add_resource(Transactions, '/api/transactions')


# Serve React app
@app.route('/')
def serve():
    return send_file(app.static_folder + '/index.html')


# Catch-all route to send any unmatched paths to the React app
@app.route('/<path:path>')
def catch_all(path):
    return send_file(app.static_folder + '/index.html')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
