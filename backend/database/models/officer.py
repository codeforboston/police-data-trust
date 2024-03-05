import enum

from .. import db


class Rank(str, enum.Enum):
    # TODO: Is this comprehensive?
    TECHNICIAN = "TECHNICIAN"
    OFFICER = "OFFICER"
    DETECTIVE = "DETECTIVE"
    CORPORAL = "CORPORAL"
    SERGEANT = "SERGEANT"
    LIEUTENANT = "LIEUTENANT"
    CAPTAIN = "CAPTAIN"
    DEPUTY = "DEPUTY"
    CHIEF = "CHIEF"


class State(str, enum.Enum):
    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DE = "DE"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VT = "VT"
    VA = "VA"
    WA = "WA"
    WV = "WV"
    WI = "WI"
    WY = "WY"


class StateID(db.Model):
    """
    Represents a Statewide ID that follows an offcier even as they move between
    law enforcement agencies. for an officer. For example, in New York, this
    would be the Tax ID Number.
    """
    id = db.Column(db.Integer, primary_key=True)
    officer_id = db.Column(
        db.Integer, db.ForeignKey("officer.id"))
    id_name = db.Column(db.Text)  # e.g. "Tax ID Number"
    state = db.Column(db.Enum(State))  # e.g. "NY"
    value = db.Column(db.Text)  # e.g. "958938"

    def __repr__(self):
        return f"<StateID {self.id}>"


class Employment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    officer_id = db.Column(db.Integer, db.ForeignKey("officer.id"))
    agency_id = db.Column(db.Integer, db.ForeignKey("agency.id"))
    earliest_employment = db.Column(db.Text)
    latest_employment = db.Column(db.Text)
    badge_number = db.Column(db.Text)
    unit = db.Column(db.Text)
    highest_rank = db.Column(db.Enum(Rank))
    currently_employed = db.Column(db.Boolean)

    officer = db.relationship("Officer", back_populates="known_employers")
    agency = db.relationship("Agency", back_populates="known_officers")

    def __repr__(self):
        return f"<Employment {self.id}>"


class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # officer id
    first_name = db.Column(db.Text)
    middle_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    race = db.Column(db.Text)
    ethnicity = db.Column(db.Text)
    gender = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    known_employers = db.relationship("Employment")

    def __repr__(self):
        return f"<Officer {self.id}>"
