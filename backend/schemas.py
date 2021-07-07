from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from .database.models.incident import Incident
from .database.models.officer import Officer


CreateIncidentSchema = sqlalchemy_to_pydantic(Incident, exclude="id")
IncidentSchema = sqlalchemy_to_pydantic(Incident)

OfficerSchema = sqlalchemy_to_pydantic(Officer, exclude="id")
