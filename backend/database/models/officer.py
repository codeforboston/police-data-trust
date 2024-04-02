import enum

from ..core import db, CrudMixin
from sqlalchemy.ext.associationproxy import association_proxy


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
    law enforcement agencies. For example, in New York, this would be
    the Tax ID Number.
    """
    id = db.Column(db.Integer, primary_key=True)
    officer_id = db.Column(
        db.Integer, db.ForeignKey("officer.id"))
    id_name = db.Column(db.Text)  # e.g. "Tax ID Number"
    state = db.Column(db.Enum(State))  # e.g. "NY"
    value = db.Column(db.Text)  # e.g. "958938"

    def __repr__(self):
        return f"<StateID: Officer {self.officer_id}, {self.state}>"


class Officer(db.Model, CrudMixin):
    id = db.Column(db.Integer, primary_key=True)  # officer id
    first_name = db.Column(db.Text)
    middle_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    race = db.Column(db.Text)
    ethnicity = db.Column(db.Text)
    gender = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    state_ids = db.relationship("StateID", backref="officer")

    agency_association = db.relationship(
        "Employment", back_populates="officer")
    employers = association_proxy("agency_association", "agency")

    perpetrator_association = db.relationship(
        "Accusation", back_populates="officer")
    accusations = association_proxy("perpetrator_association", "perpetrator")

    def __repr__(self):
        return f"<Officer {self.id}>"
