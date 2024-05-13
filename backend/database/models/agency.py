from ..core import db, CrudMixin
from enum import Enum
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import TSVECTOR


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

    officer_association = db.relationship("Employment", back_populates="agency")
    officers = association_proxy("officer_association", "officer")

    def __repr__(self):
        return f"<Agency {self.name}>"


"""
This Agency View model is for full text search based
on location search terms.
There are three tsv vector columns to rank relevant search
terms based on location

"""


class AgencyView(db.Model):
    __tablename__ = 'agency_view'
    __table_args__ = {'info': dict(is_view=True)}
    agency_id = db.Column(db.Integer, primary_key=True)
    agency_name = db.Column(db.Text)
    agency_website_url = db.Column(db.Text)
    agency_hq_address = db.Column(db.Text)
    tsv_agency_hq_address = db.Column(TSVECTOR)
    agency_hq_city = db.Column(db.Text)
    tsv_agency_hq_city = db.Column(TSVECTOR)
    agency_hq_zip = db.Column(db.Text)
    tsv_agency_hq_zip = db.Column(TSVECTOR)
    agency_jurisdiction = db.Column(db.Enum(Jurisdiction))
    # total_officers = db.Column(db.Integer)

    # officer_association = db.relationship("Employment",
    # back_populates="agency_view")
    # officers = association_proxy("officer_association", "officer")
