from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    UniqueIdProperty,
    RelationshipTo,
    RelationshipFrom,
    ZeroOrOne,
)
from neomodel.contrib.spatial_properties import PointProperty


STATE_INFO = {
    "AL": {"name": "Alabama",                  "capital": "Montgomery"},
    "AK": {"name": "Alaska",                   "capital": "Juneau"},
    "AZ": {"name": "Arizona",                  "capital": "Phoenix"},
    "AR": {"name": "Arkansas",                 "capital": "Little Rock"},
    "CA": {"name": "California",               "capital": "Sacramento"},
    "CO": {"name": "Colorado",                 "capital": "Denver"},
    "CT": {"name": "Connecticut",              "capital": "Hartford"},
    "DE": {"name": "Delaware",                 "capital": "Dover"},
    "FL": {"name": "Florida",                  "capital": "Tallahassee"},
    "GA": {"name": "Georgia",                  "capital": "Atlanta"},
    "HI": {"name": "Hawaii",                   "capital": "Honolulu"},
    "ID": {"name": "Idaho",                    "capital": "Boise"},
    "IL": {"name": "Illinois",                 "capital": "Springfield"},
    "IN": {"name": "Indiana",                  "capital": "Indianapolis"},
    "IA": {"name": "Iowa",                     "capital": "Des Moines"},
    "KS": {"name": "Kansas",                   "capital": "Topeka"},
    "KY": {"name": "Kentucky",                 "capital": "Frankfort"},
    "LA": {"name": "Louisiana",                "capital": "Baton Rouge"},
    "ME": {"name": "Maine",                    "capital": "Augusta"},
    "MD": {"name": "Maryland",                 "capital": "Annapolis"},
    "MA": {"name": "Massachusetts",            "capital": "Boston"},
    "MI": {"name": "Michigan",                 "capital": "Lansing"},
    "MN": {"name": "Minnesota",                "capital": "Saint Paul"},
    "MS": {"name": "Mississippi",              "capital": "Jackson"},
    "MO": {"name": "Missouri",                 "capital": "Jefferson City"},
    "MT": {"name": "Montana",                  "capital": "Helena"},
    "NE": {"name": "Nebraska",                 "capital": "Lincoln"},
    "NV": {"name": "Nevada",                   "capital": "Carson City"},
    "NH": {"name": "New Hampshire",            "capital": "Concord"},
    "NJ": {"name": "New Jersey",               "capital": "Trenton"},
    "NM": {"name": "New Mexico",               "capital": "Santa Fe"},
    "NY": {"name": "New York",                 "capital": "Albany"},
    "NC": {"name": "North Carolina",           "capital": "Raleigh"},
    "ND": {"name": "North Dakota",             "capital": "Bismarck"},
    "OH": {"name": "Ohio",                     "capital": "Columbus"},
    "OK": {"name": "Oklahoma",                 "capital": "Oklahoma City"},
    "OR": {"name": "Oregon",                   "capital": "Salem"},
    "PA": {"name": "Pennsylvania",             "capital": "Harrisburg"},
    "RI": {"name": "Rhode Island",             "capital": "Providence"},
    "SC": {"name": "South Carolina",           "capital": "Columbia"},
    "SD": {"name": "South Dakota",             "capital": "Pierre"},
    "TN": {"name": "Tennessee",                "capital": "Nashville"},
    "TX": {"name": "Texas",                    "capital": "Austin"},
    "UT": {"name": "Utah",                     "capital": "Salt Lake City"},
    "VT": {"name": "Vermont",                  "capital": "Montpelier"},
    "VA": {"name": "Virginia",                 "capital": "Richmond"},
    "WA": {"name": "Washington",               "capital": "Olympia"},
    "WV": {"name": "West Virginia",            "capital": "Charleston"},
    "WI": {"name": "Wisconsin",                "capital": "Madison"},
    "WY": {"name": "Wyoming",                  "capital": "Cheyenne"},
    "DC": {"name": "District of Columbia",     "capital": "Washington"},
    "AS": {"name": "American Samoa",           "capital": "Pago Pago"},
    "GU": {"name": "Guam",                     "capital": "Hagatna"},
    "MP": {"name": "Northern Mariana Islands", "capital": "Saipan"},
    "PR": {"name": "Puerto Rico",              "capital": "San Juan"},
    "VI": {"name": "U.S. Virgin Islands",      "capital": "Charlotte Amalie"},
}


class Place(StructuredNode):
    """
    Base class for all places. Adds the 'Place' label to all subclasses.
    """

    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    coordinates = PointProperty(crs="wgs-84")

    def __repr__(self):
        return f"<Place {self.name}>"


class StateNode(Place):
    abbreviation = StringProperty(required=True, unique_index=True)

    # Relationships
    capital = RelationshipTo("CityNode", "HAS_CAPITAL", cardinality=ZeroOrOne)
    counties = RelationshipTo("CountyNode", "HAS_COUNTY")

    def __repr__(self):
        return f"<State {self.name}>"


class CountyNode(Place):
    fips = StringProperty(required=True, unique_index=True)

    # Relationships
    state = RelationshipTo("StateNode", "WITHIN_STATE")
    cities = RelationshipTo("CityNode", "HAS_CITY")

    def __repr__(self):
        return f"<County {self.name}>"


class CityNode(Place):
    population = IntegerProperty()
    sm_id = StringProperty(unique_index=True)  # SimpleMaps ID

    # Relationships
    county = RelationshipTo("CountyNode", "WITHIN_COUNTY")

    def __repr__(self):
        return f"<City {self.name}>"


class PrecinctNode(Place):
    # Relationships
    city = RelationshipFrom("CityNode", "HAS_PRECINCT")

    def __repr__(self):
        return f"<Precinct {self.name}>"
