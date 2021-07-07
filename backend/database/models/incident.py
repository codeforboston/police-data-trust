"""Define the SQL classes for Users."""
import enum
from .. import db


# Question: Should we be doing string enums?


class InitialEncounter(enum.Enum):
    UNKNOWN = 1
    TRAFFIC_VIOLATION = 2
    TRESSPASSING = 3
    POTENTIAL_CRIMINAL_SUSPECT = 4
    OTHER = 5


class VictimWeapon(enum.Enum):
    UNKNOWN = 1
    FIREARM = 2
    BLADE = 3
    BLUNT = 4
    NO_WEAPON = 5
    OTHER = 6


class VictimAction(enum.Enum):
    UNKNOWN = 1
    SPEAKING = 2
    NO_ACTION = 3
    FLEEING = 4
    APPROACHING = 5
    ATTACKING = 6
    OTHER = 7


class CauseOfDeath(enum.Enum):
    UNKNOWN = 1
    BLUNT_FORCE = 2
    GUNSHOT = 3
    CHOKE = 4
    OTHER = 5


class VictimStatus(enum.Enum):
    UNKNOWN = 1
    UNHARMED = 2
    INJURED = 3
    DISABLED = 4
    DECEASED = 5


# TODO: This file's a bit of a mess (my fault!)
#  There are a lot of association tables in here, and the incidents table is
#  not clearly either a facts table or component table.
#  We need to get a better idea of the relationships we want and then we should
#  implement them accordingly.


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
    victims = db.relationship('Victim', backref='incident')
    descriptions = db.relationship('Description', backref='incident')
    tags = db.relationship('Tag', backref='incident')
    participants = db.relationship('Particpant', backref='incident')
    multimedias = db.relationship('Multimedia', backref='incident')
    investigations = db.relationship('Investigation', backref='incident')
    # TODO: Are the below one to many?
    result_of_stop = db.relationship('ResultOfStop', backref='incident', uselist=False)
    action = db.relationship('Action', backref='incident', uselist=False)
    use_of_force = db.relationship('UseOfForce', backref='incident')
    legal_case = db.relationship('LegalCase', backref='incident')


class Description(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # description id
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'), nullable=False)
    text = db.Column(db.Text)
    type = db.Column(db.Text)  # TODO: enum
    # TODO: are there rules for this column other than text?
    source = db.Column(db.Text)


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # action id
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'), nullable=False)
    date = db.Column(db.DateTime)
    action = db.Column(db.Text)  # TODO: Not sure what this is.
    actor = db.Column(db.Text)  # TODO: Not sure what this is.
    notes = db.Column(db.Text)

class UseOfForce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'))
    item = db.Text()

class ResultOfStop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'))
    result = db.Column(db.Text)