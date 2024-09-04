from enum import Enum
from backend.database.base_node import BaseNode
from neomodel import (
    StructuredNode,
    StructuredRel,
    StringProperty,
    RelationshipTo,
    DateProperty,
    UniqueIdProperty
)
from backend.database.models.unit_agency import UnitAssociation


class Jurisdiction(str, Enum):
    FEDERAL = "FEDERAL"
    STATE = "STATE"
    COUNTY = "COUNTY"
    MUNICIPAL = "MUNICIPAL"
    PRIVATE = "PRIVATE"
    OTHER = "OTHER"


class Agency(BaseNode):
    uid = UniqueIdProperty()
    name = StringProperty()
    website_url = StringProperty()
    hq_address = StringProperty()
    hq_city = StringProperty()
    hq_zip = StringProperty()
    phone = StringProperty()
    email = StringProperty()
    description = StringProperty()
    jurisdiction = StringProperty()

    # Relationships
    units = RelationshipTo("Unit", "HAS_UNIT", model=UnitAssociation)

    def __repr__(self):
        return f"<Agency {self.name}>"
