from pydantic import Field, BaseModel, field_validator
from typing import Optional
from backend.database.models.agency import State, Jurisdiction
from backend.database.models.employment import EmploymentStatus, EmploymentType, Rank
from backend.dto.common import PaginatedRequest
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

    # page: int = Field(default=1, ge=1)
    # per_page: int = Field(default=20, ge=1)
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
            "reported_units",
            "location",
        }
        if v:
            invalid = set(v) - allowed_includes
            if invalid:
                raise ValueError(
                    f"Invalid include parameters: {', '.join(invalid)}")
        return v


class GetAgencyOfficersParams(PaginatedRequest):
    term: Optional[str] = Field(
        None, description="Search term to filter officers by name or badge number."
    )
    type: Optional[List[str]] = Field(
        None, description="Filter officers by employment type (e.g., 'law_enforcement', 'corrections')."
    )
    status: Optional[List[str]] = Field(
        None, description="Filter officers by employment status (e.g., 'full-time', 'part-time')."
    )
    rank: Optional[List[str]] = Field(
        None, description="Filter officers by rank (e.g., 'Sergeant', 'Lieutenant')."
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
