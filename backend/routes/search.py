from typing import Optional, List, Dict
from collections import defaultdict
from datetime import datetime

from backend.auth.jwt import min_role_required
from backend.database.models.user import UserRole
from backend.database.models.officer import Officer
from backend.database.models.agency import Agency, Unit
from backend.schemas import add_pagination_wrapper
from flask import Blueprint, abort, request
from flask_jwt_extended.view_decorators import jwt_required
from flask import jsonify
from pydantic import BaseModel, field_validator
from neomodel import db


bp = Blueprint("search_routes", __name__, url_prefix="/api/v1/search")

OFFICER_RESULT_QUERY = """
UNWIND $uids AS uid
  MATCH (o:Officer {uid: uid})
  OPTIONAL MATCH (o)-[:ACCUSED_OF]->(al:Allegation)-[:ALLEGED]->(co:Complaint)
  WITH
    uid,
    o,
    count(DISTINCT co) AS complaint_count,
    count(DISTINCT al) AS allegation_count,
    sum(
      CASE
        WHEN toLower(trim(coalesce(al.finding, ""))) = "substantiated"
        THEN 1 ELSE 0
      END
    ) AS substantiated_count

  CALL (o) {
    OPTIONAL MATCH (o)<-[]-(e:Employment)-[]-(u:Unit)-[]-(ag:Agency)
    WITH e, u, ag,
         CASE WHEN e.latest_date IS NULL THEN 1 ELSE 0 END AS isCurrent
    ORDER BY isCurrent DESC, e.earliest_date DESC
    RETURN e, u, ag
    LIMIT 1
  }

  CALL (o) {
    OPTIONAL MATCH (o)-[r:UPDATED_BY]->(s:Source)
    RETURN s, r
    ORDER BY r.timestamp DESC
    LIMIT 1
  }

  RETURN uid, {
    complaints: complaint_count,
    allegations: allegation_count,
    substantiated: substantiated_count,
    rank: e.highest_rank,
    unit_name: u.name,
    agency_name: ag.name,
    source: s.name,
    last_updated: r.timestamp
  } AS result
"""


UNIT_RESULT_QUERY = """
UNWIND $uids AS uid
  MATCH (u:Unit {uid: uid})
  OPTIONAL MATCH (u)-[]-(a:Agency)
  OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(o:Officer)
  OPTIONAL MATCH (o)-[]-(:Allegation)-[]-(c:Complaint)

  WITH
    uid,
    u,
    a,
    count(DISTINCT o) AS officers,
    count(DISTINCT c) AS complaints

  CALL (u) {
    OPTIONAL MATCH (u)-[r:UPDATED_BY]->(s:Source)
            RETURN s, r
            ORDER BY r.timestamp DESC
            LIMIT 1
  }
  RETURN uid, {
    name: u.name,
    agency_name: a.name,
    officers: officers,
    complaints: complaints,
    source: s.name,
    last_updated: r.timestamp
  } as result
"""

AGENCY_RESULT_QUERY = """
UNWIND $uids AS uid
  MATCH (a:Agency {uid: uid})
  OPTIONAL MATCH (a)-[]-(u:Unit)
  OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(o:Officer)
  OPTIONAL MATCH (o)-[]-(:Allegation)-[]-(c:Complaint)

  WITH
    a,
    uid,
    count(DISTINCT u) AS units,
    count(DISTINCT o) AS officers,
    count(DISTINCT c) AS complaints

  CALL (a) {
    OPTIONAL MATCH (a)-[r:UPDATED_BY]->(s:Source)
    RETURN s, r
    ORDER BY r.timestamp DESC
    LIMIT 1
  }

  WITH uid, units, officers, complaints, s, r

  RETURN uid, {
    units: units,
    officers: officers,
    complaints: complaints,
    source: s.name,
    last_updated: r.timestamp
  } AS result
"""


class Searchresult(BaseModel):
    uid: str
    title: str
    subtitle: Optional[str] = None
    details: Optional[List[str]] = None
    content_type: str
    source: str
    last_updated: datetime
    href: str

    @field_validator("last_updated", mode="before")
    @classmethod
    def coerce_neo4j_datetime(cls, v):
        if v is None:
            return None
        if hasattr(v, "to_native"):
            return v.to_native()
        return v


def fetch_details(uids: List[str], type: str) -> Dict[str, dict]:
    """
    Fetch details for a list of search result uids.
    uids:   List of UIDs to fetch details for.
    type:   Type of the nodes ("Officer", "Agency", "Unit").
    returns:   A dictionary mapping uid to details dictionary.
    """
    if not uids:
        return {}

    if type == "Officer":
        query = OFFICER_RESULT_QUERY
    elif type == "Agency":
        query = AGENCY_RESULT_QUERY
    elif type == "Unit":
        query = UNIT_RESULT_QUERY
    else:
        return {}

    params = {'uids': uids}
    results, _ = db.cypher_query(query, params)
    details = {}
    for uid, row in results:
        details[uid] = row or {}
    return details


def build_agency_result(node, details_row: dict) -> Searchresult:
    a = Agency.inflate(node)
    uid = a.uid
    details = []

    subtitle = "{} Agency in {}, {}".format(
        a.jurisdiction_enum.describe() if a.jurisdiction_enum else "",
        a.hq_city if a.hq_city else "Unknown City",
        a.hq_state if a.hq_state else "Unknown State"
    )

    details.append("{} Unit(s), {} Officer(s), {} Complaint(s)".format(
        details_row.get("units", 0),
        details_row.get("officers", 0),
        details_row.get("complaints", 0)
    ))
    return Searchresult(
        uid=uid,
        title=a.name,
        subtitle=subtitle,
        details=details,
        content_type="Agency",
        source=details_row.get("source", "Unknown Source"),
        last_updated=details_row.get("last_updated", None),
        href=f"/api/v1/agencies/{uid}"
    )


def build_unit_result(node, details_row: dict) -> Searchresult:
    u = Unit.inflate(node)

    uid = u.uid
    details = []

    subtitle = "Established by {}".format(
        details_row.get("agency_name", "Unknown Agency")
    )
    details.append("{} Officer(s), {} Complaint(s)".format(
        details_row.get("officers", 0),
        details_row.get("complaints", 0)
    ))

    return Searchresult(
        uid=uid,
        title=u.name,
        subtitle=subtitle,
        details=details,
        content_type="Unit",
        source=details_row.get("source", "Unknown Source"),
        last_updated=details_row.get("last_updated", None),
        href=f"/api/v1/units/{uid}"
    )


def build_officer_result(node, details_row: dict) -> Searchresult:
    o = Officer.inflate(node)
    uid = o.uid
    details = []

    subtitle = "{ethnicity} {gender}, {rank} at the {agency}".format(
        ethnicity=(
            o.ethnicity_enum.describe()
            if o.ethnicity_enum else "Unknown Ethnicity"
        ),
        gender=(
            o.gender_enum.describe()
            if o.gender_enum else "Unknown Gender"
        ),
        rank=(
            details_row.get("rank", "Officer")
        ),
        agency=(
            details_row.get("agency_name", "Unknown Agency")
        )
    )

    details.append("{} Complaints, {} Allegations, {} Substantiated".format(
        details_row.get("complaints", 0),
        details_row.get("allegations", 0),
        details_row.get("substantiated", 0)
    ))
    return Searchresult(
        uid=uid,
        title=o.full_name,
        subtitle=subtitle,
        details=details,
        content_type="Officer",
        source=details_row.get("source", "Unknown Source"),
        last_updated=details_row.get("last_updated", None),
        href=f"/api/v1/officers/{uid}"
    )


def group_nodes_by_type(results) -> Dict[str, List]:
    """
    results:    Output rows from cypher_query, where each row is [node, score]
    returns:    A dictionary with keys "Officer", "Agency", "Unit", etc.
                and values as lists of nodes of that type.
    """
    buckets: dict[str, list] = defaultdict(list)
    seen: dict[str, set] = defaultdict(set)

    for row in results:
        node = row[0]
        labels = set(node.labels or [])

        if "Officer" in labels:
            ntype = "Officer"
        elif "Agency" in labels:
            ntype = "Agency"
        elif "Unit" in labels:
            ntype = "Unit"
        else:
            continue

        uid = node.get("uid") if hasattr(node, "get") else None
        if uid and uid in seen[ntype]:
            continue
        if uid:
            seen[ntype].add(uid)
            buckets[ntype].append(node)
    return buckets


# Text Search Endpoint
@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def text_search():
    """Text Search
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)
    query = args.get("query", None, type=str)
    updated_query_fuzzy = query + "*"
    params = {
        "query": updated_query_fuzzy,
        "page": q_page,
        "per_page": q_per_page
    }

    if not query:
        abort(400, description="Query parameter is required")

    # Count Matches
    cypher_count = """
    CALL () {
        CALL db.index.fulltext.queryNodes('officerNames',$query)  YIELD node
        RETURN count(*) AS cnt
        UNION ALL
        CALL db.index.fulltext.queryNodes('agencyNames',$query)   YIELD node
        RETURN count(*) AS cnt
        UNION ALL
        CALL db.index.fulltext.queryNodes('unitNames',$query)     YIELD node
        RETURN count(*) AS cnt
    }
    RETURN sum(cnt) AS totalMatches
    """
    count_results, _ = db.cypher_query(cypher_count, params)
    total_results = count_results[0][0] if count_results else 0

    if total_results == 0:
        return jsonify({"message": "No results found matching the query"}), 200

    if total_results < (q_page - 1) * q_per_page:
        return jsonify({"message": "Page number exceeds total results"}), 400

    # Query Everything
    cypher = """
    CALL () {
        CALL db.index.fulltext.queryNodes('officerNames', $query)
            YIELD node, score
            RETURN node, score
        UNION ALL
        CALL db.index.fulltext.queryNodes('agencyNames', $query)
            YIELD node, score
            RETURN node, score
        UNION ALL
        CALL db.index.fulltext.queryNodes('unitNames', $query)
            YIELD node, score
            RETURN node, score
    }
    RETURN node, score
    ORDER BY score DESC
    SKIP $per_page * ($page - 1)
    LIMIT $per_page
    """

    results, meta = db.cypher_query(cypher, params)
    if not results:
        return jsonify({"message": "No results found matching the query"}), 200
    buckets = group_nodes_by_type(results)
    officer_uids = [n.get("uid") for n in buckets.get(
        "Officer", []) if n.get("uid")]
    agency_uids = [n.get("uid") for n in buckets.get(
        "Agency", []) if n.get("uid")]
    unit_uids = [n.get("uid") for n in buckets.get(
        "Unit", []) if n.get("uid")]

    officer_details = fetch_details(officer_uids, "Officer")
    agency_details = fetch_details(agency_uids, "Agency")
    unit_details = fetch_details(unit_uids, "Unit")

    page = []
    for node, score in results:
        labels = set(node.labels or [])

        if "Officer" in labels:
            uid = Officer.inflate(node).uid
            row = officer_details.get(uid, {})
            item = build_officer_result(node, row)

        elif "Agency" in labels:
            uid = Agency.inflate(node).uid
            row = agency_details.get(uid, {})
            item = build_agency_result(node, row)

        elif "Unit" in labels:
            uid = Unit.inflate(node).uid
            row = unit_details.get(uid, {})
            item = build_unit_result(node, row)

        else:
            continue

        page.append(item.model_dump())

    response = add_pagination_wrapper(
        page_data=page, total=total_results,
        page_number=q_page, per_page=q_per_page)

    return jsonify(response), 200
