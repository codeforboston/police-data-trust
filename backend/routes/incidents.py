from flask import Blueprint
from backend.incidents import Incidents


incident_routes = Blueprint("incident_routes", __name__, url_prefix="/incidents")


@incident_routes.route("/", methods=["POST", "GET"])
@incident_routes.route("/<id>", methods=["PUT", "DELETE"])
def get_single_incident(id=None):
    return Incidents.get_delete_put_post(id)
