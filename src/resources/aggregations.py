from flask_restful import Resource
from sqlalchemy import func

from src import db
from src.database.models import Film, Actor


class AggregationApi(Resource):
    def get(self):
        films_count = db.session.query(func.count(Film.id)).scalar()
        max_rating = db.session.query(func.max(Film.rating)).scalar()
        min_rating = db.session.query(func.min(Film.rating)).scalar()
        avg_rating = db.session.query(func.avg(Film.rating)).scalar()
        sum_rating = db.session.query(func.sum(Film.rating)).scalar()
        max_length = db.session.query(func.max(Film.length)).scalar()
        min_length = db.session.query(func.min(Film.length)).scalar()
        films_count_gg = db.session.query(func.count(Film.id)).filter(Film.distributed_by == "Warner Bros. Pictures").scalar()
        # max_actors = db.session.query(func.count(Actor.films)).filter(Film.id==1, Actor.id==1).scalar()
        return {
            "count": films_count,
            "max_rate": max_rating,
            "min_rate": min_rating,
            "avg_rate": avg_rating,
            "sum_rate": sum_rating,
            "max_length": max_length,
            "min_length": min_length,
            "films_count_gg": films_count_gg}  # "max_actors": max_actors
