from typing import Optional

import click
from flask import Flask
from flask import redirect
from flask import request
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from .config import get_config_from_env
from .database import db, db_cli, migrate
from .database.models.users import Users, login_manager, user_manager
from .routes.incidents import incident_routes
from .utils import dev_only


def create_app(config: Optional[str] = None):
    """Create the API application."""
    app = Flask(__name__)
    config_obj = get_config_from_env(config or app.env)
    app.config.from_object(config_obj)

    with app.app_context():
        register_extensions(app)
        register_commands(app)
        register_routes(app)
        register_misc(app)

    return app


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)
    user_manager.init_app(app)


def register_commands(app: Flask):
    """Register Click commands to the app instance."""

    app.cli.add_command(db_cli)

    @app.cli.command(
        "pip-compile",
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
            help_option_names=[],
        ),
    )
    @click.pass_context
    @dev_only
    def pip_compile(ctx: click.Context):
        """Compile the .in files in /requirements.

        This command is for development purposes only.
        """
        import subprocess

        if len(ctx.args) == 1 and ctx.args[0] == "--help":
            subprocess.call(["pip-compile", "--help"])
        else:
            req_files = [
                "requirements/dev_unix.in",
                "requirements/dev_windows.in",
                "requirements/prod.in",
                "requirements/docs.in",
            ]
            for filename in req_files:
                subprocess.call(["pip-compile", filename, *ctx.args])

    @app.cli.command("scrape")
    def scrape_command():
        """Scrape from public data into the database.

        This is a handy way to populate the database to start with publicly
        available data.
        """
        pass


def register_routes(app: Flask):
    app.register_blueprint(incident_routes)

    @app.route("/")
    def hello_world():
        return "Hello, world!"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    @app.route("/login", methods=["POST"])
    def login():
        """Login Page."""
        if request.method == "POST":
            form = request.form
            # Verify user
            if (
                form.get("password") is not None
                and form.get("email") is not None
            ):
                user = Users.query.filter_by(email=form.get("email")).first()
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

    @app.route("/logout")
    @login_required
    def logout():
        """Logout Page."""
        logout_user()
        return redirect("/login")

    @app.route("/register", methods=["POST"])
    def register():
        if request.method == "POST":
            form = request.form
            # Check to see if user already exists
            user = Users.query.filter_by(email=form.get("email")).first()
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
                user = Users(
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


def register_misc(app: Flask):
    """For things that don't neatly fit into the other "register" functions."""

    @app.shell_context_processor
    def make_shell_context():
        """This function makes some objects available in the Flask shell without
        the need to manually declare an import. This is just a convenience for
        using the Flask shell.
        """
        from flask import current_app as app

        from .database import db  # noqa: F401

        client = app.test_client()
        return locals()


if __name__ == "__main__":
    app = create_app()
    app.run()
