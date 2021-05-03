from flask import Flask, redirect, render_template, session, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_user import current_user, login_required, roles_required, UserManager
from flask_migrate import Migrate
import click
from typing import Optional
from .routes.incidents import incident_routes
from .database.models.users import Users, login_manager, user_manager
from .config import get_config_from_env
from .database import db
from .database import db_cli
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
    migrate = Migrate(app, db)
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
        form = request.form
        if form['password'] != '' and form['email'] != '':
            print('EMAIL: ' + form['email'])
            user = Users.query.filter_by(email=form['email']).first()
            if(user is not None and user.verify_password(user_manager.hash_password(form['password']))):
                login_user(user, form['remember_me'])
                return {"status":"ok", "message": "Successfully logged in.", "user": { "email": form['email']}}
            else:
                return {"status":"ok", "message": "Error. Username or Password invalid."}
        missing_fields = ""
        for field in form:
            if field == '':
                missing_fields= missing_fields + ", " + field
        return {"status":"ok", "message": "Failed to log in. Please include the following fields: " + missing_fields}

    @app.route("/logout")
    @login_required
    def logout():
        """Logout Page."""
        logout_user()
        return redirect("/login")

    @app.route("/register", methods=["POST"])
    def register():
        form = request.form
        if form['username'] != '' and form['password'] != '' and form['email'] != '':
            user = Users(email=form['email'], username=form['username'], password=user_manager.hash_password(form['password']))
            db.session.add(user)
            db.session.commit()
            return {"status":"ok", "message": "Successfully registered.", "user": { "email": form['email'], "username": form['username']}}
        missing_fields = ""
        for field in form:
            if field == '':
                missing_fields= missing_fields + ", " + field


def register_misc(app: Flask):
    """For things that don't neatly fit into the other "register" functions."""

    # @app.before_first_request
    # def setup_application() -> None:
    #     """Do initial setup of application."""
    #     db.create_all()

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
