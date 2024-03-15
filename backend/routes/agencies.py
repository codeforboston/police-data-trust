import logging

from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.database.models.user import UserRole
from flask import Blueprint, abort, request
from flask_jwt_extended.view_decorators import jwt_required
from sqlalchemy.exc import DataError

from ..database import Agency, db
from ..schemas import (
    CreateAgencySchema,
    agency_orm_to_json,
    officer_orm_to_json,
    agency_to_orm,
    validate,
)


bp = Blueprint("agencies_routes", __name__, url_prefix="/api/v1/agencies")


# Create agency profile
@bp.route("/", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate(json=CreateAgencySchema)
def create_agency():
    logger = logging.getLogger("create_agency")
    """Create an agency profile.
    User must be a Contributor to create an agency.
    Must include a name and jurisdiction.
    """

    try:
        agency = agency_to_orm(request.context.json)
    except Exception as e:
        logger.error(f"Error, agency_to_orm: {e}")
        abort(400)

    try:
        created = agency.create()
    except DataError as e:
        logger.error(f"DataError: {e}")
        abort(
            400,
            description="Invalid Agency. Please include a valid jurisdiction."
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        abort(400, description="Error creating agency")

    track_to_mp(
        request,
        "create_agency",
        {
            "name": agency.name
        },
    )
    return agency_orm_to_json(created)


# Get agency profile
@bp.route("/<int:agency_id>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_agency(agency_id: int):
    """Get an agency profile.
    """
    agency = db.session.query(Agency).get(agency_id)
    if agency is None:
        abort(404, description="Agency not found")
    try:
        return agency_orm_to_json(agency)
    except Exception as e:
        abort(500, description=str(e))


# Update agency profile
@bp.route("/<int:agency_id>", methods=["PUT"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate()
def update_agency(agency_id: int):
    """Update an agency profile.
    """
    agency = db.session.query(Agency).get(agency_id)
    if agency is None:
        abort(404, description="Agency not found")

    try:
        agency.update(request.context.json)
        db.session.commit()
        track_to_mp(
            request,
            "update_agency",
            {
                "name": agency.name
            }
        )
        return agency_orm_to_json(agency)
    except Exception as e:
        abort(400, description=str(e))


# Delete agency profile
@bp.route("/<int:agency_id>", methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.ADMIN)
@validate()
def delete_agency(agency_id: int):
    """Delete an agency profile.
    Must be an admin to delete an agency.
    """
    agency = db.session.query(Agency).get(agency_id)
    if agency is None:
        abort(404, description="Agency not found")
    try:
        db.session.delete(agency)
        db.session.commit()
        track_to_mp(
            request,
            "delete_agency",
            {
                "name": agency.name
            },
        )
        return {"message": "Agency deleted successfully"}
    except Exception as e:
        abort(400, description=str(e))


# Get all agencies
@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_all_agencies():
    """Get all agencies.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    all_agencies = db.session.query(Agency)
    pagination = all_agencies.paginate(
        page=q_page, per_page=q_per_page, max_per_page=100
    )

    try:
        return {
            "results": [
                agency_orm_to_json(agency) for agency in pagination.items],
            "page": pagination.page,
            "totalPages": pagination.pages,
            "totalResults": pagination.total,
        }
    except Exception as e:
        abort(500, description=str(e))


# Get agency officers (In Progress)
@bp.route("/<int:agency_id>/officers", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_agency_officers(agency_id: int):
    """Get all officers for an agency.
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    try:
        agency = db.session.query(Agency).get(agency_id)

        all_officers = agency.officers

        pagination = all_officers.paginate(
            page=q_page, per_page=q_per_page, max_per_page=100
        )
    except Exception as e:
        abort(400, description=str(e))

    return {
        "results": [
            officer_orm_to_json(officer) for officer in pagination.items],
        "page": pagination.page,
        "totalPages": pagination.pages,
        "totalResults": pagination.total,
    }
