from pydantic import AliasChoices, Field, field_validator

from backend.dto.common_filters import (
    normalize_string_or_list,
    normalize_upper_string_or_list,
    validate_state_code,
)
from backend.dto.common import PaginatedRequest


class SearchQueryParams(PaginatedRequest):
    term: str = Field(
        ...,
        validation_alias=AliasChoices("term", "query"),
    )
    city: str | list[str] | None = None
    city_uid: str | list[str] | None = None
    state: str | list[str] | None = None
    source: str | list[str] | None = None
    source_uid: str | list[str] | None = None

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
        return normalize_string_or_list(value)

    @field_validator("city_uid", mode="before")
    @classmethod
    def normalize_city_uid(cls, value):
        return normalize_string_or_list(value)

    @field_validator("state", mode="before")
    @classmethod
    def normalize_state(cls, value):
        return normalize_upper_string_or_list(value)

    @field_validator("source", mode="before")
    @classmethod
    def normalize_source(cls, value):
        return normalize_string_or_list(value)

    @field_validator("source_uid", mode="before")
    @classmethod
    def normalize_source_uid(cls, value):
        return normalize_string_or_list(value)

    @field_validator("state")
    @classmethod
    def validate_state(cls, value):
        return validate_state_code(value)
