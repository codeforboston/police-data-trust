from .. import db
from .types.enums import Race
from .types.enums import Gender


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    gender = db.Column(db.Enum(Gender))
    race = db.Column(db.Enum(Race))
    age = db.Column(db.Integer)
    name = db.Column(db.Text)
