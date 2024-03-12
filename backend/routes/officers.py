import logging
from operator import or_
from typing import Optional

from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from mixpanel import MixpanelException
from backend.database.models.user import UserRole
from backend.database.models.employment import Employment
from flask import Blueprint, abort, request
from flask_jwt_extended.view_decorators import jwt_required
from pydantic import BaseModel

from ..database import Officer, db
from ..schemas import (
    CreateOfficerSchema,
    officer_orm_to_json,
    officer_to_orm,
    validate,
)


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
        schema_extra = {
            "example": {
                "officerName": "John Doe",
                "location" : "New York",
                "badgeNumber" : 1234,
                "page": 1,
                "perPage": 20,
            }
        }


@bp.route("/search", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate(json=SearchOfficerSchema)
def search_officer():
    """Search Officers"""
    body: SearchOfficerSchema = request.context.json
    query = db.session.query('Officer')
    logger = logging.getLogger("officers")

    try:
        if body.name:
            names = body.officerName.split()
            if len(names) == 1:
                query = Officer.query.filter(
                    or_(
                        Officer.first_name.ilike(f"%{body.officerName}%"),
                        Officer.last_name.ilike(f"%{body.officerName}%")
                    )
                )
            elif len(names) == 2:
                query = Officer.query.filter(
                    or_(
                        Officer.first_name.ilike(f"%{names[0]}%"),
                        Officer.last_name.ilike(f"%{names[1]}%")
                    )
                )
            else:
                query = Officer.query.filter(
                    or_(
                        Officer.first_name.ilike(f"%{names[0]}%"),
                        Officer.middle_name.ilike(f"%{names[1]}%"),
                        Officer.last_name.ilike(f"%{names[2]}%")
                    )
                )

        if body.badgeNumber:
            officer_ids = [
                result.officer_id for result in db.session.query(
                    Employment
                    ).filter_by(badge_number=body.badgeNumber).all()
            ]
            query = Officer.query.filter(Officer.id.in_(officer_ids)).all()

    except Exception as e:
        abort(422, description=str(e))

    results = query.paginate(
        page=body.page, per_page=body.perPage, max_per_page=100
    )

    try:
        track_to_mp(request, "search_officer", {
            "officername": body.officerName,
            "badgeNumber": body.badgeNumber
        })
    except MixpanelException as e:
        logger.error(e)
    try:
        return {
            "results": [
                officer_orm_to_json(result) for result in results.items
            ],
            "page": results.page,
            "totalPages": results.pages,
            "totalResults": results.total,
        }
    except Exception as e:
        abort(500, description=str(e))


@bp.route("/create", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate(json=CreateOfficerSchema)
def create_officer():
    """Create an officer profile.
    """

    try:
        officer = officer_to_orm(request.context.json)
    except Exception:
        abort(400)

    created = officer.create()

    track_to_mp(
        request,
        "create_officer",
        {
            "first_name": officer.first_name,
            "middle_name": officer.middle_name,
            "last_name": officer.last_name
        },
    )
    return officer_orm_to_json(created)


@bp.route("/<int:officer_id>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_officer(officer_id: int):
    """Get an officer profile.
    """
    officer = db.session.query(Officer).get(officer_id)
    if officer is None:
        abort(404, description="Officer not found")
    return officer_orm_to_json(officer)


@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_all_officers():
    """Get all officers.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    all_officers = db.session.query(Officer)
    pagination = all_officers.paginate(
        page=q_page, per_page=q_per_page, max_per_page=100
    )

    return {
        "results": [
            officer_orm_to_json(officer) for officer in pagination.items],
        "page": pagination.page,
        "totalPages": pagination.pages,
        "totalResults": pagination.total,
    }
