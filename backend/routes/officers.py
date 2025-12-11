import logging
from typing import Optional, List

from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.schemas import (validate_request, ordered_jsonify,
                             add_pagination_wrapper)
from backend.database.models.user import UserRole, User
from backend.database.models.officer import Officer, StateID
from backend.database.models.source import Source
from backend.routes.search import create_officer_result
from .tmp.pydantic.officers import CreateOfficer, UpdateOfficer, CreateStateId
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from pydantic import BaseModel
from neomodel import db


bp = Blueprint("officer_routes", __name__, url_prefix="/api/v1/officers")


class SearchOfficerSchema(BaseModel):
    name: Optional[str] = None
    agency: Optional[str] = None
    badgeNumber: Optional[str] = None
    location: Optional[str] = None
    page: Optional[int] = 1
    perPage: Optional[int] = 20

    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "officerName": "John Doe",
                "location" : "New York",
                "badgeNumber" : 1234,
                "page": 1,
                "perPage": 20,
            }
        }


class AddEmploymentSchema(BaseModel):
    agency_id: int
    badge_number: str
    officer_id: Optional[int]
    highest_rank: Optional[str]
    earliest_employment: Optional[str]
    latest_employment: Optional[str]
    unit: Optional[str]
    currently_employed: bool = True


class AddEmploymentListSchema(BaseModel):
    agencies: List[AddEmploymentSchema]


def cleanup_officer_create(new_sids: List[StateID]):
    """Cleans up newly created StateIDs if officer creation fails.
    """
    for sid in new_sids:
        try:
            sid.delete()
        except Exception as e:
            logging.error(
                f"Failed to delete StateID {sid.uid} during cleanup: {str(e)}"
            )

# Create an officer profile
@bp.route("/", methods=["POST"])
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

    # Ensure user is connected to the source
    source = Source.nodes.get_or_none(uid=body.source_uid)
    if source is None:
        abort(400, description="Source not found")
    if source.members.is_connected(current_user):
        rel = source.members.relationship(current_user)
        if not rel.is_active and rel.may_publish():
            abort(403, description="User is not permitted to publish for this source.")
    else:
        abort(403, description="User is not permitted to publish for this source.")
    
    # Ensure that there's at least 1 valid StateId
    existing_sids = []
    new_sids = []
    created_sids = []
    if not body.state_ids or len(body.state_ids) == 0:
        abort(400, description="At least one StateId is required to create an officer.")
    else:
        for state_id in body.state_ids:
            sid = StateID.nodes.get_or_none(
                state=state_id.state,
                id_name=state_id.id_name,
                value=state_id.value
            )
            if sid:
                existing_sids.append(sid)
            else:
                # Create new StateID
                try:
                    sid = StateID.from_dict(state_id.model_dump())
                except Exception:
                    cleanup_officer_create(new_sids)
                    abort(422, description="Failed to create StateID")
                new_sids.append(sid)
    
    # Identify officer by StateIds
    found_officers = []
    for sid in existing_sids:
        o = sid.officer.single()
        found_officers.append(o)

    if len(found_officers) > 1:
        cleanup_officer_create(new_sids)
        abort(400, description="Multiple officers found with the provided StateIds. Unable to merge.")
    if len(found_officers) == 1:
        officer = found_officers[0]
        for sid in new_sids:
            sid.officer.connect(officer)
        logger.info(f"Officer {officer.uid} updated with new StateIds by User {current_user.uid}")
        diff = dict()
        officer.add_citation(source, current_user)
        track_to_mp(
            request,
            "update_officer_stateids",
            {
                "officer_id": officer.uid,
                "new_stateids": [sid.uid for sid in new_sids]
            },
        )
        # TODO: Add message about using PATCH endpoint to update other info
        return officer.to_json()

    # Create a new officer profile
    o_data = {k: v for k, v in {
        "first_name": body.first_name,
        "middle_name": body.middle_name,
        "last_name": body.last_name,
        "suffix": body.suffix,
        "ethnicity": body.ethnicity,
        "gender": body.gender,
        "date_of_birth": body.date_of_birth
    }.items() if v is not None}
    try:
        officer = Officer.from_dict(o_data)
    except Exception as e:
        cleanup_officer_create(new_sids)
        abort(400, description=str(e))

    # Link StateIds to the officer
    for sid in new_sids:
        # See if this officer is already linked to a StateID with the same State and ID Name
        dupe = officer.lookup_state_id(sid.state, sid.id_name)
        if dupe:
            cleanup_officer_create(new_sids)
            officer.delete()
            abort(400, description=f"Officer already has a StateID for {sid.state} - {sid.id_name}")

        try:
            sid.officer.connect(officer)
        except Exception as e:
            cleanup_officer_create(new_sids)
            officer.delete()
            abort(400, description=str(e))
    # TODO: Add diff info
    officer.add_citation(source, current_user)

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
    return o.to_json()


# Get all officers
@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_all_officers():
    """Get all officers.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """

    args = request.args

    # Pagination
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)
    skip = (q_page - 1) * q_per_page
    limit = q_per_page

    # Build full name
    officer_name_parts = [args.get(k, "").strip() for k in
                          ["firstName", "middleName", "lastName", "suffix"]]
    officer_name = " AND ".join([p for p in officer_name_parts if p]) or None

    officer_rank = " ".join(args.getlist("rank"))
    unit = args.getlist("unit")
    agency = args.getlist("agency")
    active_after = args.get("active_after")
    active_before = args.get("active_before")
    badge_number = args.getlist("badge_number")
    ethnicity = args.getlist("ethnicity")

    # Build MATCH clauses
    match_clauses = []
    if officer_name:
        match_clauses.append(f"""
            CALL db.index.fulltext.queryNodes('officerNames',
                             '{officer_name}') YIELD node AS o
        """)
    elif officer_rank:
        match_clauses.append(f"""
            CALL db.index.fulltext.queryRelationships('officerRanks',
                             '{officer_rank}') YIELD relationship AS m
        """)

    match_clauses.append("MATCH (o:Officer)")

    if unit or active_after or active_before or badge_number or agency:
        match_clauses.append("MATCH (o)-[m:MEMBER_OF_UNIT]-(u:Unit)")

    if agency:
        match_clauses.append("MATCH (u)-[:ESTABLISHED_BY]->(a:Agency)")

    # Build WHERE clauses and params
    where_clauses = ["TRUE"]
    params = {}

    if active_after:
        where_clauses.append("m.latest_date > $active_after")
        params["active_after"] = active_after

    if active_before:
        where_clauses.append("m.earliest_date < $active_before")
        params["active_before"] = active_before

    if agency:
        where_clauses.append("a.name IN $agency")
        params["agency"] = agency

    if badge_number:
        where_clauses.append("m.badge_number IN $badge_number")
        params["badge_number"] = badge_number

    if ethnicity:
        where_clauses.append("o.ethnicity IN $ethnicity")
        params["ethnicity"] = ethnicity

    if unit:
        where_clauses.append("u.name IN $unit")
        params["unit"] = unit

    # Combine query
    match_str = "\n".join(match_clauses)
    where_str = "\nAND ".join(where_clauses)
    cypher_query = f"""
    {match_str}
    WHERE {where_str}
    RETURN o SKIP {skip} LIMIT {limit}
    """

    logging.warning("Cypher query:\n%s", cypher_query)
    logging.warning("Params: %s", params)

    # Count total results
    count_query = f"{match_str}\nWHERE {where_str}\nRETURN count(*) as c"
    count_results, _ = db.cypher_query(count_query, params)
    row_count = count_results[0][0] if count_results else 0
    logging.warning("Total results found: %s", row_count)

    if row_count == 0:
        return jsonify({"message": "No results found matching the query"}), 200
    if row_count < skip:
        return jsonify({"message": "Page number exceeds total results"}), 400

    # Run query
    results, _ = db.cypher_query(cypher_query, params)

    # Check mode — full node or SearchResult
    if args.get("searchResult", "").lower() == 'true':  # default is full node
        all_officers = [create_officer_result(o[0]) for o in results]
        page = [item.model_dump() for item in all_officers if item]
        return_func = jsonify
    else:
        all_officers = [Officer.inflate(row[0]) for row in results]
        page = [item.to_dict() for item in all_officers]
        return_func = ordered_jsonify

    # Add pagination wrapper
    response = add_pagination_wrapper(
        page_data=page, total=row_count,
        page_number=q_page, per_page=q_per_page
    )

    logging.warning("API response: %s", response)
    # return ordered_jsonify(response), 200
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
        o = Officer.from_dict(body.dict(), officer_uid)
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


# # Update an officer's employment history
# @bp.route("/<int:officer_id>/employment", methods=["PUT"])
# @jwt_required()
# @min_role_required(UserRole.CONTRIBUTOR)
# @validate(json=AddEmploymentListSchema)
# def update_employment(officer_id: int):
#     """Update an officer's employment history.
#     Must be a contributor to update an officer's employment history.
#     May include multiple records in the request body.
#     """
#     o = Officer.nodes.get_or_none(uid=officer_id)
#     if o is None:
#         abort(404, description="Officer not found")

#     records = request.context.json.agencies

#     created = []
#     failed = []
#     for record in records:
#         try:
#             agency = Agency.nodes.get_or_none(uid=record.agency_id)
#             if agency is None:
#                 failed.append({
#                     "agency_id": record.agency_id,
#                     "reason": "Agency not found"
#                 })
#             else:
#                 employments = db.session.query(Employment).filter(
#                     and_(
#                         and_(
#                             Employment.officer_id == officer_id,
#                             Employment.agency_id == record.agency_id
#                         ),
#                         Employment.badge_number == record.badge_number
#                     )
#                 )
#                 if employments is not None:
#                     # If the officer already has a records for this agency,
#                     # we need to update the earliest and
#                     # latest employment dates
#                     employment = employment_to_orm(record)
#                     employment.officer_id = officer_id
#                     employment = merge_employment_records(
#                         employments.all() + [employment],
#                         currently_employed=record.currently_employed
#                     )

#                     # Delete the old records and replace them with the new one
#                     employments.delete()
#                     created.append(employment.create())
#                 else:
#                     record.officer_id = officer_id
#                     employment = employment_to_orm(record)
#                     created.append(employment.create())
#                 # Commit before iterating to the next record
#                 db.session.commit()
#         except Exception as e:
#             failed.append({
#                 "agency_id": record.agency_id,
#                 "reason": str(e)
#             })

#     track_to_mp(
#         request,
#         "update_employment",
#         {
#             "officer_id": officer.id,
#             "agencies_added": len(created),
#             "agencies_failed": len(failed)
#         },
#     )
#     try:
#         return {
#             "created": [
#                 employment_orm_to_json(item) for item in created],
#             "failed": failed,
#             "totalCreated": len(created),
#             "totalFailed": len(failed),
#         }
#     except Exception as e:
#         abort(400, description=str(e))


# # Retrieve an officer's employment history
# @bp.route("/<int:officer_id>/employment", methods=["GET"])
# @jwt_required()
# @min_role_required(UserRole.PUBLIC)
# @validate()
# def get_employment(officer_id: int):
#     """Retrieve an officer's employment history.
#     """
#     args = request.args
#     q_page = args.get("page", 1, type=int)
#     q_per_page = args.get("per_page", 20, type=int)

#     officer = db.session.query(Officer).get(officer_id)
#     if officer is None:
#         abort(404, description="Officer not found")

#     try:
#         employments = db.session.query(Employment).filter(
#             Employment.officer_id == officer_id)

#         pagination = employments.paginate(
#             page=q_page, per_page=q_per_page, max_per_page=100
#         )

#         return {
#             "results": [
#                 employment_orm_to_json(
#                     employment) for employment in pagination.items],
#             "page": pagination.page,
#             "totalPages": pagination.pages,
#             "totalResults": pagination.total,
#         }
#     except Exception as e:
#         abort(400, description=str(e))
