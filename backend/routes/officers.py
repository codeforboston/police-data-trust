import logging
from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.schemas import (validate_request, ordered_jsonify, args_to_dict)
from backend.database.models.user import UserRole, User
from backend.database.models.officer import Officer
from backend.services.officer_service import OfficerService
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from backend.dto.officer import (
    OfficerSearchParams, GetOfficerParams, GetOfficerMetricsParams,
    CreateOfficer, UpdateOfficer)


bp = Blueprint("officer_routes", __name__, url_prefix="/api/v1/officers")
officer_service = OfficerService()


# Create an officer profile
@bp.route("", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreateOfficer)
def create_officer():
    """Create an officer profile.
    """
    body: CreateOfficer = request.validated_body
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])
    payload = body.model_dump(exclude={"source_uid"})

    try:
        response = officer_service.create_officer(
            payload=payload,
            source_uid=body.source_uid,
            current_user=current_user,
        )
        logging.getLogger("create_officer").info(
            f"Officer {response.get('uid')} created by User {current_user.uid}"
        )
        track_to_mp(
            request,
            "create_officer",
            {
                "officer_id": response.get("uid")
            },
        )
        return ordered_jsonify(response), 201
    except PermissionError as e:
        abort(403, description=str(e))
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        abort(400, description=str(e))


# Get an officer profile
@bp.route("/<officer_uid>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_officer(officer_uid: str):
    """Get an officer profile.
    """
    o = Officer.nodes.get_or_none(uid=officer_uid)
    if o is None:
        abort(404, description="Officer not found")
    raw = {
        **request.args,  # copies simple values
        "include": request.args.getlist("include"),
    }
    try:
        params = GetOfficerParams(**raw)
    except Exception as e:
        logging.debug(f"Invalid query params: {e}")
        abort(400, description=str(e))

    response = officer_service.get_officer(
        officer_uid=officer_uid,
        includes=params.include or [])
    return ordered_jsonify(response)


# Get all officers
@bp.route("", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_all_officers():
    """Get all officers.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    term: filter on officer name
    """
    raw = {
        **args_to_dict(
            request.args,
            always_list={
                "unit",
                "agency",
                "agency_uid",
                "rank",
                "badge_number",
                "ethnicity",
                "city",
                "city_uid",
                "state",
                "source",
                "source_uid",
            },
        ),
    }
    try:
        params = OfficerSearchParams(**raw)
    except Exception as e:
        logging.debug(f"Invalid query params: {e}")
        abort(400, description=str(e))

    response, status_code, use_ordered = officer_service.list_officers(params)

    if use_ordered:
        return ordered_jsonify(response), status_code
    return jsonify(response), status_code


# Update an officer profile
@bp.route("/<officer_uid>", methods=["PUT"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(UpdateOfficer)
def update_officer(officer_uid: str):
    """Update an officer profile.
    """
    body: UpdateOfficer = request.validated_body
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])
    payload = body.model_dump(exclude_unset=True, exclude={"source_uid"})

    try:
        response = officer_service.update_officer(
            officer_uid=officer_uid,
            payload=payload,
            source_uid=body.source_uid,
            current_user=current_user,
        )
    except LookupError as e:
        abort(404, description=str(e))
    except PermissionError as e:
        abort(403, description=str(e))
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        abort(400, description=str(e))

    track_to_mp(
        request,
        "update_officer",
        {
            "officer_id": response.get("uid")
        },
    )
    return ordered_jsonify(response)


# Delete an officer profile
@bp.route("/<officer_uid>", methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.ADMIN)
def delete_officer(officer_uid: str):
    """Delete an officer profile.
    Must be an admin to delete an officer.
    """
    o = Officer.nodes.get_or_none(uid=officer_uid)
    if o is None:
        abort(404, description="Officer not found")
    try:
        uid = o.uid
        o.delete()
        track_to_mp(
            request,
            "delete_officer",
            {
                "officer_id": uid
            },
        )
        return {"message": "Officer deleted successfully"}
    except Exception as e:
        abort(400, description=str(e))


# Retrieve an officer's employment history
@bp.route("/<officer_uid>/employment", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_employment(officer_uid: str):
    """Retrieve an officer's employment history.
    """
    # Get employment history
    try:
        response = officer_service.get_officer_employment(officer_uid)
        return ordered_jsonify(response)
    except Exception as e:
        abort(500, description=str(e))


# Retrieve an officer's metrics summary
@bp.route("/<officer_uid>/metrics", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_officer_metrics(officer_uid: str):
    """Retrieve an officer's metrics summary.
    """
    o = Officer.nodes.get_or_none(uid=officer_uid)
    if o is None:
        abort(404, description="Officer not found")
    raw = {
        **request.args,  # copies simple values
        "include": request.args.getlist("include"),
    }
    try:
        params = GetOfficerMetricsParams(**raw)
    except Exception as e:
        logging.debug(f"Invalid query params: {e}")
        abort(400, description=str(e))

    response = officer_service.get_officer_metrics(
        officer_uid=officer_uid,
        includes=params.include or [])
    return ordered_jsonify(response)
