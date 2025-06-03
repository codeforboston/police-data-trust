from pydantic import BaseModel, Field


class ResetPasswordDTO(BaseModel):
    token: str
    password: str = Field(..., min_length=8)
