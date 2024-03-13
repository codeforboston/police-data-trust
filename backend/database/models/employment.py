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
    COMMISSIONER = "COMMISSIONER"


class Employment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    officer_id = db.Column(db.Integer, db.ForeignKey("officer.id"))
    agency_id = db.Column(db.Integer, db.ForeignKey("agency.id"))
    earliest_employment = db.Column(db.Text)
    latest_employment = db.Column(db.Text)
    badge_number = db.Column(db.Text)
    unit = db.Column(db.Text)
    highest_rank = db.Column(db.Enum(Rank))
    currently_employed = db.Column(db.Boolean)

    officer = db.relationship("Officer", back_populates="known_employers")
    agency = db.relationship("Agency", back_populates="known_officers")

    def __repr__(self):
        return f"<Employment {self.id}>"
