from pydantic import Field
from typing import Optional
from backend.dto.common import RequestDTO


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
