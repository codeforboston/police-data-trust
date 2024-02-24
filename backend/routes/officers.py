import logging
from operator import or_
from typing import Optional
from venv import logger

from backend.auth.jwt import min_role_required
from backend.database.models.agency import JURISDICTION
from backend.mixpanel.mix import track_to_mp
from mixpanel import MixpanelException
from backend.database.models.user import UserRole
from flask import  Blueprint, abort, jsonify, request
from flask_jwt_extended.view_decorators import jwt_required
from pydantic import BaseModel

from ..database import  Officer, db, agency_officer, Agency
from ..schemas import (
    Officer_orm_to_json,
    validate,
)


bp = Blueprint("officer_routes", __name__, url_prefix="/api/v1/officers")

class SearchOfficerSchema(BaseModel):
    officerName: Optional[str] = None
    location:Optional[str]=None
    badgeNumber:Optional[str]=None
    page: Optional[int] = 1
    perPage: Optional[int] = 20

    class Config:
        extra = "forbid"
        schema_extra = {
            "example": {
                "officerName": "John Doe",
                "location":"New York",
                "badgeNumber":1234,
                "page": 1,
                "perPage": 20,
            }
        }

@bp.route("/search/officer",methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate(json=SearchOfficerSchema)
def search_officer():
    """Search Officers"""
    print("started searching..")
    body:SearchOfficerSchema=request.context.json

    query = db.session.query('Officer')
    # logger = logging.getLogger('officer')
    try:
        
        if body.officerName:
            names = body.officerName.split()
            first_name = names[0] if len(names) > 0 else ''
            last_name = names[1] if len(names) > 1 else ''
            query = Officer.query.filter(or_(
                Officer.first_name.ilike(f"%{first_name}%"),
                Officer.last_name.ilike(f"%{last_name}%")
            ))
        
        if body.badgeNumber:
            officer_ids = [result.officer_id for result in db.session.query(agency_officer).filter_by(badge_number=body.badgeNumber).all()]
            query = Officer.query.filter(Officer.id.in_(officer_ids)).all()
        # query_result = db.session.query(agency_officer)
        # officer_ids = [result.officer_id for result in db.session.query(agency_officer).all()]

        # Query Officer table to get officer data based on the list of officer_ids
        # officers = Officer.query.filter(Officer.id.in_(officer_ids)).all()

        # Create a list of officer data to return in the res ds
        # //sddaeweawdsecdf dsfsda ss
        # officer_data = []
        # for result,officer in zip(query_result,officers):
        #     officer_data.append({
        #         'id': officer.id,
        #         'badge_number':result.badge_number,
        #         'first_name': officer.first_name,
        #         'last_name': officer.last_name,
        #         'race': officer.race,
        #         'ethnicity': officer.ethnicity,
        #         'gender': officer.gender,
        #         'date_of_birth': str(officer.date_of_birth)  # Convert date to string for JSON serialization
        #     })

        # return jsonify({'officers': officer_data})
    except Exception as e:
        abort(422,description=str(e))

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

