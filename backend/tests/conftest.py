import pytest
from backend.api import create_app
from backend.config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig())
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
