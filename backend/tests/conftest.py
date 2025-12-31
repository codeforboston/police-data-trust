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
    Unit,
    Officer,
    StateID,
    Complaint,
    RecordType,
    Investigation,
    Allegation,
    Penalty,
    Location,
    EmailContact,
    SocialMediaContact
)
from datetime import datetime, date

example_email = "test@email.com"
admin_email = "admin@email.com"
member_email = "member@email.com"
contributor_email = "contributor@email.com"
s_admin_email = "admin@source.com"
example_password = "my_password"


@pytest.fixture(scope="session")
def cli_runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="session", autouse=True)
def migrate_neo4j_schema(app, cli_runner):
    """
    Run our 'neo4j-migrate' CLI once at the start of the test session
    so that all indexes & constraints exist in the test database.
    """
    result = cli_runner.invoke(args=["neo4j-migrate"])
    assert result.exit_code == 0, f"Migration failed:\n{result.output}"


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


@pytest.fixture(autouse=True)
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
    user = User.create_user(
        email=example_email,
        password=example_password,
        role=UserRole.PUBLIC.value,
        first_name="first",
        last_name="last",
        phone_number="(012) 345-6789",
    )
    yield user


@pytest.fixture
def example_source():
    source = Source(
        name="Example Source",
        url="www.example.com",
    ).save()
    email_contact = EmailContact.get_or_create(contributor_email)
    source.primary_email.connect(email_contact)
    social_contact = SocialMediaContact().save()
    source.social_media.connect(social_contact)
    yield source


@pytest.fixture
def example_agency(example_source):
    agency = Agency(
        name="Example Agency",
        website_url="www.example.com",
        hq_city="New York",
        hq_address="123 Main St",
        hq_zip="10001",
        jurisdiction=Jurisdiction.MUNICIPAL.value
    ).save()
    agency.citations.connect(example_source, {
        'date': datetime.now(),
    })
    yield agency


@pytest.fixture
def example_unit(example_agency, example_officer, example_source):
    agency = example_agency
    officer = example_officer
    source = example_source

    unit = Unit(
        name="Precinct 1"
    ).save()

    # Create relationships
    unit.agency.connect(agency)
    unit.citations.connect(source, {
        'date': datetime.now(),
    })
    unit.officers.connect(
        officer,
        {
            'badge_number': '61025'
        }
    )
    yield unit


@pytest.fixture
def example_officer(example_source):
    officer = Officer(
        first_name="John",
        last_name="Doe",
    ).save()
    StateID(
        id_name="Tax ID Number",
        state="NY",
        value="958938"
    ).save().officer.connect(officer)
    officer.citations.connect(
        example_source,
        {
            'date': datetime.now(),
        }
    )
    yield officer


@pytest.fixture  # type: ignore
def example_source_member(example_source):
    member = User.create_user(
        email=member_email,
        password=example_password,
        role=UserRole.PUBLIC.value,
        first_name="member",
        last_name="last",
        phone_number="(012) 345-6789",
    )
    # Create source
    source = Source(
        name="Example Source Member",
        url="www.example.com",
        contact_email="example_test@example.ca"
    ).save()

    # Create relationship
    source.members.connect(
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
def example_contributor(example_source):
    contributor = User.create_user(
        email=contributor_email,
        password=example_password,
        role=UserRole.CONTRIBUTOR.value,
        first_name="contributor",
        last_name="last",
        phone_number="(012) 345-6789",
    )
    # Create relationship
    example_source.members.connect(
        contributor,
        {
            'role': MemberRole.PUBLISHER.value,
            'date_joined': datetime.now(),
            'is_active': True
        }
    ).save()
    return contributor


@pytest.fixture  # type: ignore
def example_complaint(
    db_session,
    example_source: Source,
    example_contributor: User,
    example_officer: Officer,
) :
    source_rel = {
        "record_type": RecordType.government.value,
        "reporting_agency": "New York City Civilian Review Board",
        "reporting_agency_url": "https://www.nyc.gov/site/crb/index.page",
        "reporting_agency_email": "example@example.com",
        "date_published": datetime.now()
    }
    complaint = Complaint(
        record_id="C123456",
        category="Excessive Force",
        incident_date=date.today(),
        received_date=date.today(),
        closed_date=date.today(),
        reason_for_contact="Complaint about officer conduct",
        outcome_of_contact="Resolved",
    ).save()
    location = Location(
        location_type="Incident Location",
        location_description="Main Street",
        address="123 Main St",
        city="New York",
        state="NY",
        zip="10001",
        administrative_area="1st Precinct",
        administrative_area_type="Precinct"
    ).save()
    allegation = Allegation(
        allegation="Officer used unnecessary force during arrest",
        type="Excessive Force",
        subtype="Physical Force",
        recommended_finding="Sustained",
        finding="Sustained",
        recommended_outcome="Disciplinary Action",
        outcome="Disciplinary Action",
    ).save()
    penalty = Penalty(
        penalty="Suspension",
        date_assessed=date.today(),
        crb_plea="No contest",
        crb_disposition="Sustained",
        crb_case_status="Closed",
        agency_disposition="Sustained"
    ).save()
    investigation = Investigation(
        start_date=date.today(),
        end_date=date.today(),
    ).save()

    allegation.accused.connect(example_officer)
    allegation.complaint.connect(complaint)
    penalty.officer.connect(example_officer)
    penalty.complaint.connect(complaint)
    investigation.complaint.connect(complaint)
    complaint.location.connect(location)
    complaint.source_org.connect(example_source, source_rel)

    yield complaint


@pytest.fixture  # type: ignore
def example_complaints_private_public(
    example_source: Source
):
    complaints = [
    ]

    return complaints


@pytest.fixture
def admin_user():
    user = User.create_user(
        email=admin_email,
        password=example_password,
        role=UserRole.ADMIN.value,
        first_name="admin",
        last_name="last",
        phone_number="(012) 345-6789",
    )
    yield user


@pytest.fixture
def source_admin(example_source):
    user = User.create_user(
        email=s_admin_email,
        password=example_password,
        role=UserRole.CONTRIBUTOR.value,
        first_name="contributor",
        last_name="last",
        phone_number="(012) 345-6789",
    )
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
