from backend.database import db


class Participant(db.model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Enums for these? Also used in other models
    gender = db.Column(db.String)
    race = db.Column(db.String)
    age = db.Column(db.Integer)
