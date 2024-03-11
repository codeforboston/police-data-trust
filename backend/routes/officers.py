import logging
from operator import or_
from typing import Optional

from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from mixpanel import MixpanelException
from backend.database.models.user import UserRole
from flask import Blueprint, abort, request
from flask_jwt_extended.view_decorators import jwt_required
from pydantic import BaseModel

from ..database import Officer, db, agency_officer
from ..schemas import (
    officer_orm_to_json,
    validate,
)


bp = Blueprint("officer_routes", __name__, url_prefix="/api/v1/officers")


class SearchOfficerSchema(BaseModel):
    officerName: Optional[str] = None
    location: Optional[str] = None
    badgeNumber: Optional[str] = None
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
    query = Officer.query
    logger = logging.getLogger("officers")

    try:
        if body.officerName:
            names = body.officerName.split()
            first_name = names[0] if len(names) > 0 else ''
            last_name = names[1] if len(names) > 1 else ''
            query = query.filter(or_(
                Officer.first_name.ilike(f"%{first_name}%"),
                Officer.last_name.ilike(f"%{last_name}%")
            ))

        if body.badgeNumber:
            officer_ids = [
                result.officer_id for result in db.session.query(agency_officer)
                .filter_by(badge_number=body.badgeNumber).all()
            ]
            query = query.filter(Officer.id.in_(officer_ids))

    except Exception as e:
        abort(422, description=str(e))

    # Perform pagination on the query
    page = body.page
    per_page = body.perPage
    max_per_page = 100
    results = query.paginate(page=page, per_page=per_page,
                              max_per_page=max_per_page)

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