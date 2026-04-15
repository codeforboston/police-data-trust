import logging

from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from backend.auth.jwt import min_role_required
from backend.database.models.user import User, UserRole
from backend.dto.location import (
    CityLookupParams,
    CountyLookupParams,
    NearbyCityLookupParams,
    RelevantCityLookupParams,
    StateLookupParams,
)
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


@bp.route("/cities/nearby", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def list_nearby_cities():
    try:
        params = NearbyCityLookupParams(**request.args)
    except Exception as e:
        logging.debug(f"Invalid query params: {e}")
        abort(400, description=str(e))

    response, status_code = location_service.list_nearby_cities(
        latitude=params.latitude,
        longitude=params.longitude,
        per_page=params.per_page,
    )
    return jsonify(response), status_code


@bp.route("/cities/relevant", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def list_relevant_cities():
    try:
        params = RelevantCityLookupParams(**request.args)
    except Exception as e:
        logging.debug(f"Invalid query params: {e}")
        abort(400, description=str(e))

    current_user = User.nodes.get_or_none(uid=get_jwt_identity())

    response, status_code = location_service.list_relevant_cities(
        user_city=current_user.city if current_user else None,
        user_state=current_user.state if current_user else None,
        per_page=params.per_page,
    )
    return jsonify(response), status_code


@bp.route("/counties", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def list_counties():
    try:
        params = CountyLookupParams(**request.args)
    except Exception as e:
        logging.debug(f"Invalid query params: {e}")
        abort(400, description=str(e))

    response, status_code = location_service.list_counties(
        term=params.term,
        state=params.state,
        page=params.page,
        per_page=params.per_page,
    )
    return jsonify(response), status_code


@bp.route("/states", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def list_states():
    try:
        params = StateLookupParams(**request.args)
    except Exception as e:
        logging.debug(f"Invalid query params: {e}")
        abort(400, description=str(e))

    response, status_code = location_service.list_states(
        term=params.term,
        page=params.page,
        per_page=params.per_page,
    )
    return jsonify(response), status_code
