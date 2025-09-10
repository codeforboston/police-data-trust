"""Define the Classes for Complaints."""
from backend.schemas import JsonSerializable, PropertyEnum, RelQuery
from backend.database.models.source import Citation
from neomodel import (
    StructuredNode,
    StructuredRel,
    StringProperty,
    Relationship,
    RelationshipTo,
    DateProperty,
    UniqueIdProperty,
    One,
    ZeroOrOne
)


class RecordType(str, PropertyEnum):
    legal = "legal"
    news = "news"
    government = "government"
    personal = "personal"


# Neo4j Models
class ComplaintSourceRel(StructuredRel, JsonSerializable):
    uid = UniqueIdProperty()
    record_type = StringProperty(
        choices=RecordType.choices(),
        required=True
    )
    date_published = DateProperty()

    # Legal Source Properties
    court = StringProperty()
    judge = StringProperty()
    docket_number = StringProperty()
    case_event_date = DateProperty()

    # News Source Properties
    publication_name = StringProperty()
    publication_url = StringProperty()
    author = StringProperty()
    author_url = StringProperty()
    author_email = StringProperty()

    # Government Source Properties
    reporting_agency = StringProperty()
    reporting_agency_url = StringProperty()
    reporting_agency_email = StringProperty()


class Location(StructuredNode, JsonSerializable):
    location_type = StringProperty()
    location_description = StringProperty()
    address = StringProperty()
    city = StringProperty()
    state = StringProperty()
    zip = StringProperty()
    administrative_area = StringProperty()
    administrative_area_type = StringProperty()


class Complaint(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "record_id", "category",
        "incident_date", "received_date",
        "closed_date", "reason_for_contact",
        "outcome_of_contact"
    ]

    __hidden_properties__ = ["citations"]
    __virtual_relationships__ = ["allegations", "investigations", "penalties"]

    uid = UniqueIdProperty()
    record_id = StringProperty()
    category = StringProperty()
    incident_date = DateProperty()
    received_date = DateProperty()
    closed_date = DateProperty()
    reason_for_contact = StringProperty()
    outcome_of_contact = StringProperty()

    # Relationships
    source_org = RelationshipTo(
        "backend.database.models.source.Source",
        "HAS_SOURCE", model=ComplaintSourceRel)
    location = RelationshipTo("Location", "OCCURRED_AT", cardinality=One)
    civilian_witnesses = RelationshipTo(
        "backend.database.models.civilian.Civilian", "WITNESSED_BY")
    police_witnesses = RelationshipTo(
        "backend.database.models.officer.Officer", "WITNESSED_BY")
    attachments = RelationshipTo(
        "backend.database.models.attachment.Attachment", "ATTACHED_TO")
    citations = RelationshipTo(
        'backend.database.models.source.Source', "UPDATED_BY", model=Citation)

    @property
    def allegations(self) -> RelQuery:
        """Get the allegations related to this complaint."""
        base = """
        MATCH (c:Complaint {uid: $uid})-[:ALLEGED]-(a:Allegation)
        """
        return RelQuery(self, base, return_alias="a", inflate_cls=Allegation)

    @property
    def investigations(self) -> RelQuery:
        """Get the investigations related to this complaint."""
        base = """
        MATCH (c:Complaint {uid: $uid})-[:EXAMINED_BY]-(i:Investigation)
        """
        return RelQuery(
            self, base, return_alias="i", inflate_cls=Investigation)

    @property
    def penalties(self) -> RelQuery:
        """Get the penalties related to this complaint."""
        base = """
        MATCH (c:Complaint {uid: $uid})-[:RESULTS_IN]-(p:Penalty)
        """
        return RelQuery(self, base, return_alias="p", inflate_cls=Penalty)

    @property
    def complainants(self) -> RelQuery:
        """Get the complainants related to this complaint."""
        from backend.database.models.civilian import Civilian
        base = f"""
        MATCH (c:Complaint {{uid: '{self.uid}'}})-[:ALLEGED]-(:Allegation)-[
        REPORTED_BY]-(civilian:Civilian)
    """
        return RelQuery(self, base, return_alias="civilian",
                        inflate_cls=Civilian, distinct=True)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Complaint {self.uid}>"


class Allegation(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "record_id", "allegation",
        "type", "subtype", "recommended_finding",
        "recommended_outcome", "finding", "outcome"
    ]
    __hidden_properties__ = ["complaint"]

    uid = UniqueIdProperty()
    record_id = StringProperty()
    allegation = StringProperty()
    type = StringProperty()
    subtype = StringProperty()
    recommended_finding = StringProperty()
    recommended_outcome = StringProperty()
    finding = StringProperty()
    outcome = StringProperty()

    # Relationships
    complainant = RelationshipTo(
        "backend.database.models.civilian.Civilian",
        "REPORTED_BY", cardinality=ZeroOrOne)
    accused = Relationship(
        "backend.database.models.officer.Officer",
        "ACCUSED_OF", cardinality=ZeroOrOne)
    complaint = Relationship(
        "backend.database.models.complaint.Complaint",
        "ALLEGED", cardinality=One)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Allegation {self.uid}>"


class Investigation(StructuredNode, JsonSerializable):
    __hidden_properties__ = ["complaint"]
    __property_order__ = ["uid", "start_date", "end_date"]

    uid = UniqueIdProperty()
    start_date = DateProperty()
    end_date = DateProperty()

    # Relationships
    investigator = RelationshipTo(
        "backend.database.models.officer.Officer",
        "LED_BY", cardinality=ZeroOrOne)
    complaint = Relationship("Complaint", "EXAMINED_BY", cardinality=One)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Investigation {self.uid}>"


class Penalty(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "penalty", "date_assessed",
        "crb_plea", "crb_case_status",
        "crb_disposition", "agency_disposition"
    ]
    __hidden_properties__ = ["complaint"]

    uid = UniqueIdProperty()
    penalty = StringProperty()
    date_assessed = DateProperty()
    crb_plea = StringProperty()
    crb_case_status = StringProperty()
    crb_disposition = StringProperty()
    agency_disposition = StringProperty()

    # Relationships
    officer = Relationship(
        "backend.database.models.officer.Officer",
        "RECEIVED", cardinality=One)
    complaint = Relationship("Complaint", "RESULTS_IN", cardinality=One)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Penalty {self.uid}>"
