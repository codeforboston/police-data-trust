from typing import List, Any, Dict, Optional

from sqlalchemy.ext.declarative.api import DeclarativeMeta
from pydantic.main import ModelMetaclass
from pydantic import root_validator
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic


from .database.models.incident import Incident
from .database.models.victim import Victim
from .database.models.incident import Description
from .database.models.tag import Tag
from .database.models.participant import Participant
from .database.models.multimedia import Multimedia
from .database.models.investigation import Investigation
from .database.models.result_of_stop import ResultOfStop
from .database.models.action import Action
from .database.models.use_of_force import UseOfForce
from .database.models.legal_case import LegalCase
from .database.models.officer import Officer
from .database import User


_incident_list_attrs = [
    "victims",
    "officers",
    "descriptions",
    "tags",
    "participants",
    "multimedias",
    "investigations",
    "results_of_stop",
    "actions",
    "use_of_force",
    "legal_case"
]


class _IncidentMixin(BaseModel):
    @root_validator(pre=True)
    def none_to_list(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """For now it makes things easier to handle the many-to-one
        relationships in the schema by allowing for None's, but casting to
        lists prior to validation. In a sense, there is no distinction between
        Optional[List[...]] vs merely List[...].
        """
        values = {**values}  # convert mappings to base dict type.
        for i in _incident_list_attrs:
            if not values.get(i):
                values[i] = []
        return values


def schema_create(model_type: DeclarativeMeta, **kwargs) -> ModelMetaclass:
    return sqlalchemy_to_pydantic(model_type, exclude="id", **kwargs)


_BaseCreateIncidentSchema = schema_create(Incident)
CreateVictimSchema = schema_create(Victim)
CreateOfficerSchema = schema_create(Officer)
CreateDescriptionSchema = schema_create(Description)
CreateTagSchema = schema_create(Tag)
CreateParticipantSchema = schema_create(Participant)
CreateMultimediaSchema = schema_create(Multimedia)
CreateInvestigationSchema = schema_create(Investigation)
CreateResultOfStopSchema = schema_create(ResultOfStop)
CreateActionSchema = schema_create(Action)
CreateUseOfForceSchema = schema_create(UseOfForce)
CreateLegalCaseSchema = schema_create(LegalCase)


class CreateIncidentSchema(_BaseCreateIncidentSchema, _IncidentMixin):
    victims: Optional[List[CreateVictimSchema]]
    officers: Optional[List[CreateOfficerSchema]]
    descriptions: Optional[List[CreateDescriptionSchema]]
    tags: Optional[List[CreateTagSchema]]
    participants: Optional[List[CreateParticipantSchema]]
    multimedias: Optional[List[CreateMultimediaSchema]]
    investigations: Optional[List[CreateInvestigationSchema]]
    results_of_stop: Optional[List[CreateResultOfStopSchema]]
    actions: Optional[List[CreateActionSchema]]
    use_of_force: Optional[List[CreateUseOfForceSchema]]
    legal_case: Optional[List[CreateLegalCaseSchema]]


def schema_get(model_type: DeclarativeMeta, **kwargs) -> ModelMetaclass:
    return sqlalchemy_to_pydantic(model_type, **kwargs)


_BaseIncidentSchema = schema_get(Incident)
VictimSchema = schema_get(Victim)
OfficerSchema = schema_get(Officer)
DescriptionSchema = schema_get(Description)
TagSchema = schema_get(Tag)
ParticipantSchema = schema_get(Participant)
MultimediaSchema = schema_get(Multimedia)
InvestigationSchema = schema_get(Investigation)
ResultOfStopSchema = schema_get(ResultOfStop)
ActionSchema = schema_get(Action)
UseOfForceSchema = schema_get(UseOfForce)
LegalCaseSchema = schema_get(LegalCase)


class IncidentSchema(_BaseIncidentSchema, _IncidentMixin):
    victims: List[VictimSchema]
    officers: List[OfficerSchema]
    descriptions: List[DescriptionSchema]
    tags: List[TagSchema]
    participants: List[ParticipantSchema]
    multimedias: List[MultimediaSchema]
    investigations: List[InvestigationSchema]
    results_of_stop: List[ResultOfStopSchema]
    actions: List[ActionSchema]
    use_of_force: List[UseOfForceSchema]
    legal_case: List[LegalCaseSchema]


UserSchema = sqlalchemy_to_pydantic(User, exclude=["password", "id"])
