from datetime import datetime

from backend.queries.officer_cache import OfficerCacheQueries


class OfficerCacheService:
    def __init__(self, queries: OfficerCacheQueries | None = None):
        self.queries = queries or OfficerCacheQueries()

    def refresh_officer_metrics_cache(
        self,
        *,
        batch_size: int = 500,
    ) -> dict:
        rows = self.queries.fetch_officer_metrics_inputs()
        updates: list[dict] = []
        updated = 0
        updated_at = datetime.now().isoformat()

        for (
            officer_uid,
            complaint_count,
            allegation_count,
            substantiated_count,
        ) in rows:
            updates.append(
                {
                    "officer_uid": officer_uid,
                    "complaint_count_cached": complaint_count,
                    "allegation_count_cached": allegation_count,
                    "substantiated_count_cached": substantiated_count,
                    "metrics_updated_at": updated_at,
                }
            )

            if len(updates) >= batch_size:
                updated += self.queries.update_officer_metrics_cache(updates)
                updates = []

        if updates:
            updated += self.queries.update_officer_metrics_cache(updates)

        return {
            "officers_seen": len(rows),
            "officers_updated": updated,
            "metrics_updated_at": updated_at,
        }
