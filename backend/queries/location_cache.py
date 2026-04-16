from neomodel import db


CITY_RICHNESS_INPUT_QUERY = """
MATCH (city:CityNode)
CALL (city) {
    OPTIONAL MATCH (a:Agency)-[:LOCATED_IN]->(city)
    RETURN count(DISTINCT a) AS agency_count
}
CALL (city) {
    OPTIONAL MATCH (a:Agency)-[:LOCATED_IN]->(city)
    OPTIONAL MATCH (a)-[:ESTABLISHED_BY]-(:Unit)<-[:IN_UNIT]
        -(:Employment)-[:HELD_BY]-(o:Officer)
    RETURN count(DISTINCT o) AS officer_count
}
CALL (city) {
    OPTIONAL MATCH (c:Complaint)-[:LOCATED_IN]->(city)
    RETURN count(DISTINCT c) AS complaint_count
}
RETURN
    city.uid AS city_uid,
    coalesce(city.population, 0) AS population,
    agency_count,
    officer_count,
    complaint_count
ORDER BY city_uid ASC
"""

COUNTY_RICHNESS_INPUT_QUERY = """
MATCH (county:CountyNode)
CALL (county) {
    OPTIONAL MATCH (city:CityNode)-[:WITHIN_COUNTY]->(county)
    RETURN coalesce(sum(city.population), 0) AS population
}
CALL (county) {
    OPTIONAL MATCH (city:CityNode)-[:WITHIN_COUNTY]->(county)
    OPTIONAL MATCH (a:Agency)-[:LOCATED_IN]->(city)
    RETURN count(DISTINCT a) AS agency_count
}
CALL (county) {
    OPTIONAL MATCH (city:CityNode)-[:WITHIN_COUNTY]->(county)
    OPTIONAL MATCH (a:Agency)-[:LOCATED_IN]->(city)
    OPTIONAL MATCH (a)-[:ESTABLISHED_BY]-(:Unit)<-[:IN_UNIT]
        -(:Employment)-[:HELD_BY]-(o:Officer)
    RETURN count(DISTINCT o) AS officer_count
}
CALL (county) {
    OPTIONAL MATCH (city:CityNode)-[:WITHIN_COUNTY]->(county)
    OPTIONAL MATCH (c:Complaint)-[:LOCATED_IN]->(city)
    RETURN count(DISTINCT c) AS complaint_count
}
RETURN
    county.uid AS county_uid,
    population,
    agency_count,
    officer_count,
    complaint_count
ORDER BY county_uid ASC
"""


UPDATE_CITY_RICHNESS_CACHE_QUERY = """
UNWIND $updates AS row
MATCH (city:CityNode {uid: row.city_uid})
SET
    city.agency_count_cached = row.agency_count_cached,
    city.officer_count_cached = row.officer_count_cached,
    city.complaint_count_cached = row.complaint_count_cached,
    city.richness_score_cached = row.richness_score_cached,
    city.richness_updated_at = date(row.richness_updated_at)
RETURN count(city) AS updated
"""

UPDATE_COUNTY_RICHNESS_CACHE_QUERY = """
UNWIND $updates AS row
MATCH (county:CountyNode {uid: row.county_uid})
SET
    county.agency_count_cached = row.agency_count_cached,
    county.officer_count_cached = row.officer_count_cached,
    county.complaint_count_cached = row.complaint_count_cached,
    county.richness_score_cached = row.richness_score_cached,
    county.richness_updated_at = date(row.richness_updated_at)
RETURN count(county) AS updated
"""


class LocationCacheQueries:
    def fetch_city_richness_inputs(self):
        rows, _ = db.cypher_query(CITY_RICHNESS_INPUT_QUERY)
        return rows

    def fetch_county_richness_inputs(self):
        rows, _ = db.cypher_query(COUNTY_RICHNESS_INPUT_QUERY)
        return rows

    def update_city_richness_cache(self, updates: list[dict]) -> int:
        if not updates:
            return 0

        rows, _ = db.cypher_query(
            UPDATE_CITY_RICHNESS_CACHE_QUERY,
            {"updates": updates},
        )
        return rows[0][0] if rows else 0

    def update_county_richness_cache(self, updates: list[dict]) -> int:
        if not updates:
            return 0

        rows, _ = db.cypher_query(
            UPDATE_COUNTY_RICHNESS_CACHE_QUERY,
            {"updates": updates},
        )
        return rows[0][0] if rows else 0
