from backend.schemas import JsonSerializable, PropertyEnum, RelQuery
from backend.database.models.source import Citation
from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo,
    RelationshipFrom,
    Relationship,
    DateProperty,
    UniqueIdProperty,
    One,
    db
)


class LegalCaseType(str, PropertyEnum):
    CIVIL = "CIVIL"
    CRIMINAL = "CRIMINAL"


class Litigation(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "case_title", "docket_number",
        "court_level", "jurisdiction", "state",
        "description", "start_date", "settlement_date",
        "settlement_amount", "url", "case_type"
    ]
    __hidden_properties__ = ["citations"]
    __virtual_relationships__ = ["documents", "dispositions"]

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
    defendants = Relationship("Officer", "NAMED_IN")
    citations = RelationshipTo(
        'backend.database.models.source.Source', "UPDATED_BY", model=Citation)

    @property
    def documents(self):
        """
        Returns a list of Document nodes associated with this litigation.
        """
        cy = """
        MATCH (l:Litigation {uid: $uid})-[:HAS_DOCUMENT]->(d:Document)
        RETURN d
        """
        result, meta = db.cypher_query(
            cy, {'uid': self.uid}, resolve_objects=True)
        return result

    @property
    def dispositions(self) -> RelQuery:
        """
        Query the Disposition nodes associated with this litigation.
        """
        base = """
        MATCH (l:Litigation {uid: $uid})-[:DISPOSED_IN]->(d:Disposition)
        """
        return RelQuery(self, base, return_alias="d", inflate_cls=Disposition)

    @property
    def case_type_enum(self) -> LegalCaseType:
        """
        Get the litigation case type as an enum.
        Returns:
            LegalCaseType: The litigation case type as an enum.
        """
        return LegalCaseType(self.case_type) if self.case_type else None

    def __repr__(self):
        return f"<Litigation {self.uid}:{self.case_title}>"


class Document(StructuredNode, JsonSerializable):
    uid = UniqueIdProperty()
    title = StringProperty()
    description = StringProperty()
    url = StringProperty()

    # Relationships
    litigation = Relationship("Litigation", "HAS_DOCUMENT", cardinality=One)


class Disposition(StructuredNode, JsonSerializable):
    description = StringProperty()
    date = DateProperty()
    disposition = StringProperty()

    # Relationships
    litigation = RelationshipFrom("Litigation", "DISPOSED_IN", cardinality=One)
