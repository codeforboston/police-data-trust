from backend.database.core import db
from backend.database import User, UserRole
from backend.auth import user_manager
from backend.database.models.partner import Partner, PartnerMember, MemberRole
from backend.database.models.officer import Officer
from backend.database.models.agency import Agency, Unit
from backend.database.models.complaint import Complaint, RecordType
from random import choice
from datetime import datetime


def create_user(user):
    user_exists = (
        User.nodes.get_or_none(email=user.email) is not None
    )

    if not user_exists:
        user.save()


def create_partner(partner: Partner) -> Partner:
    partner_exists = (
        Partner.nodes.get_or_none(name=partner.name) is not None
    )

    if not partner_exists:
        partner.save()
    return partner


def create_officer(officer: Officer, unit_uid) -> Officer:
    officer_exists = (
        # Officer.nodes.get_or_none() is not None
        # TODO
    )

    if not officer_exists:
        officer.save()
    return officer


def create_agency(agency: Agency) -> Agency:
    agency_exists = (
        Agency.nodes.get_or_none(name=agency.name) is not None
    )

    if not agency_exists:
        agency.save()
    return agency


def create_unit(unit: Unit, agency_uid) -> Unit:
    agency = Agency.nodes.get_or_none(uid=agency_uid)

    if agency is not None:
        unit_exists = (
            agency.units.search(name=unit.name).first() is not None
        )
        if not unit_exists:
            unit.save()
            unit.agency.connect(agency).save()
    return unit


def create_complaint(
        partner_uid,
        complaint,
        allegations=None,
        location=None):
    partner = Partner.nodes.get_or_none(uid=partner_uid)

    if partner is not None:
        complaint.save()
        complaint.source.connect(
            partner,
            {'record_type': RecordType.personal}
        ).save()

        if allegations is not None:
            for allegation in allegations:
                allegation.save()
                complaint.allegations.connect(allegation).save()

        if location is not None:
            location.save()
            complaint.location.connect(location).save()


def create_seeds():
    create_user(
        User(
            email="test@example.com",
            password=user_manager.hash_password("password"),
            role=UserRole.PUBLIC.value,
            first_name="Test",
            last_name="Example",
            phone_number="(123) 456-7890",
        )
    )
    create_user(
        User(
            email="contributor@example.com",
            password=user_manager.hash_password("password"),
            role=UserRole.CONTRIBUTOR.value,
            first_name="Contributor",
            last_name="Example",
            phone_number="(123) 456-7890",
        )
    )
    create_user(
        User(
            email="admin@example.com",
            password=user_manager.hash_password("password"),
            role=UserRole.ADMIN.value,
            first_name="Admin",
            last_name="Example",
            phone_number="(012) 345-6789",
        )
    )
    create_user(
        User(
            email="passport@example.com",
            password=user_manager.hash_password("password"),
            role=UserRole.PASSPORT.value,
            first_name="Passport",
            last_name="Example",
            phone_number="(012) 345-6789",
        )
    )
    partner = create_partner(
        Partner(
            name="Mapping Police Violence",
            url="https://mappingpoliceviolence.us",
            contact_email="info@campaignzero.org"
        )
    )


create_seeds()
