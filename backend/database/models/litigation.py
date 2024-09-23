from backend.database.neo_classes import JsonSerializable, PropertyEnum
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


class Litigation(StructuredNode, JsonSerializable):
    uid = UniqueIdProperty()
    case_title = StringProperty()
    docket_number = StringProperty()
    court_level = StringProperty()
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

    def __repr__(self):
        return f"<Litigation {self.uid}:{self.case_title}>"


class Document(StructuredNode, JsonSerializable):
    uid = UniqueIdProperty()
    title = StringProperty()
    description = StringProperty()
    url = StringProperty()


class Disposition(StructuredNode):
    description = StringProperty()
    date = DateProperty()
    disposition = StringProperty()
