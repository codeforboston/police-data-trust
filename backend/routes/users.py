from flask import Blueprint, abort, request
from flask_jwt_extended import get_jwt, get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from backend.auth.jwt import min_role_required
from backend.database.models.user import UserRole
from backend.dto.user_profile import UpdateCurrentUser
from backend.schemas import ordered_jsonify, validate_request
from backend.services.user_service import UserService


bp = Blueprint("users", __name__, url_prefix="/api/v1/users")
user_service = UserService()


def _not_found_response(message: str):
    return ordered_jsonify({"message": message}), 404


@bp.route("/self", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_current_user():
    """Return the currently authenticated user's full profile."""
    jwt_decoded = get_jwt()

    try:
        response = user_service.get_user_profile(jwt_decoded["sub"])
        return ordered_jsonify(response), 200
    except LookupError as e:
        return _not_found_response(str(e))


@bp.route("/<user_uid>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_user_by_uid(user_uid: str):
    """Return a user's profile by UID."""
    try:
        response = user_service.get_user_profile(user_uid)
        return ordered_jsonify(response), 200
    except LookupError as e:
        return _not_found_response(str(e))


@bp.route("/self", methods=["PATCH"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate_request(UpdateCurrentUser)
def update_current_user():
    """Update the currently authenticated user's profile."""
    body: UpdateCurrentUser = request.validated_body
    jwt_decoded = get_jwt()

    try:
        response = user_service.update_current_user_profile(
            user_uid=jwt_decoded["sub"],
            body=body,
        )
        return ordered_jsonify(response), 200
    except LookupError as e:
        return _not_found_response(str(e))
    except ValueError as e:
        abort(400, description=str(e))


@bp.route("/self/upload-profile-image", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def upload_profile_image():
    """Update the current user's profile image."""
    if "file" not in request.files:
        abort(400, description="Missing file")

    file = request.files["file"]
    if not file or not file.filename:
        abort(400, description="Empty file")

    user_uid = get_jwt_identity()

    try:
        response = user_service.update_profile_image(user_uid, file)
        return ordered_jsonify(response), 200
    except LookupError as e:
        abort(404, description=str(e))
    except ValueError as e:
        abort(400, description=str(e))


@bp.route("/self/profile-image", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_profile_photo():
    """Retrieve the current user's profile image."""
    user_uid = get_jwt_identity()

    try:
        return user_service.get_profile_photo(user_uid)
    except LookupError as e:
        abort(404, description=str(e))
    except FileNotFoundError as e:
        abort(404, description=str(e))
