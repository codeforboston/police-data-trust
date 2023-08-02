from backend.database.core import db
from backend.database import User, UserRole
from backend.auth import user_manager
from backend.database.models.incident import Incident
from backend.database.models.perpetrator import Perpetrator
from backend.database.models.organization import Organization
from backend.database.models.use_of_force import UseOfForce


def create_user(user):
    user_exists = (
        db.session.query(User).filter_by(email=user.email).first() is not None
    )

    if not user_exists:
        user.create()


create_user(
    User(
        email="test@example.com",
        password=user_manager.hash_password("password"),
        role=UserRole.PUBLIC,
        first_name="Test",
        last_name="Example",
        phone_number="(123) 456-7890",
    )
)

create_user(
    User(
        email="contributor@example.com",
        password=user_manager.hash_password("password"),
        role=UserRole.CONTRIBUTOR,
        first_name="Contributor",
        last_name="Example",
        phone_number="(123) 456-7890",
    )
)

create_user(
    User(
        email="admin@example.com",
        password=user_manager.hash_password("password"),
        role=UserRole.ADMIN,
        first_name="Admin",
        last_name="Example",
        phone_number="(012) 345-6789",
    )
)

create_user(
    User(
        email="passport@example.com",
        password=user_manager.hash_password("password"),
        role=UserRole.PASSPORT,
        first_name="Passport",
        last_name="Example",
        phone_number="(012) 345-6789",
    )
)


def create_organization(organization):
    organization_exists = (
        db.session.query(Organization).filter_by(id=organization.id).first() is not None
    )

    if not organization_exists:
        organization.create()


create_organization(
    Organization(
        id="mpv",
        name="Mapping Police Violence",
        url="https://mappingpoliceviolence.us",
        contact_email="info@campaignzero.org"
    )
)


def create_incident(key=1, date="10-01-2019", lon=84, lat=34):
    base_id = 10000000
    id = base_id + key
    mpv = db.session.query(Organization).filter_by(
        name="Mapping Police Violence").first()
    incident = Incident(
        id=id,
        organization=mpv,
        location=f"Test location {key}",
        longitude=lon,
        latitude=lat,
        description=f"Test description {key}",
        time_of_incident=f"{date} 00:00:00",
        perpetrators=[
            Perpetrator(
                first_name=f"TestFirstName {key}",
                last_name=f"TestLastName {key}",
            )
        ],
        use_of_force=[UseOfForce(item=f"gunshot {key}")]
    )
    exists = db.session.query(Incident).filter_by(id=id).first() is not None

    if not exists:
        incident.create()


create_incident(key=1, date="10-01-2019", lon=-84.362576, lat=33.7589748)
create_incident(key=2, date="11-01-2019", lon=-118.1861128, lat=33.76702)
create_incident(key=3, date="12-01-2019", lon=-117.8827321, lat=33.800308)
create_incident(key=4, date="03-15-2020", lon=-118.1690197, lat=33.8338271)
create_incident(key=5, date="04-15-2020", lon=-83.9007382, lat=33.8389977)
create_incident(key=6, date="08-10-2020", lon=-84.2687574, lat=33.9009798)
create_incident(key=7, date="10-01-2020", lon=-118.40853, lat=33.9415889)
create_incident(key=8, date="10-15-2020", lon=-84.032149, lat=33.967774)
