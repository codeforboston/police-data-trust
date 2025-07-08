from datetime import date
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from .common import Attachemnt
from backend.database.models.types.enums import Ethnicity, Gender


class CreateLocation(BaseModel):
    """Location object"""

    location_type: Optional[str] = Field(
        None,
        description="The type of location. For example: Bar or Tavern, "
        "Street/Highway, etc.",
    )
    location_description: Optional[str] = Field(
        None, description="A written description of the location."
    )
    address: Optional[str] = Field(None, description="The address of the location.")
    city: Optional[str] = Field(None, description="The city the location is in.")
    state: Optional[str] = Field(None, description="The state the location is in.")
    zip: Optional[str] = Field(None, description="The zip code of the location.")
    responsibility: Optional[str] = Field(
        None,
        description="The responsibility area this location is assigned "
        "by the local law enforcement agency.",
    )
    responsibility_type: Optional[str] = Field(
        None,
        description="The type of responsibility area. For example: Beat, "
        "Sector, Precinct, etc.",
    )


class CreateCivilian(BaseModel):
    age: Optional[int] = Field(None, description="Estimated age of the individual.")
    age_range: Optional[str] = Field(None, description="Age range of the individual.")
    ethnicity: Optional[Ethnicity] = Field(
        None, description="The ethnicity of the individual."
    )
    gender: Optional[Gender] = Field(None, description="The gender of the individual.")


class CreateAllegation(BaseModel):
    record_id: Optional[str] = Field(
        None,
        description="The ID that was given to this allegation by the "
        "original source of the data.",
    )
    complainant: Optional[CreateCivilian] = Field(
        None,
        description="Demographic information of the individual "
        "who filed the complaint.",
    )
    allegation: Optional[str] = Field(
        None, description="The allegation made by the complainant."
    )
    type: Optional[str] = Field(None, description="The type of allegation.")
    subtype: Optional[str] = Field(None, description="The sub type of the allegation.")
    recomended_finding: Optional[str] = Field(
        None, description="The finding recommended by the review board."
    )
    recomended_outcome: Optional[str] = Field(
        None, description="The outcome recommended by the review board."
    )
    finding: Optional[str] = Field(None, description="The legal finding.")
    outcome: Optional[str] = Field(
        None, description="The final outcome of the allegation."
    )
    accused_uid: Optional[str] = Field(
        None, description="The UID of the officer the allegation is " "made against."
    )


class CreatePenalty(BaseModel):
    officer_uid: Optional[str] = Field(
        None, description="The UID of the officer the penalty is " "associated with."
    )
    crb_plea: Optional[str] = Field(
        None,
        description="A plea deal agreed by the officer and " "civilian review board.",
    )
    crb_case_status: Optional[str] = Field(
        None, description="The status of the civilian review board's " "case."
    )
    crb_disposition: Optional[str] = Field(
        None, description="The civilian review board's disposition."
    )
    agency_disposition: Optional[str] = Field(
        None, description="The agency's disposition."
    )
    penalty: Optional[str] = Field(None, description="A description of the penalty.")
    date_assesed: Optional[date] = Field(
        None, description="The date that the penalty was assessed."
    )


class CreateInvestigation(BaseModel):
    start_date: Optional[str] = Field(
        None, description="The date the investigation started."
    )
    end_date: Optional[str] = Field(
        None, description="The date the investigation ended."
    )
    investigator_uid: Optional[str] = Field(
        None, description="The UID of the officer who performed the " "investigation."
    )


class ReviewBoard(BaseModel):
    uid: Optional[str] = Field(
        None, description="Unique identifier for the review board."
    )
    name: Optional[str] = Field(None, description="The name of the review board.")
    city: Optional[str] = Field(
        None, description="The city the review board is located in."
    )
    state: Optional[str] = Field(
        None, description="The state the review board is located in."
    )
    url: Optional[str] = Field(
        None, description="The website URL for the review board."
    )


class CreateComplaintSource(BaseModel):
    record_type: str = Field(
        None, description="The type of record the complaint is associated with."
    )
    # Legal Action Properties
    date_published: Optional[date] = Field(
        None, description="The date the record was published."
    )
    court: Optional[str] = Field(
        None, description="The court the legal action was filed in."
    )
    judge: Optional[str] = Field(
        None, description="The judge who presided over the case."
    )
    docket_number: Optional[str] = Field(
        None, description="The docket number of the case."
    )
    case_event_date: Optional[date] = Field(
        None, description="The date the legal action was filed."
    )

    # News Report Properties
    publication_name: Optional[str] = Field(
        None, description="The name of the publication."
    )
    publication_url: Optional[str] = Field(
        None, description="The URL of the publication."
    )
    author: Optional[str] = Field(None, description="The author of the publication.")
    author_url: Optional[str] = Field(None, description="The URL of the author.")
    author_email: Optional[str] = Field(None, description="The email of the author.")

    # Government Record Properties
    reporting_agency: Optional[str] = Field(
        None, description="The agency that reported the record."
    )
    reporting_agency_url: Optional[str] = Field(
        None, description="The URL of the agency that reported the " "record."
    )
    reporting_agency_email: Optional[str] = Field(
        None, description="The email of the agency that reported the " "record."
    )


class CreateComplaint(BaseModel):
    source_uid: str = Field(
        None, description="The UID of the source that reported the complaint."
    )
    source_details: CreateComplaintSource = Field(
        None, description="Details about the sourcing of the complaint."
    )
    record_id: Optional[str] = Field(
        None,
        description="The ID that was given to this complaint by the "
        "original source of the data.",
    )
    category: Optional[str] = Field(None, description="The category of the complaint.")
    incident_date: Optional[date] = Field(
        None, description="The date and time the incident occurred."
    )
    received_date: Optional[date] = Field(
        None,
        description="The date and time the complaint was received "
        "by the reporting source.",
    )
    closed_date: Optional[date] = Field(
        None, description="The date and time the complaint was closed."
    )
    updated_date: Optional[date] = Field(
        None, description="The date and time the complaint was last updated."
    )
    location: Optional[CreateLocation] = None
    reason_for_contact: Optional[str] = Field(
        None, description="The reason for the contact."
    )
    outcome_of_contact: Optional[str] = Field(
        None, description="The outcome of the contact."
    )
    civilian_witnesses: Optional[List[CreateCivilian]] = Field(
        None, description="The civilian witnesses associated with the " "complaint."
    )
    attachments: Optional[List[Attachemnt]] = Field(
        None, description="Documents and multimedia associated with " "the complaint."
    )
    civilian_review_board_uid: Optional[str] = Field(
        None,
        description="The UID of the civilian review board that reviewed "
        "the complaint.",
    )
    police_witnesses: Optional[List[str]] = Field(
        None,
        description="The UID of any police witnesses associated with " "the complaint.",
    )
    allegations: Optional[List[CreateAllegation]] = Field(
        None, description="The allegations associated with the complaint."
    )
    investigations: Optional[List[CreateInvestigation]] = Field(
        None, description="The investigations associated with the " "complaint."
    )
    penalties: Optional[List[CreatePenalty]] = Field(
        None, description="The penalties associated with the complaint."
    )


class UpdateComplaint(BaseModel):
    category: Optional[str] = Field(None, description="The category of the complaint.")
    incident_date: Optional[date] = Field(
        None, description="The date and time the incident occurred."
    )
    received_date: Optional[date] = Field(
        None,
        description="The date and time the complaint was received "
        "by the reporting source.",
    )
    closed_date: Optional[date] = Field(
        None, description="The date and time the complaint was closed."
    )
    updated_date: Optional[date] = Field(
        None, description="The date and time the complaint was last updated."
    )
    location: Optional[Dict[str, Any]] = None
    reason_for_contact: Optional[str] = Field(
        None, description="The reason for the contact."
    )
    outcome_of_contact: Optional[str] = Field(
        None, description="The outcome of the contact."
    )
    civilian_witnesses: Optional[List[CreateCivilian]] = Field(
        None, description="The civilian witnesses associated with the " "complaint."
    )
    attachments: Optional[List[Attachemnt]] = Field(
        None, description="Documents and multimedia associated with " "the complaint."
    )
    civilian_review_board_uid: Optional[str] = Field(
        None,
        description="The UID of the civilian review board that reviewed "
        "the complaint.",
    )
    police_witnesses: Optional[List[str]] = Field(
        None,
        description="The UID of any police witnesses associated with " "the complaint.",
    )
    allegations: Optional[List[CreateAllegation]] = Field(
        None, description="The allegations associated with the complaint."
    )
    investigations: Optional[List[CreateInvestigation]] = Field(
        None, description="The investigations associated with the " "complaint."
    )
    penalties: Optional[List[CreatePenalty]] = Field(
        None, description="The penalties associated with the complaint."
    )
