from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union


class BaseAgency(BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the agency")
    name: Optional[str] = Field(None, description="Name of the agency")
    hq_address: Optional[str] = Field(None, description="Address of the agency")
    hq_city: Optional[str] = Field(None, description="City of the agency")
    hq_state: Optional[str] = Field(None, description="State of the agency")
    hq_zip: Optional[str] = Field(None, description="Zip code of the agency")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction of the agency")
    phone: Optional[str] = Field(None, description="Phone number of the agency")
    email: Optional[str] = Field(None, description="Email of the agency")
    website_url: Optional[str] = Field(None, description="Website of the agency")


class CreateAgency(BaseAgency, BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the agency")
    name: Optional[str] = Field(None, description="Name of the agency")
    hq_address: Optional[str] = Field(None, description="Address of the agency")
    hq_city: Optional[str] = Field(None, description="City of the agency")
    hq_state: Optional[str] = Field(None, description="State of the agency")
    hq_zip: Optional[str] = Field(None, description="Zip code of the agency")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction of the agency")
    phone: Optional[str] = Field(None, description="Phone number of the agency")
    email: Optional[str] = Field(None, description="Email of the agency")
    website_url: Optional[str] = Field(None, description="Website of the agency")


class UpdateAgency(BaseAgency, BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the agency")
    name: Optional[str] = Field(None, description="Name of the agency")
    hq_address: Optional[str] = Field(None, description="Address of the agency")
    hq_city: Optional[str] = Field(None, description="City of the agency")
    hq_state: Optional[str] = Field(None, description="State of the agency")
    hq_zip: Optional[str] = Field(None, description="Zip code of the agency")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction of the agency")
    phone: Optional[str] = Field(None, description="Phone number of the agency")
    email: Optional[str] = Field(None, description="Email of the agency")
    website_url: Optional[str] = Field(None, description="Website of the agency")


class AgencyList(PaginatedResponse, BaseModel):
    results: Optional[List[Agency]] = None


class Agency(BaseAgency, BaseModel):
    id: Optional[str] = Field(None, description="Unique identifier for the agency")
    name: Optional[str] = Field(None, description="Name of the agency")
    hq_address: Optional[str] = Field(None, description="Address of the agency")
    hq_city: Optional[str] = Field(None, description="City of the agency")
    hq_state: Optional[str] = Field(None, description="State of the agency")
    hq_zip: Optional[str] = Field(None, description="Zip code of the agency")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction of the agency")
    phone: Optional[str] = Field(None, description="Phone number of the agency")
    email: Optional[str] = Field(None, description="Email of the agency")
    website_url: Optional[str] = Field(None, description="Website of the agency")
    officers_url: Optional[str] = Field(None, description="URL to get a list of officers for this agency")
    units_url: Optional[str] = Field(None, description="URL to get a list of units for this agency")


class CreateUnit(BaseUnit, BaseModel):
    name: Optional[str] = Field(None, description="Name of the unit")
    website_url: Optional[str] = Field(None, description="Website of the unit")
    phone: Optional[str] = Field(None, description="Phone number of the unit")
    email: Optional[str] = Field(None, description="Email of the unit")
    description: Optional[str] = Field(None, description="Description of the unit")
    address: Optional[str] = Field(None, description="Street address of the unit")
    zip: Optional[str] = Field(None, description="Zip code of the unit")
    commander: Optional[str] = Field(None, description="The Officer UID of the unit's commander")


class UpdateUnit(BaseUnit, BaseModel):
    name: Optional[str] = Field(None, description="Name of the unit")
    website_url: Optional[str] = Field(None, description="Website of the unit")
    phone: Optional[str] = Field(None, description="Phone number of the unit")
    email: Optional[str] = Field(None, description="Email of the unit")
    description: Optional[str] = Field(None, description="Description of the unit")
    address: Optional[str] = Field(None, description="Street address of the unit")
    zip: Optional[str] = Field(None, description="Zip code of the unit")
    commander: Optional[str] = Field(None, description="The Officer UID of the unit's commander")


class BaseUnit(BaseModel):
    """Base properties for a unit"""
    name: Optional[str] = Field(None, description="Name of the unit")
    website_url: Optional[str] = Field(None, description="Website of the unit")
    phone: Optional[str] = Field(None, description="Phone number of the unit")
    email: Optional[str] = Field(None, description="Email of the unit")
    description: Optional[str] = Field(None, description="Description of the unit")
    address: Optional[str] = Field(None, description="Street address of the unit")
    zip: Optional[str] = Field(None, description="Zip code of the unit")
    commander: Optional[str] = Field(None, description="The Officer UID of the unit's commander")


class Unit(BaseUnit, BaseModel):
    name: Optional[str] = Field(None, description="Name of the unit")
    website_url: Optional[str] = Field(None, description="Website of the unit")
    phone: Optional[str] = Field(None, description="Phone number of the unit")
    email: Optional[str] = Field(None, description="Email of the unit")
    description: Optional[str] = Field(None, description="Description of the unit")
    address: Optional[str] = Field(None, description="Street address of the unit")
    zip: Optional[str] = Field(None, description="Zip code of the unit")
    commander: Optional[str] = Field(None, description="The Officer UID of the unit's commander")
    id: Optional[str] = Field(None, description="Unique identifier for the unit")
    agency_url: Optional[str] = Field(None, description="URL to get the agency that this unit belongs to.")
    officers_url: Optional[str] = Field(None, description="URL to get a list of officers for this unit.")


class UnitList(PaginatedResponse, BaseModel):
    results: Optional[List[Unit]] = None


class AddOfficer(BaseModel):
    officer_uid: str = Field(..., description="The id of the officer")
    earliest_employment: Optional[str] = Field(None, description="The earliest date of employment")
    latest_employment: Optional[str] = Field(None, description="The latest date of employment")
    badge_number: str = Field(..., description="The badge number of the officer")
    unit_uid: Optional[str] = Field(None, description="The UID of the unit the officer is assigned to.")
    highest_rank: Optional[str] = Field(None, description="The highest rank the officer has held during their employment.")
    currently_employed: Optional[bool] = Field(None, description="Whether the officer is currently employed by this agency.")


class AddOfficerList(BaseModel):
    officers: List[AddOfficer] = ...


class AddOfficerFailed(BaseModel):
    officer_uid: Optional[str] = Field(None, description="The id of the officer")
    reason: Optional[str] = Field(None, description="The reason the employment record could not be added")


class AddOfficerResponse(BaseModel):
    created: List[Employment] = ...
    failed: List[AddOfficerFailed] = ...
    total_created: int = ...
    total_failed: int = ...


