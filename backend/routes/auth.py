from flask import redirect
from flask import request
from flask import Blueprint
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from ..database import db
from ..database import User
from ..database import login_manager
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from ..auth import user_manager
from ..schemas import UserSchema

bp = Blueprint("auth", __name__, url_prefix="/auth")


# TODO: Place cookie on users browser with JWT token
@bp.route("/login", methods=["POST"])
def login():
    """Login Page."""
    if request.method == "POST":
        form = request.form
        # Verify user
        if form.get("password") is not None and form.get("email") is not None:
            user = User.query.filter_by(email=form.get("email")).first()
            if user is not None and user.verify_password(form.get("password")):
                login_user(user, form.get("remember_me"))
                return {
                    "status": "ok",
                    "message": "Successfully logged in.",
                    "access_token": create_access_token(identity=user.id),
                }
            else:
                return {
                    "status": "ok",
                    "message": "Error. Email or Password invalid.",
                }
        # In case of missing fields, return error message indicating
        # required fields.
        missing_fields = []
        required_keys = ["email", "password"]
        for key in required_keys:
            if key not in form.keys() or form.get(key) is None:
                missing_fields.append(key)
        return {
            "status": "ok",
            "message": "Failed to log in. Please include the following"
            " fields: " + ", ".join(missing_fields),
        }
    else:
        return {"status": 400, "message:": "Error: Bad Request."}


# TODO: Clear cookie on users browser
@bp.route("/logout")
@login_required
def logout():
    """Logout Page."""
    logout_user()
    return redirect("/login")


# TODO: place cookie on users browser
@bp.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        form = request.form
        # Check to see if user already exists
        user = User.query.filter_by(email=form.get("email")).first()
        if user is not None and user.verify_password(form.get("password")):
            return {
                "status": "ok",
                "message": "Error. Email matches existing account.",
            }
        # Verify all fields included and create user
        if form.get("password") is not None and form.get("email") is not None:
            user = User(
                email=form.get("email"),
                password=user_manager.hash_password(form.get("password")),
                first_name=form.get("firstName"),
                last_name=form.get("lastName"),
            )
            db.session.add(user)
            db.session.commit()
            return {
                "status": "ok",
                "message": "Successfully registered.",
                "access_token": create_access_token(identity=user.id),
            }
        # In case of missing fields, return error message indicating
        # required fields.
        missing_fields = []
        required_keys = ["email", "password"]
        for key in required_keys:
            if key not in form.keys() or form.get(key) is None:
                missing_fields.append(key)
        return {
            "status": "ok",
            "message": "Failed to register. Please include the following"
            " fields: " + ", ".join(missing_fields),
        }
    else:
        return {"status": 400, "message:": "Error: Bad Request."}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route("/test", methods=["GET"])
@jwt_required()
def test_auth():
    current_identity = get_jwt_identity()
    return UserSchema.from_orm(User.get(current_identity)).dict()
