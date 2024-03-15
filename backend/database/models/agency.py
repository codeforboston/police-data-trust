from ..core import db, CrudMixin
from enum import Enum


class Jurisdiction(str, Enum):
    FEDERAL = "FEDERAL"
    STATE = "STATE"
    COUNTY = "COUNTY"
    MUNICIPAL = "MUNICIPAL"
    PRIVATE = "PRIVATE"
    OTHER = "OTHER"


class Agency(db.Model, CrudMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    website_url = db.Column(db.Text)
    hq_address = db.Column(db.Text)
    hq_city = db.Column(db.Text)
    hq_zip = db.Column(db.Text)
    jurisdiction = db.Column(db.Enum(Jurisdiction))

    known_officers = db.relationship("Employment", back_populates="agency")

    def __repr__(self):
        return f"<Agency {self.name}>"
