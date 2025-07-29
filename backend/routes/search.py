import logging
from typing import Optional, List

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
    nodes = []
    for node, score in results:
        if "Officer" in node.labels:
            officer = Officer.inflate(node)
            nodes.append(officer)
        elif "Agency" in node.labels:
            agency = Agency.inflate(node)
            nodes.append(agency)
        elif "Unit" in node.labels:
            unit = Unit.inflate(node)
            nodes.append(unit)

    # Paginate results
    paginated_results = paginate_results(nodes, q_page, q_per_page)

    return ordered_jsonify(paginated_results), 200
