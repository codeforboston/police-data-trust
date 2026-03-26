from backend.database.utils.transform import transform_dates_in_dict
from backend.routes.search import fetch_details, build_officer_result


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


def serialize_officer_search_results(rows):
    details = fetch_details([row.get("uid") for row in rows], "Officer")
    officers = [
        build_officer_result(
            row,
            details.get(row.get("uid"), {})) for row in rows]
    return [item.model_dump() for item in officers if item]


def serialize_officer_detail(
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
