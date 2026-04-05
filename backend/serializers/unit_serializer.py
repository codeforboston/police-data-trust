from backend.routes.search import (
    fetch_details, build_unit_result, build_officer_result)
from backend.serializers.location_serializer import (
    serialize_location
)
from backend.serializers.complaint_serializer import format_allegation_summary


def serialize_unit_list(rows):
    return [row.to_dict() for row in rows]


def serialize_unit_search_results(rows):
    details = fetch_details([row.get("uid") for row in rows], "Unit")
    units = [build_unit_result(
        row, details.get(row.get("uid"), {})) for row in rows]
    return [item.model_dump() for item in units if item]


def serialize_reported_officers(officers):
    if not officers:
        return []
    o_array = officers[0] if isinstance(officers[0], list) else officers

    details = fetch_details([o.uid for o in o_array], "Officer")
    built = [build_officer_result(o, details.get(o.uid, {})) for o in o_array]
    dumped = [item.model_dump() for item in built if item]

    for item in dumped:
        item["last_updated"] = (
            item["last_updated"].isoformat()
            if item.get("last_updated")
            else None
        )
    return dumped


def serialize_unit_profile(result: dict, includes: list[str]) -> dict:
    unit = result["u"]
    agency = result["a"]

    data = unit.to_dict()
    data["agency"] = agency.to_dict(
        include_relationships=False) if agency else None

    if "reported_officers" in includes:
        data["most_reported_officers"] = serialize_reported_officers(
            result.get("most_reported_officers", [])
        )

    if "officers" in includes:
        data["total_officers"] = result.get("total_officers", 0)

    if "complaints" in includes:
        data["total_complaints"] = result.get("total_complaints", 0)
        data["total_allegations"] = result.get("total_allegations", 0)

    if "allegations" in includes:
        data["allegation_summary"] = format_allegation_summary(
            result.get("allegation_summary", [])
        )

    if "location" in includes:
        data["location"] = serialize_location(result.get("location"))

    return data
