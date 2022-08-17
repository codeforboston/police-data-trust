from typing import Optional

import click
from flask import Flask
from flask.testing import FlaskClient
from flask_mail import Mail
from flask_cors import CORS
from backend.config import get_config_from_env
from backend.database import db
from backend.database import db_cli
from backend.auth import user_manager, jwt, refresh_token
from backend.schemas import spec
from backend.routes.incidents import bp as incidents_bp
from backend.routes.auth import bp as auth_bp
from backend.routes.healthcheck import bp as healthcheck_bp
from backend.utils import dev_only


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

    # @app.before_first_request
    # def _():
    #     db.create_all()

    return app


def register_extensions(app: Flask):
    db.init_app(app)
    spec.register(app)
    user_manager.init_app(app)
    jwt.init_app(app)
    Mail(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})


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
        import sys

        sys.path.append("..")

        from requirements import update

        update.run()

    @app.cli.command("scrape")
    @dev_only
    def scrape_command():
        """Scrape from public data into the database.

        This is a handy way to populate the database to start with publicly
        available data.
        """
        from backend.scraper.data_scrapers.scrape_data_sources \
             import make_all_tables
        from backend.scraper.data_scrapers.load_full_database \
             import load_full_database

        make_all_tables()
        load_full_database()

    @app.cli.command("scrape-cpdp")
    @dev_only
    def scrape_cpdp():
        """Scrape CPDP data using a Jupyter notebook."""
        import subprocess

        subprocess.call(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "backend/scraper/cpdp.ipynb",
                "--output",
                "cpdp",
            ]
        )


def register_routes(app: Flask):
    app.register_blueprint(incidents_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(healthcheck_bp)

    @app.route("/")
    def hello_world():
        return "Hello, world!"

    @app.after_request
    def after_request(response):
        response = refresh_token(response)
        return response


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

    # Client that makes testing a bit easier.

    class FlaskClientWithDefaultHeaders(FlaskClient):
        def post(self, *args, **kwargs):
            kwargs.setdefault("headers", {"Content-Type": "application/json"})
            return super().post(*args, **kwargs)

    app.test_client_class = FlaskClientWithDefaultHeaders


if __name__ == "__main__":
    app = create_app()
    app.run()
