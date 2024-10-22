from backend.schemas import JsonSerializable
from backend.database.models.types.enums import State, Ethnicity, Gender

from neomodel import (
    StructuredNode,
    RelationshipTo, RelationshipFrom, Relationship,
    StringProperty, DateProperty,
    UniqueIdProperty, One
)


class StateID(StructuredNode, JsonSerializable):
    """
    Represents a Statewide ID that follows an offcier even as they move between
    law enforcement agencies. For example, in New York, this would be
    the Tax ID Number.
    """
    id_name = StringProperty()  # e.g. "Tax ID Number"
    state = StringProperty(choices=State.choices())  # e.g. "NY"
    value = StringProperty()  # e.g. "958938"
    officer = RelationshipFrom('Officer', "HAS_STATE_ID", cardinality=One)

    def __repr__(self):
        return f"<StateID: Officer {self.officer_id}, {self.state}>"


class Officer(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "first_name", "middle_name",
        "last_name", "suffix", "ethnicity",
        "gender", "date_of_birth"
    ]

    uid = UniqueIdProperty()
    first_name = StringProperty()
    middle_name = StringProperty()
    last_name = StringProperty()
    suffix = StringProperty()
    ethnicity = StringProperty(choices=Ethnicity.choices())
    gender = StringProperty(choices=Gender.choices())
    date_of_birth = DateProperty()

    # Relationships
    state_ids = RelationshipTo('StateID', "HAS_STATE_ID")
    units = Relationship(
        'backend.database.models.agency.Unit', "MEMBER_OF_UNIT")
    litigation = Relationship(
        'backend.database.models.litigation.Litigation', "NAMED_IN")
    allegations = Relationship(
        'backend.database.models.complaint.Allegation', "ACCUSED_OF")
    investigations = Relationship(
        'backend.database.models.complaint.Investigation', "LEAD_BY")
    commands = Relationship(
        'backend.database.models.agency.Unit', "COMMANDS")

    def __repr__(self):
        return f"<Officer {self.id}>"
