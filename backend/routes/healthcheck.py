from flask import Blueprint

from ..database import db, Incident

bp = Blueprint("healthcheck", __name__, url_prefix="/api/v1")


def check_db():
    """Verifies that we can read the incidents table"""
    db.session.query(Incident).count()


@bp.route("/healthcheck", methods=["GET"])
def healthcheck():
    check_db()
    return ("", 200)
