from backend.schemas import (JsonSerializable, PropertyEnum, RelQuery,
                             SearchableMixin)
from backend.database.models.types.enums import State
from backend.database.models.source import HasCitations
from backend.database.properties.datetime import DateNeo4jFormatProperty

from neomodel import (
    db,
    StructuredNode,
    StringProperty,
    RelationshipTo,
    UniqueIdProperty,
    One, ZeroOrOne
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


class Unit(StructuredNode, HasCitations, JsonSerializable, SearchableMixin):
    __property_order__ = [
        "uid", "name", "website_url", "phone",
        "email", "description", "address",
        "hq_address", "hq_city", "hq_state", "hq_zip",
        "agency", "date_established"
    ]
    __hidden_properties__ = ["citations", "city_node"]

    uid = UniqueIdProperty()
    name = StringProperty()
    hq_state = StringProperty(choices=State.choices(), required=True)
    hq_address = StringProperty()
    hq_city = StringProperty()
    hq_zip = StringProperty()
    phone = StringProperty()
    email = StringProperty()
    website_url = StringProperty()
    description = StringProperty()
    date_established = DateNeo4jFormatProperty()

    # Relationships
    agency = RelationshipTo("Agency", "ESTABLISHED_BY", cardinality=One)
    city_node = RelationshipTo(
        "backend.database.models.infra.locations.CityNode",
        "LOCATED_IN", cardinality=ZeroOrOne)

    def __repr__(self):
        return f"<Unit {self.name}>"

    def officers(self) -> RelQuery:
        """
        Query the officers related to this agency.
        Returns:
            RelQuery: A query object for the Officer nodes associated
            with this agency.
        """
        base = """
        MATCH (u:Unit {uid: $uid})-[]-(:Employment)-[]-(o:Officer)
        """
        from backend.database.models.officer import Officer
        return RelQuery(self, base, return_alias="o", inflate_cls=Officer)

    def total_officers(self):
        """
        Get the total number of officers in this agency.
        Returns:
            int: The total number of officers.
        """
        cy = """
        MATCH (u:Unit {uid: $uid})-[]-(:Employment)-[]-(o:Officer)
        RETURN COUNT(o) AS total_officers
        """
        result, meta = db.cypher_query(cy, {'uid': self.uid})
        if result:
            return result[0][0]
        return 0

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

    @classmethod
    def search(cls, query: str = None, filters: dict = None,
               count: bool = False, skip: int = 0, limit: int = 25,
               inflate: bool = False):
        """
        Model-specific search method.
        Decides which fulltext index to use and delegates to the mixin.
        """
        # --- Fulltext index parameterized safely ---
        if query:
            fulltext_index_cypher = (
                """CALL db.index.fulltext.queryNodes('unitNames', $query)
                YIELD node as n"""
            )
            params = {"query": query}
        else:
            fulltext_index_cypher = None
            params = {}

        return cls._search(
            label="Unit",
            index=fulltext_index_cypher,
            filters=filters,
            query=query,
            count=count,
            skip=skip,
            limit=limit,
            extra_params=params,  # pass parameter dict to _search()
            inflate=inflate
        )


class Agency(StructuredNode, HasCitations, JsonSerializable, SearchableMixin):
    __property_order__ = [
        "uid", "name", "website_url", "phone",
        "email", "description", "address",
        "hq_address", "hq_city", "hq_state", "hq_zip",
        "jurisdiction", "date_established"
    ]
    __hidden_properties__ = ["citations", "state_node",
                             "county_node", "city_node"]
    __virtual_relationships__ = ["units"]

    uid = UniqueIdProperty()
    name = StringProperty()
    hq_state = StringProperty(choices=State.choices(), required=True)
    hq_address = StringProperty()
    hq_city = StringProperty()
    hq_zip = StringProperty()
    phone = StringProperty()
    email = StringProperty()
    website_url = StringProperty()
    description = StringProperty()
    date_established = DateNeo4jFormatProperty()
    jurisdiction = StringProperty(choices=Jurisdiction.choices())

    # Relationships
    city_node = RelationshipTo(
        "backend.database.models.infra.locations.CityNode",
        "LOCATED_IN", cardinality=ZeroOrOne)

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
        -(u:Unit)-[]-(:Employment)-[]-(o:Officer)
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

    @classmethod
    def search(
        cls,
        query: str | None = None,
        filters: dict | None = None,
        city_uids: list[str] | None = None,
        source_uids: list[str] | None = None,
        count: bool = False,
        skip: int = 0,
        limit: int = 25
    ):
        """
        Model-specific search for Agency.
        Decides which fulltext index to use and delegates to the
        shared _search() in the mixin.
        """

        filters = filters or {}
        params = {
            **filters,
            "city_uids": city_uids or [],
            "source_uids": source_uids or [],
        }
        cypher_parts = []

        if query:
            cypher_parts.append("""
            CALL db.index.fulltext.queryNodes('agencyNames', $query)
            YIELD node, score
            WITH DISTINCT node AS n, score
            """)
            params["query"] = query
        else:
            cypher_parts.append("""
            MATCH (n:Agency)
            WITH DISTINCT n, 0 AS score
            """)

        where_clauses = []
        for key, value in filters.items():
            if isinstance(value, list):
                where_clauses.append(f"n.{key} IN ${key}")
            else:
                where_clauses.append(f"n.{key} = ${key}")
        where_clauses.append("""
        (
            size($city_uids) = 0 OR EXISTS {
                MATCH (n)-[:LOCATED_IN]->(city:CityNode)
                WHERE city.uid IN $city_uids
            }
        )
        """)
        where_clauses.append("""
        (
            size($source_uids) = 0 OR EXISTS {
                MATCH (n)-[:UPDATED_BY]->(source:Source)
                WHERE source.uid IN $source_uids
            }
        )
        """)
        cypher_parts.append("WHERE " + " AND ".join(where_clauses))
        cypher_parts.append("WITH n, max(score) AS score")

        if count:
            cypher_parts.append("RETURN count(n) AS count")
            rows, _ = db.cypher_query("\n".join(cypher_parts), params)
            return rows[0][0] if rows else 0

        cypher_parts.append("""
        RETURN n
        ORDER BY score DESC, n.uid ASC
        SKIP $skip
        LIMIT $limit
        """)
        params.update({"skip": skip, "limit": limit})
        rows, _ = db.cypher_query("\n".join(cypher_parts), params)
        return [row[0] for row in rows]

    @classmethod
    def preprocess_query(cls, query: str) -> str:
        """
        Preprocess the search query for Agency.
        Currently a placeholder for future preprocessing logic.
        Args:
            query (str): The original search query.
        Returns:
            str: The preprocessed search query.
        """
        watchlist = ["police", "department", "sheriff", "office", "of", "the"]

        return cls._preprocess_query(query, watchlist)
