import enum

from backend.database.core import SourceMixin

from .. import db



class Suspect(db.Model, SourceMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # suspect id
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    race = db.Column(db.Text)
    gender = db.Column(db.Text)
    badge = db.Column(db.Text)
    unit = db.Column(db.Text)  # type?
    # Note: rank at time of incident
    rank = db.Column(db.Text)  # type?
    star = db.Column(db.Text)  # type?
    accusations = db.relationship("Accusation", backref="suspect")
