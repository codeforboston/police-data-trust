from pydantic import BaseModel, EmailStr
from enum import Enum


class MemberRole(str, Enum):
    ADMIN = "Administrator"
    PUBLISHER = "Publisher"
    MEMBER = "Member"
    SUBSCRIBER = "Subscriber"


class InviteUserDTO(BaseModel):
    partner_id: int
    email: EmailStr
    role:  MemberRole
