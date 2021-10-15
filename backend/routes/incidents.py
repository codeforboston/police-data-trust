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
from ..schemas import CreateIncidentSchema, IncidentSchema

bp = Blueprint("incident_routes", __name__, url_prefix="/api/v1/incidents")


@bp.route("/get/<int:incident_id>", methods=["GET"])
@jwt_required()
@role_required(UserRole.PUBLIC)
def get_incidents(incident_id: int):
    return IncidentSchema.from_orm(Incident.get(incident_id)).dict()


@bp.route("/create", methods=["POST"])
@validate()
@jwt_required()
@role_required(UserRole.PUBLIC)
def create_incident(body: CreateIncidentSchema):
    if current_app.env == "production":
        abort(418)

    # pydantic-sqlalchemy only handles ORM -> JSON conversion, not the other way around.
    # sqlalchemy won't convert nested dictionaries into the corresponding ORM types, so we
    # need to manually perform the JSON -> ORM conversion. We can roll our own recursive
    # conversion if we can get the ORM model class associated with a schema instance.

    data = body.dict()
    data["officers"] = [Officer(**record) for record in data["officers"]]
    data["use_of_force"] = [
        UseOfForce(**record) for record in data["use_of_force"]
    ]

    is_empty = lambda d: d is None or (isinstance(d, list) and len(d) == 0)
    supported_fields = set(
        (
            "time_of_incident",
            "source",
            "stop_type",
            "use_of_force",
            "officers",
            "location",
        )
    )
    any_unsupported_fields = not all(
        [
            is_empty(value)
            for field, value in data.items()
            if field not in supported_fields
        ]
    )

    if any_unsupported_fields:
        abort(400)

    obj = Incident(**data).create()
    return IncidentSchema.from_orm(obj).dict()


class SearchIncidentsSchema(BaseModel):
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    incident_type: Optional[str] = None


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
    if body.incident_type:
        query = query.filter(
            Incident.stop_type.ilike(f"%{body.incident_type}%")
        )

    search_results = query.limit(100).all()

    return {
        "results": [
            IncidentSchema.from_orm(result).dict() for result in search_results
        ]
    }
