from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional

from neomodel import db
from pydantic import BaseModel, field_validator

from backend.database.models.agency import Agency, Unit
from backend.database.models.officer import Officer

OFFICER_RESULT_QUERY = """
UNWIND $uids AS uid
  MATCH (o:Officer {uid: uid})

  CALL (o) {
    OPTIONAL MATCH (o)<-[]-(e:Employment)-[]-(u:Unit)-[]-(ag:Agency)
    WITH e, u, ag,
         CASE WHEN e.latest_date IS NULL THEN 1 ELSE 0 END AS isCurrent
    ORDER BY isCurrent DESC, e.earliest_date DESC
    RETURN e, u, ag
    LIMIT 1
  }

  CALL (o) {
    OPTIONAL MATCH (o)<-[:CHANGE_TO]-(c:Change)-[:ATTRIBUTED_TO]->
    (s:Source)
    RETURN s, c.timestamp AS updated_at
    ORDER BY updated_at DESC
    LIMIT 1
  }

  RETURN uid, {
    complaints: coalesce(o.complaint_count_cached, 0),
    allegations: coalesce(o.allegation_count_cached, 0),
    substantiated: coalesce(o.substantiated_count_cached, 0),
    rank: e.highest_rank,
    unit_name: u.name,
    agency_name: ag.name,
    source: s.name,
    last_updated: updated_at
  } AS result
"""


UNIT_RESULT_QUERY = """
UNWIND $uids AS uid
  MATCH (u:Unit {uid: uid})
  OPTIONAL MATCH (u)-[]-(a:Agency)

  CALL (u) {
    OPTIONAL MATCH (u)<-[:CHANGE_TO]-(c:Change)-[:ATTRIBUTED_TO]->
    (s:Source)
    RETURN s, c.timestamp AS updated_at
    ORDER BY updated_at DESC
    LIMIT 1
  }
  RETURN uid, {
    name: u.name,
    agency_name: a.name,
    officers: coalesce(u.officer_count_cached, 0),
    complaints: coalesce(u.complaint_count_cached, 0),
    source: s.name,
    last_updated: updated_at
  } as result
"""

AGENCY_RESULT_QUERY = """
  UNWIND $uids AS uid
  MATCH (a:Agency {uid: uid})

  CALL (a) {
    OPTIONAL MATCH (a)<-[:CHANGE_TO]-(c:Change)-[:ATTRIBUTED_TO]->
    (s:Source)
    RETURN s, c.timestamp AS updated_at
    ORDER BY updated_at DESC
    LIMIT 1
  }

  RETURN uid, {
    units: coalesce(a.unit_count_cached, 0),
    officers: coalesce(a.officer_count_cached, 0),
    complaints: coalesce(a.complaint_count_cached, 0),
    source: s.name,
    last_updated: updated_at
  } AS result
"""

DETAIL_QUERY_BY_TYPE = {
    "Officer": OFFICER_RESULT_QUERY,
    "Agency": AGENCY_RESULT_QUERY,
    "Unit": UNIT_RESULT_QUERY,
}


class SearchResult(BaseModel):
    uid: str
    title: str
    subtitle: Optional[str] = None
    details: Optional[List[str]] = None
    content_type: str
    source: str
    last_updated: datetime | None
    href: str

    @field_validator("last_updated", mode="before")
    @classmethod
    def coerce_neo4j_datetime(cls, value):
        if value is None:
            return None
        if hasattr(value, "to_native"):
            return value.to_native()
        return value


def get_node_type(node) -> str | None:
    labels = set(node.labels or [])
    if "Officer" in labels:
        return "Officer"
    if "Agency" in labels:
        return "Agency"
    if "Unit" in labels:
        return "Unit"
    return None


def group_nodes_by_type(results) -> Dict[str, List]:
    buckets: dict[str, list] = defaultdict(list)
    seen: dict[str, set] = defaultdict(set)

    for row in results:
        node = row[0]
        content_type = get_node_type(node)
        if not content_type:
            continue

        uid = node.get("uid") if hasattr(node, "get") else None
        if uid and uid in seen[content_type]:
            continue
        if uid:
            seen[content_type].add(uid)
            buckets[content_type].append(node)
    return buckets


def fetch_details(uids: List[str], content_type: str) -> Dict[str, dict]:
    if not uids:
        return {}

    query = DETAIL_QUERY_BY_TYPE.get(content_type)
    if not query:
        return {}

    rows, _ = db.cypher_query(query, {"uids": uids})
    return {uid: row or {} for uid, row in rows}


def build_agency_result(node, details_row: dict) -> SearchResult:
    agency = node if isinstance(node, Agency) else Agency.inflate(node)
    uid = agency.uid

    subtitle = "{} Agency in {}, {}".format(
        agency.jurisdiction_enum.describe() if agency.jurisdiction_enum else "",
        agency.hq_city if agency.hq_city else "Unknown City",
        agency.hq_state if agency.hq_state else "Unknown State",
    )

    return SearchResult(
        uid=uid,
        title=agency.name,
        subtitle=subtitle,
        details=[(
            "{} Unit(s), {} Officer(s), {} Complaint(s)".format(
                details_row.get("units", 0),
                details_row.get("officers", 0),
                details_row.get("complaints", 0),
            )
        )],
        content_type="Agency",
        source=details_row.get("source") or "Unknown Source",
        last_updated=details_row.get("last_updated"),
        href=f"/api/v1/agencies/{uid}",
    )


def build_unit_result(node, details_row: dict) -> SearchResult:
    unit = node if isinstance(node, Unit) else Unit.inflate(node)
    uid = unit.uid

    return SearchResult(
        uid=uid,
        title=unit.name,
        subtitle="Established by {}".format(
            details_row.get("agency_name", "Unknown Agency")
        ),
        details=[(
            "{} Officer(s), {} Complaint(s)".format(
                details_row.get("officers", 0),
                details_row.get("complaints", 0),
            )
        )],
        content_type="Unit",
        source=details_row.get("source") or "Unknown Source",
        last_updated=details_row.get("last_updated"),
        href=f"/api/v1/units/{uid}",
    )


def build_officer_result(node, details_row: dict) -> SearchResult:
    officer = node if isinstance(node, Officer) else Officer.inflate(node)
    uid = officer.uid

    subtitle = "{ethnicity} {gender}, {rank} at the {agency}".format(
        ethnicity=(
            officer.ethnicity_enum.describe()
            if officer.ethnicity_enum else "Unknown Ethnicity"
        ),
        gender=(
            officer.gender_enum.describe()
            if officer.gender_enum else "Unknown Gender"
        ),
        rank=details_row.get("rank", "Officer"),
        agency=details_row.get("agency_name", "Unknown Agency"),
    )

    return SearchResult(
        uid=uid,
        title=officer.full_name,
        subtitle=subtitle,
        details=[(
            "{} Complaints, {} Allegations, {} Substantiated".format(
                details_row.get("complaints", 0),
                details_row.get("allegations", 0),
                details_row.get("substantiated", 0),
            )
        )],
        content_type="Officer",
        source=details_row.get("source") or "Unknown Source",
        last_updated=details_row.get("last_updated"),
        href=f"/api/v1/officers/{uid}",
    )
