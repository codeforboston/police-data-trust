from neomodel import (
    StructuredNode,
    # StructuredRel,
    StringProperty,
    UniqueIdProperty,
    RelationshipTo,
    RelationshipFrom,
    One,
)
from neomodel.contrib.spatial_properties import PointProperty


class Place(StructuredNode):
    """
    Base class for all places. Adds the 'Place' label to all subclasses.
    """

    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    coordinates = PointProperty(crs="wgs-84")

    def __repr__(self):
        return f"<Place {self.name}>"


class State(Place):
    abbreviation = StringProperty(required=True, unique_index=True)

    # Relationships
    capital = RelationshipFrom("City", "IS_CAPITAL", cardinality=One)
    cities = RelationshipTo("City", "HAS_CITY")
    counties = RelationshipTo("County", "HAS_COUNTY")

    def __repr__(self):
        return f"<State {self.name}>"


class County(Place):
    # Relationships
    state = RelationshipFrom("State", "HAS_COUNTY")
    cities = RelationshipTo("City", "HAS_CITY")

    def __repr__(self):
        return f"<County {self.name}>"


class City(Place):
    population = StringProperty()

    # Relationships
    state = RelationshipFrom("State", "HAS_CITY")
    county = RelationshipFrom("County", "HAS_CITY")

    def __repr__(self):
        return f"<City {self.name}>"


class Precinct(Place):
    # Relationships
    city = RelationshipFrom("City", "HAS_PRECINCT")

    def __repr__(self):
        return f"<Precinct {self.name}>"
