from backend.schemas import JsonSerializable, RelQuery
from backend.database.models.types.enums import State, Ethnicity, Gender
from backend.database.models.source import Source, Citation
from backend.database.models.agency import Unit
import logging

from neomodel import (
    db, StructuredNode,
    RelationshipTo, Relationship,
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
    officer = Relationship('Officer', "HAS_STATE_ID", cardinality=One)

    def __repr__(self):
        return f"<StateID: Officer {self.officer_id}, {self.state}>"


class Officer(StructuredNode, JsonSerializable):
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

    # Relationships
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

    @classmethod
    def search(
        cls,
        *,
        name: str | None = None,
        rank: str | None = None,
        unit: list[str] | None = None,
        agency: list[str] | None = None,
        badge_number: list[str] | None = None,
        ethnicity: list[str] | None = None,
        active_after: str | None = None,
        active_before: str | None = None,
        skip: int = 0,
        limit: int = 25,
        count: bool = False,
    ):
        """
        Search for officers based on filters.
        Args:
            filters (dict): A dictionary of filters to apply.
            skip (int): Number of records to skip for pagination.
            limit (int): Number of records to return.
            """

        # Build MATCH clauses
        match_clauses = []
        if name:
            match_clauses.append(f"""
                CALL db.index.fulltext.queryNodes('officerNames',
                                '{name}') YIELD node AS o
            """)
        elif rank:
            match_clauses.append(f"""
                CALL db.index.fulltext.queryRelationships('officerRanks',
                                '{rank}') YIELD relationship AS m
            """)

        match_clauses.append("MATCH (o:Officer)")

        if unit or active_after or active_before or badge_number or agency:
            match_clauses.append("MATCH (o)-[m:MEMBER_OF_UNIT]-(u:Unit)")

        if agency:
            match_clauses.append("MATCH (u)-[:ESTABLISHED_BY]->(a:Agency)")

        # Build WHERE clauses and params
        where_clauses = ["TRUE"]
        params = {}

        if active_after:
            where_clauses.append("m.latest_date > $active_after")
            params["active_after"] = active_after

        if active_before:
            where_clauses.append("m.earliest_date < $active_before")
            params["active_before"] = active_before

        if agency:
            where_clauses.append("a.name IN $agency")
            params["agency"] = agency

        if badge_number:
            where_clauses.append("m.badge_number IN $badge_number")
            params["badge_number"] = badge_number

        if ethnicity:
            where_clauses.append("o.ethnicity IN $ethnicity")
            params["ethnicity"] = ethnicity

        if unit:
            where_clauses.append("u.name IN $unit")
            params["unit"] = unit

        # Combine query
        match_str = "\n".join(match_clauses)
        where_str = "\nAND ".join(where_clauses)
        cypher_query = f"""
        {match_str}
        WHERE {where_str}"""

        if count:
            cypher_query += "\nRETURN count(*) as c"
            logging.warning("Cypher count query:\n%s", cypher_query)
            logging.warning("Params: %s", params)
            count_results, _ = db.cypher_query(cypher_query, params)
            return count_results[0][0] if count_results else 0
        else:
            cypher_query += f"""
                RETURN o SKIP {skip} LIMIT {limit}
            """

            logging.warning("Cypher query:\n%s", cypher_query)
            logging.warning("Params: %s", params)

            rows, _ = db.cypher_query(cypher_query, params,
                                    #   resolve_objects=True
                                      )
            return [row[0] for row in rows]
