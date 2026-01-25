from pydantic import Field, BaseModel, field_validator
from typing import Optional
from backend.dto.common import PaginatedRequest, RequestDTO
from typing import List

class StateIDEEnum():
    """
    Enum for State ID types.
    Includes the types of IDs and the states they are valid in.
    """
    pass


class StateId(RequestDTO):
    state: str = Field(..., description="The state in which the ID is valid.")
    id_name: str = Field(..., description="The name of the state ID.")
    value: str = Field(..., description="The value of the state ID.")
