from flask import Flask
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db

# Create a Flask instance
app = Flask(__name__)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookshub.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Add extensions to use with flask
api = Api(app)

# Create Hello World Resource
class HelloWorld(Resource):

    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, port=5555)
