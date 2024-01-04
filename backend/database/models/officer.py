import enum

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


class StateID(db.Model):
    """
    Represents a Statewide ID that follows an offcier even as they move between
    law enforcement agencies. for an officer. For example, in New York, this
    would be the Tax ID Number.
    """
    id = db.Column(db.Integer, primary_key=True)
    officer_id = db.Column(
        db.Integer, db.ForeignKey("officer.id"))
    id_name = db.Column(db.Text)  # e.g. "Tax ID Number"
    state = db.Column(db.Text)  # e.g. "NY"
    value = db.Column(db.Text)  # e.g. "958938"

    def __repr__(self):
        return f"<StateID {self.id}>"


class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # officer id
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    race = db.Column(db.Text)
    ethnicity = db.Column(db.Text)
    gender = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)

    def __repr__(self):
        return f"<Officer {self.id}>"
