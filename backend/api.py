from typing import Optional

import click
from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from argon2 import PasswordHasher
from backend.config import get_config_from_env
from backend.auth import jwt, refresh_token
from backend.schemas import spec
from backend.routes.sources import bp as sources_bp
# from backend.routes.incidents import bp as incidents_bp
from backend.routes.officers import bp as officers_bp
from backend.routes.agencies import bp as agencies_bp
from backend.routes.auth import bp as auth_bp
from backend.routes.healthcheck import bp as healthcheck_bp
from backend.utils import dev_only
from backend.importer.loop import Importer
from neo4j import GraphDatabase
from neomodel import config as neo_config


def create_app(config: Optional[str] = None):
    """Create the API application."""
    app = Flask(__name__)
    config_obj = get_config_from_env(config or app.env)
    app.config.from_object(config_obj)

    with app.app_context():
        register_extensions(app)
        register_commands(app)
        register_routes(app)

    # @app.before_first_request
    # def _():
    #     db.create_all()

    # start background processor for SQS imports
    if config_obj.SCRAPER_SQS_QUEUE_NAME:
        importer = Importer(queue_name=config_obj.SCRAPER_SQS_QUEUE_NAME)
        importer.start()

    return app


def register_extensions(app: Flask):
    # Neo4j setup
    # Driver setup
    db_driver = GraphDatabase.driver(
        f'bolt://{app.config["GRAPH_NM_URI"]}',
        auth=(
            app.config["GRAPH_USER"],
            app.config["GRAPH_PASSWORD"]
        ))

    try:
        db_driver.verify_connectivity()
        app.config['DB_DRIVER'] = db_driver
        neo_config.DRIVER = app.config['DB_DRIVER']
        print("Connected to Neo4j")
    except Exception as e:
        print(f"Error connecting to Database: {e}")
        raise e

    # Neomodel setup
    neo_url = "bolt://{user}:{pw}@{uri}".format(
        user=app.config["GRAPH_USER"],
        pw=app.config["GRAPH_PASSWORD"],
        uri=app.config["GRAPH_NM_URI"]
    )
    neo_config.DATABASE_URL = neo_url

    spec.register(app)

    # Authentication
    ph = PasswordHasher()
    app.config['PASSWORD_HASHER'] = ph
    jwt.init_app(app)

    Mail(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})


def register_commands(app: Flask):
    """Register Click commands to the app instance."""

    # SQLAlchemy commands
    # app.cli.add_command(db_cli)

    # Neomodel commands
    @app.cli.command("neoload")
    @app.cli.command(
        "seed",
        context_settings=dict(
            ignore_unknown_options=True,
            allow_extra_args=True,
            help_option_names=[],
        ),
    )
    @click.pass_context
    @dev_only
    def seed(ctx: click.Context):
        """Seed the database."""
        # from alembic.dev_seeds import create_seeds
        # create_seeds()
        pass

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
        from backend.scraper.data_scrapers.scrape_data_sources import (
            make_all_tables,
        )
        from backend.scraper.data_scrapers.load_full_database import (
            load_full_database,
        )

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
    app.register_blueprint(sources_bp)
    # app.register_blueprint(incidents_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(healthcheck_bp)
    app.register_blueprint(officers_bp, url_prefix="/api/v1/officers")
    app.register_blueprint(agencies_bp)

    @app.route("/")
    def hello_world():
        return "Hello, world!"

    @app.after_request
    def after_request(response):
        response = refresh_token(response)
        return response


if __name__ == "__main__":
    app = create_app()
    app.run()
