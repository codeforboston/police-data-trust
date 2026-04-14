from pydantic import AliasChoices, BaseModel, Field, field_validator
from typing import Optional
from backend.database.models.agency import Jurisdiction
from backend.database.models.employment import (
    EmploymentStatus, EmploymentType, Rank)
from backend.dto.common_filters import (
    normalize_string_or_list,
    normalize_upper_string,
    validate_state_code,
)
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
    term: str | None = Field(
        default=None,
        validation_alias=AliasChoices("term", "name"),
    )
    hq_city: str | None = None
    hq_state: str | None = None
    hq_zip: str | None = None
    jurisdiction: str | None = None
    city: str | list[str] | None = None
    city_uid: str | list[str] | None = None
    state: str | None = None
    source: str | list[str] | None = None
    source_uid: str | list[str] | None = None

    # page: int = Field(default=1, ge=1)
    # per_page: int = Field(default=20, ge=1)
    searchResult: bool = Field(default=False)

    @field_validator("city", mode="before")
    def normalize_city(cls, value):
        return normalize_string_or_list(value)

    @field_validator("city_uid", mode="before")
    def normalize_city_uid(cls, value):
        return normalize_string_or_list(value)

    @field_validator("state", mode="before")
    def normalize_state(cls, value):
        return normalize_upper_string(value)

    @field_validator("source", mode="before")
    def normalize_source(cls, value):
        return normalize_string_or_list(value)

    @field_validator("source_uid", mode="before")
    def normalize_source_uid(cls, value):
        return normalize_string_or_list(value)

    @field_validator("hq_state")
    def validate_state(cls, v):
        return validate_state_code(v)

    @field_validator("state")
    def validate_location_state(cls, v):
        return validate_state_code(v)

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
            "reported_units",
            "location",
        }
        if v:
            invalid = set(v) - allowed_includes
            if invalid:
                raise ValueError(
                    f"Invalid include parameters: {', '.join(invalid)}")
        return v


class CreateAgency(RequestDTO):
    source_uid: str = Field(
        ...,
        description="UID of the source making the creation",
    )
    name: Optional[str] = Field(None, description="Name of the agency")
    hq_address: Optional[str] = Field(
        None, description="Address of the agency")
    hq_city: Optional[str] = Field(None, description="City of the agency")
    hq_state: Optional[str] = Field(None, description="State of the agency")
    hq_zip: Optional[str] = Field(None, description="Zip code of the agency")
    jurisdiction: Optional[str] = Field(
        None, description="Jurisdiction of the agency")
    phone: Optional[str] = Field(None, description="Phone number of the agency")
    email: Optional[str] = Field(None, description="Email of the agency")
    website_url: Optional[str] = Field(
        None, description="Website of the agency")


class UpdateAgency(RequestDTO):
    source_uid: str = Field(
        ...,
        description="UID of the source making the update",
    )
    name: Optional[str] = Field(None, description="Name of the agency")
    hq_address: Optional[str] = Field(
        None, description="Address of the agency")
    hq_city: Optional[str] = Field(None, description="City of the agency")
    hq_state: Optional[str] = Field(None, description="State of the agency")
    hq_zip: Optional[str] = Field(None, description="Zip code of the agency")
    jurisdiction: Optional[str] = Field(
        None, description="Jurisdiction of the agency")
    phone: Optional[str] = Field(None, description="Phone number of the agency")
    email: Optional[str] = Field(None, description="Email of the agency")
    website_url: Optional[str] = Field(
        None, description="Website of the agency")


class GetAgencyOfficersParams(PaginatedRequest):
    term: Optional[str] = Field(
        None,
        description="Search term to filter officers by name or badge number."
    )
    type: Optional[List[str]] = Field(
        None,
        description="Filter officers by employment type "
        "(e.g., 'law_enforcement', 'corrections')."
    )
    status: Optional[List[str]] = Field(
        None,
        description="Filter officers by employment status "
        "(e.g., 'full-time', 'part-time')."
    )
    rank: Optional[List[str]] = Field(
        None,
        description="Filter officers by rank "
        "(e.g., 'Sergeant', 'Lieutenant')."
    )
    include: Optional[List[str]] = Field(
        None, description="Related data to include in the response."
    )

    @field_validator("status")
    def validate_status(cls, v):
        allowed_statuses = EmploymentStatus.choices()
        if v:
            invalid = set(v) - set(allowed_statuses)
            if invalid:
                raise ValueError(
                    f"Invalid status parameters: {', '.join(invalid)}")
        return v

    @field_validator("type")
    def validate_type(cls, v):
        allowed_types = EmploymentType.choices()
        if v:
            invalid = set(v) - set(allowed_types)
            if invalid:
                raise ValueError(
                    f"Invalid type parameters: {', '.join(invalid)}")
        return v

    @field_validator("rank")
    def validate_rank(cls, v):
        allowed_ranks = Rank.choices()
        if v:
            invalid = set(v) - set(allowed_ranks)
            if invalid:
                raise ValueError(
                    f"Invalid rank parameters: {', '.join(invalid)}")
        return v

    @field_validator("include")
    def validate_include(cls, v):
        allowed_includes = {
            "employment",
        }
        if v:
            invalid = set(v) - allowed_includes
            if invalid:
                raise ValueError(
                    f"Invalid include parameters: {', '.join(invalid)}")
        return v


class GetAgencyUnitsParams(PaginatedRequest):
    include: Optional[List[str]] = Field(
        None, description="Related data to include in the response."
    )

    @field_validator("include")
    def validate_include(cls, v):
        allowed_includes = {
            "officers",
            "complaints",
        }
        if v:
            invalid = set(v) - allowed_includes
            if invalid:
                raise ValueError(
                    f"Invalid include parameters: {', '.join(invalid)}")
        return v
