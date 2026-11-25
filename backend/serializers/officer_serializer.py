from backend.database.utils.transform import transform_dates_in_dict
from backend.serializers.search_serializer import (
    build_officer_result,
    fetch_details,
)


def serialize_officer_sources(rows: list[dict]) -> list[dict]:
    return rows or []


def serialize_employment_history(rows: list[dict]) -> list[dict]:
    return [transform_dates_in_dict(row) for row in rows]


def serialize_allegation_summary(rows) -> list[dict]:
    summary = []
    for row in rows:
        summary.append({
            "type": row[0],
            "complaint_count": row[1],
            "count": row[2],
            "substantiated_count": row[3],
            "earliest_incident_date": row[4].isoformat() if row[4] else None,
            "latest_incident_date": row[5].isoformat() if row[5] else None,
        })
    return summary


def serialize_officer_list(rows):
    return [row.to_dict() for row in rows]


def serialize_officer_rows(rows, include_employment: bool) -> list[dict]:
    """Officer-list rows: (officer, employment, exact_match), or
    (officer, exact_match) without employment."""
    officers = []
    for row in rows:
        officer = row[0]
        officer_dict = officer.to_dict(include_relationships=False)

        if include_employment:
            officer_dict["employment"] = transform_dates_in_dict(row[1])

        # Whether the officer exactly matches the search box; None when
        # nothing was searched.
        officer_dict["exact_match"] = row[-1]
        officers.append(officer_dict)
    return officers


def serialize_officer_search_results(rows):
    """Search-result cards for (officer node, exact_match) pairs."""
    details = fetch_details([node.get("uid") for node, _ in rows], "Officer")
    officers = [
        build_officer_result(
            node,
            details.get(node.get("uid"), {}),
            exact_match) for node, exact_match in rows]
    return [item.model_dump() for item in officers if item]


def serialize_officer_profile(
    officer,
    sources=None,
    employment_history=None,
    allegation_summary=None,
):
    data = officer.to_dict()
    data["sources"] = sources or []

    if employment_history is not None:
        data["employment_history"] = employment_history

    if allegation_summary is not None:
        data["allegation_summary"] = allegation_summary

    return data
