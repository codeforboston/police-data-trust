import pytest
from backend.api import create_app


@pytest.fixture
def app():
    app = create_app(config="testing")

    # Create the test database.
    # Note that it's very hard to get the test db to teardown after tests.
    # It's much easier to delete and recreate at the start of a test, which is
    # what we do below.
    cli_runner = app.test_cli_runner()
    cli_runner.invoke(app.cli, ["psql", "create", "--overwrite"])
    cli_runner.invoke(app.cli, ["psql", "init"])

    # The app should be ready! Provide the app instance here.
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
    from backend.database import db

    yield db
