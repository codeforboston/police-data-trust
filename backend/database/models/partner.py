from __future__ import annotations  # allows type hinting of class itself
# from ..core import db, CrudMixin
from backend.schemas import JsonSerializable, PropertyEnum
from datetime import datetime
from neomodel import (
    StructuredNode, StructuredRel,
    RelationshipTo, RelationshipFrom,
    StringProperty, DateTimeProperty,
    UniqueIdProperty, BooleanProperty,
    EmailProperty
)
from backend.database.models.complaint import BaseSourceRel


class MemberRole(str, PropertyEnum):
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


class Invitation(StructuredNode):
    role = StringProperty(choices=MemberRole.choices())
    is_accepted = BooleanProperty(default=False)
    # default to not accepted invite

    partner = RelationshipFrom("Partner", "INVITED_TO")
    user = RelationshipFrom(
        "backend.database.models.user.User", "EXTENDED_TO")
    extender = RelationshipFrom(
        "backend.database.models.user.User", "EXTENDED_BY")

    def serialize(self):
        return {
            'id': self.id,
            'partner': self.partner,
            'user': self.user,
            'role': self.role,
            'is_accepted': self.is_accepted,
        }


class StagedInvitation(StructuredNode):
    role = StringProperty(choices=MemberRole.choices())
    email = EmailProperty()

    partner = RelationshipFrom("Partner", "INVITATION_TO")
    extender = RelationshipFrom(
        "backend.database.models.user.User", "EXTENDED_BY")

    def serialize(self):
        return {
            'id': self.id,
            'partner_id': self.partner,
            'email': self.email,
            'role': self.role
        }


class PartnerMember(StructuredRel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    uid = UniqueIdProperty()
    role = StringProperty(choices=MemberRole.choices(), required=True)
    date_joined = DateTimeProperty(default=datetime.now())
    is_active = BooleanProperty(default=True)

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


class Partner(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "name", "url",
        "contact_email"
    ]
    uid = UniqueIdProperty()

    name = StringProperty(unique_index=True)
    url = StringProperty()
    contact_email = StringProperty()

    # Relationships
    members = RelationshipFrom(
        "backend.database.models.user.User",
        "IS_MEMBER", model=PartnerMember)
    complaints = RelationshipTo(
        "backend.database.models.complaint.Complaint",
        "REPORTED", model=BaseSourceRel)
    invitations = RelationshipTo(
        "Invitation", "HAS_PENDING_INVITATION")
    staged_invitations = RelationshipTo(
        "StagedInvitation", "_PENDING_STAGED_INVITATION")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Partner {self.uid}>"
