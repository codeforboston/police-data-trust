from backend.schemas import JsonSerializable, RelQuery
from backend.database.models.types.enums import State, Ethnicity, Gender, StateIdName
from backend.database.models.source import HasCitations
from backend.database.models.agency import Unit

from neomodel import (
    db, StructuredNode, Relationship,
    StringProperty, DateProperty,
    UniqueIdProperty, One
)


class StateID(StructuredNode, JsonSerializable):
    """
    Represents a Statewide ID that follows an offcier even as they move between
    law enforcement agencies. For example, in New York, this would be
    the Tax ID Number.
    """
    id_name = StringProperty(choices=StateIdName.choices())  # e.g. "Tax ID Number"
    state = StringProperty(choices=State.choices())  # e.g. "NY"
    value = StringProperty()  # e.g. "958938"
    officer = Relationship('Officer', "HAS_STATE_ID", cardinality=One)

    def __repr__(self):
        return f"<StateID: Officer {self.officer_id}, {self.state}>"


class Officer(StructuredNode, HasCitations, JsonSerializable):
    __property_order__ = [
        "uid", "first_name", "middle_name",
        "last_name", "suffix", "ethnicity",
        "gender", "date_of_birth"
    ]
    __hidden_properties__ = ["citations"]
    __virtual_relationships__ = ["state_ids"]

    uid = UniqueIdProperty()
    first_name = StringProperty()
    middle_name = StringProperty()
    last_name = StringProperty()
    suffix = StringProperty()
    ethnicity = StringProperty(choices=Ethnicity.choices())
    gender = StringProperty(choices=Gender.choices())
    date_of_birth = DateProperty()

    def __repr__(self):
        return f"<Officer {self.uid}>"
    
    def lookup_state_id(self, state: State, id_name: StateIdName) -> StateID:
        """
        Lookup a StateID for this officer by state and id_name.
        Args:
            state (State): The state of the StateID.
            id_name (StateIdName): The name of the StateID.
        Returns:
            StateID: The matching StateID, or None if not found.
        """
        cy = """
        MATCH (o:Officer {uid: $officer_uid})-[:HAS_STATE_ID]->(s:StateID {
            state: $state,
            id_name: $id_name
        })
        RETURN s
        LIMIT 1
        """
        result, meta = db.cypher_query(
            cy,
            {
                'officer_uid': self.uid,
                'state': state,
                'id_name': id_name
            },
            resolve_objects=True
        )
        if result:
            state_id_node = result[0][0]
            return StateID.inflate(state_id_node)
        return None

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

    @property
    def state_ids(self) -> RelQuery:
        """
        Query the state IDs associated with the officer.
        Returns:
            RelQuery: A query object for the state IDs
            associated with the officer.
        """
        cy = """
        MATCH (o:Officer {uid: $uid})-[r:HAS_STATE_ID]-(s:StateID)
        """
        return RelQuery(self, cy, return_alias="s", inflate_cls=StateID)

    @property
    def units(self) -> RelQuery:
        """
        Query the units associated with the officer.
        Returns:
            RelQuery: A query object for the units associated with the officer.
        """
        base = """
        MATCH (o:Officer {uid: $uid})-[r:MEMBER_OF_UNIT]->(u:Unit)
        """
        return RelQuery(self, base, return_alias="u", inflate_cls=Unit)

    @property
    def commands(self) -> RelQuery:
        """
        Query the units commanded by the officer.
        Returns:
            RelQuery: A query object for the units commanded by the officer.
        """
        base = """
        MATCH (o:Officer {uid: $uid})-[r:COMMANDED_BY]-(u:Unit)
        """
        return RelQuery(self, base, return_alias="u", inflate_cls=Unit)

    @property
    def allegations(self) -> RelQuery:
        """
        Query the allegations associated with the officer.
        Returns:
            RelQuery: A query object for the allegations.
        """
        base = """
        MATCH (o:Officer {uid: $uid})-[r:ACCUSED_OF]->(a:Allegation)
        """
        from backend.database.models.complaint import Allegation
        return RelQuery(self, base, return_alias="a", inflate_cls=Allegation)

    @property
    def investigations(self) -> RelQuery:
        """
        Query the investigations led by the officer.
        Returns:
            RelQuery: A query object for the investigations.
        """
        base = """
        MATCH (o:Officer {uid: $uid})-[r:LEAD_BY]->(i:Investigation)
        """
        from backend.database.models.complaint import Investigation
        return RelQuery(self, base, return_alias="i", inflate_cls=Investigation)
