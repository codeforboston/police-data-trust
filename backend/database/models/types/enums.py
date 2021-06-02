"""Enumerations shared across multiple models are defined here."""
import enum


class Gender(enum.Enum):
    UNKNOWN = 1
    MALE = 2
    FEMALE = 3
    # TODO: I don't think these enumerations are all mutually exclusive;
    #  let's circle back at a future date.
    TRANSGENDER = 4


class Race(enum.Enum):
    UNKNOWN = 1
    WHITE = 2
    BLACK_AFRICAN_AMERICAN = 3
    AMERICAN_INDIAN_ALASKA_NATIVE = 4
    ASIAN = 5
    NATIVE_HAWAIIAN_PACIFIC_ISLANDER = 6
