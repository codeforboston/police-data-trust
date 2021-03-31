import pytest
from backend.api import create_app


@pytest.fixture
def app():
    app = create_app(config="testing")
    cli_runner = app.test_cli_runner()
    cli_runner.invoke(app.cli, ["database", "create"])
    cli_runner.invoke(app.cli, ["database", "init"])
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def cli_runner(app):
    return app.test_cli_runner()
