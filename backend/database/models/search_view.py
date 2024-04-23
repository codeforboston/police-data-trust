from enum import Enum
from sqlalchemy.dialects.postgresql import TSVECTOR
from ..core import db


class Jurisdiction(str, Enum):
    FEDERAL = "FEDERAL"
    STATE = "STATE"
    COUNTY = "COUNTY"
    MUNICIPAL = "MUNICIPAL"
    PRIVATE = "PRIVATE"
    OTHER = "OTHER"


class SearchView(db.Model):
    __tablename__ = 'search_view'
    __table_args__ = {'info': dict(is_view=True)}

    id = db.Column(db.Text, primary_key=True, index=True)
    officer_id = db.Column(db.Integer)
    officer_first_name = db.Column(db.Text)
    tsv_officer_first_name = db.Column(TSVECTOR)
    officer_middle_name = db.Column(db.Text)
    tsv_officer_middle_name = db.Column(TSVECTOR)
    officer_last_name = db.Column(db.Text)
    tsv_officer_last_name = db.Column(TSVECTOR)
    officer_race = db.Column(db.Text)
    officer_ethnicity = db.Column(db.Text)
    officer_gender = db.Column(db.Text)
    officer_date_of_birth = db.Column(db.Date)
    agency_id = db.Column(db.Integer)
    agency_name = db.Column(db.Text)
    agency_website_url = db.Column(db.Text)
    agency_hq_address = db.Column(db.Text)
    agency_hq_city = db.Column(db.Text)
    agency_hq_zip = db.Column(db.Text)
    agency_jurisdiction = db.Column(db.Enum(Jurisdiction))
