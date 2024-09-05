from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union


class BaseEmployment(BaseModel):
    officer_uid: Optional[str] = Field(None, description="The UID of the officer.")
    agency_uid: Optional[str] = Field(None, description="The UID of the agency the officer is employed by.")
    unit_uid: Optional[str] = Field(None, description="The UID of the unit the officer is assigned to.")
    earliest_employment: Optional[str] = Field(None, description="The earliest date of employment")
    latest_employment: Optional[str] = Field(None, description="The latest date of employment")
    badge_number: Optional[str] = Field(None, description="The badge number of the officer")
    highest_rank: Optional[str] = Field(None, description="The highest rank the officer has held during this employment.")
    commander: Optional[bool] = Field(None, description="Indicates that the officer commanded the unit during this employment.")


class AddEmployment(BaseEmployment, BaseModel):
    officer_uid: Optional[str] = Field(None, description="The UID of the officer.")
    agency_uid: Optional[str] = Field(None, description="The UID of the agency the officer is employed by.")
    unit_uid: Optional[str] = Field(None, description="The UID of the unit the officer is assigned to.")
    earliest_employment: Optional[str] = Field(None, description="The earliest date of employment")
    latest_employment: Optional[str] = Field(None, description="The latest date of employment")
    badge_number: Optional[str] = Field(None, description="The badge number of the officer")
    highest_rank: Optional[str] = Field(None, description="The highest rank the officer has held during this employment.")
    commander: Optional[bool] = Field(None, description="Indicates that the officer commanded the unit during this employment.")


class AddEmploymentFailed(BaseModel):
    agency_uid: Optional[str] = Field(None, description="The uid of the agency that could not be added.")
    reason: Optional[str] = Field(None, description="The reason the employment record could not be added")


class AddEmploymentList(BaseModel):
    agencies: Optional[List[AddEmployment]] = Field(None, description="The units to add to the officer's employment history.")


class Employment(BaseEmployment, BaseModel):
    officer_uid: Optional[str] = Field(None, description="The UID of the officer.")
    agency_uid: Optional[str] = Field(None, description="The UID of the agency the officer is employed by.")
    unit_uid: Optional[str] = Field(None, description="The UID of the unit the officer is assigned to.")
    earliest_employment: Optional[str] = Field(None, description="The earliest date of employment")
    latest_employment: Optional[str] = Field(None, description="The latest date of employment")
    badge_number: Optional[str] = Field(None, description="The badge number of the officer")
    highest_rank: Optional[str] = Field(None, description="The highest rank the officer has held during this employment.")
    commander: Optional[bool] = Field(None, description="Indicates that the officer commanded the unit during this employment.")


class AddEmploymentResponse(BaseModel):
    created: List[Employment] = ...
    failed: List[AddEmploymentFailed] = ...
    total_created: int = ...
    total_failed: int = ...


class EmploymentList(PaginatedResponse, BaseModel):
    results: Optional[List[Employment]] = None


class BaseOfficer(BaseModel):
    first_name: Optional[str] = Field(None, description="First name of the officer")
    middle_name: Optional[str] = Field(None, description="Middle name of the officer")
    last_name: Optional[str] = Field(None, description="Last name of the officer")
    race: Optional[str] = Field(None, description="The race of the officer")
    ethnicity: Optional[str] = Field(None, description="The ethnicity of the officer")
    gender: Optional[str] = Field(None, description="The gender of the officer")
    date_of_birth: Optional[str] = Field(None, description="The date of birth of the officer")
    state_ids: Optional[List[StateId]] = Field(None, description="The state ids of the officer")


class CreateOfficer(BaseOfficer, BaseModel):
    first_name: Optional[str] = Field(None, description="First name of the officer")
    middle_name: Optional[str] = Field(None, description="Middle name of the officer")
    last_name: Optional[str] = Field(None, description="Last name of the officer")
    race: Optional[str] = Field(None, description="The race of the officer")
    ethnicity: Optional[str] = Field(None, description="The ethnicity of the officer")
    gender: Optional[str] = Field(None, description="The gender of the officer")
    date_of_birth: Optional[str] = Field(None, description="The date of birth of the officer")
    state_ids: Optional[List[StateId]] = Field(None, description="The state ids of the officer")


class UpdateOfficer(BaseOfficer, BaseModel):
    first_name: Optional[str] = Field(None, description="First name of the officer")
    middle_name: Optional[str] = Field(None, description="Middle name of the officer")
    last_name: Optional[str] = Field(None, description="Last name of the officer")
    race: Optional[str] = Field(None, description="The race of the officer")
    ethnicity: Optional[str] = Field(None, description="The ethnicity of the officer")
    gender: Optional[str] = Field(None, description="The gender of the officer")
    date_of_birth: Optional[str] = Field(None, description="The date of birth of the officer")
    state_ids: Optional[List[StateId]] = Field(None, description="The state ids of the officer")


class Officer(BaseOfficer, BaseModel):
    first_name: Optional[str] = Field(None, description="First name of the officer")
    middle_name: Optional[str] = Field(None, description="Middle name of the officer")
    last_name: Optional[str] = Field(None, description="Last name of the officer")
    race: Optional[str] = Field(None, description="The race of the officer")
    ethnicity: Optional[str] = Field(None, description="The ethnicity of the officer")
    gender: Optional[str] = Field(None, description="The gender of the officer")
    date_of_birth: Optional[str] = Field(None, description="The date of birth of the officer")
    state_ids: Optional[List[StateId]] = Field(None, description="The state ids of the officer")
    uid: Optional[str] = Field(None, description="The uid of the officer")
    employment_history: Optional[str] = Field(None, description="A link to retrieve the employment history of the officer")
    allegations: Optional[str] = Field(None, description="A link to retrieve the allegations against the officer")
    litigation: Optional[str] = Field(None, description="A link to retrieve the litigation against the officer")


class OfficerList(PaginatedResponse, BaseModel):
    results: Optional[List[Officer]] = None


class StateId(BaseModel):
    uid: Optional[str] = Field(None, description="The UUID of this state id")
    state: Optional[str] = Field(None, description="The state of the state id")
    id_name: Optional[str] = Field(None, description="The name of the id. For example, Tax ID, Driver's License, etc.")
    value: Optional[str] = Field(None, description="The value of the id.")


