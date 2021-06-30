from flask import Blueprint


bp = Blueprint("incident_routes", __name__, url_prefix="/incidents")


@bp.route("", methods=["GET"])
def get_incidents():
    return ""
