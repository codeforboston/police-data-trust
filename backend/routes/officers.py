import logging
from typing import Optional, List

from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.schemas import validate_request, ordered_jsonify, paginate_results
from backend.database.models.user import UserRole, User
from backend.database.models.officer import Officer
from .tmp.pydantic.officers import CreateOfficer, UpdateOfficer
from flask import Blueprint, abort, request
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
                "location": "New York",
                "badgeNumber": 1234,
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


# # Search for an officer or group of officers
# @bp.route("/search", methods=["POST"])
# @jwt_required()
# @min_role_required(UserRole.PUBLIC)
# @validate(json=SearchOfficerSchema)
# def search_officer():
#     """Search Officers"""
#     body: SearchOfficerSchema = request.context.json
#     query = db.session.query('Officer')
#     logger = logging.getLogger("officers")

#     try:
#         if body.name:
#             names = body.officerName.split()
#             if len(names) == 1:
#                 query = Officer.query.filter(
#                     or_(
#                         Officer.first_name.ilike(f"%{body.officerName}%"),
#                         Officer.last_name.ilike(f"%{body.officerName}%")
#                     )
#                 )
#             elif len(names) == 2:
#                 query = Officer.query.filter(
#                     or_(
#                         Officer.first_name.ilike(f"%{names[0]}%"),
#                         Officer.last_name.ilike(f"%{names[1]}%")
#                     )
#                 )
#             else:
#                 query = Officer.query.filter(
#                     or_(
#                         Officer.first_name.ilike(f"%{names[0]}%"),
#                         Officer.middle_name.ilike(f"%{names[1]}%"),
#                         Officer.last_name.ilike(f"%{names[2]}%")
#                     )
#                 )

#         if body.badgeNumber:
#             officer_ids = [
#                 result.officer_id for result in db.session.query(
#                     Employment
#                     ).filter_by(badge_number=body.badgeNumber).all()
#             ]
#             query = Officer.query.filter(Officer.id.in_(officer_ids)).all()

#     except Exception as e:
#         abort(422, description=str(e))

#     results = query.paginate(
#         page=body.page, per_page=body.perPage, max_per_page=100
#     )

#     try:
#         track_to_mp(request, "search_officer", {
#             "officername": body.officerName,
#             "badgeNumber": body.badgeNumber
#         })
#     except MixpanelException as e:
#         logger.error(e)
#     try:
#         return {
#             "results": [
#                 officer_orm_to_json(result) for result in results.items
#             ],
#             "page": results.page,
#             "totalPages": results.pages,
#             "totalResults": results.total,
#         }
#     except Exception as e:
#         abort(500, description=str(e))


# Create an officer profile
@bp.route("/", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreateOfficer)
def create_officer():
    """Create an officer profile."""
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
        {"officer_id": officer.uid},
    )
    return officer.to_json()


# Get an officer profile
@bp.route("/<officer_uid>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_officer(officer_uid: int):
    """Get an officer profile."""
    o = Officer.nodes.get_or_none(element_id=officer_uid)
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
    unit_name: filter by unit name
    ethnicity: filter by officer ethnicity
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)
    unit_name = args.get("unit_name", None)
    ethnicity = args.get("ethnicity", None)  # New parameter
    # Base query
    query = "MATCH (o:Officer)"
    conditions = []

    # Add unit filter if provided
    if unit_name:
        query += " MATCH (o)-[]-(u:Unit)"
        conditions.append("u.name CONTAINS $unit_name")

    # Add ethnicity filter if provided
    if ethnicity:
        conditions.append("o.ethnicity = $ethnicity")
    # Combine conditions
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    # Add pagination
    query += " RETURN o SKIP $skip LIMIT $limit"
    # Calculate pagination values
    skip = (q_page - 1) * q_per_page
    limit = q_per_page
    # Execute query
    all_officers, _ = db.cypher_query(
        query,
        {
            "unit_name": unit_name,
            "ethnicity": ethnicity,  # Include new param
            "skip": skip,
            "limit": limit,
        },
    )
    # Process results
    officers = [Officer.inflate(record[0]) for record in all_officers]
    results = paginate_results(officers, q_page, q_per_page)
    return ordered_jsonify(results), 200


# Update an officer profile
@bp.route("/<officer_uid>", methods=["PUT"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(UpdateOfficer)
def update_officer(officer_uid: str):
    """Update an officer profile."""
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
        {"officer_id": o.uid},
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
            {"officer_id": uid},
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
