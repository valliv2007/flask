# SELECT * FROM ....
from src import db
from src.database import models
from sqlalchemy import and_


def queries():
    films = db.session.query(models.Film).order_by(models.Film.rating.desc()).all()
    hp_ch = db.session.query(models.Film).filter(models.Film.title == "Harry Potter and Chamber of Secrets").first()
    hp_pa = db.session.query(models.Film).filter_by(title="Harry Potter and the Prizoner of Azkaban").first()
    and_req = db.session.query(models.Film).filter(and_(
        models.Film.title != "Harry Potter and Chamber of Secrets", models.Film.rating >= 7.5 )).all()
    dh = db.session.query(models.Film).filter(models.Film.title.ilike('%deathly hallows%')).all()
    in_req = db.session.query(models.Film).filter(~models.Film.length.in_([146, 161]))[:3]
    f_a = db.session.query(models.Film).join(models.Film.actors).all()
    a = db.session.query(models.Actor).first()
    print(a.films)
