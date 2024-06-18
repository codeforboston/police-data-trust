import pytest
import math
from backend.database import Agency, AgencySearch
from backend.database.core import db


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
    },
    "nhpd" : {
        "name": "New Haven Police Department",
        "website_url": "https://www.newhavenct.gov/government/ \
                    departments-divisions/new-haven-police-department",
        "hq_address": "1 Union Avenue",
        "hq_city": "New Haven",
        "hq_zip": "06519",
        "jurisdiction": "MUNICIPAL"
    }
}

mock_agency_joined = {
    "pst": {
        "agency_id": 2,
        "agency_name": "Pearson Specter Litt",
        "agency_website_url": "psl.com",
        "agency_hq_address": "123 PSL St",
        "tsv_agency_hq_address": "'123':1 'psl':2 'st':3",
        "agency_hq_city": "Vancouver",
        "tsv_agency_hq_city": "'vancouv':1",
        "agency_hq_zip": "12345",
        "tsv_agency_hq_zip": "'12345':1",
        "agency_jurisdiction": "PRIVATE"
    },
    "us_ag_sd": {
        "agency_id": 3,
        "agency_name": "US AG Southern District",
        "agency_website_url": "ags.com",
        "agency_hq_address": "5th Avenue,Manhattan",
        "tsv_agency_hq_address": "'5th':1 'avenu':2 'manhattan':3",
        "agency_hq_city": "New York",
        "tsv_agency_hq_city": "'new':1 'york':2",
        "agency_hq_zip": "222",
        "tsv_agency_hq_zip": "'222':1",
        "agency_jurisdiction": "STATE"
    },
    "us_ag_ed" : {
        "agency_id": 4,
        "agency_name": "US AG Eastern District",
        "agency_website_url": "ags_south.com",
        "agency_hq_address": "6th Avenue, Albany",
        "tsv_agency_hq_address": "'6th':1 'albani':3 'avenu':2",
        "agency_hq_city": "Albany",
        "tsv_agency_hq_city": "'albani':1",
        "agency_hq_zip": "567",
        "tsv_agency_hq_zip": "'567':1",
        "agency_jurisdiction": "STATE"
    },
    "hs" : {
        "agency_id": 5,
        "agency_name": "Harvey Specter",
        "agency_website_url": "harvey.com",
        "agency_hq_address": "Jane St, Greenwich Village",
        "tsv_agency_hq_address": "'greenwich':3 'jane':1 'st':2 'villag':4",
        "agency_hq_city": "New York",
        "tsv_agency_hq_city": "'new':1 'york':2",
        "agency_hq_zip": "123",
        "tsv_agency_hq_zip": "'123':1",
        "agency_jurisdiction": "STATE"
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


"""
Test function to ensure that Agency based location
search is working correctly.
Supports multiple words in search term
"""


def test_agency_search_location(client, contributor_access_token):
    for name, mock in mock_agency_joined.items():
        db.session.add(AgencySearch(**mock))
        db.session.commit()

    "search when search_term is empty"
    res = client.post(
        "/api/v1/agencies/test_search?per_page=10&page=1&search_term=", # noqa
        json={
        },
        headers={
            "Authorization": "Bearer {0}".format(contributor_access_token)
        },
    )
    assert res.status_code == 200
    assert res.json["results"] == []
    """
    search for Agency at location Jane Street, NY
    """
    res = client.post(
        "/api/v1/agencies/test_search?per_page=10&page=1&search_term=Jane", # noqa
        json={
        },
        headers={
            "Authorization": "Bearer {0}".format(contributor_access_token)
        },
    )
    assert res.status_code == 200
    assert res.json["results"] is not None
    """
    total one results should result
    when search_term is passed with the "Jane"
    as there is one agency located in "Jane Street,
    Greenwich Village"
    """
    query = res.json["results"]
    assert len(query) == 1

    """
    assertions to see if the query results match
    with the expected values
    """
    assert query[0]["name"] == "Harvey Specter"
    assert query[0]["hq_address"] == "Jane St, Greenwich Village"
    assert query[0]["hq_city"] == "New York"
    """
    search for Agency with address starting with 123
    """

    res = client.post(
        "/api/v1/agencies/test_search?per_page=10&page=1&search_term=123", # noqa
        json={
        },
        headers={
            "Authorization": "Bearer {0}".format(contributor_access_token)
        },
    )
    assert res.status_code == 200
    assert res.json["results"] is not None
    """
    total two results should result
    when search_term is passed with the "123"
    as there are two agencies involved with
    "123" as there address
    """
    query = res.json["results"]
    assert len(query) == 2

    """
    assertions to see if the query results match
    with the expected values
    """
    assert query[0]["name"] == "Pearson Specter Litt"
    assert query[0]["hq_address"] == "123 PSL St"
    assert query[0]["hq_zipcode"] == "12345"
    assert query[0]["hq_city"] == "Vancouver"

    assert query[1]["name"] == "Harvey Specter"
    assert query[1]["hq_address"] == "Jane St, Greenwich Village"
    assert query[1]["hq_city"] == "New York"
    assert query[1]["hq_zipcode"] == "123"

    """
    search for Agency with address "New york"
    Ensure two words in search term work
    """

    res = client.post(
        "/api/v1/agencies/test_search?per_page=10&page=1&search_term=New%20york", # noqa
        json={
        },
        headers={
            "Authorization": "Bearer {0}".format(contributor_access_token)
        },
    )
    assert res.status_code == 200
    assert res.json["results"] is not None
    """
    total two results should result
    when search_term is passed with the "New york"
    as there are two agencies involved with
    "New york" as there address
    """
    query = res.json["results"]
    assert len(query) == 2

    """
    assertions to see if the query results match
    with the expected values
    """

    assert query[1]["name"] == "Harvey Specter"
    assert query[1]["hq_address"] == "Jane St, Greenwich Village"
    assert query[1]["hq_city"] == "New York"
    assert query[1]["hq_zipcode"] == "123"

    assert query[0]["name"] == "US AG Southern District"
    assert query[0]["hq_address"] == "5th Avenue,Manhattan"
    assert query[0]["hq_city"] == "New York"
    assert query[0]["hq_zipcode"] == "222"
    """
    search for Agency with address "5th Avenue"
    Ensure two words in search term work
    """

    res = client.post(
        "/api/v1/agencies/test_search?per_page=10&page=1&search_term=5th%20Avenue", # noqa
        json={
        },
        headers={
            "Authorization": "Bearer {0}".format(contributor_access_token)
        },
    )
    assert res.status_code == 200
    assert res.json["results"] is not None
    """
    total two results should result
    when search_term is passed with the "5th Avenue"
    as there are two agencies involved with
    "5th Avenue" as there address
    """
    query = res.json["results"]
    assert len(query) == 2

    """
    assertions to see if the query results match
    with the expected values
    """
    assert query[0]["name"] == "US AG Southern District"
    assert query[0]["hq_address"] == "5th Avenue,Manhattan"
    assert query[0]["hq_city"] == "New York"
    assert query[0]["hq_zipcode"] == "222"

    assert query[1]["name"] == "US AG Eastern District"
    assert query[1]["hq_address"] == "6th Avenue, Albany"
    assert query[1]["hq_city"] == "Albany"
    assert query[1]["hq_zipcode"] == "567"
