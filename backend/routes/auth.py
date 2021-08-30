from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_access_cookies

from ..database import db
from ..database import User
from ..database import UserRole
from ..database import login_manager
from ..auth import role_required
from ..auth import user_manager
from ..schemas import UserSchema
from ..dto import RegisterUserDTO
from ..dto import LoginUserDTO
from flask_pydantic import validate


bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@bp.route("/login", methods=["POST"])
@validate()
def login(body: LoginUserDTO):
    # Verify user
    if body.password is not None and body.email is not None:
        user = User.query.filter_by(email=body.email).first()
        if user is not None and user.verify_password(body.password):
            token = create_access_token(identity=user.id)
            resp = jsonify({
                "message": "Successfully logged in.",
                "access_token": token,
            })
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
@validate()
def register(body: RegisterUserDTO):
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
        )
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=user.id)
        resp = jsonify({
            "status": "ok",
            "message": "Successfully registered.",
            "access_token": token,
        })
        set_access_cookies(resp, token)
        return  resp, 200
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
def refresh_token():
    access_token = create_access_token(identity=get_jwt_identity()) 
    resp = jsonify({
        "message": "token refreshed successfully",
        "access_token": access_token,
    })
    set_access_cookies(resp, access_token)
    return resp, 200


@bp.route("/logout", methods=["POST"])
def logout():
    resp = jsonify({ "message": "successfully logged out"})
    unset_access_cookies(resp);
    return resp, 200


@bp.route("/test", methods=["GET"])
@jwt_required()
@role_required(UserRole.PUBLIC)
def test_auth():
    current_identity = get_jwt_identity()
    return UserSchema.from_orm(User.get(current_identity)).dict()
