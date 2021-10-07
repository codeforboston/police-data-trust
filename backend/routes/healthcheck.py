from flask import abort
from flask import Blueprint
from flask import current_app

from flask_pydantic import validate


bp = Blueprint("healthcheck", __name__,)

# TODO: Add checks to validate backing services or dependencies
@bp.route("/healthcheck", methods=["GET"])
def healthcheck():
    return ('', 200)
