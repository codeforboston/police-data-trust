from pydantic import AliasChoices, BaseModel, Field, field_validator
from typing import Optional
from backend.dto.common_filters import (
    normalize_string_or_list,
    normalize_upper_string_or_list,
    validate_state_code,
)
from backend.dto.common import PaginatedRequest, RequestDTO
from typing import List


class OfficerSearchParams(PaginatedRequest):
    # Pagination
    # page: int = 1
    # per_page: int = Field(20, alias="per_page")
    searchResult: bool = Field(default=False)

    # Name components
    term: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("term", "query"),
    )
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    suffix: Optional[str] = None

    # Other filters
    rank: List[str] = []
    unit: List[str] = []
    agency: List[str] = []
    active_after: Optional[str] = None
    active_before: Optional[str] = None
    badge_number: List[str] = Field([], alias="badge_number")
    ethnicity: List[str] = []
    city: str | list[str] | None = None
    city_uid: str | list[str] | None = None
    state: str | list[str] | None = None
    source: str | list[str] | None = None
    source_uid: str | list[str] | None = None

    # Derived fields (computed below)
    @field_validator("unit", mode="before")
    def ensure_list(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            return [v]         # convert single string → list
        return v

    @field_validator("city", mode="before")
    def normalize_city(cls, value):
        return normalize_string_or_list(value)

    @field_validator("city_uid", mode="before")
    def normalize_city_uid(cls, value):
        return normalize_string_or_list(value)

    @field_validator("state", mode="before")
    def normalize_state(cls, value):
        return normalize_upper_string_or_list(value)

    @field_validator("source", mode="before")
    def normalize_source(cls, value):
        return normalize_string_or_list(value)

    @field_validator("source_uid", mode="before")
    def normalize_source_uid(cls, value):
        return normalize_string_or_list(value)

    @field_validator("state")
    def validate_state(cls, value):
        return validate_state_code(value)

    @property
    def name_parts(self):
        return [
            p.strip()
            for p in [
                self.first_name,
                self.middle_name,
                self.last_name,
                self.suffix,
            ]
            if p and p.strip()
        ]

    @property
    def officer_name(self):
        if self.term and self.term.strip():
            return self.term.strip()
        else:
            return " AND ".join(self.name_parts) or None

    @property
    def officer_rank(self):
        return " ".join(self.rank) if self.rank else None


class AddEmploymentSchema(BaseModel):
    agency_id: int
    badge_number: str
    officer_id: Optional[int]
    highest_rank: Optional[str]
    earliest_employment: Optional[str]
    latest_employment: Optional[str]
    unit: Optional[str]
    currently_employed: bool = True


class AddEmploymentListSchema(BaseModel):
    agencies: List[AddEmploymentSchema]


class GetOfficerParams(RequestDTO):
    include: Optional[List[str]] = Field(
        None, description="Related entities to include in the response."
    )

    @field_validator("include")
    def validate_include(cls, v):
        allowed_includes = {
            "employment",
            "allegations"
        }
        if v:
            invalid = set(v) - allowed_includes
            if invalid:
                raise ValueError(
                    f"Invalid include parameters: {', '.join(invalid)}")
        return v


class CreateOfficer(RequestDTO):
    source_uid: str = Field(
        ...,
        description="UID of the source making the creation",
    )
    first_name: Optional[str] = Field(
        None, description="First name of the officer")
    middle_name: Optional[str] = Field(
        None, description="Middle name of the officer")
    last_name: Optional[str] = Field(
        None, description="Last name of the officer")
    suffix: Optional[str] = Field(
        None, description="Suffix of the officer's name")
    ethnicity: Optional[str] = Field(
        None, description="The ethnicity of the officer")
    gender: Optional[str] = Field(
        None, description="The gender of the officer")
    date_of_birth: Optional[str] = Field(
        None, description="The date of birth of the officer")


class UpdateOfficer(RequestDTO):
    source_uid: str = Field(
        ...,
        description="UID of the source making the update",
    )
    first_name: Optional[str] = Field(
        None, description="First name of the officer")
    middle_name: Optional[str] = Field(
        None, description="Middle name of the officer")
    last_name: Optional[str] = Field(
        None, description="Last name of the officer")
    suffix: Optional[str] = Field(
        None, description="Suffix of the officer's name")
    ethnicity: Optional[str] = Field(
        None, description="The ethnicity of the officer")
    gender: Optional[str] = Field(
        None, description="The gender of the officer")
    date_of_birth: Optional[str] = Field(
        None, description="The date of birth of the officer")


class GetOfficerMetricsParams(RequestDTO):
    include: List[str]
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    include_source: Optional[List[str]] = None
    exclude_source: Optional[List[str]] = None

    @field_validator("include")
    def validate_include(cls, v):
        allowed_includes = {
            "allegation_types",
            "allegation_outcomes",
            "complaint_history",
            "complainant_demographics"
        }
        if v:
            invalid = set(v) - allowed_includes
            if invalid:
                raise ValueError(
                    f"Invalid include parameters: {', '.join(invalid)}")
        return v
