from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.database.models import Actor


class UserSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Actor
        load_instance = True
