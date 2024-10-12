import pytest
from neo4j import GraphDatabase
from neomodel import config, db
from backend.api import create_app
from backend.config import TestingConfig
from backend.database import User, UserRole
from backend.database import (
    Partner,
    PartnerMember,
    MemberRole,
    Jurisdiction,
    Agency,
    Officer,
)
from datetime import datetime

example_email = "test@email.com"
admin_email = "admin@email.com"
p_admin_email = "admin@partner.com"
contributor_email = "contributor@email.com"
example_password = "my_password"


@pytest.fixture(scope="session")
def test_db_driver():
    cfg = TestingConfig()

    db_driver = GraphDatabase.driver(
        f"bolt://{cfg.GRAPH_URI}",
        auth=(
            cfg.GRAPH_USER,
            cfg.GRAPH_PASSWORD
        ))
    test_db_url = "bolt://{user}:{pw}@{url}:{port}".format(
        user=cfg.GRAPH_USER,
        pw=cfg.GRAPH_PASSWORD,
        url=cfg.GRAPH_URI,
        port=cfg.GRAPH_PORT
    )
    config.DATABASE_URL = test_db_url

    yield db_driver
    db_driver.close()


@pytest.fixture
def db_session(test_db_driver):
    with test_db_driver.session() as session:
        yield session


@pytest.fixture(scope="session")
def app(test_db_driver):
    app = create_app(config="testing")
    # The app should be ready! Provide the app instance here.
    # Use the app context to make testing easier.
    # The main time where providing app context can cause false positives is
    # when testing CLI commands that don't pass the app context.
    with app.app_context():
        yield app


# This function must be called for every new test node created
def add_test_label(node):
    query = "MATCH (n) WHERE id(n) = $node_id SET n:TestData"
    params = {'node_id': node.id}
    db.cypher_query(query, params)


# This function must be called for every new test relationship created
def add_test_property_to_rel(start_node, rel_type, end_node):
    query = f"""
    MATCH (a)-[r:{rel_type}]-(b)
    WHERE id(a) = $start_id AND id(b) = $end_id
    SET r.test_data = true
    """
    params = {
        'start_id': start_node.id,
        'end_id': end_node.id
    }
    db.cypher_query(query, params)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_data():
    yield
    # After all tests have run, clean up the test data
    db.cypher_query('MATCH ()-[r]-() WHERE r.test_data = true DELETE r')
    db.cypher_query('MATCH (n:TestData) DETACH DELETE n')


@pytest.fixture
def example_user():
    user = User(
        email=example_email,
        password_hash=User.hash_password(example_password),
        role=UserRole.PUBLIC.value,
        first_name="first",
        last_name="last",
        phone_number="(012) 345-6789",
    ).save()
    add_test_label(user)
    yield user


@pytest.fixture
def example_partner():
    partner = Partner(
        name="Example Partner",
        url="www.example.com",
        contact_email=contributor_email
    ).save()
    add_test_label(partner)
    yield partner


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
    add_test_label(agency)
    yield agency


@pytest.fixture
def example_officer():
    officer = Officer(
        first_name="John",
        last_name="Doe",
    ).save()
    add_test_label(officer)
    yield officer


@pytest.fixture  # type: ignore
def example_partner_member(example_user: User):
    # Create partner
    partner = Partner(
        name="Example Partner Member",
        url="www.example.com",
        contact_email="example_test@example.ca",
        member_association=[
            PartnerMember(
                user_id=example_user.id,
                role=MemberRole.MEMBER.value,
                date_joined=datetime.now(),
                is_active=True,
            )
        ],
    ).save()
    add_test_label(partner)

    # Create relationship
    partner.members.conect(
        example_user,
        {
            'role': MemberRole.MEMBER.value,
            'date_joined': datetime.now(),
            'is_active': True
        }
    )
    add_test_property_to_rel(partner, 'HAS_MEMBER', example_user)
    yield partner


@pytest.fixture  # type: ignore
def example_partner_publisher(example_user: User):
    partner = Partner(
        name="Example Partner Member",
        url="www.example.com",
        contact_email="example_test@example.ca"
    ).save()
    add_test_label(partner)
    
    # Create relationship
    partner.members.connect(
        example_user,
        {
            'role': MemberRole.PUBLISHER.value,
            'date_joined': datetime.now(),
            'is_active': True
        }
    )
    add_test_property_to_rel(partner, 'HAS_MEMBER', example_user)


@pytest.fixture  # type: ignore
def example_complaints(
    example_partner: Partner,
    example_partner_publisher: User,
) :
    complaints = []

    yield complaints


@pytest.fixture  # type: ignore
def example_complaints_private_public(
    example_partner: Partner
):
    complaints = [
    ]

    return complaints


@pytest.fixture
def admin_user():
    user = User(
        email=admin_email,
        password_hash=User.hash_password(example_password),
        role=UserRole.ADMIN.value,
        first_name="admin",
        last_name="last",
    ).save()
    add_test_label(user)
    yield user


@pytest.fixture
def partner_admin(example_partner):
    user = User(
        email=p_admin_email,
        password_hash=User.hash_password(example_password),
        role=UserRole.CONTRIBUTOR.value,
        first_name="contributor",
        last_name="last",
        phone_number="(012) 345-6789",
    ).save()
    add_test_label(user)

    example_partner.members.connect(
        user,
        {
            'role': MemberRole.ADMIN.value,
            'date_joined': datetime.now(),
            'is_active': True
        }
    )
    add_test_property_to_rel(example_partner, 'HAS_MEMBER', user)
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
def p_admin_access_token(client, partner_admin):
    res = client.post(
        "api/v1/auth/login",
        json={
            "email": p_admin_email,
            "password": example_password,
        },
    )
    assert res.status_code == 200
    return res.json["access_token"]


@pytest.fixture
def contributor_access_token(client, partner_publisher):
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
