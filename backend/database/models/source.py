from ..core import db, CrudMixin
# from backend.database.models._assoc_tables import source_user
from enum import Enum


class MemberRole(Enum):
    ADMIN = "Administrator"
    PUBLISHER = "Publisher"
    MEMBER = "Member"
    SUBSCRIBER = "Subscriber"

    def get_value(self):
        if self == MemberRole.ADMIN:
            return 1
        elif self == MemberRole.PUBLISHER:
            return 2
        elif self == MemberRole.MEMBER:
            return 3
        elif self == MemberRole.SUBSCRIBER:
            return 4
        else:
            return 5


class Source(db.Model, CrudMixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    contact_email = db.Column(db.Text)
    reported_incidents = db.relationship(
        'Incident', backref='source', lazy="select")
    # members = db.relationship(
    #     'User', backref='contributor_orgs',
    #     secondary=source_user, lazy="select")
