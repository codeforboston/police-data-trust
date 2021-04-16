from flask import Blueprint, Response, jsonify
from backend.database import Incidents, IncidentSchema


incident_routes = Blueprint(
    "incident_routes", __name__, url_prefix="/incidents"
)


@incident_routes.route("/test", methods=["GET"])
def get_incidents():
    incidents = Incidents.query.all()
    incident_schema = IncidentSchema(many=True)
    incidents_dump = incident_schema.dump(incidents)
    return jsonify(incidents_dump)

# define these routes last, otherwise they will override /<route> routes
@incident_routes.route("/", methods=["POST", "GET"])
@incident_routes.route("/<id>", methods=["PUT", "DELETE"])
def get_single_incident(id=None):
    return Incidents.get_delete_put_post(id)