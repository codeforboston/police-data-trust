from flask import abort
from backend.database.models.agency import Unit
from backend.schemas import add_pagination_wrapper
from backend.queries.units import fetch_unit_detail
from backend.serializers.unit_serializer import (
    serialize_unit_list,
    serialize_unit_search_results,
    serialize_unit_detail,
)


class UnitService:
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
        result = fetch_unit_detail(uid=uid, includes=includes)
        if not result:
            abort(404, description="Unit not found")

        return serialize_unit_detail(result, includes)
