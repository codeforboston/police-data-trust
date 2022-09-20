from datetime import datetime
from typing import Optional

from backend.auth.jwt import min_role_required
from backend.database.models.user import UserRole
from flask import Blueprint, abort, current_app, request
from flask_jwt_extended.view_decorators import jwt_required
from pydantic import BaseModel

from ..database import Incident, db
from ..schemas import (
    CreateIncidentSchema,
    incident_orm_to_json,
    incident_to_orm,
    validate,
)

bp = Blueprint("incident_routes", __name__, url_prefix="/api/v1/incidents")


@bp.route("/get/<int:incident_id>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_incidents(incident_id: int):
    """Get a single incident by ID."""

    return incident_orm_to_json(Incident.get(incident_id))


@bp.route("/create", methods=["POST"])
@jwt_required()
# TODO: Require CONTRIBUTOR role
@min_role_required(UserRole.PUBLIC)
@validate(json=CreateIncidentSchema)
def create_incident():
    """Create a single incident.

    Cannot be called in production environments
    """
    if current_app.env == "production":
        abort(418)

    try:
        incident = incident_to_orm(request.context.json)
    except Exception:
        abort(400)

    created = incident.create()
    return incident_orm_to_json(created)


class SearchIncidentsSchema(BaseModel):
    location: Optional[str] = None
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    description: Optional[str] = None
    page: Optional[int] = 1
    perPage: Optional[int] = 20

    class Config:
        extra = "forbid"
        schema_extra = {
            "example": {
                "description": "Test description",
                "endTime": "2019-12-01 00:00:00",
                "location": "Location 1",
                "startTime": "2019-09-01 00:00:00",
            }
        }


@bp.route("/search", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate(json=SearchIncidentsSchema)
def search_incidents():
    """Search Incidents."""
    body: SearchIncidentsSchema = request.context.json
    query = db.session.query(Incident)

    if body.location:
        # TODO: Replace with .match, which uses `@@ to_tsquery` for full-text
        # search
        #
        # TODO: eventually replace with geosearch. Geocode records and integrate
        # PostGIS
        query = query.filter(Incident.location.ilike(f"%{body.location}%"))
    if body.startTime:
        query = query.filter(Incident.time_of_incident >= body.startTime)
    if body.endTime:
        query = query.filter(Incident.time_of_incident <= body.endTime)
    if body.description:
        query = query.filter(
            Incident.description.ilike(f"%{body.description}%")
        )

    results = query.paginate(
        page=body.page, per_page=body.perPage, max_per_page=100
    )

    return {
        "results": [incident_orm_to_json(result) for result in results.items],
        "page": results.page,
        "totalPages": results.pages,
        "totalResults": results.total,
    }
