from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterUserDTO(BaseModel):
    email: EmailStr
    password: str
    firstName: Optional[str]
    lastName: Optional[str]
    phoneNumber: Optional[str]
