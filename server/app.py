from flask import Flask, send_file, send_from_directory
from flask_restful import Api, Resource

# Create a Flask instance
app = Flask(__name__, static_folder='../client/dist', static_url_path='')

# Add extensions to use with flask
api = Api(app)


# Serve React app
@app.route('/')
def serve():
    return send_file(app.static_folder + '/index.html')


class Hello(Resource):

    def get(self):
        return {'hello': 'world'}


api.add_resource(Hello, '/api/hello')


# Catch-all route to send any unmatched paths to the React app
@app.route('/<path:path>')
def catch_all(path):
    return send_file(app.static_folder + '/index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5555)
