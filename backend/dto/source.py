from pydantic import Field
from typing import Optional, List
from backend.dto.common import PaginatedRequest, RequestDTO
from backend.dto.contact import UpdateSocialMedia


class CreatePartner(RequestDTO):
    name: str = Field(None, description="Name of the partner organization.")
    contact_email: str = Field(
        None, description="Contact email for the partner organization.")
    url: Optional[str] = Field(
        None, description="Website URL of the partner.")
    slug: Optional[str] = Field(
        None, description="Slug for the partner organization.")


class UpdatePartner(RequestDTO):
    name: Optional[str] = Field(
        None, description="Name of the partner organization.")
    contact_email: Optional[str] = Field(
        None, description="Contact email for the partner organization.")
    url: Optional[str] = Field(
        None, description="Website URL of the partner.")
    slug: Optional[str] = Field(
        None, description="Slug for the partner organization.")
    social_media: Optional[UpdateSocialMedia] = Field(
        None, description="Social media links for the partner organization.")


class SourceFilters(PaginatedRequest):
    name: Optional[str] = Field(
        None, description="Filter by name (case-insensitive, partial match).")
    name__in: Optional[List[str]] = Field(
        None, description="Filter by a list of names (exact match).")
