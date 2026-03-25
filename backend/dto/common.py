from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date


class RequestDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PaginatedRequest(RequestDTO):
    page: Optional[int] = Field(
        1, ge=1, description="The requested page number.")
    per_page: Optional[int] = Field(
        20, ge=1, description="The requested number of items per page.")

    @property
    def skip(self):
        return (self.page - 1) * self.per_page

    @property
    def limit(self):
        return self.per_page


class PaginatedResponse(BaseModel):
    page: Optional[int] = Field(None, description="The current page number.")
    per_page: Optional[int] = Field(
        None, description="The number of items per page.")
    total: Optional[int] = Field(None, description="The total number of items.")


class Attachment(BaseModel):
    filetype: Optional[str] = Field(
        None, description="The filetype of attachment.")
    url: Optional[str] = Field(
        None, description="The URL of the attachment.")
    title: Optional[str] = Field(
        None, description="The title of the attachment.")


class Article(BaseModel):
    url: Optional[str] = Field(
        None, description="The URL of the article.")
    title: Optional[str] = Field(
        None, description="The title of the article.")
    publisher: Optional[str] = Field(
        None, description="The publisher of the article.")
    publication_date: Optional[date] = Field(
        None, description="The date of publication of the article."
    )
