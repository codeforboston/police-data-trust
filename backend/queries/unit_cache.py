from neomodel import db


UNIT_METRICS_INPUT_QUERY = """
MATCH (u:Unit)
CALL (u) {
    OPTIONAL MATCH (u)<-[:IN_UNIT]-(:Employment)-[:HELD_BY]-(o:Officer)
    RETURN count(DISTINCT o) AS officer_count
}
CALL (u) {
    OPTIONAL MATCH (u)<-[:IN_UNIT]-(:Employment)-[:HELD_BY]-(:Officer)
        -[:ACCUSED_OF]->(al:Allegation)-[:ALLEGED]-(c:Complaint)
    RETURN
        count(DISTINCT c) AS complaint_count,
        count(DISTINCT al) AS allegation_count
}
RETURN
    u.uid AS unit_uid,
    officer_count,
    complaint_count,
    allegation_count
ORDER BY unit_uid ASC
"""

UPDATE_UNIT_METRICS_CACHE_QUERY = """
UNWIND $updates AS row
MATCH (u:Unit {uid: row.unit_uid})
SET
    u.officer_count_cached = row.officer_count_cached,
    u.complaint_count_cached = row.complaint_count_cached,
    u.allegation_count_cached = row.allegation_count_cached,
    u.metrics_updated_at = datetime(row.metrics_updated_at)
RETURN count(u) AS updated
"""


class UnitCacheQueries:
    def fetch_unit_metrics_inputs(self):
        rows, _ = db.cypher_query(UNIT_METRICS_INPUT_QUERY)
        return rows

    def update_unit_metrics_cache(self, updates: list[dict]) -> int:
        if not updates:
            return 0

        rows, _ = db.cypher_query(
            UPDATE_UNIT_METRICS_CACHE_QUERY,
            {"updates": updates},
        )
        return rows[0][0] if rows else 0
