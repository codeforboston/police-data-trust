from backend.schemas import (
    JsonSerializable, PropertyEnum
)
from backend.database.models.source import HasCitations
from backend.database.properties.datetime import DateNeo4jFormatProperty

from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    UniqueIdProperty,
    RelationshipTo,
    One
)


# Enums - Not yet used for validation, but could be in the future
class EmploymentType(str, PropertyEnum):
    LAW_ENFORCEMENT = "Law Enforcement"
    CORRECTIONS = "Corrections"


class EmploymentStatus(PropertyEnum):
    FULL_TIME = "Full-Time"
    PART_TIME = "Part-Time"
    PROVISIONAL = "Provisional"
    TEMPORARY = "Temporary"
    VOLUNTEER = "Volunteer"


class EmploymentChange(PropertyEnum):
    PROMOTION = "Promotion"
    DEMOTION = "Demotion"
    TRANSFER = "Transfer"
    TERMINATION = "Termination"
    RESIGNATION = "Resignation"


class Rank(str, PropertyEnum):
    POLICE_OFFICER = "Police Officer"
    DETECTIVE = "Detective"
    SERGEANT = "Sergeant"
    LIEUTENANT = "Lieutenant"
    CAPTAIN = "Captain"
    MAJOR = "Major"
    COLONEL = "Colonel"
    COMMANDER = "Commander"
    CHIEF = "Chief"

    def get_value(self):
        if self == Rank.POLICE_OFFICER:
            return 10
        elif self == Rank.DETECTIVE:
            return 20
        elif self == Rank.SERGEANT:
            return 30
        elif self == Rank.LIEUTENANT:
            return 40
        elif self == Rank.CAPTAIN:
            return 50
        elif self == Rank.MAJOR:
            return 60
        elif self == Rank.COLONEL:
            return 70
        elif self == Rank.COMMANDER:
            return 80
        elif self == Rank.CHIEF:
            return 90
        return 0


class Employment(StructuredNode, HasCitations, JsonSerializable):
    uid = UniqueIdProperty()
    key = StringProperty()
    type = StringProperty()
    earliest_date = DateNeo4jFormatProperty(index=True)
    latest_date = DateNeo4jFormatProperty(index=True)
    badge_number = StringProperty(index=True)
    highest_rank = StringProperty(choices=Rank.choices())
    rank_label = StringProperty()
    salary = IntegerProperty()
    status = StringProperty()
    change = StringProperty()

    # Relationships
    officer = RelationshipTo(
        "backend.database.models.officer.Officer", "HELD_BY", cardinality=One)
    unit = RelationshipTo(
        "backend.database.models.agency.Unit", "IN_UNIT", cardinality=One)

    def __repr__(self):
        return f"<Employment {self.uid}>"


class CommandAssignment(StructuredNode, HasCitations, JsonSerializable):
    uid = UniqueIdProperty()
    type = StringProperty()
    title = StringProperty()
    earliest_date = DateNeo4jFormatProperty(index=True)
    latest_date = DateNeo4jFormatProperty(index=True)
    badge_number = StringProperty(index=True)
    highest_rank = StringProperty()
    salary = IntegerProperty()
    change = StringProperty()

    # Relationships
    officer = RelationshipTo(
        "backend.database.models.officer.Officer",
        "COMMANDED_BY", cardinality=One)
    unit = RelationshipTo(
        "backend.database.models.agency.Unit",
        "UNIT_ASSIGNED", cardinality=One)

    def __repr__(self):
        return f"<CommandAssignment {self.uid}>"
