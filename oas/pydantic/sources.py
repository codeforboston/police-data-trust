from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union


class BasePartner(BaseModel):
    name: Optional[str] = Field(None, description="Name of the source organization.")
    url: Optional[str] = Field(None, description="Website URL of the source.")
    contact_email: Optional[str] = Field(None, description="Contact email for the source organization.")


class CreatePartner(BasePartner, BaseModel):
    name: Optional[str] = Field(None, description="Name of the source organization.")
    url: Optional[str] = Field(None, description="Website URL of the source.")
    contact_email: Optional[str] = Field(None, description="Contact email for the source organization.")


class UpdatePartner(BasePartner, BaseModel):
    name: Optional[str] = Field(None, description="Name of the source organization.")
    url: Optional[str] = Field(None, description="Website URL of the source.")
    contact_email: Optional[str] = Field(None, description="Contact email for the source organization.")


class Source(BasePartner, BaseModel):
    name: Optional[str] = Field(None, description="Name of the source organization.")
    url: Optional[str] = Field(None, description="Website URL of the source.")
    contact_email: Optional[str] = Field(None, description="Contact email for the source organization.")
    uid: Optional[str] = Field(None, description="Unique identifier for the source.")
    members: Optional[str] = Field(None, description="Url to get all members of the source.")
    reported_complaints: Optional[str] = Field(None, description="Url to get all complaints reported by the source.")


class PartnerList(PaginatedResponse, BaseModel):
    results: Optional[List[Source]] = None


class MemberBase(BaseModel):
    source_uid: Optional[str] = Field(None, description="Unique identifier for the source.")
    user_uid: Optional[str] = Field(None, description="Unique identifier for the user.")
    role: Optional[str] = Field(None, description="Role of the user.")
    is_active: Optional[bool] = Field(None, description="Whether the user is active.")


class Member(MemberBase, BaseModel):
    source_uid: Optional[str] = Field(None, description="Unique identifier for the source.")
    user_uid: Optional[str] = Field(None, description="Unique identifier for the user.")
    role: Optional[str] = Field(None, description="Role of the user.")
    is_active: Optional[bool] = Field(None, description="Whether the user is active.")
    uid: Optional[str] = Field(None, description="Unique identifier for the user.")
    date_joined: Optional[str] = Field(None, description="Date the user joined the source organizaation.")


class AddMember(MemberBase, BaseModel):
    source_uid: Optional[str] = Field(None, description="Unique identifier for the source.")
    user_uid: Optional[str] = Field(None, description="Unique identifier for the user.")
    role: Optional[str] = Field(None, description="Role of the user.")
    is_active: Optional[bool] = Field(None, description="Whether the user is active.")


class MemberList(PaginatedResponse, BaseModel):
    results: Optional[List[Member]] = None


