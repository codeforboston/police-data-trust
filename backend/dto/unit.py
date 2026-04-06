from pydantic import Field, field_validator
from typing import Optional, List
from backend.database.models.agency import State
from backend.database.models.employment import (
    EmploymentStatus, EmploymentType, Rank)
from backend.dto.common import PaginatedRequest, RequestDTO


class UnitQueryParams(PaginatedRequest):
    name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    searchResult: bool = Field(default=False)

    @field_validator("state")
    def validate_state(cls, v):
        if v and v not in State.choices():
            raise ValueError(f"Invalid state: {v}")
        return v


class GetUnitParams(RequestDTO):
    include: Optional[List[str]] = Field(
        None, description="Related entities to include in the response."
    )

    @field_validator("include")
    def validate_include(cls, v):
        allowed_includes = {
            "officers",
            "complaints",
            "allegations",
            "reported_officers",
            "leadership",
            "location",
        }
        if v:
            invalid = set(v) - allowed_includes
            if invalid:
                raise ValueError(
                    f"Invalid include parameters: {', '.join(invalid)}")
        return v


class GetUnitOfficersParams(PaginatedRequest):
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
