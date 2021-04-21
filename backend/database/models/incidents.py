"""Define the SQL classes for Users."""
from backend.database import db

import marshmallow_sqlalchemy as ma
from marshmallow_enum import EnumField
import enum


class Initial_Encounter_Enum(enum.Enum):
    Unknown = 1
    TrafficViolation = 2
    Trespassing = 3
    PotentialCrimeSuspect = 4
    Other = 5


class Victim_Weapon_Enum(enum.Enum):
    Unknown = 1
    Firearm = 2
    Blade = 3
    Blunt = 4
    NoWeapon = 5
    Other = 6


class Victim_Action_Enum(enum.Enum):
    Unknown = 1
    Speaking = 2
    NoAction = 3
    Fleeing = 4
    Approaching = 5
    Attacking = 6
    Other = 7


class Cause_Of_Death_Enum(enum.Enum):
    Unknown = 1
    BluntForce = 2
    GunShot = 3
    Choke = 4
    Other = 5


class Gender_Enum(enum.Enum):
    Unknown = 1
    Male = 2
    Female = 3
    Transgender = 4


class Race_Enum(enum.Enum):
    Unknown = 1
    White = 2
    Black_African_American = 3
    American_Indian_Alaska_Native = 4
    Asian = 5
    Native_Hawaiian_Pacific_Islander = 6


class Status_Enum(enum.Enum):
    Unknown = 1
    Unharmed = 2
    Injured = 3
    Disabled = 4
    Deceased = 5


class Incidents(db.Model):
    """The SQL dataclass for an Incident."""

    __tablename__ = "incidents"

    incident_id = db.Column(db.Integer, primary_key=True)

    # incident data
    occurrence_date = db.Column(db.DateTime)
    state_abbv = db.Column(db.Unicode(512))
    city = db.Column(db.Unicode(512))
    address_1 = db.Column(db.Unicode(512))
    address_2 = db.Column(db.Unicode(512))
    zip_code = db.Column(db.Unicode(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    reported_date = db.Column(db.DateTime)
    initial_reason_for_encounter = db.Column(db.Enum(Initial_Encounter_Enum))
    charges_involved = db.Column(db.Unicode(512))
    victim_weapon = db.Column(db.Enum(Victim_Weapon_Enum))
    victim_action = db.Column(db.Enum(Victim_Action_Enum))
    has_multimedia = db.Column(db.Boolean)
    media_URL = db.Column(db.Unicode(512))
    from_report = db.Column(db.Boolean)
    description = db.Column(db.Unicode(512))
    associated_incidents = db.Column(db.Unicode(512))

    # Death information
    death_state_abbv = db.Column(db.Unicode(512))
    death_date = db.Column(db.DateTime)
    death_city = db.Column(db.Unicode(512))
    death_address_1 = db.Column(db.Unicode(512))
    death_address_2 = db.Column(db.Unicode(512))
    death_zip_code = db.Column(db.Unicode(10))
    cause_of_death = db.Column(db.Enum(Cause_Of_Death_Enum))
    cause_of_death_description = db.Column(db.Unicode(512))

    # victim data
    first_name = db.Column(db.Unicode(512))
    last_name = db.Column(db.Unicode(512))
    age_at_incident = db.Column(db.Integer)
    gender = db.Column(db.Enum(Gender_Enum))
    race = db.Column(db.Enum(Race_Enum))
    status = db.Column(db.Enum(Status_Enum))

    # agency data
    agency_id = db.Column(db.Integer)
    agency_name = db.Column(db.Unicode(512))
    agency_state_abbv = db.Column(db.Unicode(512))
    agency_city = db.Column(db.Unicode(512))
    agency_address_1 = db.Column(db.Unicode(512))
    agency_address_2 = db.Column(db.Unicode(512))
    agency_zip_code = db.Column(db.Unicode(10))
    agency_latitude = db.Column(db.Float)
    agency_longitude = db.Column(db.Float)

    # role = db.relationship("RoleTable",

    # backref=db.backref("incidents", lazy=True))


class IncidentSchema(ma.SQLAlchemyAutoSchema):
    gender = EnumField(Gender_Enum)
    race = EnumField(Race_Enum)
    victim_weapon = EnumField(Victim_Weapon_Enum)
    victim_action = EnumField(Victim_Action_Enum)
    cause_of_death = EnumField(Cause_Of_Death_Enum)
    status = EnumField(Status_Enum)
    initial_reason_for_encounter = EnumField(Initial_Encounter_Enum)

    class Meta:
        model = Incidents
