from neomodel import db


AGENCY_METRICS_INPUT_QUERY = """
MATCH (a:Agency)
CALL (a) {
    OPTIONAL MATCH (a)-[:ESTABLISHED_BY]-(u:Unit)
    RETURN count(DISTINCT u) AS unit_count
}
CALL (a) {
    OPTIONAL MATCH (a)-[:ESTABLISHED_BY]-(:Unit)<-[:IN_UNIT]
        -(:Employment)-[:HELD_BY]-(o:Officer)
    RETURN count(DISTINCT o) AS officer_count
}
CALL (a) {
    OPTIONAL MATCH (a)-[:ESTABLISHED_BY]-(:Unit)<-[:IN_UNIT]
        -(:Employment)-[:HELD_BY]-(:Officer)
        -[:ACCUSED_OF]->(al:Allegation)-[:ALLEGED]-(c:Complaint)
    RETURN
        count(DISTINCT c) AS complaint_count,
        count(DISTINCT al) AS allegation_count
}
RETURN
    a.uid AS agency_uid,
    unit_count,
    officer_count,
    complaint_count,
    allegation_count
ORDER BY agency_uid ASC
"""

UPDATE_AGENCY_METRICS_CACHE_QUERY = """
UNWIND $updates AS row
MATCH (a:Agency {uid: row.agency_uid})
SET
    a.unit_count_cached = row.unit_count_cached,
    a.officer_count_cached = row.officer_count_cached,
    a.complaint_count_cached = row.complaint_count_cached,
    a.allegation_count_cached = row.allegation_count_cached,
    a.metrics_updated_at = datetime(row.metrics_updated_at)
RETURN count(a) AS updated
"""


class AgencyCacheQueries:
    def fetch_agency_metrics_inputs(self):
        rows, _ = db.cypher_query(AGENCY_METRICS_INPUT_QUERY)
        return rows

    def update_agency_metrics_cache(self, updates: list[dict]) -> int:
        if not updates:
            return 0

        rows, _ = db.cypher_query(
            UPDATE_AGENCY_METRICS_CACHE_QUERY,
            {"updates": updates},
        )
        return rows[0][0] if rows else 0
