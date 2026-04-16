from neomodel import db


OFFICER_METRICS_INPUT_QUERY = """
MATCH (o:Officer)
CALL (o) {
    OPTIONAL MATCH (o)-[:ACCUSED_OF]->(al:Allegation)-[:ALLEGED]->(c:Complaint)
    RETURN
        count(DISTINCT c) AS complaint_count,
        count(DISTINCT al) AS allegation_count,
        sum(
            CASE
                WHEN toLower(trim(coalesce(al.finding, ""))) = "substantiated"
                THEN 1 ELSE 0
            END
        ) AS substantiated_count
}
RETURN
    o.uid AS officer_uid,
    complaint_count,
    allegation_count,
    substantiated_count
ORDER BY officer_uid ASC
"""

UPDATE_OFFICER_METRICS_CACHE_QUERY = """
UNWIND $updates AS row
MATCH (o:Officer {uid: row.officer_uid})
SET
    o.complaint_count_cached = row.complaint_count_cached,
    o.allegation_count_cached = row.allegation_count_cached,
    o.substantiated_count_cached = row.substantiated_count_cached,
    o.metrics_updated_at = datetime(row.metrics_updated_at)
RETURN count(o) AS updated
"""


class OfficerCacheQueries:
    def fetch_officer_metrics_inputs(self):
        rows, _ = db.cypher_query(OFFICER_METRICS_INPUT_QUERY)
        return rows

    def update_officer_metrics_cache(self, updates: list[dict]) -> int:
        if not updates:
            return 0

        rows, _ = db.cypher_query(
            UPDATE_OFFICER_METRICS_CACHE_QUERY,
            {"updates": updates},
        )
        return rows[0][0] if rows else 0
