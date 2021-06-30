from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from .database.models.incident import Incident
from .database.models.officer import Officer


IncidentSchema = sqlalchemy_to_pydantic(Incident)
OfficerSchema = sqlalchemy_to_pydantic(Officer)


IncidentSchema()
