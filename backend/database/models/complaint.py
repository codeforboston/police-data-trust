"""Define the Classes for Complaints."""
from backend.schemas import JsonSerializable, PropertyEnum
from neomodel import (
    StructuredNode,
    StructuredRel,
    StringProperty,
    RelationshipTo,
    RelationshipFrom,
    DateProperty,
    UniqueIdProperty,
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
    __property_order__ = [
        "location_type", "location_description",
        "address", "city", "state", "zip",
        "responsibility", "responsibility_type"
    ]

    location_type = StringProperty()
    loocation_description = StringProperty()
    address = StringProperty()
    city = StringProperty()
    state = StringProperty()
    zip = StringProperty()
    responsibility = StringProperty()
    responsibility_type = StringProperty()


class Complaint(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "record_id", "category",
        "incident_date", "recieved_date",
        "closed_date", "reason_for_contact",
        "outcome_of_contact"
    ]

    uid = UniqueIdProperty()
    record_id = StringProperty()
    category = StringProperty()
    incident_date = DateProperty()
    recieved_date = DateProperty()
    closed_date = DateProperty()
    reason_for_contact = StringProperty()
    outcome_of_contact = StringProperty()

    # Relationships
    source_org = RelationshipFrom(
        "Source", "REPORTED", model=ComplaintSourceRel)
    location = RelationshipTo("Location", "OCCURRED_AT")
    civlian_witnesses = RelationshipFrom("models.civilian.Civilian", "WITNESSED")
    police_witnesses = RelationshipFrom("Officer", "WITNESSED")
    attachments = RelationshipTo(
        'backend.database.models.attachment.Attachment', "REFERENCED_IN")
    articles = RelationshipTo(
        'backend.database.models.attachment.Article', "MENTIONED_IN")
    allegations = RelationshipTo("Allegation", "ALLEGED")
    investigations = RelationshipTo("Investigation", "EXAMINED_BY")
    penalties = RelationshipTo("Penalty", "RESULTS_IN")
    # civilian_review_board = RelationshipFrom(
    #   "CivilianReviewBoard", "REVIEWED")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Complaint {self.uid}>"


class Allegation(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "record_id", "allegation",
        "type", "subtype", "recommended_finding",
        "recommended_outcome", "finding", "outcome"
    ]

    uid = UniqueIdProperty()
    record_id = StringProperty()
    allegation = StringProperty()
    type = StringProperty()
    subsype = StringProperty()
    recommended_finding = StringProperty()
    recommended_outcome = StringProperty()
    finding = StringProperty()
    outcome = StringProperty()

    # Relationships
    complainant = RelationshipFrom(
        "models.civilian.Civilian", "COMPLAINED_OF", cardinality=ZeroOrOne)
    complaint = RelationshipFrom(
        "Complaint", "ALLEGED", cardinality=ZeroOrOne)
    accused = RelationshipFrom("Officer", "ACCUSED_OF")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Allegation {self.uid}>"


class Investigation(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "start_date", "end_date"
    ]

    uid = UniqueIdProperty()
    start_date = DateProperty()
    end_date = DateProperty()

    # Relationships
    investigator = RelationshipFrom(
        "Officer", "LED_BY", cardinality=ZeroOrOne)
    complaint = RelationshipFrom("Complaint", "EXAMINED_BY")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Investigation {self.uid}>"


class Penalty(StructuredNode, JsonSerializable):
    __property_order__ = [
        "uid", "penalty", "date_assessed",
        "crb_plea", "crb_case_status",
        "crb_disposition", "agency_disposition"
    ]

    uid = UniqueIdProperty()
    penalty = StringProperty()
    date_assessed = DateProperty()
    crb_plea = StringProperty()
    crb_case_status = StringProperty()
    crb_disposition = StringProperty()
    agency_disposition = StringProperty()

    # Relationships
    officer = RelationshipFrom("models.officer.Officer", "RECEIVED")
    complaint = RelationshipFrom("Complaint", "RESULTS_IN")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Penalty {self.uid}>"
