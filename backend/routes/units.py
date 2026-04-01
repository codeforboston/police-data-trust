import logging
from backend.auth.jwt import min_role_required
from backend.schemas import ordered_jsonify
from backend.database.models.user import UserRole
from backend.database.models.agency import Unit
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended.view_decorators import jwt_required
from backend.dto.unit import (
    UnitQueryParams, GetUnitParams, GetUnitOfficersParams)
from backend.services.unit_service import UnitService

bp = Blueprint("unit_routes", __name__, url_prefix="/api/v1/units")
unit_service = UnitService()


@bp.route("", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_all_units():
    """Get all units.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    name: filter on unit name
    city: filter on unit city
    state: filter on unit state
    """
    try:
        params = UnitQueryParams(**request.args)
    except Exception as e:
        logging.warning(f"Invalid query params: {e}")
        abort(400, description=str(e))

    response, status_code, use_ordered = unit_service.list_units(params)

    if use_ordered:
        return ordered_jsonify(response), status_code
    return jsonify(response), status_code


@bp.route("/<uid>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_unit(uid: str):
    """Get unit details by UID."""
    unit = Unit.nodes.get_or_none(uid=uid)
    if not unit:
        abort(404, description="Unit not found")
    raw = {
        **request.args,
        "include": request.args.getlist("include"),
    }
    try:
        params = GetUnitParams(**raw)
    except Exception as e:
        logging.warning(f"Invalid query params: {e}")
        abort(400, description=str(e))

    unit_data = unit_service.get_unit(
        uid=uid,
        includes=params.include or [])
    return ordered_jsonify(unit_data), 200


# Get officers for a specific unit
@bp.route("/<uid>/officers", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_unit_officers(uid: str):
    """Get officers for a specific unit by UID."""
    raw = {
        **request.args,
        "include": request.args.getlist("include"),
    }
    try:
        params = GetUnitOfficersParams(**raw)
    except Exception as e:
        logging.warning(f"Invalid query params: {e}")
        abort(400, description=str(e))

    try:
        result = unit_service.list_unit_officers(
            unit_uid=uid,
            page=params.page,
            per_page=params.per_page,
            includes=params.include or [],
        )
        return ordered_jsonify(result), 200
    except IndexError:
        return jsonify({"message": "Page number exceeds total results"}), 400
    except ValueError:
        abort(404, description="Unit not found")
