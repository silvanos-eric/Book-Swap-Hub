from config import app
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db
from resources import Books

# Initialize extensions
db.init_app(app)

migrate = Migrate(app, db)

api = Api(app)

# Register resources
api.add_resource(Books, '/books')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
