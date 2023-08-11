from ..core import db, CrudMixin
from backend.database.models._assoc_tables import partner_user


class Partner(db.Model, CrudMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    contact_email = db.Column(db.Text)
    reported_incidents = db.relationship(
        'Incident', backref='source', lazy="select")
    members = db.relationship(
        'User', backref='member_of',
        secondary=partner_user, lazy="select")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Partner {self.id}>"
