from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from .common import PaginatedResponse

from backend.database.models.types.enums import State, StateIdName, Gender, Ethnicity


class StateId(BaseModel):
    state: State = Field(None, description="The state of the state id")
    id_name: StateIdName = Field(None, description="The name of the id. For example, Tax ID, Driver's License, etc.")
    value: str = Field(None, description="The value of the id.")
    uid: str = Field(None, description="The uid of the state id")


class CreateStateId(BaseModel):
    state: State = Field(None, description="The state of the state id")
    id_name: StateIdName = Field(None, description="The name of the id. For example, Tax ID, Driver's License, etc.")
    value: str = Field(None, description="The value of the id.")

    class Config:
        use_enum_values = True


class BaseEmployment(BaseModel):
    officer_uid: Optional[str] = Field(None, description="The UID of the officer.")
    agency_uid: Optional[str] = Field(None, description="The UID of the agency the officer is employed by.")
    unit_uid: Optional[str] = Field(None, description="The UID of the unit the officer is assigned to.")
    earliest_employment: Optional[str] = Field(None, description="The earliest known date of employment")
    latest_employment: Optional[str] = Field(None, description="The latest known date of employment")
    badge_number: Optional[str] = Field(None, description="The badge number of the officer")
    highest_rank: Optional[str] = Field(None, description="The highest rank the officer has held during this employment.")
    commander: Optional[bool] = Field(None, description="Indicates that the officer commanded the unit during this employment.")


class AddEmployment(BaseEmployment, BaseModel):
    officer_uid: Optional[str] = Field(None, description="The UID of the officer.")
    agency_uid: Optional[str] = Field(None, description="The UID of the agency the officer is employed by.")
    unit_uid: Optional[str] = Field(None, description="The UID of the unit the officer is assigned to.")
    earliest_employment: Optional[str] = Field(None, description="The earliest known date of employment")
    latest_employment: Optional[str] = Field(None, description="The latest known date of employment")
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
    earliest_employment: Optional[str] = Field(None, description="The earliest known date of employment")
    latest_employment: Optional[str] = Field(None, description="The latest known date of employment")
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
    suffix: Optional[str] = Field(None, description="Suffix of the officer's name")
    ethnicity: Optional[Ethnicity] = Field(None, description="The ethnicity of the officer")
    gender: Optional[Gender] = Field(None, description="The gender of the officer")
    date_of_birth: Optional[str] = Field(None, description="The date of birth of the officer")
    state_ids: Optional[List[StateId]] = Field(None, description="The state ids of the officer")


class CreateOfficer(BaseOfficer, BaseModel):
    state_ids: List[CreateStateId] = Field(None, description="The state ids of the officer")
    source_uid: str = Field(None, description="The uid of the source creating this officer")
    first_name: str = Field(None, description="First name of the officer")
    last_name: str = Field(None, description="Last name of the officer")
    middle_name: Optional[str] = Field(None, description="Middle name of the officer")
    suffix: Optional[str] = Field(None, description="Suffix of the officer's name")
    ethnicity: Optional[Ethnicity] = Field(None, description="The ethnicity of the officer")
    gender: Optional[Gender] = Field(None, description="The gender of the officer")
    date_of_birth: Optional[str] = Field(None, description="The date of birth of the officer")

    class Config:
        use_enum_values = True


class UpdateOfficer(BaseOfficer, BaseModel):
    source_uid: str = Field(None, description="The uid of the source updating this officer")
    first_name: Optional[str] = Field(None, description="First name of the officer")
    middle_name: Optional[str] = Field(None, description="Middle name of the officer")
    last_name: Optional[str] = Field(None, description="Last name of the officer")
    suffix: Optional[str] = Field(None, description="Suffix of the officer's name")
    ethnicity: Optional[Ethnicity] = Field(None, description="The ethnicity of the officer")
    gender: Optional[Gender] = Field(None, description="The gender of the officer")
    date_of_birth: Optional[str] = Field(None, description="The date of birth of the officer")
    state_ids: Optional[List[StateId]] = Field(None, description="The state ids of the officer")

    class Config:
        use_enum_values = True


class Officer(BaseOfficer, BaseModel):
    state_ids: List[StateId] = Field(None, description="The state ids of the officer")
    first_name: Optional[str] = Field(None, description="First name of the officer")
    middle_name: Optional[str] = Field(None, description="Middle name of the officer")
    last_name: Optional[str] = Field(None, description="Last name of the officer")
    suffix: Optional[str] = Field(None, description="Suffix of the officer's name")
    ethnicity: Optional[Ethnicity] = Field(None, description="The ethnicity of the officer")
    gender: Optional[Gender] = Field(None, description="The gender of the officer")
    date_of_birth: Optional[str] = Field(None, description="The date of birth of the officer")
    uid: Optional[str] = Field(None, description="The uid of the officer")
    employment_history: Optional[str] = Field(None, description="A link to retrieve the employment history of the officer")
    allegations: Optional[str] = Field(None, description="A link to retrieve the allegations against the officer")
    litigation: Optional[str] = Field(None, description="A link to retrieve the litigation against the officer")


class OfficerList(PaginatedResponse, BaseModel):
    results: List[Officer] = None