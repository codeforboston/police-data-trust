from backend.database.utils.transform import transform_dates_in_dict
from backend.routes.search import fetch_details, build_unit_result


def format_allegation_summary(summary: list[dict]) -> list[dict]:
    for item in summary or []:
        if item.get("earliest_incident_date"):
            item["earliest_incident_date"] = item[
                "earliest_incident_date"].isoformat()
        if item.get("latest_incident_date"):
            item["latest_incident_date"] = item[
                "latest_incident_date"].isoformat()
    return summary or []


def serialize_location(location: dict | None) -> dict | None:
    if not location or not location.get("coords"):
        return None
    return {
        "latitude": location["coords"].y,
        "longitude": location["coords"].x,
        "city": location["city"],
        "state": location["state"],
    }


def serialize_reported_units(units: list[dict] | list) -> list[dict]:
    if not units:
        return []

    details = fetch_details([u.get("uid") for u in units], "Unit")
    built = [build_unit_result(u, details.get(u.get("uid"), {})) for u in units]
    dumped = [item.model_dump() for item in built if item]

    for item in dumped:
        item["last_updated"] = (
            item["last_updated"].isoformat()
            if item.get("last_updated")
            else None
        )
    return dumped


def serialize_agency_profile_row(result: dict, includes: list[str]) -> dict:
    agency = result["a"]
    data = agency._properties.copy()

    if "units" in includes:
        data["total_units"] = result.get("total_units", 0)

    if "officers" in includes:
        data["total_officers"] = result.get("total_officers", 0)

    if "complaints" in includes:
        data["total_complaints"] = result.get("total_complaints", 0)

    if "allegations" in includes:
        data["allegation_summary"] = format_allegation_summary(
            result.get("allegation_summary", [])
        )

    if "reported_units" in includes:
        data["most_reported_units"] = serialize_reported_units(
            result.get("most_reported_units", [])
        )

    if "location" in includes:
        data["location"] = serialize_location(result.get("location"))

    return data


def serialize_officer_rows(rows, include_employment: bool) -> list[dict]:
    officers = []
    for row in rows:
        officer = row[0]
        officer_dict = officer.to_dict()

        if include_employment:
            officer_dict["employment"] = transform_dates_in_dict(row[1])

        officers.append(officer_dict)

    return officers
