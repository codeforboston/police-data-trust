from flask import abort
from flask import Blueprint
from flask import current_app

from flask_pydantic import validate

from ..schemas import IncidentSchema
from ..schemas import CreateIncidentSchema
from ..database import Incident


bp = Blueprint("incident_routes", __name__, url_prefix="/api/v1/incidents")

@bp.route("/get/<int:incident_id>", methods=["GET"])
def get_incidents(incident_id: int):
    return IncidentSchema.from_orm(Incident.get(incident_id)).dict()


@bp.route("/create", methods=["POST"])
@validate()
def create_incident(body: CreateIncidentSchema):
    if current_app.env == "production":
        abort(418)
    # <-- Add stuff here
    obj = Incident(**body.dict()).create()
    # <-- Add more stuff here
    return IncidentSchema.from_orm(obj).dict()
