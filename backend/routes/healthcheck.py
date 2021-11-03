from flask import Blueprint
from pydantic import BaseModel
from spectree import Response

from ..database import db, Incident
from ..schemas import spec, validate

bp = Blueprint("healthcheck", __name__, url_prefix="/api/v1")


def check_db():
    """Verifies that we can read the incidents table"""
    db.session.query(Incident).count()


class Resp(BaseModel):
    apiVersion: str


@bp.route("/healthcheck", methods=["GET"])
@validate(auth=False, resp=Response("HTTP_500", HTTP_200=Resp))
def healthcheck():
    """Verifies service health and returns the api version"""
    check_db()
    return ({"apiVersion": spec.config.VERSION}, 200)
