"""Define the Classes for Complaints."""
from backend.schemas import JsonSerializable, PropertyEnum
from backend.database.models.source import Citation
from neomodel import (
    StructuredNode,
    StructuredRel,
    StringProperty,
    RelationshipTo,
    RelationshipFrom,
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
    loocation_description = StringProperty()
    address = StringProperty()
    city = StringProperty()
    state = StringProperty()
    zip = StringProperty()
    administrative_area = StringProperty()
    administrative_area_type = StringProperty()


class Complaint(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "record_id", "category",
        "incident_date", "recieved_date",
        "closed_date", "reason_for_contact",
        "outcome_of_contact"
    ]

    __hidden_properties__ = ["citations"]

    uid = UniqueIdProperty()
    record_id = StringProperty()
    category = StringProperty()
    incident_date = DateProperty()
    recieved_date = DateProperty()
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
    allegations = RelationshipTo("Allegation", "ALLEGED")
    investigations = RelationshipTo("Investigation", "EXAMINED_BY")
    penalties = RelationshipTo("Penalty", "RESULTS_IN")
    citations = RelationshipTo(
        'backend.database.models.source.Source', "UPDATED_BY", model=Citation)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Complaint {self.uid}>"


class Allegation(StructuredNode, JsonSerializable):
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
    accused = RelationshipFrom(
        "backend.database.models.officer.Officer",
        "ACCUSED_OF", cardinality=ZeroOrOne)
    complaint = RelationshipFrom(
        "backend.database.models.complaint.Complaint",
        "ALLEGED", cardinality=One)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Allegation {self.uid}>"


class Investigation(StructuredNode, JsonSerializable):
    uid = UniqueIdProperty()
    start_date = DateProperty()
    end_date = DateProperty()

    # Relationships
    investigator = RelationshipTo(
        "backend.database.models.officer.Officer",
        "LED_BY", cardinality=ZeroOrOne)
    complaint = RelationshipFrom("Complaint", "EXAMINED_BY")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Investigation {self.uid}>"


class Penalty(StructuredNode, JsonSerializable):
    uid = UniqueIdProperty()
    penalty = StringProperty()
    date_assessed = DateProperty()
    crb_plea = StringProperty()
    crb_case_status = StringProperty()
    crb_disposition = StringProperty()
    agency_disposition = StringProperty()

    # Relationships
    officer = RelationshipFrom(
        "backend.database.models.officer.Officer",
        "RECEIVED", cardinality=One)
    complaint = RelationshipFrom("Complaint", "RESULTS_IN", cardinality=One)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Penalty {self.uid}>"
