from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union


class BasePartner(BaseModel):
    name: Optional[str] = Field(None, description="Name of the partner organization.")
    url: Optional[str] = Field(None, description="Website URL of the partner.")
    contact_email: Optional[str] = Field(None, description="Contact email for the partner organization.")


class CreatePartner(BasePartner, BaseModel):
    name: Optional[str] = Field(None, description="Name of the partner organization.")
    url: Optional[str] = Field(None, description="Website URL of the partner.")
    contact_email: Optional[str] = Field(None, description="Contact email for the partner organization.")


class UpdatePartner(BasePartner, BaseModel):
    name: Optional[str] = Field(None, description="Name of the partner organization.")
    url: Optional[str] = Field(None, description="Website URL of the partner.")
    contact_email: Optional[str] = Field(None, description="Contact email for the partner organization.")


class Partner(BasePartner, BaseModel):
    name: Optional[str] = Field(None, description="Name of the partner organization.")
    url: Optional[str] = Field(None, description="Website URL of the partner.")
    contact_email: Optional[str] = Field(None, description="Contact email for the partner organization.")
    uid: Optional[str] = Field(None, description="Unique identifier for the partner.")
    members: Optional[str] = Field(None, description="Url to get all members of the partner.")
    reported_incidents: Optional[str] = Field(None, description="Url to get all incidents reported by the partner.")


class PartnerList(PaginatedResponse, BaseModel):
    results: Optional[List[Partner]] = None


class MemberBase(BaseModel):
    partner_uid: Optional[str] = Field(None, description="Unique identifier for the partner.")
    user_uid: Optional[str] = Field(None, description="Unique identifier for the user.")
    role: Optional[str] = Field(None, description="Role of the user.")
    is_active: Optional[bool] = Field(None, description="Whether the user is active.")


class Member(MemberBase, BaseModel):
    partner_uid: Optional[str] = Field(None, description="Unique identifier for the partner.")
    user_uid: Optional[str] = Field(None, description="Unique identifier for the user.")
    role: Optional[str] = Field(None, description="Role of the user.")
    is_active: Optional[bool] = Field(None, description="Whether the user is active.")
    uid: Optional[str] = Field(None, description="Unique identifier for the user.")
    date_joined: Optional[str] = Field(None, description="Date the user joined the partner organizaation.")


class AddMember(MemberBase, BaseModel):
    partner_uid: Optional[str] = Field(None, description="Unique identifier for the partner.")
    user_uid: Optional[str] = Field(None, description="Unique identifier for the user.")
    role: Optional[str] = Field(None, description="Role of the user.")
    is_active: Optional[bool] = Field(None, description="Whether the user is active.")


class MemberList(PaginatedResponse, BaseModel):
    results: Optional[List[Member]] = None


