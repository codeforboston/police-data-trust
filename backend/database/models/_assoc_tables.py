from .. import db


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
