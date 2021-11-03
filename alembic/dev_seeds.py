from backend.database.core import db
from backend.database import User, UserRole
from backend.auth import user_manager
from backend.database.models.incident import Incident
from backend.database.models.officer import Officer
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
        phone_number="(123) 456-7890"
    )
)

create_user(
    User(
        email="contributor@example.com",
        password=user_manager.hash_password("password"),
        role=UserRole.CONTRIBUTOR,
        first_name="Contributor",
        last_name="Example",
        phone_number="(123) 456-7890"
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


def create_incident(key=1, date="10-01-2019"):
    base_id = 10000000
    id = base_id + key
    incident = Incident(
        id=id,
        location=f"Test location {key}",
        description=f"Test description {key}",
        department=f"Small Police Department {key}",
        time_of_incident=f"{date} 00:00:00",
        officers=[
            Officer(
                first_name=f"TestFirstName {key}",
                last_name=f"TestLastName {key}",
            )
        ],
        use_of_force=[UseOfForce(item=f"gunshot {key}")],
        source="mpv",
    )
    exists = db.session.query(Incident).filter_by(id=id).first() is not None

    if not exists:
        incident.create()


create_incident(key=1, date="10-01-2019")
create_incident(key=2, date="11-01-2019")
create_incident(key=3, date="12-01-2019")
create_incident(key=4, date="03-15-2020")
create_incident(key=5, date="04-15-2020")
create_incident(key=6, date="08-10-2020")
create_incident(key=7, date="10-01-2020")
create_incident(key=8, date="10-15-2020")
