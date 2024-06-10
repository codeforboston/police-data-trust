from __future__ import annotations

import textwrap
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, root_validator
from pydantic.main import ModelMetaclass
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from spectree import SecurityScheme, SpecTree
from spectree.models import Server
from sqlalchemy.ext.declarative import DeclarativeMeta

from .database import User
from .database.models.action import Action
from .database.models.partner import Partner, PartnerMember, MemberRole
from .database.models.incident import Incident, SourceDetails
from .database.models.agency import Agency, Jurisdiction
from .database.models.unit import Unit
from .database.models.officer import Officer, StateID
from .database.models.employment import Employment
from .database.models.accusation import Accusation
from .database.models.investigation import Investigation
from .database.models.legal_case import LegalCase
from .database.models.attachment import Attachment
from .database.models.perpetrator import Perpetrator
from .database.models.participant import Participant
from .database.models.result_of_stop import ResultOfStop
from .database.models.tag import Tag
from .database.models.use_of_force import UseOfForce
from .database.models.victim import Victim

spec = SpecTree(
    "flask",
    title="National Police Data Collaborative Index",
    description=textwrap.dedent(
        """
        This API provides federated sharing of police data using a searchable
        index of police records. The index only contains information necessary
        for search and aggregation. NPDC partners contribute to the index while
        maintaining ownership over the full record. Partners can use the API to
        authorize users to access the full records on their systems. This thus
        facilitates federated access control and data ownership.
        """
    ),
    # The version of the API. 0.X.Y is initial development with breaking changes
    # allowed on minor version changes.
    version="0.1.0",
    # Version of the `/apidoc/openapi.json` format
    # https://swagger.io/specification/
    openapi_version="3.0.3",
    # Only document routes decorated with validators
    mode="strict",
    # By default, all routes require either cookie or bearer auth
    security={"cookieAuth": [], "bearerAuth": []},
    servers=[
        Server(
            url="",
            description="This Origin",
        ),
        Server(
            url="https://dev-api.nationalpolicedata.org",
            description="Development environment",
        ),
        Server(
            url="https://stage-api.nationalpolicedata.org",
            description="Staging environment",
        ),
        Server(
            url="https://api.nationalpolicedata.org",
            description="Production environment",
        ),
    ],
    security_schemes=[
        # Cookie auth is used by browsers for GET requests
        SecurityScheme(
            name="cookieAuth",
            data={
                "type": "apiKey",
                "name": "access_token_cookie",
                "in": "cookie",
            },
        ),
        # Bearer auth is used by other API consumers
        SecurityScheme(
            name="bearerAuth",
            data={
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            },
        ),
    ],
)


def validate(auth=True, **kwargs):
    if not auth:
        # Disable security for the route
        kwargs["security"] = {}

    return spec.validate(**kwargs)


_incident_list_attrs = [
    "victims",
    "perpetrators",
    "tags",
    "participants",
    "attachments",
    "investigations",
    "results_of_stop",
    "actions",
    "use_of_force",
    "legal_case",
]

_officer_list_attributes = [
    'employers',
    'agency_association',
    'accusations',
    'perpetrator_association',
    'accusations',
    'state_ids',
]

_agency_list_attributes = [
    'units',
    'officer_association',
    'officers'
]

_unit_list_attributes = [
    'agency',
    'officer_association',
    'officers'
]

_partner_list_attrs = ["reported_incidents"]


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


class _OfficerMixin(BaseModel):
    @root_validator(pre=True)
    def none_to_list(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values = {**values}  # convert mappings to base dict type.
        for i in _officer_list_attributes:
            if not values.get(i):
                values[i] = []
        return values


class _PartnerMixin(BaseModel):
    @root_validator(pre=True)
    def none_to_list(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """For now it makes things easier to handle the many-to-one
        relationships in the schema by allowing for None's, but casting to
        lists prior to validation. In a sense, there is no distinction between
        Optional[List[...]] vs merely List[...].
        """
        values = {**values}  # convert mappings to base dict type.
        for i in _partner_list_attrs:
            if not values.get(i):
                values[i] = []
        return values


class _AgencyMixin(BaseModel):
    @root_validator(pre=True)
    def none_to_list(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values = {**values}  # convert mappings to base dict type.
        for i in _agency_list_attributes:
            if not values.get(i):
                values[i] = []
        return values


class _UnitMixin(BaseModel):
    @root_validator(pre=True)
    def none_to_list(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        values = {**values}  # convert mappings to base dict type.
        for i in _unit_list_attributes:
            if not values.get(i):
                values[i] = []
        return values


def schema_create(model_type: DeclarativeMeta, **kwargs) -> ModelMetaclass:
    return sqlalchemy_to_pydantic(model_type, exclude="id", **kwargs)


_BaseCreatePartnerSchema = schema_create(Partner)
_BaseCreateIncidentSchema = schema_create(Incident)
_BaseCreateOfficerSchema = schema_create(Officer)
_BaseCreateAgencySchema = schema_create(Agency)
_BaseCreateUnitSchema = schema_create(Unit)
CreateStateIDSchema = schema_create(StateID)
CreateEmploymentSchema = schema_create(Employment)
CreateAccusationSchema = schema_create(Accusation)
CreateVictimSchema = schema_create(Victim)
CreatePerpetratorSchema = schema_create(Perpetrator)
CreateSourceDetailsSchema = schema_create(SourceDetails)
CreateTagSchema = schema_create(Tag)
CreateParticipantSchema = schema_create(Participant)
CreateAttachmentSchema = schema_create(Attachment)
CreateInvestigationSchema = schema_create(Investigation)
CreateResultOfStopSchema = schema_create(ResultOfStop)
CreateActionSchema = schema_create(Action)
CreateUseOfForceSchema = schema_create(UseOfForce)
CreateLegalCaseSchema = schema_create(LegalCase)


class CreateIncidentSchema(_BaseCreateIncidentSchema, _IncidentMixin):
    victims: Optional[List[CreateVictimSchema]]
    perpetrators: Optional[List[CreatePerpetratorSchema]]
    tags: Optional[List[CreateTagSchema]]
    participants: Optional[List[CreateParticipantSchema]]
    attachments: Optional[List[CreateAttachmentSchema]]
    investigations: Optional[List[CreateInvestigationSchema]]
    results_of_stop: Optional[List[CreateResultOfStopSchema]]
    actions: Optional[List[CreateActionSchema]]
    use_of_force: Optional[List[CreateUseOfForceSchema]]
    legal_case: Optional[List[CreateLegalCaseSchema]]


class CreatePartnerSchema(_BaseCreatePartnerSchema, _PartnerMixin):
    reported_incidents: Optional[List[_BaseCreateIncidentSchema]]


class CreatePartnerMemberSchema(BaseModel):
    user_id: int
    role: MemberRole
    is_active: Optional[bool] = True


class CreateOfficerSchema(_BaseCreateOfficerSchema, _OfficerMixin):
    agency_association: Optional[List[CreateEmploymentSchema]]
    perpetrator_association: Optional[List[CreateAccusationSchema]]
    state_ids: Optional[List[CreateStateIDSchema]]


class CreateAgencySchema(_BaseCreateAgencySchema, _AgencyMixin):
    name: str
    jurisdiction: str
    website_url: Optional[str]
    hq_address: Optional[str]
    hq_city: Optional[str]
    hq_zip: Optional[str]


class CreateUnitSchema(_BaseCreateUnitSchema, _UnitMixin):
    name: str
    website_url: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    description: Optional[str]
    address: Optional[str]
    zip: Optional[str]
    agency_url: Optional[str]
    officers_url: Optional[str]
    agency_id: int


AddMemberSchema = sqlalchemy_to_pydantic(
    PartnerMember, exclude=["id", "date_joined", "partner", "user"]
)


def schema_get(model_type: DeclarativeMeta, **kwargs) -> ModelMetaclass:
    return sqlalchemy_to_pydantic(model_type, **kwargs)


_BasePartnerSchema = schema_get(Partner)
_BaseIncidentSchema = schema_get(Incident)
_BaseOfficerSchema = schema_get(Officer)
_BasePartnerMemberSchema = schema_get(PartnerMember)
_BaseAgencySchema = schema_get(Agency)
_BaseUnitSchema = schema_get(Unit)
VictimSchema = schema_get(Victim)
PerpetratorSchema = schema_get(Perpetrator)
TagSchema = schema_get(Tag)
ParticipantSchema = schema_get(Participant)
AttachmentSchema = schema_get(Attachment)
InvestigationSchema = schema_get(Investigation)
ResultOfStopSchema = schema_get(ResultOfStop)
ActionSchema = schema_get(Action)
UseOfForceSchema = schema_get(UseOfForce)
LegalCaseSchema = schema_get(LegalCase)
EmploymentSchema = schema_get(Employment)
UserSchema = schema_get(User, exclude=["password", "id"])


class PartnerMemberSchema(_BasePartnerMemberSchema):
    user: UserSchema


class IncidentSchema(_BaseIncidentSchema, _IncidentMixin):
    victims: List[VictimSchema]
    perpetrators: List[PerpetratorSchema]
    tags: List[TagSchema]
    participants: List[ParticipantSchema]
    attachments: List[AttachmentSchema]
    investigations: List[InvestigationSchema]
    results_of_stop: List[ResultOfStopSchema]
    actions: List[ActionSchema]
    use_of_force: List[UseOfForceSchema]
    legal_case: List[LegalCaseSchema]


class OfficerSchema(_BaseOfficerSchema, _OfficerMixin):
    agency_association: List[CreateEmploymentSchema]
    perpetrator_association: List[CreateAccusationSchema]
    state_ids: List[CreateStateIDSchema]


class AgencySchema(_BaseAgencySchema, _AgencyMixin):
    units: List[CreateUnitSchema]
    officer_association: List[CreateEmploymentSchema]


class UnitSchema(_BaseUnitSchema):
    officer_association: List[CreateEmploymentSchema]


class PartnerSchema(_BasePartnerSchema, _PartnerMixin):
    reported_incidents: List[IncidentSchema]


def incident_to_orm(incident: CreateIncidentSchema) -> Incident:
    """Convert the JSON incident into an ORM instance

    pydantic-sqlalchemy only handles ORM -> JSON conversion, not the other way
    around. sqlalchemy won't convert nested dictionaries into the corresponding
    ORM types, so we need to manually perform the JSON -> ORM conversion. We can
    roll our own recursive conversion if we can get the ORM model class
    associated with a schema instance.
    """

    converters = {"perpetrators": Perpetrator, "use_of_force": UseOfForce}
    orm_attrs = incident.dict()
    for k, v in orm_attrs.items():
        is_dict = isinstance(v, dict)
        is_list = isinstance(v, list)
        if is_dict:
            orm_attrs[k] = converters[k](**v)
        elif is_list and len(v) > 0:
            orm_attrs[k] = [converters[k](**d) for d in v]
    return Incident(**orm_attrs)


def incident_orm_to_json(incident: Incident) -> dict[str, Any]:
    return IncidentSchema.from_orm(incident).dict(
        exclude_none=True,
        # Exclude a bunch of currently-unused empty lists
        exclude={
            "actions",
            "investigations",
            "legal_case",
            "participants",
            "results_of_stop",
            "tags",
            "victims",
        },
    )


def officer_to_orm(officer: CreateOfficerSchema) -> Officer:
    """Convert the JSON officer into an ORM instance

    pydantic-sqlalchemy only handles ORM -> JSON conversion, not the other way
    around. sqlalchemy won't convert nested dictionaries into the corresponding
    ORM types, so we need to manually perform the JSON -> ORM conversion. We can
    roll our own recursive conversion if we can get the ORM model class
    associated with a schema instance.
    """

    converters = {
        "state_ids": StateID,
        "agency_association": Employment,
    }
    try:
        orm_attrs = officer.dict()
    except Exception:
        raise Exception(f"Error creating dict from officer: {officer}")
    try:
        for k, v in orm_attrs.items():
            is_dict = isinstance(v, dict)
            is_list = isinstance(v, list)
            if is_dict:
                orm_attrs[k] = converters[k](**v)
            elif is_list and len(v) > 0:
                orm_attrs[k] = [converters[k](**d) for d in v]
    except Exception:
        raise Exception(f"Error converting {k}, {v}")
    return Officer(**orm_attrs)


def officer_orm_to_json(officer: Officer) -> dict:
    return OfficerSchema.from_orm(officer).dict(
        exclude_none=True,
        # Exclude a bunch of currently-unused empty lists
    )


def agency_to_orm(agency: CreateAgencySchema) -> Agency:
    """Convert the JSON agency into an ORM instance"""
    try:
        converters = {
            "jurisdiction": Jurisdiction
        }
        orm_attrs = agency.dict()
        for k, v in orm_attrs.items():
            is_dict = isinstance(v, dict)
            is_list = isinstance(v, list)
            if is_dict:
                orm_attrs[k] = converters[k](**v)
            elif is_list and len(v) > 0:
                orm_attrs[k] = [converters[k](**d) for d in v]
        return Agency(**orm_attrs)
    except Exception as e:
        raise e


def agency_orm_to_json(agency: Agency) -> dict:
    return AgencySchema.from_orm(agency).dict(
        exclude_none=True,
    )


def unit_to_orm(unit: CreateUnitSchema) -> Unit:
    """Convert the JSON unit into an ORM instance"""
    orm_attrs = unit.dict()
    return Unit(**orm_attrs)


def unit_orm_to_json(unit: Unit) -> dict:
    return UnitSchema.from_orm(unit).dict(
        exclude_none=True,
    )


def employment_to_orm(employment: CreateEmploymentSchema) -> Employment:
    """Convert the JSON employment into an ORM instance"""
    orm_attrs = employment.dict()
    return Employment(**orm_attrs)


def employment_orm_to_json(employment: Employment) -> Dict[str, Any]:
    return EmploymentSchema.from_orm(employment).dict(
        exclude_none=True,
    )


def partner_to_orm(partner: CreatePartnerSchema) -> Partner:
    """Convert the JSON partner into an ORM instance

    pydantic-sqlalchemy only handles ORM -> JSON conversion, not the other way
    around. sqlalchemy won't convert nested dictionaries into the corresponding
    ORM types, so we need to manually perform the JSON -> ORM conversion. We can
    roll our own recursive conversion if we can get the ORM model class
    associated with a schema instance.
    """

    converters = {"reported_incidents": Incident}
    orm_attrs = partner.dict()
    for k, v in orm_attrs.items():
        is_dict = isinstance(v, dict)
        is_list = isinstance(v, list)
        if is_dict:
            orm_attrs[k] = converters[k](**v)
        elif is_list and len(v) > 0:
            orm_attrs[k] = [converters[k](**d) for d in v]
    return Partner(**orm_attrs)


def partner_orm_to_json(partner: Partner) -> dict:
    return PartnerSchema.from_orm(partner).dict(
        exclude_none=True,
    )


def partner_member_to_orm(
    partner_member: CreatePartnerMemberSchema,
) -> PartnerMember:
    """Convert the JSON partner member into an ORM instance"""
    orm_attrs = partner_member.dict()
    return PartnerMember(**orm_attrs)


def partner_member_orm_to_json(partner_member: PartnerMember) -> Dict[str, Any]:
    return PartnerMemberSchema.from_orm(partner_member).dict(
        exclude_none=True,
    )


def user_orm_to_json(user: User) -> Dict[str, Any]:
    return UserSchema.from_orm(user).dict(
        exclude={
            "password",
            "email_confirmed_at",
        }
    )
