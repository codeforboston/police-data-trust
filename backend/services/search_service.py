from backend.schemas import add_pagination_wrapper
from backend.queries.search import SearchQueries
from backend.serializers.search_serializer import (
    build_agency_result,
    build_officer_result,
    build_unit_result,
    get_node_type,
    group_nodes_by_type,
)


class SearchService:
    def __init__(self, queries: SearchQueries | None = None):
        self.queries = queries or SearchQueries()

    def search_text(
        self,
        *,
        query: str,
        page: int,
        per_page: int,
        city: str | list[str] | None = None,
        city_uid: str | list[str] | None = None,
        state: str | None = None,
        source: str | list[str] | None = None,
        source_uid: str | list[str] | None = None,
    ) -> tuple[dict, int]:
        city_uids = self.queries.resolve_search_city_uids(
            city=city,
            city_uid=city_uid,
            state=state,
        )
        if (city or city_uid or state) and not city_uids:
            return {"message": "No results found matching the query"}, 200

        source_uids = self.queries.resolve_search_source_uids(
            source=source,
            source_uid=source_uid,
        )
        if (source or source_uid) and not source_uids:
            return {"message": "No results found matching the query"}, 200

        total_results = self.queries.count_search_results(
            query=query,
            page=page,
            per_page=per_page,
            city_uids=city_uids,
            source_uids=source_uids,
        )

        if total_results == 0:
            return {"message": "No results found matching the query"}, 200

        skip = (page - 1) * per_page
        if total_results <= skip:
            return {"message": "Page number exceeds total results"}, 400

        results = self.queries.fetch_search_results(
            query=query,
            page=page,
            per_page=per_page,
            city_uids=city_uids,
            source_uids=source_uids,
        )
        buckets = group_nodes_by_type(results)
        details = self.queries.fetch_search_details(
            officer_uids=[
                node.get("uid")
                for node in buckets.get("Officer", [])
                if node.get("uid")
            ],
            agency_uids=[
                node.get("uid")
                for node in buckets.get("Agency", [])
                if node.get("uid")
            ],
            unit_uids=[
                node.get("uid")
                for node in buckets.get("Unit", [])
                if node.get("uid")
            ],
        )
        officer_details = details.get("Officer", {})
        agency_details = details.get("Agency", {})
        unit_details = details.get("Unit", {})

        page_data = []
        for node, _score in results:
            content_type = get_node_type(node)
            uid = node.get("uid") if hasattr(node, "get") else None

            if content_type == "Officer":
                item = build_officer_result(node, officer_details.get(uid, {}))
            elif content_type == "Agency":
                item = build_agency_result(node, agency_details.get(uid, {}))
            elif content_type == "Unit":
                item = build_unit_result(node, unit_details.get(uid, {}))
            else:
                continue

            page_data.append(item.model_dump())

        response = add_pagination_wrapper(
            page_data=page_data,
            total=total_results,
            page_number=page,
            per_page=per_page,
        )
        return response, 200
