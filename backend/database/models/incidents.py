"""Define the SQL classes for Users."""
from backend.database.core import db

from flask_serialize.flask_serialize import FlaskSerialize
import enum


fs_mixin = FlaskSerialize(db)


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


class Incidents(db.Model, fs_mixin):
    """The SQL dataclass for an Incident."""

    __tablename__ = "incidents"

    Incident_ID = db.Column(db.Integer, primary_key=True)

    # incident data
    Occurrence_Date = db.Column(db.DateTime)
    State_Abbv = db.Column(db.Unicode(512))
    City = db.Column(db.Unicode(512))
    Address_1 = db.Column(db.Unicode(512))
    Address_2 = db.Column(db.Unicode(512))
    Zip_Code = db.Column(db.Unicode(10))
    Latitude = db.Column(db.Float)
    Longitude = db.Column(db.Float)
    Reported_Date = db.Column(db.DateTime)
    Initial_Reason_For_Encounter = db.Column(db.Enum(Initial_Encounter_Enum))
    Charges_Involved = db.Column(db.Unicode(512))
    Victim_Weapon = db.Column(db.Enum(Victim_Weapon_Enum))
    Victim_Action = db.Column(db.Enum(Victim_Action_Enum))
    Has_Multimedia = db.Column(db.Boolean)
    Media_URL = db.Column(db.Unicode(512))
    From_Report = db.Column(db.Boolean)
    Description = db.Column(db.Unicode(512))
    Associated_Incidents = db.Column(db.Unicode(512))

    # Death information
    Death_Date = db.Column(db.DateTime)
    Death_State_Abbv = db.Column(db.Unicode(512))
    Death_City = db.Column(db.Unicode(512))
    Death_Address_1 = db.Column(db.Unicode(512))
    Death_Address_2 = db.Column(db.Unicode(512))
    Death_Zip_Code = db.Column(db.Unicode(10))
    Cause_Of_Death = db.Column(db.Enum(Cause_Of_Death_Enum))
    Cause_Of_Death_Description = db.Column(db.Unicode(512))

    # victim data
    First_Name = db.Column(db.Unicode(512))
    Last_Name = db.Column(db.Unicode(512))
    Age_At_Incident = db.Column(db.Integer)
    Gender = db.Column(db.Enum(Gender_Enum))
    Race = db.Column(db.Enum(Race_Enum))
    Status = db.Column(db.Enum(Status_Enum))

    # agency data
    Agency_ID = db.Column(db.Integer)
    Agency_Name = db.Column(db.Unicode(512))
    Agency_State_Abbv = db.Column(db.Unicode(512))
    Agency_City = db.Column(db.Unicode(512))
    Agency_Address_1 = db.Column(db.Unicode(512))
    Agency_Address_2 = db.Column(db.Unicode(512))
    Agency_Zip_Code = db.Column(db.Unicode(10))
    Agency_Latitude = db.Column(db.Float)
    Agency_Longitude = db.Column(db.Float)

    # role = db.relationship("RoleTable",

    # backref=db.backref("incidents", lazy=True))
