from neomodel import (
    StructuredNode,
    StructuredRel,
    StringProperty,
    RelationshipTo,
    RelationshipFrom,
    DateProperty,
    UniqueIdProperty,
    BooleanProperty
)


class Unit(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()
    website_url = StringProperty()
    phone = StringProperty()
    email = StringProperty()
    description = StringProperty()
    address = StringProperty()
    zip = StringProperty()
    agency_url = StringProperty()
    officers_url = StringProperty()

    # Relationships
    commander = RelationshipTo("Officer", "COMMANDED_BY")
    agency = RelationshipFrom("Agency", "HAS_UNIT", model="UnitAssociation")
    officers = RelationshipTo("Officer", "MEMBER_OF", model="UnitMembership")

    def __repr__(self):
        return f"<Unit {self.name}>"


class UnitMembership(StructuredRel):
    earliest_date = DateProperty()
    latest_date = DateProperty()
    badge_number = StringProperty()
    highest_rank = StringProperty()
    current_member = BooleanProperty()
