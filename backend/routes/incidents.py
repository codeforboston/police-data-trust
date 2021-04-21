from flask import Blueprint, jsonify
from backend.database import Incidents, IncidentSchema


incident_routes = Blueprint(
    "incident_routes", __name__, url_prefix="/incidents"
)


@incident_routes.route("", methods=["GET"])
def get_incidents():
    incidents = Incidents.query.all()
    incident_schema = IncidentSchema(many=True)
    incidents_dump = incident_schema.dump(incidents)
    return jsonify(incidents_dump)
