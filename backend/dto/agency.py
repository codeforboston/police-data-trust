from pydantic import Field, BaseModel, field_validator
from typing import Optional
from backend.database.models.agency import State, Jurisdiction
from backend.dto.common import PaginatedRequest, RequestDTO
from typing import List


class AddOfficerSchema(BaseModel):
    officer_id: int
    badge_number: str
    agency_id: Optional[int]
    highest_rank: Optional[str]
    earliest_employment: Optional[str]
    latest_employment: Optional[str]
    unit: Optional[str]
    currently_employed: bool = True


class AddOfficerListSchema(BaseModel):
    officers: List[AddOfficerSchema]


class AgencyQueryParams(PaginatedRequest):
    name: str | None = None
    hq_city: str | None = None
    hq_state: str | None = None
    hq_zip: str | None = None
    jurisdiction: str | None = None

    searchResult: bool = Field(default=False)

    @field_validator("hq_state")
    def validate_state(cls, v):
        if v and v not in State.choices():
            raise ValueError(f"Invalid state: {v}")
        return v

    @field_validator("jurisdiction")
    def validate_jurisdiction(cls, v):
        if v and v not in Jurisdiction.choices():
            raise ValueError(f"Invalid jurisdiction: {v}")
        return v


class GetAgencyParams(BaseModel):
    include: Optional[List[str]] = Field(
        None, description="Related data to include in the response."
    )

    @field_validator("include")
    def validate_include(cls, v):
        allowed_includes = {
            "units",
            "officers",
            "complaints",
            "allegations",
        }
        if v:
            invalid = set(v) - allowed_includes
            if invalid:
                raise ValueError(
                    f"Invalid include parameters: {', '.join(invalid)}")
        return v


class CreateAgency(RequestDTO):
    name: str = Field(..., description="Required. The name of the agency.")
    hq_state: str = Field(
        ..., description="Required. The headquarters state of the agency.")
    hq_address: Optional[str] = Field(
        None, description="The headquarters address of the agency.")
    hq_city: Optional[str] = Field(
        None, description="The headquarters city of the agency.")
    hq_zip: Optional[str] = Field(
        None, description="The headquarters zip code of the agency.")
    jurisdiction: Optional[str] = Field(
        None, description="The jurisdiction type of the agency."
    )
    phone: Optional[str] = Field(
        None, description="The phone number of the agency.")
    email: Optional[str] = Field(
        None, description="The email address of the agency.")
    website_url: Optional[str] = Field(
        None, description="The website URL of the agency.")
    description: Optional[str] = Field(
        None, description="A description of the agency.")
    date_established: Optional[str] = Field(
        None, description="The date the agency was established.")

    @field_validator("hq_state")
    def validate_state(cls, v):
        if v and v not in State.choices():
            raise ValueError(f"Invalid state: {v}")
        return v

    @field_validator("jurisdiction")
    def validate_jurisdiction(cls, v):
        if v and v not in Jurisdiction.choices():
            raise ValueError(f"Invalid jurisdiction: {v}")
        return v


class UpdateAgency(RequestDTO):
    name: Optional[str] = Field(None, description="The name of the agency.")
    hq_address: Optional[str] = Field(
        None, description="The headquarters address of the agency.")
    hq_city: Optional[str] = Field(
        None, description="The headquarters city of the agency.")
    hq_state: Optional[str] = Field(
        None, description="The headquarters state of the agency.")
    hq_zip: Optional[str] = Field(
        None, description="The headquarters zip code of the agency.")
    jurisdiction: Optional[str] = Field(
        None, description="The jurisdiction type of the agency."
    )
    phone: Optional[str] = Field(
        None, description="The phone number of the agency.")
    email: Optional[str] = Field(
        None, description="The email address of the agency.")
    website_url: Optional[str] = Field(
        None, description="The website URL of the agency.")
    description: Optional[str] = Field(
        None, description="A description of the agency.")
    date_established: Optional[str] = Field(
        None, description="The date the agency was established.")

    @field_validator("hq_state")
    def validate_state(cls, v):
        if v and v not in State.choices():
            raise ValueError(f"Invalid state: {v}")
        return v

    @field_validator("jurisdiction")
    def validate_jurisdiction(cls, v):
        if v and v not in Jurisdiction.choices():
            raise ValueError(f"Invalid jurisdiction: {v}")
        return v
