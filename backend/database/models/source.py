from __future__ import annotations  # allows type hinting of class itself

from typing import TYPE_CHECKING
import logging
from backend.schemas import JsonSerializable, PropertyEnum
from datetime import datetime
from neomodel import (
    StructuredNode, StructuredRel,
    RelationshipTo, RelationshipFrom,
    StringProperty, DateTimeProperty,
    UniqueIdProperty, BooleanProperty,
    EmailProperty, db
)
if TYPE_CHECKING:
    from backend.database.models.user import User


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

    def may_publish(self):
        return self.role_enum.get_value() <= MemberRole.PUBLISHER.get_value()

    def get_default_role():
        return MemberRole.SUBSCRIBER

    def create(self, refresh: bool = True):
        self.date_joined = datetime.now()
        return super().create(refresh)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<SourceMember( \
        uid={self.uid}>"


class Citation(StructuredRel, JsonSerializable):
    uid = UniqueIdProperty()
    date = DateTimeProperty(default=datetime.now())
    url = StringProperty()
    user_uid = StringProperty()
    diff = StringProperty()

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Citation {self.uid}>"


class HasCitations:
    """Mix me into a database model to give it citation capabilities."""
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not issubclass(cls, StructuredNode):
            raise TypeError(
                f"{cls.__name__} mixes in HasCitations " +
                "but does not inherit StructuredNode"
            )

    # Relationships
    citations = RelationshipTo(
        'backend.database.models.source.Source', "UPDATED_BY", model=Citation)

    def add_citation(self, source, user: "User", diff: dict = None):
        """
        Add a citation to an item from a source.

        :param item: The item to add the citation to
        :param source: The source of the citation
        :param data: The citation data
        """
        context = {k: v for k, v in {
            "date": datetime.now(),
            "user_uid": user.uid,
            "diff": diff
        }.items() if v is not None}
        try:
            self.citations.connect(source, context)
        except Exception as e:
            logging.error(f"Error adding citation: {e} to {self.uid}")
            raise e

    def _source_where_clause(self) -> str:
        return ""  # subclasses can add e.g. "WHERE s.is_active = true"

    def _source_score_expr(self) -> str:
        # default: newest wins
        return "coalesce(r.date, datetime({epochMillis: 0})).epochMillis"

    @property
    def primary_source(self) -> Source | None:
        """Get the primary source for this item based on citation scores."""
        where = self._source_where_clause().strip()
        score = self._source_score_expr().strip()

        cy = """
        MATCH (n)-[r:UPDATED_BY]->(s:Source)
        WHERE elementId(n) = $eid
        RETURN s
        ORDER BY r.date DESC
        LIMIT 1
        """
        result, _ = db.cypher_query(cy, {"eid": self.element_id})
        return Source.inflate(result[0][0]) if result else None


class Source(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "name", "url",
        "contact_email"
    ]
    __hidden_properties__ = ["invitations", "staged_invitations"]
    uid = UniqueIdProperty()

    name = StringProperty(unique_index=True)
    url = StringProperty()
    contact_email = StringProperty(required=True)

    # Relationships
    members = RelationshipFrom(
        "backend.database.models.user.User",
        "IS_MEMBER", model=SourceMember)
    complaints = RelationshipTo(
        "backend.database.models.complaint.Complaint",
        "REPORTED")
    invitations = RelationshipTo(
        "Invitation", "HAS_PENDING_INVITATION")
    staged_invitations = RelationshipTo(
        "StagedInvitation", "PENDING_STAGED_INVITATION")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Source {self.uid}>"
