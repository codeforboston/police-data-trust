from __future__ import annotations  # allows type hinting of class itself

from typing import TYPE_CHECKING
import logging
from backend.schemas import (
    JsonSerializable, PropertyEnum, NodeConflictException)
from backend.database.models.contact import SocialMediaContact, EmailContact
from datetime import datetime
from slugify import slugify
from neomodel import (
    StructuredNode, StructuredRel,
    RelationshipTo, RelationshipFrom,
    Relationship,
    StringProperty, DateTimeNeo4jFormatProperty,
    UniqueIdProperty, BooleanProperty,
    EmailProperty, One, db
)
from neomodel.exceptions import DoesNotExist
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
    date_joined = DateTimeNeo4jFormatProperty(default_now=True)
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
    timestamp = DateTimeNeo4jFormatProperty(
        default_now=True,
        index=True
    )
    url = StringProperty()
    user_uid = StringProperty()
    diff = StringProperty()

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Citation {self.timestamp}>"


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
            "timestamp": datetime.now(),
            "user_uid": user.uid,
            "diff": diff
        }.items() if v is not None}
        try:
            self.citations.connect(source, context)
        except Exception as e:
            logging.error(f"Error adding citation: {e} to {self.uid}")
            raise e

    @property
    def primary_source(self) -> Source | None:
        """Get the primary source for this item based on citation scores."""

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
    """
    An organization that provides data to the index. These can be journalistic
    organizations, government agencies, non-profits, or private firms.
    """
    __property_order__ = [
        "uid", "name", "url", "slug"
    ]
    __hidden_properties__ = [
        "invitations", "staged_invitations",
        "slug_value", "slug_generated_from", "slug_generated",
        "complaints"]
    uid = UniqueIdProperty()

    name = StringProperty(unique_index=True, required=True)
    url = StringProperty()

    # Slug property for easy URL access
    slug = StringProperty(unique_index=True)
    slug_generated = BooleanProperty(default=True)
    slug_generated_from = StringProperty()

    # Relationships
    primary_email = Relationship(
        EmailContact, "HAS_CONTACT_EMAIL", cardinality=One)
    social_media = Relationship(
        SocialMediaContact, "HAS_SOCIAL_MEDIA_CONTACT", cardinality=One)
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

    def _auto_generate_slug(self) -> None:
        """Auto-generate the slug for the source."""
        self.slug = slugify(self.name)
        self.slug_generated_from = self.name

    def set_slug(self, new_slug: str) -> None:
        """
        Set the slug for the source. Use this function to ensure that the slug
        is marked as set by a source admin.
        """
        self.slug = slugify(new_slug)
        self.slug_generated = False
        self.slug_generated_from = None
        self.save()

    def pre_save(self):
        """Hook to run before saving the source."""
        if not self.name:
            # Let neomodel validation handle this
            return

        should_autogen = (
            not self.slug or
            (self.slug_generated and self.slug_generated_from != self.name)
        )
        if should_autogen:
            self._auto_generate_slug()

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Source {self.uid}>"

    def update_source(
        self,
        *,
        name: str | None = None,
        contact_email: str | None = None,
        url: str | None = None,
        slug: str | None = None
    ) -> None:
        """Update the source details.

        Args:
            name (str | None): The name of the source.
            contact_email (str | None): The contact email for the source.
            url (str | None): The website URL for the source.
        """
        if name is not None and name != self.name:
            self.name = name
        if url is not None and url != self.url:
            self.url = url
        if contact_email is not None:
            email_node = EmailContact.get_or_create(contact_email)
            current_email = self.primary_email.single()
            self.primary_email.reconnect(current_email, email_node)
        if slug is not None:
            self.set_slug(slug)
        self.save()

    @classmethod
    def create_source(
        cls,
        *,
        name: str,
        contact_email: str,
        url: str | None = None,
        slug: str | None = None
    ) -> "Source":
        """Create a new data source.
        Wires up the relationships to contact methods.

        Args:
            name (str): The name of the source.
            contact_email (str): The contact email for the source.
            url (str | None): The website URL for the source.
            slug (str | None): The slug for the source.

        Returns:
            Source: The created source.
        """
        # Handle unique constraints
        try:
            existing = cls.nodes.get(name=name)
            if existing:
                raise NodeConflictException(
                    f"Source with name {name} "
                    "already exists with uid {existing.uid}")
        except DoesNotExist:
            source = cls(
                name=name,
                url=url
            ).save()
        except Exception as e:
            logging.error(f"Error creating source: {e}")
            raise e
        if slug:
            source.set_slug(slug)
        email = EmailContact.get_or_create(contact_email)
        social = SocialMediaContact().save()
        source.primary_email.connect(email)
        source.social_media.connect(social)
        return source

    @classmethod
    def filter_sources(
        cls,
        *,
        name: str | None = None,
        name__in: list[str] | None = None,
        page: int = 1,
        per_page: int = 20
    ):
        """
        Filter sources based on provided criteria.
        As these are not data nodes, we do not implement the full search
        functionality here. It's possible to search for a name or a list
        of names.

        If a single name is provided, the list of names is ignored.

        Args:
            name (str | None): Filter by name
                (case-insensitive, partial match).
            name__in (list[str] | None): Filter by a list of names
                (exact match).
            page (int): Page number for pagination.
            per_page (int): Number of items per page.

        Returns:
            Sources: A list of matching Source nodes.
            Count: Total count of matching nodes.
        """
        match_statements = ["MATCH (s:Source)\n"]
        where_clauses = []
        if name is not None:
            where_clauses.append("""
            WHERE toLower(s.name) CONTAINS toLower($name)
            """)
        elif name__in is not None:
            where_clauses.append("""
            WHERE s.name IN $name__in
            """)
        count_query = f"""
        {' '.join(match_statements)}
        {' AND '.join(where_clauses) if where_clauses else ''}
        RETURN count(s)
        """
        response_query = f"""
        {' '.join(match_statements)}
        {' AND '.join(where_clauses) if where_clauses else ''}
        RETURN s
        SKIP $skip
        LIMIT $limit
        """

        params = {
            "name": name,
            "name__in": name__in,
            "skip": (page - 1) * per_page,
            "limit": per_page
        }
        count_results, _ = db.cypher_query(count_query, params)
        rows, _ = db.cypher_query(response_query, params, resolve_objects=True)
        return [
            row[0] for row in rows
            ], count_results[0][0] if count_results else 0
