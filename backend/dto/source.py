from pydantic import Field
from typing import Optional, List
from backend.dto.common import PaginatedRequest, RequestDTO


class CreatePartner(RequestDTO):
    name: str = Field(None, description="Name of the partner organization.")
    contact_email: str = Field(
        None, description="Contact email for the partner organization.")
    url: Optional[str] = Field(
        None, description="Website URL of the partner.")
    slug: Optional[str] = Field(
        None, description="Slug for the partner organization.")


class UpdateSocialMedia(RequestDTO):
    twitter_url: Optional[str] = Field(
        None, description="Twitter URL of the source.")
    linkedin_url: Optional[str] = Field(
        None, description="LinkedIn URL of the source.")
    facebook_url: Optional[str] = Field(
        None, description="Facebook URL of the source.")
    instagram_url: Optional[str] = Field(
        None, description="Instagram URL of the source.")
    youtube_url: Optional[str] = Field(
        None, description="YouTube URL of the source.")
    tiktok_url: Optional[str] = Field(
        None, description="TikTok URL of the source.")


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
