from backend.database import db
import enum


class Rank(str, enum.enum):
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


class Officer(db.model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Is this different than primary key, can we name it better
    officer_ID = db.Column(db.String)
    first = db.Column(db.String)
    last = db.Column(db.String)
    gender = db.Column(db.String)
    race = db.Column(db.String)
    apptDate = db.Column(db.DateTime)
    # TODO: is this a number?
    unit = db.Column(db.String)
    rank = db.Column(db.Enum(Rank))
    # TODO: number of stars?
    star = db.Column(db.Integer)
    age = db.Column(db.Integer)
