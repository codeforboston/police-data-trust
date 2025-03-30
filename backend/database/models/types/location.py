from neomodel import (
    StructuredNode,
    StringProperty,
    UniqueIdProperty,
    RelationshipTo,
    RelationshipFrom,
    One
)
from neomodel.contrib.spatial_properties import PointProperty


class Place(StructuredNode):
    """
    Base class for all places. Adds the 'Place' label to all subclasses.
    """
    uid = UniqueIdProperty()
    name = StringProperty(required=True)  # Common property for all places
    coordinates = PointProperty(crs="wgs-84")  # Spatial property for geographic coordinates

    def __repr__(self):
        return f"<Place {self.name}>"


class State(Place):  
    abbreviation = StringProperty(required=True, unique_index=True)  # e.g., "IL"

    # Relationships
    capital = RelationshipTo("City", "HAS_CAPITAL", cardinality=One)  # A state has one capital city
    counties = RelationshipTo("County", "HAS_COUNTY")  # A state contains multiple counties

    def __repr__(self):
        return f"<State {self.name}>"


class County(Place):  
    # Relationships
    state = RelationshipFrom("State", "HAS_COUNTY")  # A county belongs to a state
    cities = RelationshipTo("City", "HAS_CITY")  # A county contains multiple cities

    def __repr__(self):
        return f"<County {self.name}>"


class City(Place):  
    population = StringProperty()  # Optional: population of the city

    # Relationships
    state = RelationshipFrom("State", "HAS_CAPITAL")  # A city can be the capital of a state
    county = RelationshipFrom("County", "HAS_CITY")  # A city belongs to a county

    def __repr__(self):
        return f"<City {self.name}>"