from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_access_cookies,
)
from pydantic.main import BaseModel
from ..auth import min_role_required, user_manager
from ..database import User, UserRole, db
from ..dto import LoginUserDTO, RegisterUserDTO
from ..schemas import UserSchema, validate

bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@bp.route("/login", methods=["POST"])
@validate(auth=False, json=LoginUserDTO)
def login():
    """Sign in with email and password.

    Returns an access token and sets cookies.
    """

    body: LoginUserDTO = request.context.json

    # Verify user
    if body.password is not None and body.email is not None:
        user = User.query.filter_by(email=body.email).first()
        if user is not None and user.verify_password(body.password):
            token = create_access_token(identity=user.id)
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
@validate(auth=False, json=RegisterUserDTO)
def register():
    """Register for a new public account.

    If successful, also performs login.
    """

    body: RegisterUserDTO = request.context.json

    # Check to see if user already exists
    user = User.query.filter_by(email=body.email).first()
    if user is not None:
        return {
            "status": "ok",
            "message": "Error. Email matches existing account.",
        }, 400
    # Verify all fields included and create user
    if body.password is not None and body.email is not None:
        user = User(
            email=body.email,
            password=user_manager.hash_password(body.password),
            first_name=body.firstName,
            last_name=body.lastName,
            role=UserRole.PUBLIC,
            phone_number=body.phoneNumber,
        )
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=user.id)
        resp = jsonify(
            {
                "status": "ok",
                "message": "Successfully registered.",
                "access_token": token,
            }
        )
        set_access_cookies(resp, token)
        return resp, 200
    # In case of missing fields, return error message indicating
    # required fields.
    missing_fields = []
    required_keys = ["email", "password"]
    for key in required_keys:
        if key not in body.keys() or body.get(key) is None:
            missing_fields.append(key)
    return {
        "status": "ok",
        "message": "Failed to register. Please include the following"
        " fields: " + ", ".join(missing_fields),
    }, 400


@bp.route("/refresh", methods=["POST"])
@jwt_required()
@validate()
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
@validate(auth=False)
def logout():
    """Unsets access cookies."""
    resp = jsonify({"message": "successfully logged out"})
    unset_access_cookies(resp)
    return resp, 200


@bp.route("/whoami", methods=["GET"])
@cross_origin()
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def test_auth():
    """Returns the currently-authenticated user."""
    current_identity = get_jwt_identity()
    return UserSchema.from_orm(User.get(current_identity)).dict()


class EmailDTO(BaseModel):
    email: str


@bp.route("/forgotPassword", methods=["POST"])
@validate(auth=False, json=EmailDTO)
def send_reset_email():
    body: EmailDTO = request.context.json
    print(user_manager.find_user_by_email(body.email))
    user_manager.send_reset_password_email(body.email)
    # always 200 so you cant use this endpoint to find emails of users
    return {}, 200


class PasswordDTO(BaseModel):
    password: str


@bp.route("/resetPassword", methods=["POST"])
@jwt_required()
@validate(auth=True, json=PasswordDTO)
def reset_password():
    body: PasswordDTO = request.context.json
    # NOTE: 401s if the user or token is not valid
    # NOTE: This token follows the logged in user token lifespan
    user = User.get(get_jwt_identity())
    user.password = user_manager.hash_password(body.password)
    db.session.commit()
    return {"message": "Password successfully changed"}, 200
