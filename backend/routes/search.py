import logging
from typing import Optional, List
from datetime import datetime

from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.schemas import validate_request, ordered_jsonify, paginate_results
from backend.database.models.user import UserRole, User
from backend.database.models.officer import Officer
from backend.database.models.agency import Agency, Unit
from .tmp.pydantic.officers import CreateOfficer, UpdateOfficer
from flask import Blueprint, abort, request
from flask_jwt_extended import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from flask import jsonify
from pydantic import BaseModel
from neomodel import db


bp = Blueprint("search_routes", __name__, url_prefix="/api/v1/search")

class Searchresult(BaseModel):
    uid: str
    title: str
    subtitle: Optional[str] = None
    details: Optional[List[str]] = None
    content_type: str
    source: str
    last_updated: datetime
    href: str


def create_officer_result(node) -> Searchresult:
    o = Officer.inflate(node)

    uid = o.uid

    # Subtitle Example: "Asian Man, Sergeant at Agency X"
    u = o.current_unit
    a = u.agency.single() if u else None
    u_rel = u.officers.relationship(o) if u else None

    s = o.primary_source()
    s_rel = o.citations.relationship(s)



    sub_title = "{ethnicity} {gender}, {rank} at {unit}, {agency}".format(
        ethnicity=o.ethnicity_enum.describe() if o.ethnicity_enum else "Unknown Ethnicity",
        gender=o.gender_enum.describe() if o.gender_enum else "Unknown Gender",
        rank=u_rel.highest_rank if u_rel else "Officer",
        unit=u.name if u else "Unknown Unit",
        agency=a.name if a else "Unknown Agency"
    )

    return Searchresult(
        uid=uid,
        title=o.full_name,
        subtitle=sub_title,
        content_type="Officer",
        source=s.name if s else "Unknown Source",
        last_updated=s_rel.date,
        href=f"/api/v1/officers/{uid}"
    )


def create_search_result(node) -> Searchresult:
    if "Officer" in node.labels:
        return create_officer_result(node)
    else:
        return None



# Get all officers
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
    location = args.get("location", None, type=str)
    source = args.get("source", None, type=str)
    query = args.get("query", None, type=str)
    params = {"query": query}

    if not query:
        abort(400, description="Query parameter is required")

    # Query Everything
    cypher = """
    CALL {
        CALL db.index.fulltext.queryNodes('officerNames', $query) YIELD node, score
            RETURN node, score
        UNION ALL
        CALL db.index.fulltext.queryNodes('agencyNames', $query) YIELD node, score
            RETURN node, score
        UNION ALL
        CALL db.index.fulltext.queryNodes('unitNames', $query) YIELD node, score
            RETURN node, score
    }
    RETURN node, score
    ORDER BY score DESC
    """

    results, meta = db.cypher_query(cypher, params)
    if not results:
        return jsonify({"message": "No results found matching the query"}), 204

    res = []
    for result in results[:10]:
        item = create_search_result(result[0])
        res.append(item.model_dump()) if item else None
    return jsonify(res), 200
