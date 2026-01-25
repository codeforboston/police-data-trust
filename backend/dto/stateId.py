from pydantic import Field, field_validator
from backend.dto.common import RequestDTO
from backend.database.models.types.stateId import StateIdName
from backend.database.models.types.enums import State


class StateId(RequestDTO):
    state: str = Field(..., description="The state in which the ID is valid.")
    id_name: str = Field(..., description="The name of the state ID.")
    value: str = Field(..., description="The value of the state ID.")

    @field_validator("state")
    def validate_state(cls, v):
        if v not in State.choices():
            raise ValueError(f"Invalid state: {v}")
        return v

    @field_validator("id_name")
    def validate_id_name(cls, v):
        if v not in StateIdName.choices():
            raise ValueError(f"Invalid ID name: {v}")
        return v
