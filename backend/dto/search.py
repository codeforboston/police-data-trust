from pydantic import AliasChoices, Field, field_validator

from backend.dto.common import PaginatedRequest


class SearchQueryParams(PaginatedRequest):
    term: str = Field(
        ...,
        validation_alias=AliasChoices("term", "query"),
    )

    @field_validator("term", mode="before")
    @classmethod
    def normalize_term(cls, value):
        if value is None:
            raise ValueError("Query parameter is required")

        normalized = " ".join(str(value).split())
        if not normalized:
            raise ValueError("Query parameter is required")

        return normalized
