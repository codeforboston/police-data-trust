from flask import Blueprint
incident_routes = Blueprint("incident_routes", __name__, url_prefix="/incidents")

@incident_routes.route("/")
def get_all_incidents():
  return "All incidents!";

@incident_routes.route("/<id>")
def get_single_incident(id):
  return "Incident: " + id;