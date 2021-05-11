"""Define the SQL classes for Users."""
from backend.database import db

import marshmallow_sqlalchemy as ma
from marshmallow_enum import EnumField
import enum


class InitialEncounter(enum.Enum):
    # https://docs.python.org/3/library/enum.html#creating-an-enum
    UNKNOWN = 1
    TRAFFIC_VIOLATION = 2
    TRESSPASSING = 3
    PotentialCrimeSuspect = 4
    Other = 5


class VictimWeapon(enum.Enum):
    Unknown = 1
    Firearm = 2
    Blade = 3
    Blunt = 4
    NoWeapon = 5
    Other = 6


class VictimAction(enum.Enum):
    Unknown = 1
    Speaking = 2
    NoAction = 3
    Fleeing = 4
    Approaching = 5
    Attacking = 6
    Other = 7


class CauseOfDeath(enum.Enum):
    Unknown = 1
    BluntForce = 2
    GunShot = 3
    Choke = 4
    Other = 5


class Gender(enum.Enum):
    Unknown = 1
    Male = 2
    Female = 3
    Transgender = 4


class Race(enum.Enum):
    Unknown = 1
    White = 2
    Black_African_American = 3
    American_Indian_Alaska_Native = 4
    Asian = 5
    Native_Hawaiian_Pacific_Islander = 6


class VictimStatus(enum.Enum):
    Unknown = 1
    Unharmed = 2
    Injured = 3
    Disabled = 4
    Deceased = 5


class Victim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    race = db.Column(db.Enum(Race))
    gender = db.Column(db.Enum(Gender))
    date_of_birth = db.Column(db.Date)  # TODO: add "estimated"?
    manner_of_injury = db.Column(db.Text)  # TODO: is an enum
    # TODO: deceased is better as calculated value; if time of death is null.
    deceased = db.Column(db.Boolean)
    time_of_death = db.Column(db.DateTime, nullable=True)


class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # officer id
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    race = db.Column(db.Enum(Race))
    gender = db.Column(db.Enum(Gender))
    appointed_date = db.Column(db.DateTime)
    badge = db.Column(db.Text)
    unit = db.Column(db.Text)  # type?
    # TODO: How do we handle changes over time in rank?
    rank = db.Column(db.Text)  # type?
    star = db.Column(db.Text)  # type?
    age = db.Column(db.Integer)
    # TODO: Age changes over time. Might we use birth year?


class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_of_incident = db.Column(db.DateTime)
    location = db.Column(db.Text)  # TODO: location object
    # TODO: neighborhood seems like a weird identifier that may not always
    #  apply in consistent ways across municipalities.
    neighborhood = db.Column(db.Text)
    stop_type = db.Column(db.Text)  # TODO: enum
    call_type = db.Column(db.Text)  # TODO: enum
    has_multimedia = db.Column(db.Boolean)
    from_report = db.Column(db.Boolean)
    # These may require an additional table. Also can dox a victim
    was_victim_arrested = db.Column(db.Boolean)
    arrest_id = db.Column(db.Integer)  # TODO: foreign key of some sort?
    # Does an existing warrant count here?
    criminal_case_brought = db.Column(db.Boolean)
    case_id = db.Column(db.Integer)  # TODO: foreign key of some sort?


class IncidentVictim(db.Model):  # TODO: rename as IncidentVictimXRef ?
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer)  # TODO: foreign key
    victim_id = db.Column(db.Integer)  # TODO: foreign key


class IncidentDescription(db.Model):
    # (Note) Removed all the `description_*` prefixes.
    id = db.Column(db.Integer, primary_key=True)  # description id
    incident_id = db.Column(db.Integer)  # TODO: foreign key
    text = db.Column(db.Text)
    type = db.Column(db.Text)  # TODO: enum
    # TODO: are there rules for this column other than text?
    source = db.Column(db.Text)


class IncidentAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # action id
    incident_id = db.Column(db.Integer)  # TODO: foreign key
    date = db.Column(db.DateTime)
    action = db.Column(db.Text)  # TODO: Not sure what this is.
    actor = db.Column(db.Text)  # TODO: Not sure what this is.
    notes = db.Column(db.Text)


class IncidentTag(db.Model):
    # TODO: rename as IncidentTagXRef ?
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer)  # TODO: foreign key
    tag_id = db.Column(db.Integer)  # TODO: foreign key


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.Text)


class IncidentUseOfForce(db.Model):
    # TODO: rename to IncidentUseOfForceXRef ?
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer)  # TODO: foreign key
    use_of_force_id = db.Column(db.Integer)  # TODO: foreign key


class ResultOfStopAtIncident(db.Model):
    # TODO: Rename to IncidentResultOfStopXRef?
    # TODO:
    #  Does this need to be an crossref table?
    #  Is there a many-to-many relationship?
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer)  # TODO: foreign key
    result_of_stop_id = db.Column(db.Integer)  # TODO: foreign key


class ResultOfStop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Text)


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
    initial_reason_for_encounter = db.Column(db.Enum(InitialEncounter))
    charges_involved = db.Column(db.Unicode(512))
    victim_weapon = db.Column(db.Enum(VictimWeapon))
    victim_action = db.Column(db.Enum(VictimAction))
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
    cause_of_death = db.Column(db.Enum(CauseOfDeath))
    cause_of_death_description = db.Column(db.Unicode(512))

    # victim data
    first_name = db.Column(db.Unicode(512))
    last_name = db.Column(db.Unicode(512))
    age_at_incident = db.Column(db.Integer)
    gender = db.Column(db.Enum(Gender))
    race = db.Column(db.Enum(Race))
    status = db.Column(db.Enum(VictimStatus))

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
    gender = EnumField(Gender)
    race = EnumField(Race)
    victim_weapon = EnumField(VictimWeapon)
    victim_action = EnumField(VictimAction)
    cause_of_death = EnumField(CauseOfDeath)
    status = EnumField(VictimStatus)
    initial_reason_for_encounter = EnumField(InitialEncounter)

    class Meta:
        model = Incidents
