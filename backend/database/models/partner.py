from __future__ import annotations  # allows type hinting of class itself
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import RelationshipProperty
from ..core import db, CrudMixin
from enum import Enum
from datetime import datetime


class MemberRole(str, Enum):
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


class PartnerMember(db.Model, CrudMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    __tablename__ = "partner_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    partner_id = db.Column(
        db.Integer, db.ForeignKey("partner.id"), primary_key=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    user = db.relationship("User", back_populates="partner_association")
    partner = db.relationship("Partner", back_populates="member_association")
    role = db.Column(db.Enum(MemberRole))
    date_joined = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean)

    def is_administrator(self):
        return self.role == MemberRole.ADMIN

    def get_default_role():
        return MemberRole.SUBSCRIBER

    def create(self, refresh: bool = True):
        self.date_joined = datetime.now()
        return super().create(refresh)


class Partner(db.Model, CrudMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    contact_email = db.Column(db.Text)
    reported_incidents: RelationshipProperty[int] = db.relationship(
        "Incident", backref="source", lazy="select"
    )
    member_association: RelationshipProperty[PartnerMember] = db.relationship(
        "PartnerMember", back_populates="partner", lazy="select"
    )
    members = association_proxy("member_association", "user")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Partner {self.id}>"
