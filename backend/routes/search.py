import logging
from typing import Optional, List
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
MATCH (o:Officer {uid: $uid})
OPTIONAL MATCH (o)-[:ACCUSED_OF]->(al:Allegation)-[:ALLEGED]->(co:Complaint)
WITH
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
  MATCH (o)<-[]-(e:Employment)-[]-(u:Unit)-[]-(ag:Agency)
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

RETURN {
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
MATCH (u:Unit {uid: $uid})
OPTIONAL MATCH (u)-[]-(a:Agency)
OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(o:Officer)
OPTIONAL MATCH (o)-[]-(:Allegation)-[]-(c:Complaint)

WITH
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
RETURN {
  name: u.name,
  agency_name: a.name,
  officers: officers,
  complaints: complaints,
  source: s.name,
  last_updated: r.timestamp
} as result
"""

AGENCY_RESULT_QUERY = """
MATCH (a:Agency {uid: $uid})
OPTIONAL MATCH (a)-[]-(u:Unit)
OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(o:Officer)
OPTIONAL MATCH (o)-[]-(:Allegation)-[]-(c:Complaint)

WITH
  a,
  count(DISTINCT u) AS units,
  count(DISTINCT o) AS officers,
  count(DISTINCT c) AS complaints

CALL (a) {
  OPTIONAL MATCH (a)-[r:UPDATED_BY]->(s:Source)
  RETURN s, r
  ORDER BY r.timestamp DESC
  LIMIT 1
}

WITH units, officers, complaints, s, r

RETURN {
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


def create_officer_result(node) -> Searchresult:
    o = Officer.inflate(node)

    uid = o.uid
    details = []

    result, _ = db.cypher_query(OFFICER_RESULT_QUERY, {'uid': uid})
    row = result[0][0] if result else None
    if not row:
        logging.error("No result row for officer uid %s", uid)
        abort(500, description="Error creating officer search result")

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
            row.get("rank", "Officer")
        ),
        agency=(
            row.get("agency_name", "Unknown Agency")
        )
    )
    
    details.append("{} Complaints, {} Allegations, {} Substantiated".format(
        row.get("complaints", 0),
        row.get("allegations", 0),
        row.get("substantiated", 0)
    ))
    return Searchresult(
        uid=uid,
        title=o.full_name,
        subtitle=subtitle,
        details=details,
        content_type="Officer",
        source=row.get("source", "Unknown Source"),
        last_updated=row.get("last_updated", None),
        href=f"/api/v1/officers/{uid}"
    )


def create_agency_result(node) -> Searchresult:
    a = Agency.inflate(node)
    uid = a.uid
    details = []

    result, _ = db.cypher_query(AGENCY_RESULT_QUERY, {'uid': uid})
    row = result[0][0] if result else None
    if not row:
        logging.error("No result row for agency uid %s", uid)
        abort(500, description="Error creating agency search result")
    subtitle = "{} Agency in {}, {}".format(
        a.jurisdiction_enum.describe() if a.jurisdiction_enum else "",
        a.hq_city if a.hq_city else "Unknown City",
        a.hq_state if a.hq_state else "Unknown State"
    )

    details.append("{} Unit(s), {} Officer(s), {} Complaint(s)".format(
        row.get("units", 0),
        row.get("officers", 0),
        row.get("complaints", 0)
    ))
    return Searchresult(
        uid=uid,
        title=a.name,
        subtitle=subtitle,
        details=details,
        content_type="Agency",
        source=row.get("source", "Unknown Source"),
        last_updated=row.get("last_updated", None),
        href=f"/api/v1/agencies/{uid}"
    )


def create_unit_result(node) -> Searchresult:
    u = Unit.inflate(node)

    uid = u.uid
    details = []

    result, _ = db.cypher_query(UNIT_RESULT_QUERY, {'uid': uid})
    row = result[0][0] if result else None
    if not row:
        logging.error("No result row for unit uid %s", uid)
        abort(500, description="Error creating unit search result")
    subtitle = "Established by {}".format(
        row.get("agency_name", "Unknown Agency")
    )
    details.append("{} Officer(s), {} Complaint(s)".format(
        row.get("officers", 0),
        row.get("complaints", 0)
    ))

    return Searchresult(
        uid=uid,
        title=u.name,
        subtitle=subtitle,
        details=details,
        content_type="Unit",
        source=row.get("source", "Unknown Source"),
        last_updated=row.get("last_updated", None),
        href=f"/api/v1/units/{uid}"
    )


def create_search_result(node) -> Searchresult:
    if "Officer" in node.labels:
        return create_officer_result(node)
    elif "Agency" in node.labels:
        return create_agency_result(node)
    elif "Unit" in node.labels:
        return create_unit_result(node)
    return None


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
    params = {
        "query": query,
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

    page = []
    for result in results:
        item = create_search_result(result[0])
        page.append(item.model_dump()) if item else None

    response = add_pagination_wrapper(
        page_data=page, total=total_results,
        page_number=q_page, per_page=q_per_page)

    return jsonify(response), 200
