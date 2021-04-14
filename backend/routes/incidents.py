from flask import Blueprint, Response, jsonify
from backend.database import Incidents, IncidentSchema


incident_routes = Blueprint(
    "incident_routes", __name__, url_prefix="/incidents"
)

@incident_routes.route("/test/test", methods=["GET"])
def get_incidents():
    incidents = Incidents.query.all()
    print(incidents)
    incident_schema = IncidentSchema(many=True)
    incidents_dump = incident_schema.dump(incidents)
    print(incidents_dump)
    return jsonify(incidents_dump)
