from backend.database import db
import enum


class LegalCaseType(str, enum.enum):
    # TODO: Do we want string enumerations to be all caps? i.e. CIVIL = "CIVIL"
    CIVIL = "CIVIL"
    CRIMINAL = "CRIMINAL"


class LegalCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.Enum(LegalCaseType))
    jurisdiction = db.Column(db.String)
    judge = db.Column(db.String)
    docket_number = db.Column(db.String)
    # TODO: Foreign key to officer/victim?
    defendant = db.Column(db.String)
    defendent_council = db.Column(db.String)
    plaintiff = db.Column(db.String)
    plantiff_council = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    outcome = db.Column(db.String)
