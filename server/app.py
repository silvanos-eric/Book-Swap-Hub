from config import app
from flask_migrate import Migrate
from flask_restful import Api
from models import db
from resources import BookByID, Books, Reviews

# Initialize extensions
db.init_app(app)

migrate = Migrate(app, db)

api = Api(app)

# Register resources
api.add_resource(Books, '/books')
api.add_resource(BookByID, '/books/<int:id>')
api.add_resource(Reviews, '/reviews')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
