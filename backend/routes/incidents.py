from flask import Blueprint


incident_routes = Blueprint(
    "incident_routes", __name__, url_prefix="/incidents"
)


@incident_routes.route("", methods=["GET"])
def get_incidents():
    return ""
