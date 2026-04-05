from pydantic import Field, field_validator
from typing import Optional, List
from backend.database.models.agency import State
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
    include: Optional[List[str]] = Field(
        None, description="Related data to include in the response."
    )

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
