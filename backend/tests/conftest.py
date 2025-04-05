import pytest
from neo4j import GraphDatabase
from neomodel import db
from backend.api import create_app
from backend.config import TestingConfig
from backend.database import User, UserRole
from backend.database import (
    Source,
    MemberRole,
    Jurisdiction,
    Agency,
    Officer,
)
from datetime import datetime

example_email = "test@email.com"
admin_email = "admin@email.com"
member_email = "member@email.com"
contributor_email = "contributor@email.com"
s_admin_email = "admin@source.com"
example_password = "my_password"


@pytest.fixture(scope="session")
def test_db_driver():
    cfg = TestingConfig()

    uri = f"bolt://{cfg.GRAPH_NM_URI}"
    print(f"Driver URI: {uri}")
    test_driver = GraphDatabase.driver(
        uri,
        auth=(
            cfg.GRAPH_USER,
            cfg.GRAPH_PASSWORD
        ))
    print(test_driver.get_server_info().address)
    test_driver.verify_connectivity()
    yield test_driver
    test_driver.close()


@pytest.fixture
def db_session(test_db_driver):
    with test_db_driver.session() as session:
        yield session


@pytest.fixture(scope="session")
def app():
    app = create_app(config="testing")
    # The app should be ready! Provide the app instance here.
    # Use the app context to make testing easier.
    # The main time where providing app context can cause false positives is
    # when testing CLI commands that don't pass the app context.
    print("App created.")
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


# This function should be called for every new test node created
def add_test_property(node):
    query = "MATCH (n) WHERE elementId(n) = $node_id SET n.is_test_data = true"
    params = {'node_id': node.element_id}
    db.cypher_query(query, params)


# This function must be called for every new test relationship created
def add_test_property_to_rel(start_node, rel_type, end_node):
    query = f"""
    MATCH (a)-[r:{rel_type}]-(b)
    WHERE elementId(a) = $start_id AND elementId(b) = $end_id
    SET r.test_data = true
    """
    params = {
        'start_id': start_node.element_id,
        'end_id': end_node.element_id
    }
    db.cypher_query(query, params)


def is_test_database():
    query = "MATCH (n:TestMarker {name: 'TEST_DATABASE'}) RETURN n"
    results, _ = db.cypher_query(query)
    return bool(results)


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_data():
    yield
    # Check if this is the test database before performing any deletion
    if is_test_database():
        # Delete all nodes except the TestMarker node
        db.cypher_query(
            'MATCH ()-[r]-() WHERE NOT EXISTS((:TestMarker)-[r]-()) DELETE r')
        db.cypher_query('MATCH (n) WHERE NOT n:TestMarker DETACH DELETE n')


@pytest.fixture
def example_user():
    user = User(
        primary_email=example_email,
        password_hash=User.hash_password(example_password),
        role=UserRole.PUBLIC.value,
        first_name="first",
        last_name="last",
        phone_number="(012) 345-6789",
    ).save()
    add_test_property(user)
    yield user


@pytest.fixture
def example_source(scope="session"):
    source = Source(
        name="Example Source",
        url="www.example.com",
        contact_email=contributor_email
    ).save()
    add_test_property(source)
    yield source


@pytest.fixture
def example_agency():
    agency = Agency(
        name="Example Agency",
        website_url="www.example.com",
        hq_city="New York",
        hq_address="123 Main St",
        hq_zip="10001",
        jurisdiction=Jurisdiction.MUNICIPAL.value
    ).save()
    add_test_property(agency)
    yield agency


@pytest.fixture
def example_officer():
    officer = Officer(
        first_name="John",
        last_name="Doe",
    ).save()
    add_test_property(officer)
    yield officer


@pytest.fixture  # type: ignore
def example_source_member(example_source):
    member = User(
        primary_email=member_email,
        password_hash=User.hash_password(example_password),
        role=UserRole.PUBLIC.value,
        first_name="member",
        last_name="last",
        phone_number="(012) 345-6789",
    ).save()
    add_test_property(member)
    # Create source
    source = Source(
        name="Example Source Member",
        url="www.example.com",
        contact_email="example_test@example.ca"
    ).save()
    add_test_property(source)

    # Create relationship
    source.members.conect(
        member,
        {
            'role': MemberRole.MEMBER.value,
            'date_joined': datetime.now(),
            'is_active': True
        }
    )
    add_test_property_to_rel(source, 'HAS_MEMBER', member)
    yield member


@pytest.fixture  # type: ignore
def example_contributor():
    contributor = User(
        primary_email=contributor_email,
        password_hash=User.hash_password(example_password),
        role=UserRole.CONTRIBUTOR.value,
        first_name="contributor",
        last_name="last",
        phone_number="(012) 345-6789",
    ).save()
    add_test_property(contributor)

    source = Source(
        name="Example Contributor",
        url="www.example.com",
        contact_email="example_test@example.ca"
    ).save()
    add_test_property(source)

    # Create relationship
    source.members.connect(
        contributor,
        {
            'role': MemberRole.PUBLISHER.value,
            'date_joined': datetime.now(),
            'is_active': True
        }
    ).save()
    add_test_property_to_rel(source, 'HAS_MEMBER', contributor)
    return contributor


@pytest.fixture  # type: ignore
def example_complaints(
    example_source: Source,
    example_contributor: User,
) :
    complaints = []

    yield complaints


@pytest.fixture  # type: ignore
def example_complaints_private_public(
    example_source: Source
):
    complaints = [
    ]

    return complaints


@pytest.fixture
def admin_user():
    user = User(
        primary_email=admin_email,
        password_hash=User.hash_password(example_password),
        role=UserRole.ADMIN.value,
        first_name="admin",
        last_name="last",
    ).save()
    add_test_property(user)
    yield user


@pytest.fixture
def source_admin(example_source):
    user = User(
        primary_email=s_admin_email,
        password_hash=User.hash_password(example_password),
        role=UserRole.CONTRIBUTOR.value,
        first_name="contributor",
        last_name="last",
        phone_number="(012) 345-6789",
    ).save()
    add_test_property(user)

    example_source.members.connect(
        user,
        {
            'role': MemberRole.ADMIN.value,
            'date_joined': datetime.now(),
            'is_active': True
        }
    )
    add_test_property_to_rel(example_source, 'HAS_MEMBER', user)
    yield user


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
def p_admin_access_token(client, source_admin):
    res = client.post(
        "api/v1/auth/login",
        json={
            "email": s_admin_email,
            "password": example_password,
        },
    )
    assert res.status_code == 200
    return res.json["access_token"]


@pytest.fixture
def contributor_access_token(client, example_contributor):
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
