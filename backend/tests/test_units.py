from __future__ import annotations
import pytest
from datetime import date
from backend.database import (
    Unit
)


mock_units = {
    "unit_alpha": {
        "name": "Unit Alpha",
        "website_url": "https://agency.gov/unit-alpha",
        "phone": "(555) 123-4567",
        "email": "alpha@agency.gov",
        "description": "Responsible for general investigations \
            and field operations.",
        "address": "100 Alpha Ave",
        "city": "Chicago",
        "state": "MI",
        "zip": "60001",
        "agency_url": "https://agency.gov",
        "officers_url": "https://agency.gov/unit-alpha/officers",
        "date_established": date(2001, 5, 14)
    },
    "unit_bravo": {
        "name": "Unit Bravo",
        "website_url": "https://agency.gov/unit-bravo",
        "phone": "(555) 234-5678",
        "email": "bravo@agency.gov",
        "description": "Handles specialized enforcement and \
            tactical operations.",
        "address": "200 Bravo Blvd",
        "city": "NYC",
        "state": "NY",
        "zip": "75001",
        "agency_url": "https://agency.gov",
        "officers_url": "https://agency.gov/unit-bravo/officers",
        "date_established": date(1998, 9, 3)
    },
    "unit_charlie": {
        "name": "Unit Charlie",
        "website_url": "https://agency.gov/unit-charlie",
        "phone": "(555) 345-6789",
        "email": "charlie@agency.gov",
        "description": "Focuses on community outreach and \
            civilian safety programs.",
        "address": "300 Charlie Rd",
        "city": "Oakridge",
        "state": "OH",
        "zip": "43001",
        "agency_url": "https://agency.gov",
        "officers_url": "https://agency.gov/unit-charlie/officers",
        "date_established": date(2010, 2, 28)
    }
}


@pytest.fixture
def example_units():
    # Create Units in the database
    units = {}
    for name, mock in mock_units.items():
        u = Unit(**mock).save()
        units[name] = u

    # create citation and source
    return units


def test_get_all_units(client, example_units, access_token):
    total_units = Unit.nodes.all().__len__()
    print(f"Total units in DB: {total_units}")

    # Test that we can get all units
    res = client.get(
        "/api/v1/units/",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 200
    assert res.json["results"].__len__() == total_units


def test_get_search_result(client, example_units, access_token):
    expected_ct = Unit.nodes.filter(
        name__icontains='Charlie'
    ).__len__()
    res = client.get(
        "/api/v1/units/?name=Charlie&searchResult=true",
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 200
    assert res.json["results"].__len__() == expected_ct
