import enum
from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo,
    DateProperty,
    UniqueIdProperty
)


class LegalCaseType(str, enum.Enum):
    CIVIL = "CIVIL"
    CRIMINAL = "CRIMINAL"

    @classmethod
    def choices(cls):
        return {item.value: item.name for item in cls}


class Litigation(StructuredNode):
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


class Document(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty()
    description = StringProperty()
    url = StringProperty()


class Disposition(StructuredNode):
    description = StringProperty()
    date = DateProperty()
    disposition = StringProperty()