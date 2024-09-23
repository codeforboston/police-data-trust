from backend.database.neo_classes import JsonSerializable
from neomodel import (
    StringProperty,
    UniqueIdProperty,
    StructuredNode
)


class Attachment(JsonSerializable, StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty()
    hash = StringProperty()
    url = StringProperty()
    filetype = StringProperty()
