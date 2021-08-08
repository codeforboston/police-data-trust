import pytest

import psycopg2.errors
from pytest_postgresql.janitor import DatabaseJanitor

from backend.api import create_app
from backend.config import TestingConfig
from backend.database import db


@pytest.fixture(scope="session")
def database():
    cfg = TestingConfig()
    janitor = DatabaseJanitor(
        cfg.POSTGRES_USER,
        cfg.POSTGRES_HOST,
        cfg.POSTGRES_PORT,
        cfg.POSTGRES_DB,
        9.6,
        cfg.POSTGRES_PASSWORD,
    )

    try:
        janitor.init()
    except psycopg2.errors.lookup("42P04"):
        pass

    yield

    janitor.drop()


@pytest.fixture(scope="session")
def app(database):
    app = create_app(config="testing")
    # The app should be ready! Provide the app instance here.
    # Use the app context to make testing easier.
    # The main time where providing app context can cause false positives is
    # when testing CLI commands that don't pass the app context.
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def cli_runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def _db(app):
    """See this:

    https://github.com/jeancochrane/pytest-flask-sqlalchemy

    Basically, this '_db' fixture is required for the above extension to work.
    We use this extension to allow for easy testing of the database.
    """
    db.create_all()
    yield db
