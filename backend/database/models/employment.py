from backend.schemas import (
    JsonSerializable, PropertyEnum, RelQuery
)
from backend.database.models.source import HasCitations

from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    DateProperty,
    UniqueIdProperty,
    RelationshipTo,
    One
)

# Enums - Not yet used for validation, but could be in the future
class EmploymentType(str, PropertyEnum):
    LAW_ENFORCEMENT = "LAW_ENFORCEMENT"
    CORRECTIONS = "CORRECTIONS"

class EmploymentStatus(PropertyEnum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    PROVISIONAL = "PROVISIONAL"
    TEMPORARY = "TEMPORARY"
    VOLUNTEER = "VOLUNTEER"

class EmploymentChange(PropertyEnum):
    PROMOTION = "PROMOTION"
    DEMOTION = "DEMOTION"
    TRANSFER = "TRANSFER"
    TERMINATION = "TERMINATION"
    RESIGNATION = "RESIGNATION"


class Employment(StructuredNode, HasCitations, JsonSerializable):
    uid = UniqueIdProperty()
    key = StringProperty()
    type = StringProperty()
    earliest_date = DateProperty(index=True)
    latest_date = DateProperty(index=True)
    badge_number = StringProperty(index=True)
    highest_rank = StringProperty()
    salary = IntegerProperty()
    status = StringProperty()
    change = StringProperty()

    # Relationships
    officer = RelationshipTo("backend.database.models.officer.Officer", "HELD_BY", cardinality=One)
    unit = RelationshipTo("backend.database.models.agency.Unit", "IN_UNIT", cardinality=One)

    def __repr__(self):
        return f"<Employment {self.uid}>"
    
    
class CommandAssignment(StructuredNode, HasCitations, JsonSerializable):
    uid = UniqueIdProperty()
    type = StringProperty()
    title = StringProperty()
    earliest_date = DateProperty(index=True)
    latest_date = DateProperty(index=True)
    badge_number = StringProperty(index=True)
    highest_rank = StringProperty()
    salary = IntegerProperty()
    change = StringProperty()

    # Relationships
    officer = RelationshipTo("backend.database.models.officer.Officer", "COMMANDED_BY", cardinality=One)
    unit = RelationshipTo("backend.database.models.agency.Unit", "UNIT_ASSIGNED", cardinality=One)


    def __repr__(self):
        return f"<CommandAssignment {self.uid}>"
