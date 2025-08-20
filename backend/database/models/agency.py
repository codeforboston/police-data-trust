from backend.schemas import JsonSerializable, PropertyEnum, RelQuery
from backend.database.models.types.enums import State
from backend.database.models.source import Citation, Source

from neomodel import (
    db,
    StructuredNode,
    StructuredRel,
    StringProperty,
    Relationship,
    RelationshipTo,
    RelationshipFrom,
    DateProperty,
    UniqueIdProperty,
    One
)


class Jurisdiction(str, PropertyEnum):
    FEDERAL = "FEDERAL"
    STATE = "STATE"
    COUNTY = "COUNTY"
    MUNICIPAL = "MUNICIPAL"
    PRIVATE = "PRIVATE"
    OTHER = "OTHER"

    def describe(self):
        if self == self.FEDERAL:
            return "Federal"
        elif self == self.STATE:
            return "State"
        elif self == self.COUNTY:
            return "County"
        elif self == self.MUNICIPAL:
            return "Municipal"
        elif self == self.PRIVATE:
            return "Private"
        else:
            return ""


class UnitMembership(StructuredRel, JsonSerializable):
    earliest_date = DateProperty()
    latest_date = DateProperty()
    badge_number = StringProperty()
    highest_rank = StringProperty()


class Unit(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "name", "website_url", "phone",
        "email", "description", "address",
        "city", "state", "zip", "agency_url",
        "officers_url", "date_established"
    ]
    __hidden_properties__ = ["citations"]

    uid = UniqueIdProperty()
    name = StringProperty()
    website_url = StringProperty()
    phone = StringProperty()
    email = StringProperty()
    description = StringProperty()
    address = StringProperty()
    city = StringProperty()
    state = StringProperty(choices=State.choices())
    zip = StringProperty()
    agency_url = StringProperty()
    officers_url = StringProperty()
    date_established = DateProperty()

    # Relationships
    agency = Relationship("Agency", "ESTABLISHED_BY", cardinality=One)
    commander = Relationship(
        "backend.database.models.officer.Officer",
        "COMMANDED_BY", model=UnitMembership)
    officers = Relationship(
        "backend.database.models.officer.Officer",
        "MEMBER_OF_UNIT", model=UnitMembership)
    citations = RelationshipTo(
        'backend.database.models.source.Source', "UPDATED_BY", model=Citation)

    def __repr__(self):
        return f"<Unit {self.name}>"

    @property
    def primary_source(self):
        """
        Get the primary source for this unit.
        Returns:
            Source: The primary source node for this unit.
        """
        cy = """
        MATCH (o:Unit {uid: $uid})-[r:UPDATED_BY]->(s:Source)
        RETURN s
        ORDER BY r.date DESC
        LIMIT 1;
        """
        from backend.database import db
        result, meta = db.cypher_query(cy, {'uid': self.uid})
        if result:
            source_node = result[0][0]
            return Source.inflate(source_node)
        return None

    @property
    def current_commander(self):
        """
        Get the current commander of the unit.
        Returns:
            Officer: The current commander of the unit.
        """
        cy = """
        MATCH (u:Unit {uid: $uid})-[r:COMMANDED_BY]-(o:Officer)
        WITH u, r, o,
            CASE WHEN r.latest_date IS NULL THEN 1 ELSE 0 END AS isCurrent
        ORDER BY isCurrent DESC, r.earliest_date DESC
        RETURN o AS officer
        LIMIT 1;
        """
        result, meta = db.cypher_query(
            cy, {'uid': self.uid}, resolve_objects=True)
        if result:
            officer_node = result[0][0]
            return officer_node
        return None


class Agency(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "name", "website_url", "hq_address",
        "hq_city", "hq_state", "hq_zip", "phone",
        "email", "description", "jurisdiction"
    ]
    __hidden_properties__ = ["citations", "state_node",
                             "county_node", "city_node"]
    __virtual_relationships__ = ["units"]

    uid = UniqueIdProperty()
    name = StringProperty()
    website_url = StringProperty()
    hq_address = StringProperty()
    hq_city = StringProperty()
    hq_state = StringProperty(choices=State.choices())
    hq_zip = StringProperty()
    phone = StringProperty()
    email = StringProperty()
    description = StringProperty()
    jurisdiction = StringProperty(choices=Jurisdiction.choices())

    # Relationships
    citations = RelationshipTo(
        'backend.database.models.source.Source', "UPDATED_BY", model=Citation)
    state_node = RelationshipFrom(
        "backend.database.models.infra.locations.StateNode",
        "WITHIN_STATE", cardinality=One)
    county_node = RelationshipFrom(
        "backend.database.models.infra.locations.CountyNode",
        "WITHIN_COUNTY", cardinality=One)
    city_node = RelationshipFrom(
        "backend.database.models.infra.locations.CityNode",
        "WITHIN_CITY", cardinality=One)

    @property
    def units(self) -> RelQuery:
        """
        Query the units related to this agency.
        Returns:
            RelQuery: A query object for the Unit nodes associated
            with this agency.
        """
        base = """
        MATCH (a:Agency {uid: $uid})-[:ESTABLISHED_BY]-(u:Unit)
        """
        return RelQuery(self, base, return_alias="u", inflate_cls=Unit)

    @property
    def officers(self) -> RelQuery:
        """
        Query the officers related to this agency.
        Returns:
            RelQuery: A query object for the Officer nodes associated
            with this agency.
        """
        base = """
        MATCH (a:Agency {uid: $uid})-[:ESTABLISHED_BY]
        -(u:Unit)-[:MEMBER_OF_UNIT]-(o:Officer)
        """
        from backend.database.models.officer import Officer
        return RelQuery(self, base, return_alias="o", inflate_cls=Officer)

    @property
    def jurisdiction_enum(self) -> Jurisdiction:
        """
        Get the agency's jurisdiction as an enum.
        Returns:
            Jurisdiction: The agency's jurisdiction as an enum.
        """
        return Jurisdiction(self.jurisdiction) if self.jurisdiction else None

    def __repr__(self):
        return f"<Agency {self.name}>"

    @property
    def primary_source(self):
        """
        Get the primary source for this agency.
        Returns:
            Source: The primary source node for this agency.
        """
        cy = """
        MATCH (o:Agency {uid: $uid})-[r:UPDATED_BY]->(s:Source)
        RETURN s
        ORDER BY r.date DESC
        LIMIT 1;
        """
        result, meta = db.cypher_query(cy, {'uid': self.uid})
        if result:
            source_node = result[0][0]
            return Source.inflate(source_node)
        return None

    def total_officers(self):
        """
        Get the total number of officers in this agency.
        Returns:
            int: The total number of officers.
        """
        cy = """
        MATCH (a:Agency {uid: $uid})-[:ESTABLISHED_BY]-
        (u:Unit)-[:MEMBER_OF_UNIT]-(o:Officer)
        RETURN COUNT(o) AS total_officers
        """
        result, meta = db.cypher_query(cy, {'uid': self.uid})
        if result:
            return result[0][0]
        return 0
