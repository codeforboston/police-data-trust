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
            return {"results": [], "page": page, "per_page": per_page, "total": 0, "pages": 0}, 200

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
            for uid, city_name, sm_id, state_abbreviation, state_name, _score in rows
        ]

        response = add_pagination_wrapper(
            page_data=results,
            total=total,
            page_number=page,
            per_page=per_page,
        )
        return response, 200
