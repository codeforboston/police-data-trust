import logging
from backend.auth.jwt import min_role_required
from backend.schemas import (
    add_pagination_wrapper, ordered_jsonify)
from backend.database.models.user import UserRole
from backend.database.models.agency import Unit
from backend.routes.search import fetch_details, build_unit_result
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended.view_decorators import jwt_required
from backend.dto.unit import UnitQueryParams, GetUnitParams
from backend.database import db

bp = Blueprint("unit_routes", __name__, url_prefix="/api/v1/units")

SOURCES_CYPHER = """
MATCH (o:Unit {uid: $uid})-[:UPDATED_BY]->(s:Source)
RETURN DISTINCT {
  name: s.name,
  url: s.url,
  contact_email: s.contact_email
} AS source
"""

LOCATION_CYPHER = """
CALL (u) {
    MATCH (u)-[]-(:Agency)-[]-(city:CityNode)
    RETURN city.coordinates AS location
}
"""

MOST_REPORTED_OFFICER_CYPHER = """
CALL (u) {
  MATCH (u)<-[]-(e:Employment)-[]->(o:Officer)
    -[:ACCUSED_OF]->(a:Allegation)-[:ALLEGED]-(c:Complaint)
  WITH
    o,
    e,
    count(DISTINCT c) AS complaint_count,
    count(DISTINCT a) AS allegation_count
  ORDER BY complaint_count DESC
  LIMIT 3
  RETURN collect({
    officer_uid: o.uid,
    name: o.first_name + " " + o.last_name,
    gender: o.gender,
    ethnicity: o.ethnicity,
    rank: e.rank,
    complaint_count: complaint_count,
    allegation_count: allegation_count
  }) AS most_reported_officers
}
"""

TOTAL_OFFICER_CYPHER = """
CALL (u) {
  OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(o:Officer)
  WITH count(DISTINCT o) AS total_officers
  RETURN total_officers
}
"""

COMPLAINT_CYPHER = """
CALL (u) {
  OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(:Officer)
      -[:ACCUSED_OF]->(a:Allegation)-[:ALLEGED]-(c:Complaint)
  WITH count(DISTINCT c) AS total_complaints, count(DISTINCT a) AS total_allegations
  RETURN total_complaints, total_allegations
}
"""

@bp.route("", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_all_units():
    """Get all units.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    name: filter on unit name
    city: filter on unit city
    state: filter on unit state
    """
    try:
        params = UnitQueryParams(**request.args)
    except Exception as e:
        logging.warning(f"Invalid query params: {e}")
        abort(400, description=str(e))

    # Extract filters
    search_term = params.name
    filters = {k: v for k, v in {"city": params.city,
                                 "state": params.state}.items() if v}

    # --- Count total matches ---
    row_count = Unit.search(query=search_term, filters=filters, count=True)

    if row_count == 0:
        return jsonify({"message": "No results found matching the query"}), 200
    if row_count <= params.skip:
        return jsonify({"message": "Page number exceeds total results"}), 400

    # --- Fetch paginated results ---
    results = Unit.search(
        query=search_term,
        filters=filters,
        skip=params.skip,
        limit=params.per_page,
        inflate=not params.searchResult)

    # Optional searchResult format
    if params.searchResult:
        details = fetch_details(
            [row.get("uid") for row in results], "Unit")
        units = [build_unit_result(
            row, details.get(row.get("uid"), {})) for row in results]
        page = [item.model_dump() for item in units if item]
        return_func = jsonify

    else:
        page = [row.to_dict() for row in results]
        return_func = ordered_jsonify

    response = add_pagination_wrapper(
        page_data=page,
        total=row_count,
        page_number=params.page,
        per_page=params.per_page
    )
    # logging.warning(response)
    return return_func(response), 200


@bp.route("/<uid>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_unit(uid: str):
    """Get unit details by UID."""
    unit = Unit.nodes.get_or_none(uid=uid)
    if not unit:
        abort(404, description="Unit not found")
    raw = {
        **request.args,
        "include": request.args.getlist("include"),
    }
    try:
        params = GetUnitParams(**raw)
    except Exception as e:
        logging.warning(f"Invalid query params: {e}")
        abort(400, description=str(e))
    match_clause = "MATCH (u:Unit {uid: $uid})"
    return_clause = "RETURN u"
    subqueries = ""
    if params.include:
        if "reported_officers" in params.include:
            subqueries += MOST_REPORTED_OFFICER_CYPHER
            return_clause += ", most_reported_officers"
        if "total_officers" in params.include:
            subqueries += TOTAL_OFFICER_CYPHER
            return_clause += ", total_officers"
        if "total_complaints" in params.include:
            subqueries += COMPLAINT_CYPHER
            return_clause += ", total_complaints, total_allegations"
        if "location" in params.include:
            subqueries += LOCATION_CYPHER
            return_clause += ", location"
    cy = f"{match_clause} {subqueries} {return_clause}"

    rows, _ = db.cypher_query(cy, {"uid": uid})
    if not rows:
        abort(404, description="Unit not found")
    row = rows[0]
    unit_data = row[0]._properties
    if params.include:
        idx = 1
        if "reported_officers" in params.include:
            unit_data["most_reported_officers"] = row[idx]
            idx += 1
        if "total_officers" in params.include:
            unit_data["total_officers"] = row[idx]
            idx += 1
        if "total_complaints" in params.include:
            unit_data["total_complaints"] = row[idx]
            unit_data["total_allegations"] = row[idx + 1]
            idx += 2
        if "location" in params.include:
            coords = row[idx]
            unit_data["location"] = {"latitude": coords.y, "longitude": coords.x} if coords else None
    return ordered_jsonify(unit_data), 200