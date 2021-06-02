from .. import db
from .types.enums import Gender
from .types.enums import Race
import enum


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


class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # officer id
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    race = db.Column(db.Enum(Race))
    gender = db.Column(db.Enum(Gender))
    appointed_date = db.Column(db.DateTime)
    badge = db.Column(db.Text)
    unit = db.Column(db.Text)  # type?
    # Note: rank at time of incident
    rank = db.Column(db.Text)  # type?
    star = db.Column(db.Text)  # type?
    date_of_birth = db.Column(db.Date)
    # TODO: Age changes over time. Might we use birth year?


class OfficerAtIncident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Relationships, fields?
