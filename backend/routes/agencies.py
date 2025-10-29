import logging

from typing import Optional, List
from backend.auth.jwt import min_role_required
from backend.schemas import (
    validate_request, add_pagination_wrapper, ordered_jsonify, paginate_results,
    NodeConflictException)
from backend.mixpanel.mix import track_to_mp
from backend.database.models.user import UserRole
from backend.database.models.agency import Agency, State, Jurisdiction
from backend.routes.search import create_agency_result
from .tmp.pydantic.agencies import CreateAgency, UpdateAgency
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended.view_decorators import jwt_required
from pydantic import BaseModel
from neomodel import db


bp = Blueprint("agencies_routes", __name__, url_prefix="/api/v1/agencies")


class AddOfficerSchema(BaseModel):
    officer_id: int
    badge_number: str
    agency_id: Optional[int]
    highest_rank: Optional[str]
    earliest_employment: Optional[str]
    latest_employment: Optional[str]
    unit: Optional[str]
    currently_employed: bool = True


class AddOfficerListSchema(BaseModel):
    officers: List[AddOfficerSchema]


# Create agency profile
@bp.route("/", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreateAgency)
def create_agency():
    logger = logging.getLogger("create_agency")
    """Create an agency profile.
    User must be a Contributor to create an agency.
    Must include a name and jurisdiction.
    """
    body: CreateAgency = request.validated_body

    try:
        agency = Agency.from_dict(body.dict())
    except NodeConflictException:
        abort(409, description="Agency already exists")
    except Exception as e:
        logger.error(f"Error, Agency.from_dict: {e}")
        abort(400)

    try:
        Agency.link_location(agency, state=agency.hq_state, city=agency.hq_city)
    except Exception as e:
        logging.error(f"Error linking location {agency.name}: {e}")
        print(f"Error linking location {agency.name}: {e}")
        return

    track_to_mp(
        request,
        "create_agency",
        {
            "name": agency.name
        },
    )
    return agency.to_json()


# Get agency profile
@bp.route("/<agency_id>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_agency(agency_id: str):
    """Get an agency profile.
    """
    # logger = logging.getLogger("get_agency")
    agency = Agency.nodes.get_or_none(uid=agency_id)
    if agency is None:
        abort(404, description="Agency not found")
    try:
        return agency.to_json()
    except Exception as e:
        abort(500, description=str(e))


# Update agency profile
@bp.route("/<agency_uid>", methods=["PUT"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(UpdateAgency)
def update_agency(agency_uid: str):
    """Update an agency profile.
    """
    # logger = logging.getLogger("update_agency")
    body: UpdateAgency = request.validated_body
    agency = Agency.nodes.get_or_none(uid=agency_uid)
    if agency is None:
        abort(404, description="Agency not found")

    try:
        agency = Agency.from_dict(body.dict(), agency_uid)
        agency.refresh()
        track_to_mp(
            request,
            "update_agency",
            {
                "name": agency.name
            }
        )
        return agency.to_json()
    except Exception as e:
        abort(400, description=str(e))


# Delete agency profile
@bp.route("/<agency_id>", methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.ADMIN)
def delete_agency(agency_id: str):
    """Delete an agency profile.
    Must be an admin to delete an agency.
    """
    agency = Agency.nodes.get_or_none(uid=agency_id)
    if agency is None:
        abort(404, description="Agency not found")
    try:
        name = agency.name
        agency.delete()
        track_to_mp(
            request,
            "delete_agency",
            {
                "name": name
            }
        )
        return {"message": "Agency deleted successfully"}
    except Exception as e:
        abort(400, description=str(e))


# Get all agencies
@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_all_agencies():
    """Get all agencies.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    name: filter on agency name
    hq_city: filter on agency city
    hq_state: filter on agency state
    hq_zip: filter on agency zipcode
    jurisdiction: filter on agency jurisdiction
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    params = ["name", "hq_city", "hq_state", "hq_zip", "jurisdiction"]
    params_used = set(params).intersection(args.keys())
    params.extend(["page", "per_page", "searchResult"])

    # includes unrecognized parameters
    if bool(set(args).difference(params)):
        logging.warning(set(args).difference(params))
        abort(400)

    cypher_match = "MATCH (a:Agency)"
    cypher_where_clauses = []
    cypher_params = {}

    # Build WHERE conditions dynamically
    if bool(params_used):
        for p in params_used:
            input_value = args.get(p, None, type=str)
            if p == "hq_state" and input_value not in State.choices():
                abort(400)
            if (p == "jurisdiction" and
                    input_value not in Jurisdiction.choices()):
                abort(400)
            cypher_where_clauses.append(f"a.{p} = ${p}")
            cypher_params[p] = input_value

    cypher_where = ""
    if cypher_where_clauses:
        cypher_where = " WHERE " + " AND ".join(cypher_where_clauses)

    # ----------- Get total count -----------
    cypher_count = f"""
        {cypher_match}
        {cypher_where}
        RETURN count(a) AS total
    """
    count_result, _ = db.cypher_query(cypher_count, cypher_params)
    row_count = count_result[0][0] if count_result else 0

    skip = (q_page - 1) * q_per_page

    if row_count == 0:
        return jsonify({"message": "No results found matching the query"}), 200
    if row_count < skip:
        return jsonify({"message": "Page number exceeds total results"}), 400

    # ----------- Get paginated results -----------
    cypher_data = f"""
        {cypher_match}
        {cypher_where}
        RETURN a
        ORDER BY a.name
        SKIP $skip
        LIMIT $limit
    """
    cypher_params.update({"skip": skip, "limit": q_per_page})
    results, _ = db.cypher_query(cypher_data, cypher_params)

    # Optional: convert to SearchResult format
    if args.get("searchResult", "").lower() == 'true':  # default is full node
        agencies = [create_agency_result(row[0]) for row in results]
        page = [item.model_dump() for item in agencies if item]
        return_func = jsonify
    else:
        agencies = [Agency.inflate(row[0]) for row in results]
        page = [item.to_dict() for item in agencies]
        return_func = ordered_jsonify

    # Add pagination wrapper
    response = add_pagination_wrapper(
        page_data=page,
        total=row_count,
        page_number=q_page,
        per_page=q_per_page
    )

    return return_func(response), 200


# # Add officer employment information
# @bp.route("/<int:agency_id>/officers", methods=["POST"])
# @jwt_required()
# @min_role_required(UserRole.CONTRIBUTOR)
# @validate(json=AddOfficerListSchema)
# def add_officer_to_agency(agency_id: int):
#     """Add any number of officer employment records to an agency.
#     Must be a Contributor to add officers to an agency.
#     """
#     agency = Agency.nodes.get_or_none(uid=agency_id)
#     if agency is None:
#         abort(404, description="Agency not found")

#     records = request.context.json.officers

#     created = []
#     failed = []
#     for record in records:
#         try:
#             officer = db.session.query(Officer).get(
#                 record.officer_id)
#             if officer is None:
#                 failed.append({
#                     "officer_id": record.officer_id,
#                     "reason": "Officer not found"
#                 })
#             else:
#                 employments = db.session.query(Employment).filter(
#                     and_(
#                         and_(
#                             Employment.officer_id == record.officer_id,
#                             Employment.agency_id == agency_id
#                         ),
#                         Employment.badge_number == record.badge_number
#                     )
#                 )
#                 if employments is not None:
#                     # If the officer already has a records for this agency,
#                     # we need to update the earliest and
#                     # latest employment dates
#                     employment = employment_to_orm(record)
#                     employment.agency_id = agency_id
#                     employment = merge_employment_records(
#                         employments.all() + [employment],
#                         currently_employed=record.currently_employed
#                     )

#                     # Delete the old records and replace them with the new one
#                     employments.delete()
#                     created.append(employment.create())
#                 else:
#                     record.agency_id = agency_id
#                     employment = employment_to_orm(record)
#                     created.append(employment.create())
#         except Exception as e:
#             failed.append({
#                 "officer_id": record.officer_id,
#                 "reason": str(e)
#             })
#     try:
#         track_to_mp(
#             request,
#             "add_officers_to_agency",
#             {
#                 "agency_id": agency.id,
#                 "officers_added": len(created),
#                 "officers_failed": len(failed)
#             },
#         )
#         return {
#             "created": [
#                 employment_orm_to_json(item) for item in created],
#             "failed": failed,
#             "totalCreated": len(created),
#             "totalFailed": len(failed),
#         }
#     except Exception as e:
#         abort(400, description=str(e))


# Get agency officers
@bp.route("/<agency_id>/officers", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_agency_officers(agency_id):
    """Get all officers for an agency.
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    try:
        query = f"""
                MATCH (a:Agency)-[]-(u:Unit)-[]-(o:Officer)
                WHERE a.uid='{agency_id}'
                RETURN o
                """
        res, meta = db.cypher_query(query, resolve_objects=True)
        officers = [record[0] for record in res]

        result = paginate_results(officers, q_page, q_per_page)
        return ordered_jsonify(result), 200

    except Exception as e:
        abort(400, description=str(e))
