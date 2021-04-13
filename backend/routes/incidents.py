from flask import Blueprint, jsonify
from backend.models.incidents import Incident


incident_routes = Blueprint("incident_routes", __name__,
                            url_prefix="/incidents")

@incident_routes.route("/test/test", methods=["GET"])
def get_incidents():
    incidents = Incident.query.all()
    incidents = list(map(lambda x: x.as_dict(), incidents))
    return jsonify(incidents)
