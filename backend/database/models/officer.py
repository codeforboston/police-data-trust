from backend.schemas import JsonSerializable, PropertyEnum

from neomodel import (
    StructuredNode,
    RelationshipTo, RelationshipFrom, Relationship,
    StringProperty, DateProperty,
    UniqueIdProperty
)


class State(str, PropertyEnum):
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


class StateID(StructuredNode):
    """
    Represents a Statewide ID that follows an offcier even as they move between
    law enforcement agencies. For example, in New York, this would be
    the Tax ID Number.
    """
    id_name = StringProperty()  # e.g. "Tax ID Number"
    state = StringProperty(choices=State.choices())  # e.g. "NY"
    value = StringProperty()  # e.g. "958938"
    officer = RelationshipFrom('Officer', "HAS_STATE_ID")

    def __repr__(self):
        return f"<StateID: Officer {self.officer_id}, {self.state}>"


class Officer(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "first_name", "middle_name",
        "last_name", "suffix",
        "race", "ethnicity", "gender",
        "date_of_birth"
    ]

    uid = UniqueIdProperty()
    first_name = StringProperty()
    middle_name = StringProperty()
    last_name = StringProperty()
    suffix = StringProperty()
    race = StringProperty()
    ethnicity = StringProperty()
    gender = StringProperty()
    date_of_birth = DateProperty()

    # Relationships
    state_ids = RelationshipTo('StateID', "HAS_STATE_ID")
    units = Relationship(
        'backend.database.models.agency.Unit', "MEMBER_OF_UNIT")
    litigation = Relationship(
        'backend.database.models.litigation.Litigation', "NAMED_IN")
    allegations = Relationship(
        'backend.database.models.complaint.Allegation', "ACCUSED_OF")
    investigations = Relationship(
        'backend.database.models.complaint.Investigation', "LEAD_BY")
    commands = Relationship(
        'backend.database.models.agency.Unit', "COMMANDS")

    def __repr__(self):
        return f"<Officer {self.id}>"
