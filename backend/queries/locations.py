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


NEARBY_CITY_LOOKUP_QUERY = """
WITH point({
    longitude: $longitude,
    latitude: $latitude,
    crs: 'wgs-84'
}) AS user_point
MATCH (city:CityNode)-[:WITHIN_COUNTY]->(:CountyNode)
    -[:WITHIN_STATE]->(state:StateNode)
WHERE city.coordinates IS NOT NULL
WITH
    city,
    state,
    point.distance(user_point, city.coordinates) AS distance_meters
RETURN
    city.uid AS uid,
    city.name AS city_name,
    city.sm_id AS sm_id,
    state.abbreviation AS state_abbreviation,
    state.name AS state_name,
    distance_meters
ORDER BY distance_meters ASC, coalesce(city.population, 0) DESC, city.name ASC
LIMIT $limit
"""


PROFILE_CITY_LOOKUP_QUERY = """
MATCH (city:CityNode {name: $city_name})
    -[:WITHIN_COUNTY]->(:CountyNode)-[:WITHIN_STATE]->(state:StateNode)
WHERE state.abbreviation = $state
RETURN
    city.uid AS uid,
    city.name AS city_name,
    city.sm_id AS sm_id,
    state.abbreviation AS state_abbreviation,
    state.name AS state_name
ORDER BY coalesce(city.population, 0) DESC, city.name ASC
LIMIT 1
"""


RICH_CITY_LOOKUP_QUERY = """
MATCH (city:CityNode)-[:WITHIN_COUNTY]->(:CountyNode)
    -[:WITHIN_STATE]->(state:StateNode)
WHERE
    city.coordinates IS NOT NULL
    AND ($state IS NULL OR state.abbreviation = $state)
    AND NOT city.uid IN $exclude_uids
RETURN
    city.uid AS uid,
    city.name AS city_name,
    city.sm_id AS sm_id,
    state.abbreviation AS state_abbreviation,
    state.name AS state_name,
    coalesce(city.agency_count_cached, 0) AS agency_count,
    coalesce(city.complaint_count_cached, 0) AS complaint_count,
    coalesce(city.officer_count_cached, 0) AS officer_count,
    coalesce(city.population, 0) AS population,
    coalesce(city.richness_score_cached, 0.0) AS richness_score
ORDER BY
    richness_score DESC,
    complaint_count DESC,
    officer_count DESC,
    agency_count DESC,
    population DESC,
    city.name ASC
LIMIT $limit
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

    def fetch_nearby_cities(
        self,
        *,
        latitude: float,
        longitude: float,
        limit: int = 5,
    ):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "limit": limit,
        }
        rows, _ = db.cypher_query(NEARBY_CITY_LOOKUP_QUERY, params)
        return rows

    def fetch_profile_city(
        self,
        *,
        city_name: str,
        state: str,
    ):
        params = {
            "city_name": " ".join(city_name.split()),
            "state": state.strip().upper(),
        }
        rows, _ = db.cypher_query(PROFILE_CITY_LOOKUP_QUERY, params)
        return rows[0] if rows else None

    def fetch_rich_cities(
        self,
        *,
        state: str | None = None,
        exclude_uids: list[str] | None = None,
        limit: int = 5,
    ):
        params = {
            "state": state.strip().upper() if state else None,
            "exclude_uids": exclude_uids or [],
            "limit": limit,
        }
        rows, _ = db.cypher_query(RICH_CITY_LOOKUP_QUERY, params)
        return rows
