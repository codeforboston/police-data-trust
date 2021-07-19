from flask import redirect
from flask import request
from flask import Blueprint
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from ..database import db
from ..database.models.User import User
from ..database.models.User import login_manager
from ..database.models.User import user_manager


bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
def login():
    """Login Page."""
    if request.method == "POST":
        form = request.form
        # Verify user
        if (
                form.get("password") is not None
                and form.get("email") is not None
        ):
            user = User.query.filter_by(email=form.get("email")).first()
            if user is not None and user.verify_password(
                    form.get("password")
            ):
                login_user(user, form.get("remember_me"))
                return {
                    "status": "ok",
                    "message": "Successfully logged in.",
                    "user": {"email": form.get("email")},
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


@bp.route("/logout")
@login_required
def logout():
    """Logout Page."""
    logout_user()
    return redirect("/login")


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
        if (
                form.get("password") is not None
                and form.get("email") is not None
        ):
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
                "user": {"email": form.get("email")},
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
