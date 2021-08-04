from pydantic import BaseModel, EmailStr


class LoginUserDTO(BaseModel):
    email: EmailStr
    password: str
