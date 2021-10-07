from flask import Blueprint


bp = Blueprint("healthcheck", __name__,)

# TODO: Add checks to validate backing services or dependencies
@bp.route("/healthcheck", methods=["GET"])
def healthcheck():
    return ('', 200)
