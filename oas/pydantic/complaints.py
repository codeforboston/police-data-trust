from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union


class BaseComplaint(BaseModel):
    """Base complaint object"""
    source_details: Optional[SourceDetails] = None
    category: Optional[str] = Field(None, description="The category of the complaint.")
    incident_date: Optional[str] = Field(None, description="The date and time the incident occurred.")
    recieved_date: Optional[str] = Field(None, description="The date and time the complaint was received by the reporting partner.")
    closed_date: Optional[str] = Field(None, description="The date and time the complaint was closed.")
    location: Optional[Dict[str, Any]] = None
    reason_for_contact: Optional[str] = Field(None, description="The reason for the contact.")
    outcome_of_contact: Optional[str] = Field(None, description="The outcome of the contact.")
    civilian_witnesses: Optional[List[Civilian]] = Field(None, description="The civilian witnesses associated with the complaint.")
    attachements: Optional[List[Attachemnts]] = Field(None, description="Documents and multimeida associated with the complaint.")


class CreateComplaint(BaseComplaint, BaseModel):
    source_details: Optional[SourceDetails] = None
    category: Optional[str] = Field(None, description="The category of the complaint.")
    incident_date: Optional[str] = Field(None, description="The date and time the incident occurred.")
    recieved_date: Optional[str] = Field(None, description="The date and time the complaint was received by the reporting partner.")
    closed_date: Optional[str] = Field(None, description="The date and time the complaint was closed.")
    location: Optional[Dict[str, Any]] = None
    reason_for_contact: Optional[str] = Field(None, description="The reason for the contact.")
    outcome_of_contact: Optional[str] = Field(None, description="The outcome of the contact.")
    civilian_witnesses: Optional[List[Civilian]] = Field(None, description="The civilian witnesses associated with the complaint.")
    attachements: Optional[List[Attachemnts]] = Field(None, description="Documents and multimeida associated with the complaint.")
    source_uid: Optional[str] = Field(None, description="The UID of the partner that reported the complaint.")
    civilian_review_board_uid: Optional[str] = Field(None, description="The UID of the civilian review board that reviewed the complaint.")
    police_witnesses: Optional[List[str]] = Field(None, description="The UID of any police witnesses associated with the complaint.")
    allegations: Optional[List[CreateAllegation]] = Field(None, description="The allegations associated with the complaint.")
    investigations: Optional[List[CreateInvestigation]] = Field(None, description="The investigations associated with the complaint.")
    penalties: Optional[List[CreatePenalty]] = Field(None, description="The penalties associated with the complaint.")


class UpdateComplaint(BaseComplaint, BaseModel):
    source_details: Optional[SourceDetails] = None
    category: Optional[str] = Field(None, description="The category of the complaint.")
    incident_date: Optional[str] = Field(None, description="The date and time the incident occurred.")
    recieved_date: Optional[str] = Field(None, description="The date and time the complaint was received by the reporting partner.")
    closed_date: Optional[str] = Field(None, description="The date and time the complaint was closed.")
    location: Optional[Dict[str, Any]] = None
    reason_for_contact: Optional[str] = Field(None, description="The reason for the contact.")
    outcome_of_contact: Optional[str] = Field(None, description="The outcome of the contact.")
    civilian_witnesses: Optional[List[Civilian]] = Field(None, description="The civilian witnesses associated with the complaint.")
    attachements: Optional[List[Attachemnts]] = Field(None, description="Documents and multimeida associated with the complaint.")
    civilian_review_board_uid: Optional[str] = Field(None, description="The UID of the civilian review board that reviewed the complaint.")
    police_witnesses: Optional[List[str]] = Field(None, description="The uid of any police witnesses associated with the complaint.")
    allegations: Optional[List[CreateAllegation]] = Field(None, description="The allegations associated with the complaint.")
    investigations: Optional[List[CreateInvestigation]] = Field(None, description="The investigations associated with the complaint.")
    penalties: Optional[List[CreatePenalty]] = Field(None, description="The penalties associated with the complaint.")


class Complaint(BaseComplaint, BaseModel):
    source_details: Optional[SourceDetails] = None
    category: str = Field(..., description="The category of the complaint.")
    incident_date: str = Field(..., description="The date and time the incident occurred.")
    recieved_date: str = Field(..., description="The date and time the complaint was received by the reporting partner.")
    closed_date: Optional[str] = Field(None, description="The date and time the complaint was closed.")
    location: Dict[str, Any] = ...
    reason_for_contact: Optional[str] = Field(None, description="The reason for the contact.")
    outcome_of_contact: Optional[str] = Field(None, description="The outcome of the contact.")
    civilian_witnesses: List[Civilian] = Field(..., description="The civilian witnesses associated with the complaint.")
    attachements: Optional[List[Attachemnts]] = Field(None, description="Documents and multimeida associated with the complaint.")
    uid: str = Field(..., description="Unique identifier for the complaint.")
    created_at: str = Field(..., description="Date and time the complaint was created.")
    updated_at: str = Field(..., description="Date and time the complaint was last updated.")
    source: Optional[Partner] = Field(None, description="The partner that reported the complaint.")
    civilian_review_board: Optional[ReviewBoard] = Field(None, description="The civilian review board that reviewed the complaint.")
    police_witnesses: List[Officer] = Field(..., description="The police witnesses associated with the complaint.")
    allegations: List[Allegation] = Field(..., description="The allegations associated with the complaint.")
    investigations: List[Investigation] = Field(..., description="The investigations associated with the complaint.")
    penalties: List[Penalty] = Field(..., description="The penalties associated with the complaint.")


class ComplaintList(PaginatedResponse, BaseModel):
    results: Optional[List[Complaint]] = Field(None, description="List of complaints.")


class BaseAllegation(BaseModel):
    complaintant: Optional[Civilian] = Field(None, description="Demographic information of the individual who filed the complaint.")
    allegation: Optional[str] = Field(None, description="The allegation made by the complaintant.")
    recomended_finding: Optional[str] = Field(None, description="The finding recomended by the review board.")
    recomended_outcome: Optional[str] = Field(None, description="The outcome recomended by the review board.")
    finding: Optional[str] = Field(None, description="The legal finding.")
    outcome: Optional[str] = Field(None, description="The final outcome of the allegation.")


class CreateAllegation(BaseAllegation, BaseModel):
    complaintant: Optional[Civilian] = Field(None, description="Demographic information of the individual who filed the complaint.")
    allegation: Optional[str] = Field(None, description="The allegation made by the complaintant.")
    recomended_finding: Optional[str] = Field(None, description="The finding recomended by the review board.")
    recomended_outcome: Optional[str] = Field(None, description="The outcome recomended by the review board.")
    finding: Optional[str] = Field(None, description="The legal finding.")
    outcome: Optional[str] = Field(None, description="The final outcome of the allegation.")
    perpetrator_uid: Optional[str] = Field(None, description="The UID of the officer the allegation is made against.")


class Allegation(BaseAllegation, BaseModel):
    complaintant: Optional[Civilian] = Field(None, description="Demographic information of the individual who filed the complaint.")
    allegation: Optional[str] = Field(None, description="The allegation made by the complaintant.")
    recomended_finding: Optional[str] = Field(None, description="The finding recomended by the review board.")
    recomended_outcome: Optional[str] = Field(None, description="The outcome recomended by the review board.")
    finding: Optional[str] = Field(None, description="The legal finding.")
    outcome: Optional[str] = Field(None, description="The final outcome of the allegation.")
    uid: Optional[str] = Field(None, description="Unique identifier for the allegation.")
    perpetrator: Optional[Officer] = Field(None, description="The officer who the allegation is made against.")


class Penalty(BaseModel):
    officer: Optional[Officer] = Field(None, description="The officer who the penalty is associated with.")
    description: Optional[str] = Field(None, description="A description of the penalty.")


class CreatePenalty(BaseModel):
    officer_uid: Optional[str] = Field(None, description="The UID of the officer the penalty is associated with.")
    description: Optional[str] = Field(None, description="A description of the penalty.")


class BaseInvestigation(BaseModel):
    start_date: Optional[str] = Field(None, description="The date the investigation started.")
    end_date: Optional[str] = Field(None, description="The date the investigation ended.")


class CreateInvestigation(BaseInvestigation, BaseModel):
    start_date: Optional[str] = Field(None, description="The date the investigation started.")
    end_date: Optional[str] = Field(None, description="The date the investigation ended.")
    investigator_uid: Optional[str] = Field(None, description="The UID of the officer who preformed the investigation.")


class Investigation(BaseInvestigation, BaseModel):
    start_date: Optional[str] = Field(None, description="The date the investigation started.")
    end_date: Optional[str] = Field(None, description="The date the investigation ended.")
    uid: Optional[str] = Field(None, description="Unique identifier for the investigation.")
    investigator: Optional[Officer] = Field(None, description="The officer who preformed the investigation.")


class Civilian(BaseModel):
    age: Optional[str] = Field(None, description="Age range of the individual.")
    race: Optional[str] = Field(None, description="The race of the individual.")
    gender: Optional[str] = None


class ReviewBoard(BaseModel):
    uid: Optional[str] = Field(None, description="Unique identifier for the review board.")
    name: Optional[str] = Field(None, description="The name of the review board.")
    city: Optional[str] = Field(None, description="The city the review board is located in.")
    state: Optional[str] = Field(None, description="The state the review board is located in.")
    url: Optional[str] = Field(None, description="The website URL for the review board.")


class Attachemnts(BaseModel):
    type: Optional[str] = Field(None, description="The type of attachment.")
    url: Optional[str] = Field(None, description="The url of the attachment.")
    description: Optional[str] = Field(None, description="A description of the attachment.")


class SourceDetails(BaseModel):
    record_type: Optional[str] = Field(None, description="The type of record the complaint is associated with.")


class LegalAction(BaseModel):
    record_type: Optional[str] = Field(None, description="The type of record the complaint is associated with.")
    court: Optional[str] = Field(None, description="The court the legal action was filed in.")
    judge: Optional[str] = Field(None, description="The judge who presided over the case.")
    docket_number: Optional[str] = Field(None, description="The docket number of the case.")
    date_of_action: Optional[str] = Field(None, description="The date the legal action was filed.")


class PersonalAccount(BaseModel):
    record_type: Optional[str] = Field(None, description="The type of record the complaint is associated with.")


class GovernmentRecord(BaseModel):
    record_type: Optional[str] = Field(None, description="The type of record the complaint is associated with.")
    reporting_agency: Optional[str] = Field(None, description="The agency that reported the record.")
    reporting_agency_url: Optional[str] = Field(None, description="The url of the agency that reported the record.")
    reporting_agency_email: Optional[str] = Field(None, description="The email of the agency that reported the record.")


class NewsReport(BaseModel):
    record_type: Optional[str] = Field(None, description="The type of record the complaint is associated with.")
    publication_name: Optional[str] = Field(None, description="The name of the publication.")
    publication_date: Optional[str] = Field(None, description="The date the publication was released.")
    publication_url: Optional[str] = Field(None, description="The url of the publication.")
    author: Optional[str] = Field(None, description="The author of the publication.")
    author_url: Optional[str] = Field(None, description="The url of the author.")
    author_email: Optional[str] = Field(None, description="The email of the author.")


