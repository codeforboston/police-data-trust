import pytest
import math
from backend.database import Agency


mock_officers = {
    "severe": {
        "first_name": "Bad",
        "last_name": "Cop",
        "race": "White",
        "ethnicity": "Non-Hispanic",
        "gender": "M",
        "known_employers": []
    },
    "light": {
        "first_name": "Decent",
        "last_name": "Cop",
        "race": "White",
        "ethnicity": "Non-Hispanic",
        "gender": "M",
        "known_employers": []
    },
    "none": {
        "first_name": "Good",
        "last_name": "Cop",
        "race": "White",
        "ethnicity": "Non-Hispanic",
        "gender": "M",
        "known_employers": []
    },
}

mock_agencies = {
    "cpd": {
        "name": "Chicago Police Department",
        "website_url": "https://www.chicagopolice.org/",
        "hq_address": "3510 S Michigan Ave",
        "hq_city": "Chicago",
        "hq_zip": "60653",
        "jurisdiction": "MUNICIPAL"
    },
    "nypd": {
        "name": "New York Police Department",
        "website_url": "https://www1.nyc.gov/site/nypd/index.page",
        "hq_address": "1 Police Plaza",
        "hq_city": "New York",
        "hq_zip": "10038",
        "jurisdiction": "MUNICIPAL"
    }
}


@pytest.fixture
def example_agencies(db_session):
    agencies = {}

    for name, mock in mock_agencies.items():
        db_session.add(Agency(**mock))
        db_session.commit()
        agencies[name] = db_session.query(
            Agency).filter(Agency.name == mock["name"]).first()

    db_session.commit()
    return agencies


def test_create_agency(db_session, client, contributor_access_token):
    test_agency = mock_agencies["cpd"]

    for id, mock in mock_agencies.items():
        res = client.post(
            "/api/v1/agencies/",
            json=mock,
            headers={"Authorization": "Bearer {0}".format(
                contributor_access_token)},
        )
        assert res.status_code == 200

    agency_obj = (
        db_session.query(Agency)
        .filter(Agency.name == test_agency["name"])
        .first()
    )

    assert agency_obj.name == test_agency["name"]
    assert agency_obj.website_url == test_agency["website_url"]
    assert agency_obj.hq_address == test_agency["hq_address"]
    assert agency_obj.hq_city == test_agency["hq_city"]
    assert agency_obj.hq_zip == test_agency["hq_zip"]
    assert agency_obj.jurisdiction == test_agency["jurisdiction"]


def test_unauthorized_create_agency(client, access_token):
    test_agency = mock_agencies["cpd"]

    res = client.post(
        "/api/v1/agencies/",
        json=test_agency,
        headers={"Authorization": "Bearer {0}".format(
            access_token)},
     )
    assert res.status_code == 403


def test_get_agency(client, access_token, example_agency):
    # Test that we can get example_agency
    res = client.get(
        f"/api/v1/agencies/{example_agency.id}",
        headers={"Authorization": "Bearer {0}".format(access_token)})
    assert res.status_code == 200
    assert res.json["name"] == example_agency.name
    assert res.json["website_url"] == example_agency.website_url


def test_get_all_agencies(client, access_token, example_agencies):
    # Create agencies in the database
    agencies = example_agencies

    # Test that we can get agencies
    res = client.get(
        "/api/v1/agencies/",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 200
    assert res.json["results"].__len__() == agencies.__len__()
    test_agency = res.json["results"][0]
    single_res = client.get(
        f"/api/v1/agencies/{test_agency['id']}",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )
    assert test_agency == single_res.json


def test_agency_pagination(client, example_agencies, access_token):
    per_page = 1
    expected_total_pages = math.ceil(len(example_agencies)//per_page)
    actual_ids = set()
    for page in range(1, expected_total_pages + 1):
        res = client.get(
            f"/api/v1/agencies/?per_page={per_page}&page={page}",
            headers={"Authorization": "Bearer {0}".format(access_token)},
        )

        assert res.status_code == 200
        assert res.json["page"] == page
        assert res.json["totalPages"] == expected_total_pages
        assert res.json["totalResults"] == expected_total_pages

        incidents = res.json["results"]
        assert len(incidents) == per_page
        actual_ids.add(incidents[0]["id"])

    assert actual_ids == set(i.id for i in example_agencies.values())

    res = client.get(
        (
            f"/api/v1/agencies/?per_page={per_page}"
            f"&page={expected_total_pages + 1}"
        ),
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 404
