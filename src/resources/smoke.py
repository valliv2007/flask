from flask_restful import Resource

from src.database.inserts import populate_films
from src.database.queries import queries


class Smoke(Resource):
    def get(self):
        # populate_films()
        queries()
        return {'message': 'OK'}
