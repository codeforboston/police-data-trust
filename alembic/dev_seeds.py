from backend.database.core import db
from backend.database import User, UserRole
from backend.auth import user_manager
from backend.database.models.partner import Partner, PartnerMember, MemberRole
from random import choice
from datetime import datetime


def create_user(user):
    user_exists = (
        db.session.query(User).filter_by(email=user.email).first() is not None
    )

    if not user_exists:
        user.create()


def create_partner(partner: Partner) -> Partner:
    partner_exists = (
        db.session.query(Partner).filter_by(id=partner.id).first() is not None
    )

    if not partner_exists:
        partner.create()

    return partner


""" def create_incident(key=1, date="10-01-2019", lon=84, lat=34, partner_id=1):
    incident = Incident(
        source_id=partner_id,
        privacy_filter=choice([PrivacyStatus.PUBLIC, PrivacyStatus.PRIVATE]),
        date_record_created=f"{date} 00:00:00",
        time_of_incident=f"{date} 00:00:00",
        time_confidence="1",
        complaint_date=f"{date} 00:00:00",
        closed_date=f"{date} 00:00:00",
        location=f"Test location {key}",
        longitude=lon,
        latitude=lat,
        description=f"Test description {key}",
        stop_type="Traffic",
        call_type="Emergency",
        has_attachments=False,
        from_report=True,
        was_victim_arrested=True,
        arrest_id=1,
        criminal_case_brought=True,
        case_id=1,
        perpetrators=[
            Perpetrator(
                first_name=f"TestFirstName {key}",
                last_name=f"TestLastName {key}",
            )
        ],
        use_of_force=[UseOfForce(item=f"gunshot {key}")],
    )
    exists = db.session.query(Incident).filter_by(id=key).first() is not None

    if not exists:
        incident.create() """


def create_seeds():
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
    partner = create_partner(
        Partner(
            name="Mapping Police Violence",
            url="https://mappingpoliceviolence.us",
            contact_email="info@campaignzero.org",
            member_association=[
                PartnerMember(
                    user_id=1,
                    role=MemberRole.MEMBER,
                    date_joined=datetime.now(),
                    is_active=True,
                )
            ],
        )
    )
    # Create Complaints here


# create_seeds()
