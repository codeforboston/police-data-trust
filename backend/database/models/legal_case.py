from .. import db
import enum


class LegalCaseType(str, enum.Enum):
    CIVIL = "CIVIL"
    CRIMINAL = "CRIMINAL"


class LegalCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    case_type = db.Column(db.Enum(LegalCaseType))
    jurisdiction = db.Column(db.String)
    judge = db.Column(db.String)
    docket_number = db.Column(db.String)
    defendant = db.Relationship(
        "Officer", back_populates="defendant_cases")
    defendant_council = db.relationship(
        "Attorney", back_populates="defendant_cases"
    )
    plaintiff = db.Column(db.String)
    plaintiff_council = db.relationship(
        "Attorney", backref="plaintiff_cases"
    )
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    outcome = db.Column(db.String)
