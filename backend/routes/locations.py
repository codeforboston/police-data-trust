import logging

from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended.view_decorators import jwt_required

from backend.auth.jwt import min_role_required
from backend.database.models.user import UserRole
from backend.dto.location import CityLookupParams
from backend.services.location_service import LocationService

bp = Blueprint("location_routes", __name__, url_prefix="/api/v1/locations")
location_service = LocationService()


@bp.route("/cities", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def list_cities():
    try:
        params = CityLookupParams(**request.args)
    except Exception as e:
        logging.debug(f"Invalid query params: {e}")
        abort(400, description=str(e))

    response, status_code = location_service.list_cities(
        term=params.term,
        state=params.state,
        page=params.page,
        per_page=params.per_page,
    )
    return jsonify(response), status_code
