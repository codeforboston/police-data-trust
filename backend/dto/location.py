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
