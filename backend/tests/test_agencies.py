import pytest
import math
from datetime import datetime
from backend.database import Agency
from backend.database.models.infra.locations import CityNode, CountyNode, StateNode
from backend.database.models.source import Source
from neomodel import db

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
        "hq_state": "IL",
        "jurisdiction": "MUNICIPAL"
    },
    "nypd": {
        "name": "New York Police Department",
        "website_url": "https://www1.nyc.gov/site/nypd/index.page",
        "hq_address": "1 Police Plaza",
        "hq_city": "New York",
        "hq_zip": "10038",
        "hq_state": "NY",
        "jurisdiction": "MUNICIPAL"
    },
    "npd": {
        "name": "Newton Police Dept.",
        "website_url": "https://www.newtonma.gov/government/police-department",
        "hq_address": "1321 Washington St.",
        "hq_city": "Newton",
        "hq_zip": "02465",
        "hq_state": "MA",
        "jurisdiction": "MUNICIPAL"
    }
}

new_agency = {
    "name": "New Agency",
    "website_url": "https://www.newagency.com/",
    "hq_address": "123 Main St",
    "hq_city": "New York",
    "hq_zip": "10001",
    "hq_state": "NY",
    "jurisdiction": "MUNICIPAL"
}


@pytest.fixture
def example_agencies(db_session, example_source):
    agencies = {}

    for name, mock in mock_agencies.items():
        a = Agency(**mock).save()
        a.citations.connect(example_source, {
            'timestamp': datetime.now(),
        })
        agencies[name] = a
    return agencies


def test_create_agency(
        db_session,
        client,
        example_source,
        contributor_access_token
):
    test_agency = new_agency.copy()
    test_agency["source_uid"] = example_source.uid

    res = client.post(
        "/api/v1/agencies",
        json=test_agency,
        headers={"Authorization": "Bearer {0}".format(
            contributor_access_token)},
    )
    assert res.status_code == 201

    agency_obj = Agency.nodes.get(uid=res.json["uid"])

    assert agency_obj.name == test_agency["name"]
    assert agency_obj.website_url == test_agency["website_url"]
    assert agency_obj.hq_address == test_agency["hq_address"]
    assert agency_obj.hq_city == test_agency["hq_city"]
    assert agency_obj.hq_zip == test_agency["hq_zip"]
    assert agency_obj.jurisdiction == test_agency["jurisdiction"]


def test_unauthorized_create_agency(client, access_token):
    test_agency = mock_agencies["nypd"]

    res = client.post(
        "/api/v1/agencies",
        json=test_agency,
        headers={"Authorization": "Bearer {0}".format(
            access_token)},
     )
    assert res.status_code == 403


def test_get_agency(client, access_token, example_agency):
    # Test that we can get example_agency
    res = client.get(
        f"/api/v1/agencies/{example_agency.uid}",
        headers={"Authorization": "Bearer {0}".format(access_token)})
    assert res.status_code == 200
    assert res.json["name"] == example_agency.name
    assert res.json["website_url"] == example_agency.website_url


def test_get_all_agencies(client, access_token, example_agencies):
    # Create agencies in the database
    total_agencies = Agency.nodes.all().__len__()

    # Test that we can get agencies
    res = client.get(
        "/api/v1/agencies",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 200
    assert res.json["results"].__len__() == total_agencies


def test_filter_agencies(client, access_token, example_agencies):
    # Test filtering
    expect_name_ct = Agency.nodes.filter(
        name="New York Police Department"
    ).__len__()
    res = client.get(
        "/api/v1/agencies?term=New York Police Department",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 200
    assert res.json['results'].__len__() == expect_name_ct

    expect_city_ct = Agency.nodes.filter(hq_city="Chicago").__len__()
    res = client.get(
        "/api/v1/agencies?hq_city=Chicago",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 200
    assert res.json['results'].__len__() == expect_city_ct

    expect_state_ct = Agency.nodes.filter(hq_state="NY").__len__()
    res = client.get(
        "/api/v1/agencies?hq_state=NY",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 200
    assert res.json['results'].__len__() == expect_state_ct

    # State name not abbreviated correctly
    res = client.get(
        "/api/v1/agencies?hq_state=New York",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 400

    illinois = StateNode(name="Illinois", abbreviation="IL").save()
    new_york_state = StateNode(name="New York", abbreviation="NY").save()
    cook = CountyNode(name="Cook County", fips="17031").save()
    new_york_county = CountyNode(name="New York County", fips="36061").save()
    chicago = CityNode(name="Chicago").save()
    new_york = CityNode(name="New York").save()

    cook.state.connect(illinois)
    new_york_county.state.connect(new_york_state)
    chicago.county.connect(cook)
    new_york.county.connect(new_york_county)
    example_agencies["cpd"].city_node.connect(chicago)
    example_agencies["nypd"].city_node.connect(new_york)

    res = client.get(
        "/api/v1/agencies?state=NY",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 200
    assert [agency["uid"] for agency in res.json["results"]] == [
        example_agencies["nypd"].uid
    ]

    expect_zip_ct = Agency.nodes.filter(hq_zip="60653").__len__()
    res = client.get(
        "/api/v1/agencies?hq_zip=60653",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 200
    assert res.json['results'].__len__() == expect_zip_ct

    # If leading zeroes get coerced anywhere, zip codes will break
    res = client.get(
        "/api/v1/agencies?hq_zip=02465",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 200

    expect_juri_ct = Agency.nodes.filter(jurisdiction="MUNICIPAL").__len__()
    res = client.get(
        "/api/v1/agencies?jurisdiction=MUNICIPAL",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 200
    assert res.json['results'].__len__() == expect_juri_ct

    res = client.get(
        "/api/v1/agencies?jurisdiction=SPACESTATION",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 400


def test_filter_agencies_by_city_uid(
        client, access_token, example_agencies):
    illinois = StateNode(name="Illinois", abbreviation="IL").save()
    new_york_state = StateNode(name="New York", abbreviation="NY").save()
    cook = CountyNode(name="Cook County", fips="17031").save()
    new_york_county = CountyNode(name="New York County", fips="36061").save()
    chicago = CityNode(name="Chicago").save()
    new_york = CityNode(name="New York").save()

    cook.state.connect(illinois)
    new_york_county.state.connect(new_york_state)
    chicago.county.connect(cook)
    new_york.county.connect(new_york_county)
    example_agencies["cpd"].city_node.connect(chicago)
    example_agencies["nypd"].city_node.connect(new_york)

    res = client.get(
        f"/api/v1/agencies?city_uid={chicago.uid}",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )

    assert res.status_code == 200
    assert [agency["uid"] for agency in res.json["results"]] == [
        example_agencies["cpd"].uid
    ]


def test_filter_agencies_by_source_name(
        client, access_token, example_agencies):
    other_source = Source(name="Another Source", url="www.other.com").save()
    other_agency = Agency(
        name="Albany Police Department",
        website_url="https://albany.example.gov",
        hq_address="10 Main St",
        hq_city="Albany",
        hq_zip="12207",
        hq_state="NY",
        jurisdiction="MUNICIPAL",
    ).save()
    other_agency.citations.connect(other_source, {
        "timestamp": datetime.now(),
    })

    res = client.get(
        "/api/v1/agencies?source=Example%20Source",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )

    assert res.status_code == 200
    result_uids = {agency["uid"] for agency in res.json["results"]}
    assert example_agencies["cpd"].uid in result_uids
    assert other_agency.uid not in result_uids


def test_filter_agencies_by_multiple_source_uids(
        client, access_token, example_agencies, example_source):
    other_source = Source(name="Another Source", url="www.other.com").save()
    other_agency = Agency(
        name="Albany Police Department",
        website_url="https://albany.example.gov",
        hq_address="10 Main St",
        hq_city="Albany",
        hq_zip="12207",
        hq_state="NY",
        jurisdiction="MUNICIPAL",
    ).save()
    other_agency.citations.connect(other_source, {
        "timestamp": datetime.now(),
    })

    res = client.get(
        "/api/v1/agencies"
        f"?source_uid={example_source.uid}"
        f"&source_uid={other_source.uid}",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )

    assert res.status_code == 200
    result_uids = {agency["uid"] for agency in res.json["results"]}
    assert example_agencies["cpd"].uid in result_uids
    assert other_agency.uid in result_uids


def test_get_agency_officers(client,
                             example_agency,
                             example_unit,
                             example_employment,
                             access_token):
    query = f"""
                    MATCH (a:Agency)-[]-(u:Unit)-[]-(:Employment)-[]-(o:Officer)
                    WHERE a.uid='{example_agency.uid}'
                    RETURN o
                    """
    cypherres, meta = db.cypher_query(query)
    res = client.get(
        f"/api/v1/agencies/{example_agency.uid}/officers",
        headers={"Authorization": "Bearer {0}".format(access_token)}
    )
    assert res.status_code == 200
    assert res.json['results'].__len__() == len(cypherres)


def test_agency_pagination(client, example_agencies, access_token):
    per_page = 1
    total_agencies = Agency.nodes.all().__len__()
    expected_total_pages = math.ceil(total_agencies//per_page)
    for page in range(1, expected_total_pages + 1):
        res = client.get(
            f"/api/v1/agencies?per_page={per_page}&page={page}",
            headers={"Authorization": "Bearer {0}".format(access_token)},
        )

        assert res.status_code == 200
        assert res.json["page"] == page
        assert res.json["total"] == expected_total_pages

        incidents = res.json["results"]
        assert len(incidents) == per_page

    res = client.get(
        (
            f"/api/v1/agencies?per_page={per_page}"
            f"&page={expected_total_pages + 1}"
        ),
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 400
    assert res.json == {"message": "Page number exceeds total results"}


def test_agency_search_result(client, example_agencies, access_token):
    search_term = "New York"
    expected_ct = Agency.nodes.filter(
        name__icontains=search_term
    ).__len__()

    res = client.get(
        f"/api/v1/agencies?term={search_term}&searchResult=true",
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 200
    assert res.json["results"].__len__() == expected_ct


def test_bad_query_param(client, access_token):
    res = client.get(
        "/api/v1/agencies?unknown_param=value",
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )

    assert "Extra inputs are not permitted" in res.get_data(as_text=True)
    assert res.status_code == 400
