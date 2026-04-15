from pydantic import Field, field_validator

from backend.database.models.agency import State
from backend.dto.common import PaginatedRequest


class CityLookupParams(PaginatedRequest):
    term: str = Field(...)
    state: str | None = None

    @field_validator("term", mode="before")
    @classmethod
    def normalize_term(cls, value):
        if value is None:
            raise ValueError("term is required")

        normalized = " ".join(str(value).split())
        if not normalized:
            raise ValueError("term is required")

        return normalized

    @field_validator("state", mode="before")
    @classmethod
    def normalize_state(cls, value):
        if value is None:
            return None
        return str(value).strip().upper() or None

    @field_validator("state")
    @classmethod
    def validate_state(cls, value):
        if value and value not in State.choices():
            raise ValueError(f"Invalid state: {value}")
        return value


class CountyLookupParams(CityLookupParams):
    pass


class StateLookupParams(PaginatedRequest):
    term: str = Field(...)

    @field_validator("term", mode="before")
    @classmethod
    def normalize_term(cls, value):
        if value is None:
            raise ValueError("term is required")

        normalized = " ".join(str(value).split())
        if not normalized:
            raise ValueError("term is required")

        return normalized


class NearbyCityLookupParams(PaginatedRequest):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    per_page: int = Field(5, ge=1, le=25)


class RelevantCityLookupParams(PaginatedRequest):
    per_page: int = Field(5, ge=1, le=25)
