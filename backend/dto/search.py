from pydantic import AliasChoices, Field, field_validator

from backend.database.models.agency import State
from backend.dto.common import PaginatedRequest


class SearchQueryParams(PaginatedRequest):
    term: str = Field(
        ...,
        validation_alias=AliasChoices("term", "query"),
    )
    city: str | None = None
    state: str | None = None

    @field_validator("term", mode="before")
    @classmethod
    def normalize_term(cls, value):
        if value is None:
            raise ValueError("Query parameter is required")

        normalized = " ".join(str(value).split())
        if not normalized:
            raise ValueError("Query parameter is required")

        return normalized

    @field_validator("city", mode="before")
    @classmethod
    def normalize_city(cls, value):
        if value is None:
            return None

        normalized = " ".join(str(value).split())
        return normalized or None

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
