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


class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # officer id
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    race = db.Column(db.Text)
    ethnicity = db.Column(db.Text)
    gender = db.Column(db.Text)
    # Note: rank at time of incident
    rank = db.Column(db.Enum(Rank))
    star = db.Column(db.Text)  # type?
    date_of_birth = db.Column(db.Date)

    def __repr__(self):
        return f"<Officer {self.id}>"
