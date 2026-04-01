from backend.database.models.agency import Unit
from backend.queries.units import UnitQueries
from backend.schemas import add_pagination_wrapper
from backend.serializers.unit_serializer import (
    serialize_unit_list,
    serialize_unit_search_results,
    serialize_unit_profile,
)
from backend.serializers.officer_serializer import (
    serialize_officer_rows
)


class UnitService:
    def __init__(self):
        self.queries = UnitQueries()

    def list_units(self, params):
        search_term = params.name
        filters = {
            k: v for k, v in {
                "city": params.city,
                "state": params.state,
            }.items() if v
        }

        row_count = Unit.search(query=search_term, filters=filters, count=True)

        if row_count == 0:
            return {
                "message": "No results found matching the query"}, 200, False

        if row_count <= params.skip:
            return {"message": "Page number exceeds total results"}, 400, False

        results = Unit.search(
            query=search_term,
            filters=filters,
            skip=params.skip,
            limit=params.per_page,
            inflate=not params.searchResult,
        )

        if params.searchResult:
            page = serialize_unit_search_results(results)
            use_ordered = False
        else:
            page = serialize_unit_list(results)
            use_ordered = True

        response = add_pagination_wrapper(
            page_data=page,
            total=row_count,
            page_number=params.page,
            per_page=params.per_page,
        )
        return response, 200, use_ordered

    def get_unit(self, uid: str, includes: list[str]) -> dict:
        result = self.queries.fetch_unit_profile(uid=uid, includes=includes)
        if not result:
            raise ValueError("Unit not found")

        return serialize_unit_profile(result, includes)

    def list_unit_officers(
        self,
        unit_uid: str,
        page: int,
        per_page: int,
        includes: list[str],
    ) -> dict:
        unit = Unit.nodes.get_or_none(uid=unit_uid)
        if not unit:
            raise ValueError("Unit not found")
        include_employment = "employment" in includes
        total = self.queries.count_unit_officers(unit_uid)

        if total == 0:
            return {
                "message": "No officers found for this unit"
            }

        skip = (page - 1) * per_page
        if total <= skip:
            raise IndexError("Page number exceeds total results")

        rows = self.queries.fetch_unit_officers(
            unit_uid=unit_uid,
            skip=skip,
            limit=per_page,
            include_employment=include_employment,
        )

        officers = serialize_officer_rows(
            rows,
            include_employment=include_employment,
        )

        return add_pagination_wrapper(
            page_data=officers,
            total=total,
            page_number=page,
            per_page=per_page,
        )
