from datetime import date
import math

from backend.queries.location_cache import LocationCacheQueries


class LocationCacheService:
    def __init__(self, queries: LocationCacheQueries | None = None):
        self.queries = queries or LocationCacheQueries()

    @staticmethod
    def compute_richness_score(
        *,
        agency_count: int,
        officer_count: int,
        complaint_count: int,
        population: int,
    ) -> float:
        score = (
            agency_count * 10
            + officer_count * 2
            + complaint_count * 5
            + math.log10((population or 0) + 1)
        )
        return round(score, 4)

    def refresh_city_richness_cache(
        self,
        *,
        batch_size: int = 500,
    ) -> dict:
        rows = self.queries.fetch_city_richness_inputs()
        updates: list[dict] = []
        updated = 0
        updated_at = date.today().isoformat()

        for (
            city_uid,
            population,
            agency_count,
            officer_count,
            complaint_count,
        ) in rows:
            updates.append(
                {
                    "city_uid": city_uid,
                    "agency_count_cached": agency_count,
                    "officer_count_cached": officer_count,
                    "complaint_count_cached": complaint_count,
                    "richness_score_cached": self.compute_richness_score(
                        agency_count=agency_count,
                        officer_count=officer_count,
                        complaint_count=complaint_count,
                        population=population,
                    ),
                    "richness_updated_at": updated_at,
                }
            )

            if len(updates) >= batch_size:
                updated += self.queries.update_city_richness_cache(updates)
                updates = []

        if updates:
            updated += self.queries.update_city_richness_cache(updates)

        return {
            "cities_seen": len(rows),
            "cities_updated": updated,
            "richness_updated_at": updated_at,
        }

    def refresh_county_richness_cache(
        self,
        *,
        batch_size: int = 500,
    ) -> dict:
        rows = self.queries.fetch_county_richness_inputs()
        updates: list[dict] = []
        updated = 0
        updated_at = date.today().isoformat()

        for (
            county_uid,
            population,
            agency_count,
            officer_count,
            complaint_count,
        ) in rows:
            updates.append(
                {
                    "county_uid": county_uid,
                    "agency_count_cached": agency_count,
                    "officer_count_cached": officer_count,
                    "complaint_count_cached": complaint_count,
                    "richness_score_cached": self.compute_richness_score(
                        agency_count=agency_count,
                        officer_count=officer_count,
                        complaint_count=complaint_count,
                        population=population,
                    ),
                    "richness_updated_at": updated_at,
                }
            )

            if len(updates) >= batch_size:
                updated += self.queries.update_county_richness_cache(updates)
                updates = []

        if updates:
            updated += self.queries.update_county_richness_cache(updates)

        return {
            "counties_seen": len(rows),
            "counties_updated": updated,
            "richness_updated_at": updated_at,
        }

    def refresh_location_richness_cache(
        self,
        *,
        batch_size: int = 500,
    ) -> dict:
        city_result = self.refresh_city_richness_cache(batch_size=batch_size)
        county_result = self.refresh_county_richness_cache(
            batch_size=batch_size,
        )
        return {
            **city_result,
            **county_result,
            "richness_updated_at": city_result["richness_updated_at"],
        }
