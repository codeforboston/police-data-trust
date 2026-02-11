from typing import Any
import neo4j
from datetime import date
from neomodel.properties import (
    Property, TOO_MANY_DEFAULTS, validator)


class DateNeo4jFormatProperty(Property):
    """
    Store a date by native neo4j format
    """

    form_field_class = "DateNeo4jFormatField"

    def __init__(self, default_now: bool = False, **kwargs: Any):
        if default_now:
            if "default" in kwargs:
                raise ValueError(TOO_MANY_DEFAULTS)
            kwargs["default"] = date.today()

        self.format = format
        super(DateNeo4jFormatProperty, self).__init__(**kwargs)

    @validator
    def inflate(self, value: Any) -> date:
        return value.to_native()

    @validator
    def deflate(self, value: date) -> neo4j.time.Date:
        if not isinstance(value, date):
            raise ValueError(
                "datetime.date object expected, got {0}.".format(type(value)))
        return neo4j.time.Date.from_native(value)
