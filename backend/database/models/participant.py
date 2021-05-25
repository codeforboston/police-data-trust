from .. import db


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Enums for these? Also used in other models
    gender = db.Column(db.String)
    race = db.Column(db.String)
    age = db.Column(db.Integer)


class ParticipantAtIncident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
