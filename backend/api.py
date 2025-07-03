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
from backend.database import MODEL_CLASSES
from neo4j import GraphDatabase
from neomodel import db, install_labels, config as neo_config

mail = Mail()


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

    mail.init_app(app)
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

    @app.cli.command("neo4j-migrate")
    def neo4j_migrate():
        """Install Neomodel labels/indexes and run migrations."""
        click.echo("Running Neo4j migrations...")
        install_labels(MODEL_CLASSES)
        index_db()


def register_routes(app: Flask):
    app.register_blueprint(sources_bp)
    # app.register_blueprint(incidents_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(healthcheck_bp)
    app.register_blueprint(officers_bp)
    app.register_blueprint(agencies_bp)

    @app.route("/")
    def hello_world():
        return "Hello, world!"

    @app.after_request
    def after_request(response):
        response = refresh_token(response)
        return response


def index_db():
    """Index the database."""
    db.cypher_query("CREATE FULLTEXT INDEX officerNames IF NOT EXISTS FOR (n:Officer) ON EACH [n.first_name, n.last_name, n.middle_name, n.suffix]")
    db.cypher_query("CREATE FULLTEXT INDEX allegationTypes IF NOT EXISTS FOR (a:Allegation) ON EACH [a.type]")
    db.cypher_query("CREATE FULLTEXT INDEX complaintCategories IF NOT EXISTS FOR (c:Complaint) ON EACH [c.category]")
    db.cypher_query("CREATE FULLTEXT INDEX officerRanks IF NOT EXISTS FOR ()-[r:MEMBER_OF_UNIT]->() ON EACH [r.highest_rank]")
    db.cypher_query("CREATE FULLTEXT INDEX cityNames IF NOT EXISTS FOR (c:CityNode) ON EACH [c.name]")
    db.cypher_query("CREATE FULLTEXT INDEX countyNames IF NOT EXISTS FOR (c:CountyNode) ON EACH [c.name]")



if __name__ == "__main__":
    app = create_app()
    app.run()
