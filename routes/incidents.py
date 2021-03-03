from flask import Blueprint, request, jsonify
from incidents import Incidents
incident_routes = Blueprint("incident_routes", __name__, url_prefix="/incidents")

@incident_routes.route("/")
@incident_routes.route("/<id>")
def get_single_incident(id):
  return Incidents.get_delete_put_post(id)

@incident_routes.route("/", methods=["POST"])
def create_incident():
  Incidents.get_delete_put_post()
  return "201"
  # return jsonify(inc)