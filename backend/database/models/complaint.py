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
)


class RecordType(str, PropertyEnum):
    legal = "legal"
    news = "news"
    government = "government"
    personal = "personal"


# Neo4j Models
class BaseSourceRel(StructuredRel, JsonSerializable):
    record_type = StringProperty(choices=RecordType.choices(), required=True)


class LegalSourceRel(BaseSourceRel):
    court = StringProperty()
    judge = StringProperty()
    docket_number = StringProperty()
    date_of_action = DateProperty()


class NewsSourceRel(BaseSourceRel):
    publication_name = StringProperty()
    publication_date = DateProperty()
    publication_url = StringProperty()
    author = StringProperty()
    author_url = StringProperty()
    author_email = StringProperty()


class GovernmentSourceRel(BaseSourceRel):
    reporting_agency = StringProperty()
    reporting_agency_url = StringProperty()
    reporting_agency_email = StringProperty()


class Complaint(StructuredNode, JsonSerializable):
    uid = UniqueIdProperty()
    record_id = StringProperty()
    category = StringProperty()
    incident_date = DateProperty()
    recieved_date = DateProperty()
    closed_date = DateProperty()
    reason_for_contact = StringProperty()
    outcome_of_contact = StringProperty()

    # Relationships
    source_org = RelationshipFrom("Source", "REPORTED", model=BaseSourceRel)
    location = RelationshipTo("Location", "OCCURRED_AT")
    civlian_witnesses = RelationshipFrom("Civilian", "WITNESSED")
    police_witnesses = RelationshipFrom("Officer", "WITNESSED")
    attachments = RelationshipTo("Attachment", "ATTACHED_TO")
    allegations = RelationshipTo("Allegation", "ALLEGED")
    investigations = RelationshipTo("Investigation", "EXAMINED_BY")
    penalties = RelationshipTo("Penalty", "RESULTS_IN")
    civilian_review_board = RelationshipFrom("CivilianReviewBoard", "REVIEWED")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Complaint {self.uid}>"


class Allegation(StructuredNode):
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
    complainant = RelationshipFrom("Civilian", "COMPLAINED_OF")
    accused = RelationshipFrom("Officer", "ACCUSED_OF")
    complaint = RelationshipFrom("Complaint", "ALLEGED")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Allegation {self.uid}>"


class Investigation(StructuredNode):
    uid = UniqueIdProperty()
    start_date = DateProperty()
    end_date = DateProperty()

    # Relationships
    investigator = RelationshipFrom("Officer", "LED_BY")
    complaint = RelationshipFrom("Complaint", "EXAMINED_BY")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Investigation {self.uid}>"


class Penalty(StructuredNode):
    uid = UniqueIdProperty()
    description = StringProperty()
    date_assessed = DateProperty()

    # Relationships
    officer = RelationshipFrom("Officer", "RECEIVED")
    complaint = RelationshipFrom("Complaint", "RESULTS_IN")

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Penalty {self.uid}>"
