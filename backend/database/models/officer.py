from backend.schemas import JsonSerializable
from backend.database.models.types.enums import State, Ethnicity, Gender
from backend.database.models.source import Source, Citation
from backend.database.models.agency import Unit

from neomodel import (
    db, StructuredNode,
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
    __hidden_properties__ = ["citations"]

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
    units = RelationshipTo(
        'backend.database.models.agency.Unit', "MEMBER_OF_UNIT")
    litigation = Relationship(
        'backend.database.models.litigation.Litigation', "NAMED_IN")
    allegations = Relationship(
        'backend.database.models.complaint.Allegation', "ACCUSED_OF")
    investigations = Relationship(
        'backend.database.models.complaint.Investigation', "LEAD_BY")
    commands = Relationship(
        'backend.database.models.agency.Unit', "COMMANDS")
    citations = RelationshipTo(
        'backend.database.models.source.Source', "UPDATED_BY", model=Citation)

    def __repr__(self):
        return f"<Officer {self.uid}>"

    @property
    def full_name(self):
        """Returns the full name of the officer."""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        if self.suffix:
            parts.append(self.suffix)
        return " ".join(parts).strip()

    @property
    def ethnicity_enum(self) -> Ethnicity:
        """
        Get the user's ethnicity as an enum.
        Returns:
            Ethnicity: The user's ethnicity as an enum.
        """
        return Ethnicity(self.ethnicity) if self.ethnicity else None

    @property
    def gender_enum(self) -> Gender:
        """
        Get the user's gender as an enum.
        Returns:
            Gender: The user's gender as an enum.
        """
        return Gender(self.gender) if self.gender else None

    @property
    def current_unit(self):
        """
        Get the current unit of the officer.
        Returns:
            Unit: The current or most recent unit of the officer.
        """
        cy = """
        MATCH (u:Unit)-[r:MEMBER_OF_UNIT]-(o:Officer {uid: $uid})
        WITH u, r, o,
            CASE WHEN r.latest_date IS NULL THEN 1 ELSE 0 END AS isCurrent
        ORDER BY isCurrent DESC, r.earliest_date DESC
        RETURN u AS unit, r AS membership, o
        LIMIT 1;
        """

        result, meta = db.cypher_query(cy, {'uid': self.uid})
        if result:
            unit_node = result[0][0]
            return Unit.inflate(unit_node)
        return None

    def primary_source(self):
        """
        Get the primary source of the officer.
        Returns:
            Source: The primary source of the officer.
        """
        cy = """
        MATCH (o:Officer {uid: $uid})-[r:UPDATED_BY]->(s:Source)
        RETURN s
        ORDER BY r.date DESC
        LIMIT 1;
        """

        result, meta = db.cypher_query(cy, {'uid': self.uid})
        if result:
            source_node = result[0][0]
            return Source.inflate(source_node)
        return None
