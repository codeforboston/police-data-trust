import logging
from flask import abort

from backend.serializers.search_serializer import (
    build_unit_result,
    fetch_details,
)
from backend.serializers.location_serializer import serialize_location
from backend.serializers.complaint_serializer import format_allegation_summary


def serialize_reported_units(units: list[dict] | list) -> list[dict]:
    if not units:
        return []
    u_array = units[0] if isinstance(units[0], list) else units

    details = fetch_details([u.uid for u in u_array], "Unit")
    logging.debug(f"Fetched details for reported units: {details}")
    try:
        built = [build_unit_result(u, details.get(u.uid, {})) for u in u_array]
    except Exception as e:
        logging.error(f"Error building unit results: {e}")
        abort(500, description="Error building unit results")
    dumped = [item.model_dump() for item in built if item]

    for item in dumped:
        item["last_updated"] = (
            item["last_updated"].isoformat()
            if item.get("last_updated")
            else None
        )
    return dumped


def serialize_agency_profile(result: dict, includes: list[str]) -> dict:
    agency = result["a"]
    data = agency.to_dict()

    if "units" in includes:
        data["total_units"] = result.get("total_units", 0)

    if "officers" in includes:
        data["total_officers"] = result.get("total_officers", 0)

    if "complaints" in includes:
        data["total_complaints"] = result.get("total_complaints", 0)
        data["total_allegations"] = result.get("total_allegations", 0)

    if "allegations" in includes:
        data["allegation_summary"] = format_allegation_summary(
            result.get("allegation_summary", [])
        )

    if "reported_units" in includes:
        logging.debug(
            f"Serializing reported units with data: {result.get(
                'most_reported_units', [])}")
        data["most_reported_units"] = serialize_reported_units(
            result.get("most_reported_units", [])
        )

    if "location" in includes:
        data["location"] = serialize_location(result.get("location"))

    return data
