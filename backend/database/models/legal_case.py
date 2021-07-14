from .. import db
import enum


class LegalCaseType(str, enum.Enum):
    # TODO: Do we want string enumerations to be all caps? i.e. CIVIL = "CIVIL"
    CIVIL = "CIVIL"
    CRIMINAL = "CRIMINAL"


class LegalCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    case_type = db.Column(db.Enum(LegalCaseType))
    jurisdiction = db.Column(db.String)
    judge = db.Column(db.String)
    docket_number = db.Column(db.String)
    # TODO: Foreign key to officer/victim?
    defendant = db.Column(db.String)
    defendant_council = db.relationship(
        "Attorney", backref="legal_case_defendant", uselist=False
    )
    plaintiff = db.Column(db.String)
    plaintiff_council = db.relationship(
        "Attorney", backref="legal_case_plaintiff", uselist=False
    )
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    outcome = db.Column(db.String)
