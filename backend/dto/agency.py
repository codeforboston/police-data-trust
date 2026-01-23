from pydantic import Field, BaseModel, validator, field_validator
from typing import Optional
from backend.database.models.agency import State, Jurisdiction
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

    @validator("hq_state")
    def validate_state(cls, v):
        if v and v not in State.choices():
            raise ValueError(f"Invalid state: {v}")
        return v

    @validator("jurisdiction")
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
