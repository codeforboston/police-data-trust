from backend.database.neo_classes import ExportableNode
from neomodel import (
    StringProperty,
    UniqueIdProperty,
)


class Attachment(ExportableNode):
    uid = UniqueIdProperty()
    title = StringProperty()
    hash = StringProperty()
    url = StringProperty()
    filetype = StringProperty()
