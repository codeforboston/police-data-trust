from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import date


class PaginatedResponse(BaseModel):
    page: Optional[int] = Field(None, description="The current page number.")
    per_page: Optional[int] = Field(None, description="The number of items per page.")
    total: Optional[int] = Field(None, description="The total number of items.")


class Attachment(BaseModel):
    type: Optional[str] = Field(None, description="The filetype of attachment.")
    url: Optional[str] = Field(None, description="The URL of the attachment.")
    title: Optional[str] = Field(None, description="The title of the attachment.")
    description: Optional[str] = Field(
        None, description="A description of the attachment."
    )


class Article(BaseModel):
    url: Optional[str] = Field(None, description="The URL of the article.")
    title: Optional[str] = Field(None, description="The title of the article.")
    publisher: Optional[str] = Field(None, description="The publisher of the article.")
    publication_date: Optional[date] = Field(
        None, description="The date of publication of the article."
    )