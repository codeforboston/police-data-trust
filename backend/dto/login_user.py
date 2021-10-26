from pydantic import BaseModel, EmailStr


class LoginUserDTO(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "test@example.com",
                "password": "password",
            }
        }
