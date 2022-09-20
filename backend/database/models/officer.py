import enum

from backend.database.core import SourceMixin

from .. import db


class Rank(str, enum.Enum):
    # TODO: Is this comprehensive?
    TECHNICIAN = "TECHNICIAN"
    OFFICER = "OFFICER"
    DETECTIVE = "DETECTIVE"
    CORPORAL = "CORPORAL"
    SERGEANT = "SERGEANT"
    LIEUTENANT = "LIEUTENANT"
    CAPTAIN = "CAPTAIN"
    DEPUTY = "DEPUTY"
    CHIEF = "CHIEF"


class Officer(db.Model, SourceMixin):
    id = db.Column(db.Integer, primary_key=True)  # officer id
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    race = db.Column(db.Text)
    gender = db.Column(db.Text)
    appointed_date = db.Column(db.DateTime)
    badge = db.Column(db.Text)
    unit = db.Column(db.Text)  # type?
    # Note: rank at time of incident
    rank = db.Column(db.Text)  # type?
    star = db.Column(db.Text)  # type?
    date_of_birth = db.Column(db.Date)
    accusations = db.relationship("Accusation", backref="officer")
