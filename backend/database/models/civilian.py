"""Define the Classes for Civilians."""
from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    RelationshipTo
)


class Civilian(StructuredNode):
    age = IntegerProperty()
    race = StringProperty()
    gender = StringProperty()

    # Relationships
    complaints = RelationshipTo(
        "backend.database.models.complaint.Complaint", "COMPLAINED_OF")
    witnessed_complaints = RelationshipTo(
        "backend.database.models.complaint.Complaint", "WITNESSED")
