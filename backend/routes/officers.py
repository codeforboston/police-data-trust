import logging
from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.schemas import (validate_request, ordered_jsonify,
                             add_pagination_wrapper)
from backend.database.models.user import UserRole, User
from backend.database.models.officer import Officer
from backend.routes.search import create_officer_result
from .tmp.pydantic.officers import CreateOfficer, UpdateOfficer
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from backend.dto.officer import OfficerSearchParams
from neomodel import db


bp = Blueprint("officer_routes", __name__, url_prefix="/api/v1/officers")


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

    # try:
    officer = Officer.from_dict(body.dict())
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
        all_officers = [create_officer_result(o) for o in results]
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
    # Coalesce employment stints per agency + unit
    cy = """
    MATCH (o:Officer {uid: $uid})-[:HELD_BY]-(e:Employment)-[:IN_UNIT]-(u:Unit)-[:ESTABLISHED_BY]-(a:Agency)
    WITH a, u, e
    ORDER BY coalesce(e.latest_date, e.earliest_date) DESC
    WITH
      a,
      u,
      head(collect(e)) AS rep,          // “representative” stint (most recent by our ORDER BY)
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

    try:
        results, _meta = db.cypher_query(cy, {'uid': officer_uid})
    except Exception as e:
        abort(400, description=str(e))
    employment_history = [row[0] for row in results]
    return jsonify({
        "officer_uid": officer_uid,
        "employment_history": employment_history,
        "total_records": len(employment_history)
    })


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
