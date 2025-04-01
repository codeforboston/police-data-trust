from backend.schemas import JsonSerializable
from neomodel import StringProperty, UniqueIdProperty, StructuredNode


class Attachment(JsonSerializable, StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty()
    hash = StringProperty()
    url = StringProperty()
    filetype = StringProperty()
