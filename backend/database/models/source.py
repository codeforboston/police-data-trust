from __future__ import annotations  # allows type hinting of class itself
# from ..core import db, CrudMixin
from backend.schemas import JsonSerializable, PropertyEnum
from datetime import datetime
from neomodel import (
    StructuredNode, StructuredRel,
    RelationshipTo, RelationshipFrom,
    StringProperty, DateTimeProperty,
    UniqueIdProperty, BooleanProperty,
    EmailProperty, JSONProperty,
    ZeroOrOne
)


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
    uid = UniqueIdProperty()
    role = StringProperty(choices=MemberRole.choices())
    is_accepted = BooleanProperty(default=False)
    # default to not accepted invite

    source_org = RelationshipFrom("Source", "INVITED_TO")
    user = RelationshipFrom(
        "backend.database.models.user.User", "EXTENDED_TO")
    extender = RelationshipFrom(
        "backend.database.models.user.User", "EXTENDED_BY")

    def serialize(self):
        return {
            'id': self.id,
            'source': self.source,
            'user': self.user,
            'role': self.role,
            'is_accepted': self.is_accepted,
        }


class StagedInvitation(StructuredNode):
    uid = UniqueIdProperty()
    role = StringProperty(choices=MemberRole.choices())
    email = EmailProperty()

    source_org = RelationshipFrom("Source", "INVITATION_TO")
    extender = RelationshipFrom(
        "backend.database.models.user.User", "EXTENDED_BY")

    def serialize(self):
        return {
            'uid': self.uid,
            'source_uid': self.source_org,
            'email': self.email,
            'role': self.role
        }


class SourceMember(StructuredRel, JsonSerializable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    uid = UniqueIdProperty()
    role = StringProperty(choices=MemberRole.choices(), required=True)
    date_joined = DateTimeProperty(default=datetime.now())
    is_active = BooleanProperty(default=True)

    @property
    def role_enum(self) -> MemberRole:
        """
        Get the role as a MemberRole enum.
        Returns:
            MemberRole: The role as a MemberRole enum.
        """
        return MemberRole(self.role)

    def is_administrator(self):
        return self.role == MemberRole.ADMIN

    def get_default_role():
        return MemberRole.SUBSCRIBER

    def create(self, refresh: bool = True):
        self.date_joined = datetime.now()
        return super().create(refresh)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<SourceMember( \
        id={self.uid}>"


class Citation(StructuredRel, JsonSerializable):
    """
    Created when a source creates or updates a record.
    """
    uid = UniqueIdProperty()
    date = DateTimeProperty(default=datetime.now())
    url = StringProperty(required=True)
    diff = JSONProperty()

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Citation {self.uid}>"


class Source(StructuredNode, JsonSerializable):
    """
    Represents a source organization that provides data to the platform.
    """
    __property_order__ = [
        "uid", "name", "description", "website_url",
        "contact_email", "contact_phone"
    ]
    __hidden_properties__ = ["invitations", "staged_invitations"]

    uid = UniqueIdProperty()

    name = StringProperty(unique_index=True)
    description = StringProperty()
    website_url = StringProperty()
    contact_email = StringProperty(required=True)
    contact_phone = StringProperty()

    # Relationships
    social_media = RelationshipTo(
        "backend.database.models.attachment.SocialMediaInfo",
        "HAS", cardinality=ZeroOrOne)
    members = RelationshipFrom(
        "backend.database.models.user.User",
        "IS_MEMBER", model=SourceMember)
    invitations = RelationshipTo(
        "Invitation", "HAS_PENDING_INVITATION")
    staged_invitations = RelationshipTo(
        "StagedInvitation", "PENDING_STAGED_INVITATION")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Source {self.uid}>"
