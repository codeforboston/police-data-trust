from pydantic import Field, field_validator

from backend.dto.common import RequestDTO
from backend.dto.common_filters import validate_state_code


class UserContactInfoDTO(RequestDTO):
    additional_emails: list[str] | None = None
    phone_numbers: list[str] | None = None


class UserLocationDTO(RequestDTO):
    city: str | None = None
    state: str | None = None

    @field_validator("state")
    def validate_state(cls, value):
        return validate_state_code(value)


class UserEmploymentDTO(RequestDTO):
    employer: str | None = None
    title: str | None = None


class UserSocialMediaDTO(RequestDTO):
    twitter_url: str | None = None
    facebook_url: str | None = None
    linkedin_url: str | None = None
    instagram_url: str | None = None
    youtube_url: str | None = None
    tiktok_url: str | None = None


class UpdateCurrentUser(RequestDTO):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    primary_email: str | None = None
    contact_info: UserContactInfoDTO | None = None
    website: str | None = None
    location: UserLocationDTO | None = None
    employment: UserEmploymentDTO | None = None
    profile_image: str | None = None
    social_media: UserSocialMediaDTO | None = None


class GetUserParams(RequestDTO):
    include: list[str] | None = Field(
        None,
        description="Related entities to include in the response.",
    )

    @field_validator("include")
    def validate_include(cls, value):
        allowed_includes = {"memberships"}
        if value:
            invalid = set(value) - allowed_includes
            if invalid:
                raise ValueError(
                    f"Invalid include parameters: {', '.join(sorted(invalid))}"
                )
        return value


class UserSuggestionParams(RequestDTO):
    limit: int = Field(
        4,
        ge=1,
        le=20,
        description="Maximum number of suggested people to return.",
    )
