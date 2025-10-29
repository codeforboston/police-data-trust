import logging
from backend.auth.jwt import min_role_required
from backend.schemas import (
    add_pagination_wrapper, ordered_jsonify)
from backend.database.models.user import UserRole
from backend.database.models.agency import Unit, State
from backend.routes.search import create_unit_result
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended.view_decorators import jwt_required
from neomodel import db


bp = Blueprint("unit_routes", __name__, url_prefix="/api/v1/units")


@bp.route("/", methods=["GET"])
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
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    params = ["name", "city", "state"]
    params_used = set(params).intersection(args.keys())
    params.extend(["page", "per_page", "searchResult"])

    # includes unrecognized parameters
    if bool(set(args).difference(params)):
        logging.warning(set(args).difference(params))
        abort(400)

    skip = (q_page - 1) * q_per_page

    # base query
    cypher = "MATCH (u:Unit) "
    filters = []
    cypher_params = {}

    # filtering
    for p in params_used:
        input_value = args.get(p, type=str)
        if p == "state" and input_value not in State.choices():
            abort(400)
        filters.append(f"toLower(u.{p}) CONTAINS toLower(${p})")
        cypher_params[p] = input_value

    if filters:
        cypher += "WHERE " + " AND ".join(filters) + " "

    # count total matches
    count_query = cypher + "RETURN count(u) AS total"
    row_count = db.cypher_query(count_query, cypher_params)[0][0][0]

    if row_count == 0:
        return jsonify({"message": "No results found matching the query"}), 200
    if row_count < skip:
        return jsonify({"message": "Page number exceeds total results"}), 400

    # get paginated results
    cypher += "RETURN u SKIP $skip LIMIT $limit"
    cypher_params.update({"skip": skip, "limit": q_per_page})
    results, _ = db.cypher_query(cypher, cypher_params)

    # optional searchResult format
    if args.get("searchResult", "").lower() == "true":
        units = [create_unit_result(row[0]) for row in results]
        page = [item.model_dump() for item in units if item]
        return_func = jsonify
    else:
        units = [Unit.inflate(row[0]) for row in results]
        page = [item.to_dict() for item in units]
        return_func = ordered_jsonify

    response = add_pagination_wrapper(
        page_data=page,
        total=row_count,
        page_number=q_page,
        per_page=q_per_page
    )

    return return_func(response), 200
