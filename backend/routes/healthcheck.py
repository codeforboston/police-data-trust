from flask import Blueprint
from pydantic import BaseModel
from spectree import Response

from ..schemas import spec, validate

bp = Blueprint("healthcheck", __name__, url_prefix="/api/v1")


class Resp(BaseModel):
    apiVersion: str


# TODO: Add checks to validate backing services or dependencies
@bp.route("/healthcheck", methods=["GET"])
@validate(auth=False, resp=Response("HTTP_500", HTTP_200=Resp))
def healthcheck():
    """Verifies service health and returns the api version"""
    return ({"apiVersion": spec.config.VERSION}, 200)
