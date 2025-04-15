from neomodel.contrib.spatial_properties import NeomodelPoint
from backend.database.models.location import State, County, City, Place


def test_create_state():
    # Create a State node
    state = State(name="Illinois", abbreviation="IL").save()
    assert state.name == "Illinois"
    assert state.abbreviation == "IL"
    assert repr(state) == "<State Illinois>"


def test_create_county():
    # Create a County node
    county = County(name="Cook County").save()
    assert county.name == "Cook County"
    assert repr(county) == "<County Cook County>"


def test_create_city():
    # Create a City node
    city = City(name="Chicago", population="2.7M").save()
    assert city.name == "Chicago"
    assert city.population == "2.7M"
    assert repr(city) == "<City Chicago>"


def test_relationships():
    # Create a State, County, and City and link them
    state = State(name="Illinois", abbreviation="IL").save()
    county = County(name="Cook County").save()
    city = City(name="Chicago", population="2.7M").save()

    # Create relationships
    state.counties.connect(county)
    county.cities.connect(city)
    state.cities.connect(city)

    # Verify relationships
    assert county in state.counties.all()
    assert city in county.cities.all()
    assert city in state.cities.all()


def test_create_place_with_coordinates():
    coordinates = NeomodelPoint(
        latitude=41.8781, longitude=-87.6298, crs="wgs-84")
    place = Place(name="Chicago", coordinates=coordinates).save()
    assert place.name == "Chicago"
    assert place.coordinates.latitude == 41.8781
    assert place.coordinates.longitude == -87.6298
    assert place.coordinates.crs == "wgs-84"
    assert repr(place) == "<Place Chicago>"


def test_relationships_with_coordinates():
    # Create nodes with spatial coordinates
    state_coordinates = NeomodelPoint(
        latitude=40.6331, longitude=-89.3985, crs="wgs-84")
    county_coordinates = NeomodelPoint(
        latitude=41.7377, longitude=-87.6976, crs="wgs-84")
    city_coordinates = NeomodelPoint(
        latitude=41.8781, longitude=-87.6298, crs="wgs-84")

    state = State(name="Illinois", abbreviation="IL",
                  coordinates=state_coordinates).save()
    county = County(name="Cook County", coordinates=county_coordinates).save()
    city = City(name="Chicago", population="2.7M",
                coordinates=city_coordinates).save()

    # Create relationships
    state.counties.connect(county)
    county.cities.connect(city)
    state.cities.connect(city)

    # Verify relationships
    assert county in state.counties.all()
    assert city in county.cities.all()
    assert city in state.cities.all()

    # Verify spatial data
    assert state.coordinates.latitude == 40.6331
    assert state.coordinates.longitude == -89.3985
    assert county.coordinates.latitude == 41.7377
    assert county.coordinates.longitude == -87.6976
    assert city.coordinates.latitude == 41.8781
