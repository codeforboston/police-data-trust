from neomodel import db

CITY_LOOKUP_QUERY = """
CALL db.index.fulltext.queryNodes("cityNames", $term) YIELD node, score
MATCH (node)-[:WITHIN_COUNTY]->(:CountyNode)-[:WITHIN_STATE]->(state:StateNode)
WHERE $state IS NULL OR state.abbreviation = $state
RETURN
    node.uid AS uid,
    node.name AS city_name,
    node.sm_id AS sm_id,
    state.abbreviation AS state_abbreviation,
    state.name AS state_name,
    score
ORDER BY
CASE
    WHEN toLower(node.name) = $normalized_term THEN 0
    WHEN toLower(node.name) STARTS WITH $normalized_term THEN 1
    ELSE 2
END ASC,
score DESC,
node.name ASC,
state.abbreviation ASC
SKIP $skip
LIMIT $limit
"""


CITY_LOOKUP_COUNT_QUERY = """
CALL db.index.fulltext.queryNodes("cityNames", $term) YIELD node
MATCH (node)-[:WITHIN_COUNTY]->(:CountyNode)-[:WITHIN_STATE]->(state:StateNode)
WHERE $state IS NULL OR state.abbreviation = $state
RETURN count(DISTINCT node) AS total
"""

COUNTY_LOOKUP_QUERY = """
CALL db.index.fulltext.queryNodes("countyNames", $term) YIELD node, score
MATCH (node)-[:WITHIN_STATE]->(state:StateNode)
WHERE $state IS NULL OR state.abbreviation = $state
RETURN
    node.uid AS uid,
    node.name AS county_name,
    node.fips AS fips,
    state.abbreviation AS state_abbreviation,
    state.name AS state_name,
    score
ORDER BY
CASE
    WHEN toLower(node.name) = $normalized_term THEN 0
    WHEN toLower(node.name) STARTS WITH $normalized_term THEN 1
    ELSE 2
END ASC,
score DESC,
node.name ASC,
state.abbreviation ASC
SKIP $skip
LIMIT $limit
"""


COUNTY_LOOKUP_COUNT_QUERY = """
CALL db.index.fulltext.queryNodes("countyNames", $term) YIELD node
MATCH (node)-[:WITHIN_STATE]->(state:StateNode)
WHERE $state IS NULL OR state.abbreviation = $state
RETURN count(DISTINCT node) AS total
"""


STATE_LOOKUP_QUERY = """
MATCH (state:StateNode)
WHERE
    toLower(state.name) CONTAINS $normalized_term
    OR toLower(state.abbreviation) CONTAINS $normalized_term
RETURN
    state.uid AS uid,
    state.name AS state_name,
    state.abbreviation AS state_abbreviation
ORDER BY
CASE
    WHEN toLower(state.name) = $normalized_term THEN 0
    WHEN toLower(state.abbreviation) = $normalized_term THEN 0
    WHEN toLower(state.name) STARTS WITH $normalized_term THEN 1
    WHEN toLower(state.abbreviation) STARTS WITH $normalized_term THEN 1
    ELSE 2
END ASC,
state.name ASC
SKIP $skip
LIMIT $limit
"""


STATE_LOOKUP_COUNT_QUERY = """
MATCH (state:StateNode)
WHERE
    toLower(state.name) CONTAINS $normalized_term
    OR toLower(state.abbreviation) CONTAINS $normalized_term
RETURN count(DISTINCT state) AS total
"""


class LocationQueries:
    def build_city_lookup_term(self, term: str) -> str:
        normalized = " ".join(term.split())
        if not normalized:
            raise ValueError("term is required")
        return f"{normalized}*"

    def count_matching_cities(
        self, *, term: str, state: str | None = None
    ) -> int:
        params = {
            "term": self.build_city_lookup_term(term),
            "normalized_term": " ".join(term.lower().split()),
            "state": state,
        }
        rows, _ = db.cypher_query(CITY_LOOKUP_COUNT_QUERY, params)
        return rows[0][0] if rows else 0

    def fetch_matching_cities(
        self,
        *,
        term: str,
        state: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ):
        params = {
            "term": self.build_city_lookup_term(term),
            "normalized_term": " ".join(term.lower().split()),
            "state": state,
            "skip": skip,
            "limit": limit,
        }
        rows, _ = db.cypher_query(CITY_LOOKUP_QUERY, params)
        return rows

    def count_matching_counties(
        self, *, term: str, state: str | None = None
    ) -> int:
        params = {
            "term": self.build_city_lookup_term(term),
            "normalized_term": " ".join(term.lower().split()),
            "state": state,
        }
        rows, _ = db.cypher_query(COUNTY_LOOKUP_COUNT_QUERY, params)
        return rows[0][0] if rows else 0

    def fetch_matching_counties(
        self,
        *,
        term: str,
        state: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ):
        params = {
            "term": self.build_city_lookup_term(term),
            "normalized_term": " ".join(term.lower().split()),
            "state": state,
            "skip": skip,
            "limit": limit,
        }
        rows, _ = db.cypher_query(COUNTY_LOOKUP_QUERY, params)
        return rows

    def count_matching_states(self, *, term: str) -> int:
        params = {
            "normalized_term": " ".join(term.lower().split()),
        }
        rows, _ = db.cypher_query(STATE_LOOKUP_COUNT_QUERY, params)
        return rows[0][0] if rows else 0

    def fetch_matching_states(
        self,
        *,
        term: str,
        skip: int = 0,
        limit: int = 20,
    ):
        params = {
            "normalized_term": " ".join(term.lower().split()),
            "skip": skip,
            "limit": limit,
        }
        rows, _ = db.cypher_query(STATE_LOOKUP_QUERY, params)
        return rows
