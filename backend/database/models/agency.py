from backend.schemas import JsonSerializable, PropertyEnum
from backend.database.models.types.enums import State
from backend.database.models.source import Citation

from neomodel import (
    StructuredNode,
    StructuredRel,
    StringProperty,
    RelationshipTo,
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


class UnitMembership(StructuredRel, JsonSerializable):
    earliest_date = DateProperty()
    latest_date = DateProperty()
    badge_number = StringProperty()
    highest_rank = StringProperty()


class Unit(StructuredNode, JsonSerializable):
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
    agency = RelationshipTo("Agency", "ESTABLISHED_BY", cardinality=One)
    commander = RelationshipTo(
        "backend.database.models.officer.Officer",
        "COMMANDED_BY", model=UnitMembership)
    officers = RelationshipTo(
        "backend.database.models.officer.Officer",
        "MEMBER_OF", model=UnitMembership)
    citations = RelationshipTo(
        'backend.database.models.source.Source', "UPDATED_BY", model=Citation)

    def __repr__(self):
        return f"<Unit {self.name}>"


class Agency(StructuredNode, JsonSerializable):
    __hidden_properties__ = ["citations", "state_node",
                             "county_node", "city_node"]

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
    units = RelationshipTo("Unit", "ESTABLISHED")
    citations = RelationshipTo(
        'backend.database.models.source.Source', "UPDATED_BY", model=Citation)
    state_node = RelationshipTo(
        "backend.database.models.infra.locations.StateNode", "WITHIN_STATE")
    county_node = RelationshipTo(
        "backend.database.models.infra.locations.CountyNode", "WITHIN_COUNTY")
    city_node = RelationshipTo(
        "backend.database.models.infra.locations.CityNode", "WITHIN_CITY")

    def __repr__(self):
        return f"<Agency {self.name}>"
