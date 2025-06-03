import logging
from datetime import timedelta
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import (
    create_access_token,
    decode_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_access_cookies,
)

from ..auth import min_role_required
from pydantic.main import BaseModel
from ..mixpanel.mix import track_to_mp
from ..database import User, UserRole, Invitation, StagedInvitation
from ..dto import LoginUserDTO, RegisterUserDTO, ResetPasswordDTO
from ..schemas import validate_request

bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@bp.route("/login", methods=["POST"])
@validate_request(LoginUserDTO)
def login():
    """Sign in with email and password.

    Returns an access token and sets cookies.
    """
    logger = logging.getLogger("user_login")

    body: LoginUserDTO = request.validated_body

    # Verify user
    if body.password is not None and body.email is not None:
        user = User.nodes.first_or_none(email=body.email)
        if user is not None and user.verify_password(body.password):
            token = create_access_token(identity=user.uid)
            logger.info(f"User {user.uid} logged in successfully.")
            resp = jsonify(
                {
                    "message": "Successfully logged in.",
                    "access_token": token,
                }
            )
            set_access_cookies(resp, token)
            return resp, 200
        else:
            return {
                "message": "Error. Email or Password invalid.",
            }, 401
    # In case of missing fields, return error message indicating
    # required fields.
    missing_fields = []
    required_keys = ["email", "password"]
    for key in required_keys:
        if key not in body or body[key] is None:
            missing_fields.append(key)
    return {
        "message": "Failed to log in. Please include the following"
        "fields: " + ", ".join(missing_fields),
    }, 400


@bp.route("/register", methods=["POST"])
@validate_request(RegisterUserDTO)
def register():
    """Register for a new public account.

    If successful, also performs login.
    """
    logger = logging.getLogger("user_register")
    body: RegisterUserDTO = request.validated_body
    logger.info(f"Registering user with email {body.email}.")

    # Check to see if user already exists
    user = User.nodes.first_or_none(email=body.email)
    if user is not None:
        return {
            "status": "Conflict",
            "message": "Error. Email matches existing account.",
        }, 409
    # Verify all fields included and create user
    if body.password is not None and body.email is not None:
        user = User(
            email=body.email,
            password_hash=User.hash_password(body.password),
            first_name=body.firstname,
            last_name=body.lastname,
            phone_number=body.phone_number,
        )
        user.save()
        token = create_access_token(identity=user.uid)

        """
        code to handle adding staged_invitations-->invitations for users
        who have just signed up for NPDC
        """
        staged_invite = StagedInvitation.nodes.filter(email=user.email)
        if staged_invite is not None and len(staged_invite) > 0:
            for instance in staged_invite:
                new_invitation = Invitation(
                    user_uid=user.uid,
                    role=instance.role,
                    partner_uid=instance.partner_id)
                new_invitation.save()
                instance.delete()

        resp = jsonify(
            {
                "status": "OK",
                "message": "Successfully registered.",
                "access_token": token,
            }
        )
        set_access_cookies(resp, token)

        logger.info(f"User {user.uid} registered successfully.")
        track_to_mp(request, "register", {
            'user_id': user.uid,
            'success': True,
        })
        return resp, 200
    # In case of missing fields, return error message indicating
    # required fields.
    missing_fields = []
    required_keys = ["email", "password"]
    for key in required_keys:
        if key not in body.keys() or body.get(key) is None:
            missing_fields.append(key)
    return {
        "status": "Unprocessable Entity",
        "message": "Invalid request body. Please include the following"
        " fields: " + ", ".join(missing_fields),
    }, 422


@bp.route("/refresh", methods=["POST"])
@jwt_required()
def refresh_token():
    """Refreshes the currently-authenticated user's access token."""

    access_token = create_access_token(identity=get_jwt_identity())
    resp = jsonify(
        {
            "message": "token refreshed successfully",
            "access_token": access_token,
        }
    )
    set_access_cookies(resp, access_token)
    return resp, 200


@bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Unsets access cookies."""
    resp = jsonify({"message": "successfully logged out"})
    unset_access_cookies(resp)
    return resp, 200


@bp.route("/whoami", methods=["GET"])
@cross_origin()
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def test_auth():
    """Returns the currently-authenticated user."""
    current_identity = get_jwt_identity()
    return User.nodes.get(uid=current_identity).to_dict()


class EmailDTO(BaseModel):
    email: str


@bp.route("/forgotPassword", methods=["POST"])
@validate_request(EmailDTO)
def send_reset_email():
    body: EmailDTO = request.validated_body
    logger = logging.getLogger("user_forgot_password")
    user = User.get_by_email(body.email)
    if user is not None:
        reset_token = create_access_token(
            identity=body.email,
            additional_claims={"pw_reset": True},
            expires_delta=timedelta(minutes=20))
        user.send_reset_password_email(body.email, reset_token)
        logger.info(f"User {user.uid} requested a password reset.")
    else:
        logger.info(f"Invalid email address {body.email}.")
    # always 200 so you cant use this endpoint to find emails of users
    return {}, 200


class PasswordDTO(BaseModel):
    password: str


@bp.route("/setPassword", methods=["POST"])
@jwt_required()
@validate_request(PasswordDTO)
def reset_password():
    logger = logging.getLogger("user_reset_password")
    body: PasswordDTO = request.validated_body
    # NOTE: 401s if the user or token is not valid
    # NOTE: This token follows the logged in user token lifespan
    user = User.get(get_jwt_identity())
    user.set_password(body.password)
    logger.info(f"User {user.uid} reset their password.")
    return {"message": "Password successfully changed"}, 200


@bp.route("/resetPassword", methods=["POST"])
@validate_request(ResetPasswordDTO)  # includes token and new password
def reset_password_from_token():
    logger = logging.getLogger("user_reset_password")
    body: ResetPasswordDTO = request.validated_body
    try:
        decoded_token = decode_token(body.token)
        if not decoded_token.get("pw_reset"):
            logger.info("Invalid token")
            return {"message": "Invalid token"}, 400
    except Exception:
        return {"message": "Invalid or expired token"}, 400

    user = User.get_by_email(decoded_token["sub"])
    if not user:
        return {"message": "User not found"}, 404

    logger.info(f"Updating password for user {user.email}")
    user.set_password(body.password)
    user.save()

    # log the user in after resetting the password
    token = create_access_token(identity=user.uid)
    resp = jsonify(
        {
            "message": "Password has been reset successfully.",
            "access_token": token,
        }
    )
    set_access_cookies(resp, token)
    logger.info(f"User {user.uid} logged in after password reset.")

    return resp, 200
