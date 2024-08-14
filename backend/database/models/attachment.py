from neomodel import (
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
)


class Attachment(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty()
    hash = StringProperty()
    url = StringProperty()
    filetype = StringProperty()
