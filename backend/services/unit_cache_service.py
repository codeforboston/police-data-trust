from datetime import datetime

from backend.queries.unit_cache import UnitCacheQueries


class UnitCacheService:
    def __init__(self, queries: UnitCacheQueries | None = None):
        self.queries = queries or UnitCacheQueries()

    def refresh_unit_metrics_cache(
        self,
        *,
        batch_size: int = 500,
    ) -> dict:
        rows = self.queries.fetch_unit_metrics_inputs()
        updates: list[dict] = []
        updated = 0
        updated_at = datetime.now().isoformat()

        for (
            unit_uid,
            officer_count,
            complaint_count,
            allegation_count,
        ) in rows:
            updates.append(
                {
                    "unit_uid": unit_uid,
                    "officer_count_cached": officer_count,
                    "complaint_count_cached": complaint_count,
                    "allegation_count_cached": allegation_count,
                    "metrics_updated_at": updated_at,
                }
            )

            if len(updates) >= batch_size:
                updated += self.queries.update_unit_metrics_cache(updates)
                updates = []

        if updates:
            updated += self.queries.update_unit_metrics_cache(updates)

        return {
            "units_seen": len(rows),
            "units_updated": updated,
            "metrics_updated_at": updated_at,
        }
