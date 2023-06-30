from datetime import datetime
from flask import request
from marshmallow import ValidationError
from flask_restful import Resource
from sqlalchemy.orm import joinedload, selectinload

from src import db
from src.database.models import Film
from src.schemas.films import FilmSchema
from src.resources.auth import token_required, admin_required
from src.services.film_service import FilmService


class FilmListApi(Resource):
    film_schema = FilmSchema()

    def get(self, uuid=None):
        if not uuid:
            films = FilmService.fetch_all_films(db.session).options(selectinload(Film.actors)).all()
            return self.film_schema.dump(films, many=True), 200
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return 'not', 404
        return self.film_schema.dump(film), 200

    # @token_required
    def post(self):
        try:
            film = self.film_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return {'message': str(error)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 201

    # @admin_required
    def put(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return 'not', 404
        try:
            film = self.film_schema.load(request.json, session=db.session, instance=film)
        except ValidationError as error:
            return {'message': str(error)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 200

    @admin_required
    def patch(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return 'not', 404
        film_json = request.json
        title = film_json.get('title')
        release_date = datetime.strptime(film_json.get('release_date'), '%B %d, %Y') if film_json.get('release_date') else None
        distributed_by = film_json.get('distributed_by')
        description = film_json.get('description')
        length = film_json.get('length')
        rating = film_json.get('rating')

        if title:
            film.title = title
        if release_date:
            film.release_date = release_date
        if distributed_by:
            film.distributed_by = distributed_by
        if description:
            film.description = description
        if length:
            film.length = length
        if rating:
            film.rating = rating
        db.session.add(film)
        db.session.commit()
        return {'message': "updated"}, 200

    # @admin_required
    def delete(self, uuid):
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return 'not', 404
        db.session.delete(film)
        db.session.commit()
        return "deleted", 204
