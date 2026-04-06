
def format_allegation_summary(summary: list[dict]) -> list[dict]:
    summary = summary[0]
    for item in summary or []:
        if item.get("earliest_incident_date"):
            item["earliest_incident_date"] = item[
                "earliest_incident_date"].isoformat()
        if item.get("latest_incident_date"):
            item["latest_incident_date"] = item[
                "latest_incident_date"].isoformat()
    return summary or []
