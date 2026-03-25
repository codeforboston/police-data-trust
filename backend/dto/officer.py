from pydantic import Field, BaseModel, field_validator
from typing import Optional
from backend.dto.common import PaginatedRequest, RequestDTO
from typing import List


class OfficerSearchParams(PaginatedRequest):
    # Pagination
    # page: int = 1
    # per_page: int = Field(20, alias="per_page")
    searchResult: bool = Field(default=False)

    # Name components
    query: Optional[str] = None
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

    # Derived fields (computed below)
    @field_validator("unit", mode="before")
    def ensure_list(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            return [v]         # convert single string → list
        return v

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
        if self.query and self.query.strip():
            return self.query.strip()
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
