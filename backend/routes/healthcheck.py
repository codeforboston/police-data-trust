from flask import Blueprint


bp = Blueprint("healthcheck", __name__, url_prefix="/api/v1")


# TODO: Add checks to validate backing services or dependencies
@bp.route("/healthcheck", methods=["GET"])
def healthcheck():
    return ('', 200)
