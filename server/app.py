from config import api, app
from flask_restful import Resource


class Index(Resource):

    def get(self):
        return {'hello': 'world'}


api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
