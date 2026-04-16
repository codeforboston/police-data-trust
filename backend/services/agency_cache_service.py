from datetime import datetime

from backend.queries.agency_cache import AgencyCacheQueries


class AgencyCacheService:
    def __init__(self, queries: AgencyCacheQueries | None = None):
        self.queries = queries or AgencyCacheQueries()

    def refresh_agency_metrics_cache(
        self,
        *,
        batch_size: int = 500,
    ) -> dict:
        rows = self.queries.fetch_agency_metrics_inputs()
        updates: list[dict] = []
        updated = 0
        updated_at = datetime.now().isoformat()

        for (
            agency_uid,
            unit_count,
            officer_count,
            complaint_count,
            allegation_count,
        ) in rows:
            updates.append(
                {
                    "agency_uid": agency_uid,
                    "unit_count_cached": unit_count,
                    "officer_count_cached": officer_count,
                    "complaint_count_cached": complaint_count,
                    "allegation_count_cached": allegation_count,
                    "metrics_updated_at": updated_at,
                }
            )

            if len(updates) >= batch_size:
                updated += self.queries.update_agency_metrics_cache(updates)
                updates = []

        if updates:
            updated += self.queries.update_agency_metrics_cache(updates)

        return {
            "agencies_seen": len(rows),
            "agencies_updated": updated,
            "metrics_updated_at": updated_at,
        }
