from enum import Enum
from sqlalchemy.ext.associationproxy import association_proxy
from ..core import CrudMixin, db


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
    # total_officers = db.Column(db.Integer)

    units = db.relationship("Unit", back_populates="agency")

    officer_association = db.relationship("Employment", back_populates="agency")
    officers = association_proxy("officer_association", "officer")

    def __repr__(self):
        return f"<Agency {self.name}>"
