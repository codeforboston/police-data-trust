import logging
from operator import or_
from typing import Optional
from venv import logger

from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from mixpanel import MixpanelException
from backend.database.models.user import UserRole
from flask import  Blueprint, abort, request
from flask_jwt_extended.view_decorators import jwt_required
from pydantic import BaseModel

from ..database import  Officer, db
from ..schemas import (
    Officer_orm_to_json,
    validate,
)


bp = Blueprint("officer_routes", __name__, url_prefix="/api/v1/officers")

class SearchOfficerSchema(BaseModel):
    officerName: Optional[str] = None
    page: Optional[int] = 1
    perPage: Optional[int] = 20

    class Config:
        extra = "forbid"
        schema_extra = {
            "example": {
                "officername": "John Doe",
                "page": 1,
                "perPage": 20,
            }
        }

@bp.route("/search/officer",methods=["POST"])
# @jwt_required()
# @min_role_required(UserRole.PUBLIC)
@validate(json=SearchOfficerSchema)
def search_officer():
    """Search Officers"""
    print("started searching..")
    body:SearchOfficerSchema=request.context.json
    query = db.session.query('Officer')
    # logger = logging.getLogger('officer')
    try:
        data=Officer.query.all()
        # user_data= [{'id': user.id, 'name': user.first_name, } for user in data]
        # return jsonify(user_data), 200

        if body.officerName:
            names = body.officerName.split()
            firstName = names[0] if len(names) > 0 else ''
            lastName = names[1] if len(names) > 1 else ''
            print(firstName)
            print(lastName)
            query = query.filter(or_(
                Officer.first_name.ilike(f"%{firstName}%"),
                Officer.last_name.ilike(f"%{lastName}%")
            ))
            # location
            # badgeid(officer id)

    except Exception as e:
        abort(422,description=str(e))

    results = query.paginate(
        page=body.page, per_page=body.perPage, max_per_page=100
    )
    # print(len(results))

    try:
        track_to_mp(request, "search_officer", {
            "officername": body.officerName
            
        })
    except MixpanelException as e:
        logger.error(e)
    try:
        return{
            "results":[
                
                Officer_orm_to_json(result) for result in results.items
            ],
            "page": results.page,
            "totalPages": results.pages,
            "totalResults": results.total,
        }
    except Exception as e:
        abort(500, description=str(e))
