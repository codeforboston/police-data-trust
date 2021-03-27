from flask import Blueprint, jsonify
from backend.incidents import Incidents
from backend.incidents import db


incident_routes = Blueprint("incident_routes", __name__,
                            url_prefix="/incidents")

@incident_routes.route("/test/test", methods=["GET"])
def get_incidents():
    incidents = Incidents.query.all()
    print(incidents)
    return jsonify(incidents)
