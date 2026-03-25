from neomodel.contrib.spatial_properties import NeomodelPoint
from backend.database.models.infra.locations import (
    StateNode, CountyNode, CityNode, Place)


def test_create_state():
    # Create a State node
    state = StateNode(
        name="Illinois", abbreviation="IL", capital="Springfield").save()
    assert state.name == "Illinois"
    assert state.abbreviation == "IL"
    assert state.capital == "Springfield"
    assert repr(state) == "<State Illinois>"


def test_create_county():
    # Create a County node
    county = CountyNode(name="Cook County", fips=17031).save()
    assert county.name == "Cook County"
    assert repr(county) == "<County Cook County>"


def test_create_city():
    # Create a City node
    city = CityNode(name="Chicago", population=2700000).save()
    assert city.name == "Chicago"
    assert city.population == 2700000
    assert repr(city) == "<City Chicago>"


def test_relationships():
    # Create a State, County, and City and link them
    state = StateNode(name="Illinois", abbreviation="IL").save()
    county = CountyNode(name="Cook County", fips=17031).save()
    city = CityNode(name="Chicago", population=2700000).save()

    # Create relationships
    county.state.connect(state)
    city.county.connect(county)

    # Verify relationships
    assert county.state.single() == state
    assert city.county.single() == county


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

    state = StateNode(name="Illinois", abbreviation="IL",
                      coordinates=state_coordinates).save()
    county = CountyNode(name="Cook County", fips=17031,
                        coordinates=county_coordinates).save()
    city = CityNode(name="Chicago", population=2700000,
                    coordinates=city_coordinates).save()

    # Create relationships
    county.state.connect(state)
    city.county.connect(county)

    # Verify relationships
    assert county.state.single() == state
    assert city.county.single() == county

    # Verify spatial data
    assert state.coordinates.latitude == 40.6331
    assert state.coordinates.longitude == -89.3985
    assert county.coordinates.latitude == 41.7377
    assert county.coordinates.longitude == -87.6976
    assert city.coordinates.latitude == 41.8781
