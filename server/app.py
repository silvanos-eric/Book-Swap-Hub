from flask import Flask
from flask_restful import Api, Resource

# Create a Flask instance
app = Flask(__name__)

# Add extensions to use with flask
api = Api(app)


# Create Hello World Resource
class HelloWorld(Resource):

    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, port=5555)
