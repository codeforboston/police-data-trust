"""Enumerations shared across multiple models are defined here."""
import enum


class Gender(enum.Enum):
    OTHER = 1
    MALE = 2
    FEMALE = 3


class Race(enum.Enum):
    UNKNOWN = 1
    WHITE = 2
    BLACK_AFRICAN_AMERICAN = 3
    AMERICAN_INDIAN_ALASKA_NATIVE = 4
    ASIAN = 5
    NATIVE_HAWAIIAN_PACIFIC_ISLANDER = 6
