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

perpetrator_officer = db.Table(
    'perpetrator_officer',
    db.Column('perpetrator_id', db.Integer, db.ForeignKey('perpetrator.id'),
              primary_key=True),
    db.Column('officer_id', db.Integer, db.ForeignKey('officer.id'),
              primary_key=True),
    db.Column('accuser_id', db.Integer, db.ForignKey('user.id'),
              primary_key=True),
    db.Column('date_created', db.Text),
    db.Column('basis', db.Text),
    db.Column('attachments',
              db.relationship("Attachment", backref="accusation"))
    # Can we reuse the attachements Table here?

)
