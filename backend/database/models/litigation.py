from backend.schemas import JsonSerializable, PropertyEnum
from backend.database.models.source import Citation
from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo,
    DateProperty,
    UniqueIdProperty
)


class LegalCaseType(str, PropertyEnum):
    CIVIL = "CIVIL"
    CRIMINAL = "CRIMINAL"


class CourtLevel(str, PropertyEnum):
    MUNICIPAL_OR_COUNTY = "Municipal or County"
    STATE_TRIAL = "State Trial Court"
    STATE_INTERMEDIATE_APPELLATE = "State Intermediate Appellate"
    STATE_HIGHEST = "State Highest"
    FEDERAL_DISTRICT = "Federal District"
    FEDERAL_APPELLATE = "Federal Appellate"
    US_SUPREME_COURT = "U.S. Supreme"


class Litigation(StructuredNode, JsonSerializable):
    """
    Represents a legal case or litigation.
    """
    __property_order__ = [
        "uid", "case_type", "case_title", "state",
        "court_name",  "court_level", "jurisdiction",
        "docket_number", "description", "start_date",
        "settlement_date", "settlement_amount",
        "url"
    ]
    __hidden_properties__ = ["citations"]

    uid = UniqueIdProperty()
    case_title = StringProperty()
    docket_number = StringProperty()
    court_name = StringProperty()
    court_level = StringProperty(choices=CourtLevel.choices())
    jurisdiction = StringProperty()
    state = StringProperty()
    description = StringProperty()
    start_date = DateProperty()
    settlement_date = DateProperty()
    settlement_amount = StringProperty()
    url = StringProperty()
    case_type = StringProperty(choices=LegalCaseType.choices())

    # Relationships
    documents = RelationshipTo("Document", "RELATED_TO")
    dispositions = RelationshipTo("Disposition", "YIELDED")
    defendants = RelationshipTo("Officer", "NAMED_IN")
    citations = RelationshipTo(
        'backend.database.models.source.Source', "UPDATED_BY", model=Citation)

    def __repr__(self):
        return f"<Litigation {self.uid}:{self.case_title}>"


class Document(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "title", "description", "url"
    ]

    uid = UniqueIdProperty()
    title = StringProperty()
    description = StringProperty()
    url = StringProperty()


class Disposition(StructuredNode, JsonSerializable):
    description = StringProperty()
    date = DateProperty()
    disposition = StringProperty()
