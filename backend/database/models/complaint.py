"""Define the Classes for Complaints."""
from datetime import date
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr, HttpUrl, validator
from neomodel import (
    StructuredNode,
    StructuredRel,
    StringProperty,
    RelationshipTo,
    RelationshipFrom,
    DateProperty,
    UniqueIdProperty
)


class RecordTypeEnum(str, Enum):
    legal = "legal"
    news = "news"
    government = "government"

# Pydantic Models
""" class BaseSourceModel(BaseModel):
    record_type: RecordTypeEnum

    class Config:
        use_enum_values = True


class LegalSourceModel(BaseSourceModel):
    record_type: RecordTypeEnum = RecordTypeEnum.legal
    court: str
    judge: str
    docket_number: str
    date_of_action: date

    class Config:
        use_enum_values = True


class NewsSourceModel(BaseSourceModel):
    record_type: RecordTypeEnum = RecordTypeEnum.news
    publication_name: str
    publication_date: date
    publication_url: HttpUrl
    author: str
    author_url: Optional[HttpUrl]
    author_email: Optional[EmailStr]

    class Config:
        use_enum_values = True


class GovernmentSourceModel(BaseSourceModel):
    record_type: RecordTypeEnum = RecordTypeEnum.government
    reporting_agency: str
    reporting_agency_url: Optional[HttpUrl]
    reporting_agency_email: Optional[EmailStr]

    class Config:
        use_enum_values = True


class AllegationModel(BaseModel):
    uid: Optional[str]
    allegation: str
    recommended_finding: Optional[str]
    recommended_outcome: Optional[str]
    finding: Optional[str]
    outcome: Optional[str]

    # Relationships (assumed as references to IDs or related models)
    complainant_id: Optional[str]
    accused_id: Optional[str]
    complaint_id: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174001",
                "allegation": "Excessive Force",
                "recommended_finding": "Sustained",
                "recommended_outcome": "Suspension",
                "finding": "Sustained",
                "outcome": "Suspension",
                "complainant_id": "123e4567-e89b-12d3-a456-426614174002",
                "accused_id": "123e4567-e89b-12d3-a456-426614174003",
                "complaint_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class InvestigationModel(BaseModel):
    uid: Optional[str]
    start_date: date
    end_date: Optional[date]

    # Relationships (assumed as references to IDs or related models)
    investigator_id: Optional[str]
    complaint_id: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174004",
                "start_date": date(2024, 7, 1),
                "end_date": date(2024, 7, 15),
                "investigator_id": "123e4567-e89b-12d3-a456-426614174005",
                "complaint_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class PenaltyModel(BaseModel):
    uid: Optional[str]
    description: str
    date: date

    # Relationships (assumed as references to IDs or related models)
    officer_id: Optional[str]
    complaint_id: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174006",
                "description": "Suspension",
                "date": date(2024, 8, 16),
                "officer_id": "123e4567-e89b-12d3-a456-426614174007",
                "complaint_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class ComplaintModel(BaseModel):
    uid: Optional[str]
    category: str
    incident_date: date
    received_date: Optional[date]
    closed_date: Optional[date]
    reason_for_contact: str
    outcome_of_contact: str

    # Relationships
    source: BaseSourceModel
    location: "LocationModel"
    # civilian_review_board: CivilianReviewBoardModel
    civlian_witnesses: List["CivilianModel"]
    police_witnesses: List["OfficerModel"]
    attachments: List["AttachmentModel"]
    allegations: List[AllegationModel]
    investigations: List[InvestigationModel]
    penalties: List[PenaltyModel]
    # Other relationships can be added here in similar fashion

    @validator('closed_date', always=True)
    def check_dates(cls, v, values):
        if 'received_date' in values and v:
            assert v >= values['received_date'], 'closed_date must be after received_date'
        return v
 """


# Neo4j Models
class BaseSourceRel(StructuredRel):
    record_type = StringProperty()


class LegalSourceRel(BaseSourceRel):
    court = StringProperty()
    judge = StringProperty()
    docket_number = StringProperty()
    date_of_action = DateProperty()


class NewsSourceRel(BaseSourceRel):
    publication_name = StringProperty()
    publication_date = DateProperty()
    publication_url = StringProperty()
    author = StringProperty()
    author_url = StringProperty()
    author_email = StringProperty()


class GovernmentSourceRel(BaseSourceRel):
    reporting_agency = StringProperty()
    reporting_agency_url = StringProperty()
    reporting_agency_email = StringProperty()


class Complaint(StructuredNode):
    uid = UniqueIdProperty()
    category = StringProperty()
    incident_date = DateProperty()
    recieved_date = DateProperty()
    closed_date = DateProperty()
    reason_for_contact = StringProperty()
    outcome_of_contact = StringProperty()

    # Relationships
    source = RelationshipFrom("Partner", "REPORTED", model=BaseSourceRel)
    location = RelationshipTo("Location", "OCCURRED_AT")
    civlian_witnesses = RelationshipFrom("Civilian", "WITNESSED")
    police_witnesses = RelationshipFrom("Officer", "WITNESSED")
    attachments = RelationshipTo("Attachment", "ATTACHED_TO")
    allegations = RelationshipTo("Allegation", "ALLEGED")
    investigations = RelationshipTo("Investigation", "EXAMINED_BY")
    penalties = RelationshipTo("Penalty", "RESULTS_IN")
    civilian_review_board = RelationshipFrom("CivilianReviewBoard", "REVIEWED")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Complaint {self.id}>"


class Allegation(StructuredNode):
    uid = UniqueIdProperty()
    allegation = StringProperty()
    recommended_finding = StringProperty()
    recommended_outcome = StringProperty()
    finding = StringProperty()
    outcome = StringProperty()

    # Relationships
    complainant = RelationshipFrom("Civilian", "COMPLAINED_OF")
    accused = RelationshipFrom("Officer", "ACCUSED_OF")
    complaint = RelationshipFrom("Complaint", "ALLEGED")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Allegation {self.id}>"


class Investigation(StructuredNode):
    uid = UniqueIdProperty()
    start_date = DateProperty()
    end_date = DateProperty()

    # Relationships
    investigator = RelationshipFrom("Officer", "LEAD_BY")
    complaint = RelationshipFrom("Complaint", "EXAMINED_BY")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Investigation {self.id}>"


class Penalty(StructuredNode):
    uid = UniqueIdProperty()
    description = StringProperty()
    date = DateProperty()

    # Relationships
    officer = RelationshipFrom("Officer", "RECEIVED")
    complaint = RelationshipFrom("Complaint", "RESULTS_IN")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Penalty {self.id}>"
