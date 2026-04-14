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


class LocationQueries:
    def build_city_lookup_term(self, term: str) -> str:
        normalized = " ".join(term.split())
        if not normalized:
            raise ValueError("term is required")
        return f"{normalized}*"

    def count_matching_cities(self, *, term: str, state: str | None = None) -> int:
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
