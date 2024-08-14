from __future__ import annotations  # allows type hinting of class itself
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import RelationshipProperty
from ..core import db, CrudMixin
from enum import Enum
from datetime import datetime
from neomodel import (
    StructuredNode, StructuredRel,
    RelationshipTo, RelationshipFrom, Relationship,
    StringProperty, DateTimeProperty,
    UniqueIDProperty, BooleanProperty
)


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


class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    partner_id = db.Column(
        db.Integer, db.ForeignKey('partner.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role = db.Column(db.Enum(MemberRole), nullable=False)
    is_accepted = db.Column(db.Boolean, default=False)
    # default to not accepted invite

    def serialize(self):
        return {
            'id': self.id,
            'partner_id': self.partner_id,
            'user_id': self.user_id,
            'role': self.role,
            'is_accepted': self.is_accepted,
        }


class StagedInvitation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    partner_id = db.Column(
        db.Integer, db.ForeignKey('partner.id'), primary_key=True)
    email = db.Column(db.String, unique=True, primary_key=True)
    role = db.Column(db.Enum(MemberRole), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'partner_id': self.partner_id,
            'email': self.email,
            'role': self.role
        }


class PartnerMember(StructuredRel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    uid = UniqueIDProperty()
    role = StringProperty(choices=[e.value for e in MemberRole])
    date_joined = DateTimeProperty()
    is_active = BooleanProperty()

    def is_administrator(self):
        return self.role == MemberRole.ADMIN

    def get_default_role():
        return MemberRole.SUBSCRIBER

    def create(self, refresh: bool = True):
        self.date_joined = datetime.now()
        return super().create(refresh)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<PartnerMember( \
        id={self.uid}>"


class Partner(StructuredNode):
    uid = UniqueIDProperty()

    name = StringProperty()
    url = StringProperty()
    contact_email = StringProperty()

    # Relationships
    members = RelationshipFrom("User", "IS_MEMBER", model=PartnerMember)
    complaints = RelationshipTo("Complaint", "REPORTED", model="BaseSourceRel")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Partner {self.uid}>"
