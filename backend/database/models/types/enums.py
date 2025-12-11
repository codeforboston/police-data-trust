"""Enumerations shared across multiple models are defined here."""
from backend.schemas import PropertyEnum


class Gender(str, PropertyEnum):
    OTHER = 'Other'
    MALE = 'Male'
    FEMALE = 'Female'

    def describe(self):
        if self == self.OTHER:
            return "Other"
        elif self == self.MALE:
            return "Man"
        elif self == self.FEMALE:
            return "Woman"


class Ethnicity(str, PropertyEnum):
    UNKNOWN = 'Unknown'
    WHITE = 'White'
    BLACK_AFRICAN_AMERICAN = 'Black/African American'
    AMERICAN_INDIAN_ALASKA_NATIVE = 'American Indian/Alaska Native'
    ASIAN = 'Asian'
    NATIVE_HAWAIIAN_PACIFIC_ISLANDER = 'Native Hawaiian/Pacific Islander'
    HISPANIC_LATINO = 'Hispanic/Latino'

    def describe(self):
        if self == self.UNKNOWN:
            return ""
        elif self == self.WHITE:
            return "White"
        elif self == self.BLACK_AFRICAN_AMERICAN:
            return "Black"
        elif self == self.AMERICAN_INDIAN_ALASKA_NATIVE:
            return "Native American"
        elif self == self.ASIAN:
            return "Asian"
        elif self == self.NATIVE_HAWAIIAN_PACIFIC_ISLANDER:
            return "NHPI"
        elif self == self.HISPANIC_LATINO:
            return "Hispanic"


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
    DC = "DC"
    PR = "PR"
    VI = "VI"
    GU = "GU"


class StateIdName(str, PropertyEnum):
    TAX_ID = "Tax ID"
    NPI_ID = "NPI ID"
    DRIVER_LICENSE = "Driver License"
