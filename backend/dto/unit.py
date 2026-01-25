from pydantic import Field, field_validator
from typing import Optional
from backend.database.models.agency import State
from backend.dto.common import PaginatedRequest


class UnitQueryParams(PaginatedRequest):
    name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    # page: int = Field(default=1, ge=1)
    # per_page: int = Field(default=20, ge=1)
    searchResult: bool = Field(default=False)

    @field_validator("state")
    def validate_state(cls, v):
        if v and v not in State.choices():
            raise ValueError(f"Invalid state: {v}")
        return v
