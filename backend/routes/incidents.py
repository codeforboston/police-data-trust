from flask import abort
from flask import Blueprint
from flask import current_app

from flask_pydantic import validate

from backend.database.models.officer import Officer
from backend.database.models.use_of_force import UseOfForce

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
        ("time_of_incident", "stop_type", "use_of_force", "officers")
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

    # <-- Add stuff here
    obj = Incident(**data).create()
    # <-- Add more stuff here
    return IncidentSchema.from_orm(obj).dict()
