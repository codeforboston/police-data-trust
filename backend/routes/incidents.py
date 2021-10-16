from datetime import datetime
from typing import Optional

from backend.auth.jwt import role_required
from backend.database.models.officer import Officer
from backend.database.models.use_of_force import UseOfForce
from backend.database.models.user import UserRole
from flask import Blueprint, abort, current_app
from flask_jwt_extended.view_decorators import jwt_required
from flask_pydantic import validate
from pydantic import BaseModel

from ..database import Incident, db
from ..schemas import (
    CreateIncidentSchema,
    incident_to_orm,
    incident_orm_to_json,
)

bp = Blueprint("incident_routes", __name__, url_prefix="/api/v1/incidents")


@bp.route("/get/<int:incident_id>", methods=["GET"])
@jwt_required()
@role_required(UserRole.PUBLIC)
def get_incidents(incident_id: int):
    return incident_orm_to_json(Incident.get(incident_id))


@bp.route("/create", methods=["POST"])
@validate()
@jwt_required()
# TODO: Require CONTRIBUTOR role
@role_required(UserRole.PUBLIC)
def create_incident(body: CreateIncidentSchema):
    if current_app.env == "production":
        abort(418)

    try:
        incident = incident_to_orm(body)
    except:
        abort(400)

    created = incident.create()
    return incident_orm_to_json(created)


class SearchIncidentsSchema(BaseModel):
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    description: Optional[str] = None


@bp.route("/search", methods=["GET"])
@validate()
@jwt_required()
@role_required(UserRole.PUBLIC)
def search_incidents(body: SearchIncidentsSchema):
    query = db.session.query(Incident)

    if body.location:
        # TODO: Replace with .match, which uses `@@ to_tsquery` for full-text search
        # TODO: eventually replace with geosearch. Geocode records and integrate PostGIS
        query = query.filter(Incident.location.ilike(f"%{body.location}%"))
    if body.start_time:
        query = query.filter(Incident.time_of_incident >= body.start_time)
    if body.end_time:
        query = query.filter(Incident.time_of_incident <= body.end_time)
    if body.description:
        query = query.filter(
            Incident.description.ilike(f"%{body.description}%")
        )

    search_results = query.limit(100).all()

    return {
        "results": [incident_orm_to_json(result) for result in search_results]
    }
