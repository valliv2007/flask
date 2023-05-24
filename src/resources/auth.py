from functools import wraps
import jwt
import datetime
from flask_restful import Resource
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from src import db, app
from src.schemas.users import UserSchema
from src.database.models import User


class AuthRegister(Resource):
    user_schema = UserSchema()

    def post(self):
        try:
            user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return {'message': str(error)}, 400
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': "User already exist"}, 409
        return self.user_schema.dump(user), 201


class AuthLogin(Resource):
    def get(self):
        auth = request.authorization
        if not auth:
            return "you are not provide your data", 401, {"WWW-Authenticate": "Basic realm='Authentication_required'"}
        print(auth)
        user = db.session.query(User).filter_by(username=auth.get('username', '')).first()
        if not user or not check_password_hash(user.password, auth.get('password', '')):
            return "incorrect password or user", 401, {"WWW-Authenticate": "Basic realm='Authentication_required'"}
        token = jwt.encode({
            "user_id": user.uuid,
            "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'],
        )
        return jsonify({"token": token})


def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.headers.get("X-API-KEY", '')
        if not token:
            return "You are not authorized", 401, {"WWW-Authenticate": "Basic realm='Authentication_required'"}
        try:
            uuid = jwt.decode(token, app.config['SECRET_KEY'], "HS256")['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return "You are not authorized", 401, {"WWW-Authenticate": "Basic realm='Authentication_required'"}
        user = db.session.query(User).filter_by(uuid=uuid).first()
        if not user:
            return "You are not authorized", 401, {"WWW-Authenticate": "Basic realm='Authentication_required'"}
        return func(self, *args, **kwargs)
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.headers.get("X-API-KEY", '')
        if not token:
            return "You are not authorized", 401, {"WWW-Authenticate": "Basic realm='Authentication_required'"}
        try:
            uuid = jwt.decode(token, app.config['SECRET_KEY'], "HS256")['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return "You are not authorized", 401, {"WWW-Authenticate": "Basic realm='Authentication_required'"}
        user = db.session.query(User).filter_by(uuid=uuid).first()
        if not user:
            return "You are not authorized", 401, {"WWW-Authenticate": "Basic realm='Authentication_required'"}
        print(user.is_admin)
        if not user.is_admin:
            return "You are not permitted", 403
        return func(self, *args, **kwargs)
    return wrapper