from config import app
from flask import request, send_file
from flask_migrate import Migrate
from flask_restful import Api
from models import db
from resources import (BookByID, Books, CheckSession, ClearSession, Login,
                       Logout, ReviewByID, Reviews, SignUp, Transactions,
                       UserByID, Users)
from utils import camel_to_snake_case

# Initialize extensions
db.init_app(app)

migrate = Migrate(app, db)

api = Api(app)


# Middleware function to convert request data to snake_case
@app.before_request
def before_request_func():
    # Check if request is JSON data
    if request.is_json:
        # Convert camelCase to snake_case
        request_data = request.json
        request.snake_case_data = camel_to_snake_case(request_data)


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
