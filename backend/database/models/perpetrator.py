from backend.database.models._assoc_tables import perpetrator_officer
from backend.database.models.officer import Rank
from .. import db


class Perpetrator(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    race = db.Column(db.Text)
    gender = db.Column(db.Text)
    badge = db.Column(db.Text)
    unit = db.Column(db.Text)  # type?
    # Note: rank at time of incident
    rank = db.Column(db.Enum(Rank))
    star = db.Column(db.Text)  # type?
    suspects = db.relationship(
        "Officer", secondary=perpetrator_officer, backref="suspected_matches")

    def __repr__(self):
        return f"<Perpetrator {self.id}>"
