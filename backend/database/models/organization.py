from ..core import db, CrudMixin
from backend.database.models._assoc_tables import organization_user


class Organization(db.Model, CrudMixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    contact_email = db.Column(db.Text)
    reported_incidents = db.relationship(
        'Incident', backref='source', lazy="select")
    members = db.relationship(
        'User', backref='member_of',
        secondary=organization_user, lazy="select")
