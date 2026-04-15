from backend.queries.locations import LocationQueries
from backend.schemas import add_pagination_wrapper


class LocationService:
    def __init__(self, queries: LocationQueries | None = None):
        self.queries = queries or LocationQueries()

    def list_cities(
        self,
        *,
        term: str,
        state: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[dict, int]:
        total = self.queries.count_matching_cities(term=term, state=state)

        if total == 0:
            return {
                "results": [],
                "page": page,
                "per_page": per_page,
                "total": 0,
                "pages": 0,
            }, 200

        skip = (page - 1) * per_page
        if total <= skip:
            return {"message": "Page number exceeds total results"}, 400

        rows = self.queries.fetch_matching_cities(
            term=term,
            state=state,
            skip=skip,
            limit=per_page,
        )
        results = [
            {
                "uid": uid,
                "name": city_name,
                "state": {
                    "abbreviation": state_abbreviation,
                    "name": state_name,
                },
                "sm_id": sm_id,
            }
            for (
                uid,
                city_name,
                sm_id,
                state_abbreviation,
                state_name,
                _score,
            ) in rows
        ]

        response = add_pagination_wrapper(
            page_data=results,
            total=total,
            page_number=page,
            per_page=per_page,
        )
        return response, 200

    def list_counties(
        self,
        *,
        term: str,
        state: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[dict, int]:
        total = self.queries.count_matching_counties(term=term, state=state)

        if total == 0:
            return {
                "results": [],
                "page": page,
                "per_page": per_page,
                "total": 0,
                "pages": 0,
            }, 200

        skip = (page - 1) * per_page
        if total <= skip:
            return {"message": "Page number exceeds total results"}, 400

        rows = self.queries.fetch_matching_counties(
            term=term,
            state=state,
            skip=skip,
            limit=per_page,
        )
        results = [
            {
                "uid": uid,
                "name": county_name,
                "fips": fips,
                "state": {
                    "abbreviation": state_abbreviation,
                    "name": state_name,
                },
            }
            for (
                uid,
                county_name,
                fips,
                state_abbreviation,
                state_name,
                _score,
            ) in rows
        ]

        response = add_pagination_wrapper(
            page_data=results,
            total=total,
            page_number=page,
            per_page=per_page,
        )
        return response, 200

    def list_states(
        self,
        *,
        term: str,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[dict, int]:
        total = self.queries.count_matching_states(term=term)

        if total == 0:
            return {
                "results": [],
                "page": page,
                "per_page": per_page,
                "total": 0,
                "pages": 0,
            }, 200

        skip = (page - 1) * per_page
        if total <= skip:
            return {"message": "Page number exceeds total results"}, 400

        rows = self.queries.fetch_matching_states(
            term=term,
            skip=skip,
            limit=per_page,
        )
        results = [
            {
                "uid": uid,
                "name": state_name,
                "abbreviation": state_abbreviation,
            }
            for uid, state_name, state_abbreviation in rows
        ]

        response = add_pagination_wrapper(
            page_data=results,
            total=total,
            page_number=page,
            per_page=per_page,
        )
        return response, 200

    def list_nearby_cities(
        self,
        *,
        latitude: float,
        longitude: float,
        per_page: int = 5,
    ) -> tuple[dict, int]:
        rows = self.queries.fetch_nearby_cities(
            latitude=latitude,
            longitude=longitude,
            limit=per_page,
        )

        results = [
            {
                "uid": uid,
                "name": city_name,
                "state": {
                    "abbreviation": state_abbreviation,
                    "name": state_name,
                },
                "sm_id": sm_id,
                "distance_meters": distance_meters,
            }
            for (
                uid,
                city_name,
                sm_id,
                state_abbreviation,
                state_name,
                distance_meters,
            ) in rows
        ]

        return {
            "results": results,
            "page": 1,
            "per_page": per_page,
            "total": len(results),
            "pages": 1 if results else 0,
        }, 200

    def list_relevant_cities(
        self,
        *,
        user_city: str | None = None,
        user_state: str | None = None,
        per_page: int = 5,
    ) -> tuple[dict, int]:
        results: list[dict] = []
        excluded_uids: list[str] = []

        if user_city and user_state:
            row = self.queries.fetch_profile_city(city_name=user_city, state=user_state)
            if row:
                uid, city_name, sm_id, state_abbreviation, state_name = row
                results.append(
                    {
                        "uid": uid,
                        "name": city_name,
                        "state": {
                            "abbreviation": state_abbreviation,
                            "name": state_name,
                        },
                        "sm_id": sm_id,
                        "reason": "profile_city",
                    }
                )
                excluded_uids.append(uid)

        remaining = max(per_page - len(results), 0)
        if remaining > 0:
            rows = self.queries.fetch_rich_cities(
                state=user_state,
                exclude_uids=excluded_uids,
                limit=remaining,
            )
            results.extend(
                {
                    "uid": uid,
                    "name": city_name,
                    "state": {
                        "abbreviation": state_abbreviation,
                        "name": state_name,
                    },
                    "sm_id": sm_id,
                    "reason": "data_rich",
                }
                for uid, city_name, sm_id, state_abbreviation, state_name, *_rest in rows
            )
            excluded_uids.extend([row[0] for row in rows])

        remaining = max(per_page - len(results), 0)
        if remaining > 0 and user_state:
            rows = self.queries.fetch_rich_cities(
                exclude_uids=excluded_uids,
                limit=remaining,
            )
            results.extend(
                {
                    "uid": uid,
                    "name": city_name,
                    "state": {
                        "abbreviation": state_abbreviation,
                        "name": state_name,
                    },
                    "sm_id": sm_id,
                    "reason": "data_rich",
                }
                for uid, city_name, sm_id, state_abbreviation, state_name, *_rest in rows
            )

        return {
            "results": results,
            "page": 1,
            "per_page": per_page,
            "total": len(results),
            "pages": 1 if results else 0,
        }, 200
