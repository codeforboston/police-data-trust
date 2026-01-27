import logging
from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.schemas import (validate_request, ordered_jsonify,
                             add_pagination_wrapper)
from backend.database.models.user import UserRole, User
from backend.database.models.officer import Officer
from backend.routes.search import fetch_details, build_officer_result
from .tmp.pydantic.officers import CreateOfficer, UpdateOfficer
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from backend.dto.officer import OfficerSearchParams, GetOfficerParams
from neomodel import db


bp = Blueprint("officer_routes", __name__, url_prefix="/api/v1/officers")

EMPLOYMENT_CYPHER = """
    MATCH (o:Officer {uid: $uid})-[:HELD_BY]-(e:Employment)-[:IN_UNIT]
    -(u:Unit)-[:ESTABLISHED_BY]-(a:Agency)
    WITH a, u, e
    ORDER BY coalesce(e.latest_date, e.earliest_date) DESC
    WITH
      a,
      u,
      head(collect(e)) AS rep,
      min(e.earliest_date) AS earliest_date,
      max(e.latest_date)   AS latest_date
    RETURN {
      agency_uid:   a.uid,
      agency_name:  a.name,
      unit_uid:     u.uid,
      unit_name:    u.name,
      badge_number: rep.badge_number,
      highest_rank: rep.highest_rank,
      salary:       rep.salary,
      earliest_date: earliest_date,
      latest_date:   latest_date
    } AS item
    LIMIT 20;
    """

ALLEGATION_CYPHER = """
MATCH (o:Officer {uid: $uid})-[:ACCUSED_OF]->(a:Allegation)
MATCH (a)-[:ALLEGED]->(c:Complaint)
WITH
  CASE
    WHEN a.type IS NULL OR trim(a.type) = "" THEN "Unknown"
    ELSE a.type
  END AS type,
  count(*) AS occurrences,
  sum(CASE WHEN toLower(
    trim(coalesce(a.finding,""))) = "substantiated" THEN 1 ELSE 0 END)
    AS substantiated_count,
  min(c.incident_date) AS earliest_incident_date,
  max(c.incident_date) AS latest_incident_date
ORDER BY occurrences DESC, type ASC
RETURN
  type,
  occurrences,
  substantiated_count,
  earliest_incident_date,
  latest_incident_date
LIMIT 10;
"""


# Create an officer profile
@bp.route("", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreateOfficer)
def create_officer():
    """Create an officer profile.
    """
    logger = logging.getLogger("create_officer")
    body: CreateOfficer = request.validated_body
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])

    # try:
    officer = Officer.from_dict(body.model_dump())
    # except Exception as e:
    #     abort(400, description=str(e))

    logger.info(f"Officer {officer.uid} created by User {current_user.uid}")
    track_to_mp(
        request,
        "create_officer",
        {
            "officer_id": officer.uid
        },
    )
    return officer.to_json()


# Get an officer profile
@bp.route("/<officer_uid>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_officer(officer_uid: int):
    """Get an officer profile.
    """
    o = Officer.nodes.get_or_none(uid=officer_uid)
    if o is None:
        abort(404, description="Officer not found")
    raw = {
        **request.args,  # copies simple values
        "include": request.args.getlist("include"),
    }
    try:
        params = GetOfficerParams(**raw)
    except Exception as e:
        logging.warning(f"Invalid query params: {e}")
        abort(400, description=str(e))

    response = o.to_dict()

    employment_history = None

    if params.include:
        if "employment" in params.include:
            # Load employment history
            try:
                results, _meta = db.cypher_query(
                    EMPLOYMENT_CYPHER, {'uid': officer_uid})
            except Exception as e:
                abort(500, description=str(e))
            employment_history = [row[0] for row in results]
            response.update({"employment_history": employment_history})
        if "allegations" in params.include:
            # Load allegation summary
            try:
                results, _meta = db.cypher_query(
                    ALLEGATION_CYPHER, {'uid': officer_uid})
            except Exception as e:
                abort(500, description=str(e))
            allegation_summary = []
            for row in results:
                allegation_summary.append({
                    "type": row[0],
                    "count": row[1],
                    "substantiated_count": row[2],
                    "earliest_incident_date": row[3],
                    "latest_incident_date": row[4],
                })
            response.update({"allegation_summary": allegation_summary})

    return ordered_jsonify(response)


# Get all officers
@bp.route("", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_all_officers():
    """Get all officers.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    raw = {
        **request.args,  # copies simple values
        "unit": request.args.getlist("unit"),
        "agency": request.args.getlist("agency"),
        "rank": request.args.getlist("rank"),
        "badge_number": request.args.getlist("badge_number"),
        "ethnicity": request.args.getlist("ethnicity"),
    }
    try:
        params = OfficerSearchParams(**raw)
    except Exception as e:
        logging.warning(f"Invalid query params: {e}")
        abort(400, description=str(e))

    row_count = Officer.search(
        name=params.officer_name,
        rank=params.officer_rank,
        unit=params.unit,
        agency=params.agency,
        badge_number=params.badge_number,
        ethnicity=params.ethnicity,
        active_after=params.active_after,
        active_before=params.active_before,
        count=True,
    )
    logging.warning("Total results found: %s", row_count)

    if row_count == 0:
        return jsonify({"message": "No results found matching the query"}), 200
    if row_count <= params.skip:
        return jsonify({"message": "Page number exceeds total results"}), 400

    # Run query
    results = Officer.search(
        name=params.officer_name,
        rank=params.officer_rank,
        unit=params.unit,
        agency=params.agency,
        badge_number=params.badge_number,
        ethnicity=params.ethnicity,
        active_after=params.active_after,
        active_before=params.active_before,
        skip=params.skip,
        limit=params.limit,
        inflate=not params.searchResult
    )

    # Check mode — full node or SearchResult
    if params.searchResult:  # default is full node
        details = fetch_details(
            [row.get("uid") for row in results], "Officer")
        all_officers = [build_officer_result(
            o, details.get(o.get("uid"), {})) for o in results]
        page = [item.model_dump() for item in all_officers if item]
        return_func = jsonify
    else:
        page = [row.to_dict() for row in results]
        return_func = ordered_jsonify
    # logging.warning('response is --------------------------------\n%s', page)

    # Add pagination wrapper
    response = add_pagination_wrapper(
        page_data=page,
        total=row_count,
        page_number=params.page,
        per_page=params.per_page
    )

    return return_func(response), 200


# Update an officer profile
@bp.route("/<officer_uid>", methods=["PUT"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(UpdateOfficer)
def update_officer(officer_uid: str):
    """Update an officer profile.
    """
    body: UpdateOfficer = request.validated_body
    o = Officer.nodes.get_or_none(uid=officer_uid)
    if o is None:
        abort(404, description="Officer not found")

    try:
        o = Officer.from_dict(body.model_dump(), officer_uid)
        o.refresh()
    except Exception as e:
        abort(400, description=str(e))

    track_to_mp(
        request,
        "update_officer",
        {
            "officer_id": o.uid
        },
    )
    return o.to_json()


# Delete an officer profile
@bp.route("/<officer_uid>", methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.ADMIN)
def delete_officer(officer_uid: str):
    """Delete an officer profile.
    Must be an admin to delete an officer.
    """
    o = Officer.nodes.get_or_none(uid=officer_uid)
    if o is None:
        abort(404, description="Officer not found")
    try:
        uid = o.uid
        o.delete()
        track_to_mp(
            request,
            "delete_officer",
            {
                "officer_id": uid
            },
        )
        return {"message": "Officer deleted successfully"}
    except Exception as e:
        abort(400, description=str(e))


# Retrieve an officer's employment history
@bp.route("/<officer_uid>/employment", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_employment(officer_uid: str):
    """Retrieve an officer's employment history.
    """

    o = Officer.nodes.get_or_none(uid=officer_uid)
    if o is None:
        abort(404, description="Officer not found")

    # Get employment history
    try:
        results, _meta = db.cypher_query(
            EMPLOYMENT_CYPHER, {'uid': officer_uid})
    except Exception as e:
        abort(400, description=str(e))
    employment_history = [row[0] for row in results]
    return jsonify({
        "officer_uid": officer_uid,
        "employment_history": employment_history,
        "total_records": len(employment_history)
    })
