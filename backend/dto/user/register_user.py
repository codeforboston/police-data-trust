from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterUserDTO(BaseModel):
    email: EmailStr
    password: str
    firstname: Optional[str]
    lastname: Optional[str]
    phone_number: Optional[str]
