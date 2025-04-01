from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union


class PaginatedResponse(BaseModel):
    page: Optional[int] = Field(None, description="The current page number.")
    per_page: Optional[int] = Field(
        None, description="The number of items per page."
    )
    total: Optional[int] = Field(None, description="The total number of items.")
