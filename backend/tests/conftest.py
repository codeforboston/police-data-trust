import psycopg2.errors
import pytest
from backend.api import create_app
from backend.auth import user_manager
from backend.config import TestingConfig
from backend.database import User, UserRole, db, Partner, partner_user
from backend.database.models._assoc_tables import MemberRole
from datetime import datetime
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy import insert

example_email = "test@email.com"
admin_email = "admin@email.com"
contributor_email = "contributor@email.com"
example_password = "my_password"


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
def example_partner(db_session):
    partner = Partner(
        name="Example Partner",
        url="www.example.com",
        contact_email=contributor_email,
    )
    db_session.add(partner)
    db_session.commit()
    return partner


@pytest.fixture
def example_user(db_session):
    user = User(
        email=example_email,
        password=user_manager.hash_password(example_password),
        role=UserRole.PUBLIC,
        first_name="first",
        last_name="last",
        phone_number="(012) 345-6789",
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def admin_user(db_session):
    user = User(
        email=admin_email,
        password=user_manager.hash_password(example_password),
        role=UserRole.ADMIN,
        first_name="admin",
        last_name="last",
    )
    db_session.add(user)
    db_session.commit()

    return user


@pytest.fixture
def contributor_user(db_session, example_partner):
    user = User(
        email=contributor_email,
        password=user_manager.hash_password(example_password),
        role=UserRole.CONTRIBUTOR,
        first_name="contributor",
        last_name="last"
    )
    db_session.add(user)
    db_session.commit()
    insert_statement = insert(partner_user).values(
        partner_id=example_partner.id, user_id=user.id,
        role=MemberRole.PUBLISHER, joined_at=datetime.now(),
        is_active=True, is_admin=False
    )
    db_session.execute(insert_statement)
    db_session.commit()

    return user


@pytest.fixture
def access_token(client, example_user):
    res = client.post(
        "api/v1/auth/login",
        json={
            "email": example_email,
            "password": example_password,
        },
    )
    assert res.status_code == 200
    return res.json["access_token"]


@pytest.fixture
def contributor_access_token(client, contributor_user):
    res = client.post(
        "api/v1/auth/login",
        json={
            "email": contributor_email,
            "password": example_password,
        },
    )
    assert res.status_code == 200
    return res.json["access_token"]


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
