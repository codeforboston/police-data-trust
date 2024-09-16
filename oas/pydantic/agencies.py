from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union


class BaseAgency(BaseModel):
    uid: Optional[str] = Field(None, description="Unique identifier for the agency")
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
    uid: Optional[str] = Field(None, description="Unique identifier for the agency")
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
    uid: Optional[str] = Field(None, description="Unique identifier for the agency")
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
    uid: Optional[str] = Field(None, description="Unique identifier for the agency")
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
    name: str = Field(..., description="Name of the unit")
    website_url: Optional[str] = Field(None, description="Website of the unit")
    phone: Optional[str] = Field(None, description="Phone number of the unit")
    email: Optional[str] = Field(None, description="Email of the unit")
    description: Optional[str] = Field(None, description="Description of the unit")
    address: Optional[str] = Field(None, description="Street address of the unit")
    zip: Optional[str] = Field(None, description="Zip code of the unit")
    date_established: Optional[str] = Field(None, description="The date that this unit was established by its parent agency.")
    commander_uid: Optional[str] = Field(None, description="The UID of the unit's current commander.")


class UpdateUnit(BaseUnit, BaseModel):
    name: Optional[str] = Field(None, description="Name of the unit")
    website_url: Optional[str] = Field(None, description="Website of the unit")
    phone: Optional[str] = Field(None, description="Phone number of the unit")
    email: Optional[str] = Field(None, description="Email of the unit")
    description: Optional[str] = Field(None, description="Description of the unit")
    address: Optional[str] = Field(None, description="Street address of the unit")
    zip: Optional[str] = Field(None, description="Zip code of the unit")
    date_established: Optional[str] = Field(None, description="The date that this unit was established by its parent agency.")
    commander_uid: Optional[str] = Field(None, description="The UID of the unit's current commander.")


class BaseUnit(BaseModel):
    """Base properties for a unit"""
    name: Optional[str] = Field(None, description="Name of the unit")
    website_url: Optional[str] = Field(None, description="Website of the unit")
    phone: Optional[str] = Field(None, description="Phone number of the unit")
    email: Optional[str] = Field(None, description="Email of the unit")
    description: Optional[str] = Field(None, description="Description of the unit")
    address: Optional[str] = Field(None, description="Street address of the unit")
    zip: Optional[str] = Field(None, description="Zip code of the unit")
    date_established: Optional[str] = Field(None, description="The date that this unit was established by its parent agency.")


class Unit(BaseUnit, BaseModel):
    name: Optional[str] = Field(None, description="Name of the unit")
    website_url: Optional[str] = Field(None, description="Website of the unit")
    phone: Optional[str] = Field(None, description="Phone number of the unit")
    email: Optional[str] = Field(None, description="Email of the unit")
    description: Optional[str] = Field(None, description="Description of the unit")
    address: Optional[str] = Field(None, description="Street address of the unit")
    zip: Optional[str] = Field(None, description="Zip code of the unit")
    date_established: Optional[str] = Field(None, description="The date that this unit was established by its parent agency.")
    uid: Optional[str] = Field(None, description="Unique identifier for the unit")
    commander: Optional[Officer] = Field(None, description="The current commander of the unit.")
    commander_history_url: Optional[str] = Field(None, description="-| URL that returns the past commanders of the unit and the period of their respective commands.")
    agency_url: Optional[str] = Field(None, description="URL to get the agency that this unit belongs to.")
    officers_url: Optional[str] = Field(None, description="URL to get a list of officers for this unit.")


class UnitList(PaginatedResponse, BaseModel):
    results: Optional[List[Unit]] = None


class AddOfficer(BaseModel):
    officer_uid: str = Field(..., description="The uid of the officer")
    earliest_employment: Optional[str] = Field(None, description="The earliest date of employment")
    latest_employment: Optional[str] = Field(None, description="The latest date of employment")
    badge_number: str = Field(..., description="The badge number of the officer")
    unit_uid: str = Field(..., description="The UID of the unit the officer is assigned to.")
    highest_rank: Optional[str] = Field(None, description="The highest rank the officer has held during their employment.")
    commander: Optional[bool] = Field(None, description="-| If true, this officer will be added as the commander of the unit for the specified time period.")


class AddOfficerList(BaseModel):
    officers: List[AddOfficer] = ...


class AddOfficerFailed(BaseModel):
    officer_uid: Optional[str] = Field(None, description="The uid of the officer")
    reason: Optional[str] = Field(None, description="The reason the employment record could not be added")


class AddOfficerResponse(BaseModel):
    created: List[Employment] = ...
    failed: List[AddOfficerFailed] = ...
    total_created: int = ...
    total_failed: int = ...


