# import logging
# from datetime import datetime
# from backend.database.db import db
# from backend.schemas import JsonSerializable
# from neomodel import (
#     StructuredNode,
#     StructuredRel,
#     StringProperty,
#     DateTimeNeo4jFormatProperty,
#     RelationshipTo,
#     StructuredNode,
# )
# from backend.database.models.source import Source

# class Auditable(StructuredNode):
#     """Mixin for models that need created_at and updated_at timestamps."""
#     pass

# class Citation(StructuredNode, JsonSerializable):
#     timestamp = DateTimeNeo4jFormatProperty(
#         default_now=True,
#         index=True
#     )
#     url = StringProperty()
#     diff = StringProperty()

#     # Relationships
#     source = RelationshipTo("backend.database.models.source.Source", "ATTRIBUTED_TO")
#     user = RelationshipTo("backend.database.models.user.User", "AUTHORED_BY")
#     data = RelationshipTo("backend.database.models.citation.Auditable", "MODIFIES")



#     def __repr__(self):
#         """Represent instance as a unique string."""
#         return f"<Citation {self.timestamp}>"


# class HasCitations:
#     """Mix me into a database model to give it citation capabilities."""
#     def __init_subclass__(cls, **kwargs):
#         super().__init_subclass__(**kwargs)
#         if not issubclass(cls, StructuredNode):
#             raise TypeError(
#                 f"{cls.__name__} mixes in HasCitations " +
#                 "but does not inherit StructuredNode"
#             )

#     # Relationships
#     citations = RelationshipTo(
#         'backend.database.models.source.Source', "UPDATED_BY", model=Citation)

#     def add_citation(self, source, user: "User", diff: dict = None):
#         """
#         Add a citation to an item from a source.

#         :param item: The item to add the citation to
#         :param source: The source of the citation
#         :param data: The citation data
#         """
#         context = {k: v for k, v in {
#             "timestamp": datetime.now(),
#             "user_uid": user.uid,
#             "diff": diff
#         }.items() if v is not None}
#         try:
#             self.citations.connect(source, context)
#         except Exception as e:
#             logging.error(f"Error adding citation: {e} to {self.uid}")
#             raise e

#     @property
#     def primary_source(self) -> Source | None:
#         """Get the primary source for this item based on citation scores."""

#         cy = """
#         MATCH (n)-[r:UPDATED_BY]->(s:Source)
#         WHERE elementId(n) = $eid
#         RETURN s
#         ORDER BY r.timestamp DESC
#         LIMIT 1
#         """
#         result, _ = db.cypher_query(cy, {"eid": self.element_id})
#         return Source.inflate(result[0][0]) if result else None

