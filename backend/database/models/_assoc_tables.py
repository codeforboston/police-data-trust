from .. import db
from backend.database.models.officer import Rank

incident_agency = db.Table(
    'incident_agency',
    db.Column('incident_id',  db.Integer, db.ForeignKey('incident.id'),
              primary_key=True),
    db.Column('agency_id', db.Integer, db.ForeignKey('agency.id'),
              primary_key=True),
    db.Column('officers_present', db.Integer)
)

incident_tag = db.Table(
    'incident_tag',
    db.Column('incident_id', db.Integer, db.ForeignKey('incident.id'),
              primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

agency_officer = db.Table(
    'agency_officer',
    db.Column('agency_id', db.Integer, db.ForeignKey('agency.id'),
              primary_key=True),
    db.Column('officer_id', db.Integer, db.ForeignKey('officer.id'),
              primary_key=True),
    db.Column('earliest_employment', db.Text),
    db.Column('latest_employment', db.Text),
    db.Column('badge_number', db.Text),
    db.Column('unit', db.Text),
    db.Column('highest_rank', db.Enum(Rank)),
    db.Column('currently_employed', db.Boolean)
)

perpetrator_officer = db.Table(
    'perpetrator_officer',
    db.Column('perpetrator_id', db.Integer, db.ForeignKey('perpetrator.id'),
              primary_key=True),
    db.Column('officer_id', db.Integer, db.ForeignKey('officer.id'),
              primary_key=True)
)
