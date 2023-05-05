from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from datetime import datetime
from sqlalchemy.orm import selectinload

from src import db
from src.schemas.actors import ActorSchema
from src.database.models import Actor


class ActorListApi(Resource):
    actor_schema = ActorSchema()

    def get(self, uuid=None):
        if not uuid:
            actors = db.session.query(Actor).options(selectinload(Actor.films)).all()
            return self.actor_schema.dump(actors, many=True), 200
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return 'not', 404
        return self.actor_schema.dump(actor), 200

    def post(self):
        try:
            actor = self.actor_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return {'message': str(error)}, 400
        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 201

    def put(self, uuid):
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return 'not', 404
        try:
            actor = self.actor_schema.load(request.json, session=db.session, instance=actor)
        except ValidationError as error:
            return {'message': str(error)}, 400
        db.session.add(actor)
        db.session.commit()
        return self.actor_schema.dump(actor), 200

    def patch(self, uuid):
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return 'not', 404
        actor_json = request.json
        name = actor_json.get('name')
        birthday = datetime.strptime(actor_json.get('birthday'), '%B %d, %Y') if actor_json.get('release_date') else None
        is_action = actor_json.get('is_action')
        if name:
            actor.name = name
        if birthday:
            actor.birthday = birthday
        if is_action is not None:
            actor.is_action = is_action
        db.session.add(actor)
        db.session.commit()
        return {'message': "updated"}, 200

    def delete(self, uuid):
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return 'not', 404
        db.session.delete(actor)
        db.session.commit()
        return "deleted", 204
