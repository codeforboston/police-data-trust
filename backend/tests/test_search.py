import urllib.parse
import pytest

from backend.database.models.agency import Agency, Unit
from backend.database.models.infra.locations import (
    CityNode,
    CountyNode,
    StateNode,
)
from backend.database.models.officer import Officer
from backend.database.models.source import Source
from backend.queries.search import SearchQueries


search_queries = SearchQueries()


@pytest.mark.parametrize(
    ("query", "expected_content"),
    [
        (
            "john",
            "Officer",
        ),
        (
            "Example AND Agency",
            "Agency",
        )
    ],
)
def test_search_text(
        client, db_session, example_officer, example_agency, example_unit,
        access_token, query, expected_content):
    """Test the search results endpoint."""
    params = {
        "query": query,
    }
    if expected_content == "Officer":
        uid = example_officer.uid
        title = example_officer.full_name
    elif expected_content == "Agency":
        uid = example_agency.uid
        title = example_agency.name

    query_string = urllib.parse.urlencode(params)

    # Perform a search query
    res = client.get(
        f"/api/v1/search?{query_string}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    data = res.get_json()
    results = data["results"]
    assert isinstance(results, list)
    assert len(results) > 0
    assert results[0]["uid"] == uid
    assert results[0]["title"] == title
    assert results[0]["content_type"] == expected_content
    assert results[0]["href"].split("/")[-1] == uid
    assert results[0]["source"] == "Example Source"
    assert "last_updated" in results[0]


def test_search_requires_query(client, access_token):
    res = client.get(
        "/api/v1/search",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 400


@pytest.mark.parametrize("query_string", [
    "query=",
    "query=   ",
    "term=   ",
])
def test_search_rejects_blank_query(client, access_token, query_string):
    res = client.get(
        f"/api/v1/search?{query_string}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 400
    assert "Query parameter is required" in res.get_data(as_text=True)


@pytest.mark.parametrize("query_string", [
    "page=0&query=john",
    "per_page=0&query=john",
    "page=-1&query=john",
    "per_page=-1&query=john",
])
def test_search_rejects_invalid_pagination(client, access_token, query_string):
    res = client.get(
        f"/api/v1/search?{query_string}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 400
    assert "greater than or equal to 1" in res.get_data(as_text=True)


def test_search_rejects_unknown_param(client, access_token):
    res = client.get(
        "/api/v1/search?query=john&unknown_param=value",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 400
    assert "Extra inputs are not permitted" in res.get_data(as_text=True)


def test_search_rejects_page_past_end(
        client, db_session, example_officer, access_token):
    res = client.get(
        "/api/v1/search?query=john&per_page=1&page=2",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 400
    assert res.json == {"message": "Page number exceeds total results"}


def test_search_returns_no_results_message(client, access_token):
    res = client.get(
        "/api/v1/search?query=notarealresult",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert res.json == {"message": "No results found matching the query"}


def test_search_accepts_term_alias(
        client, db_session, example_officer, access_token):
    res = client.get(
        "/api/v1/search?term=john",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert res.json["results"][0]["uid"] == example_officer.uid


@pytest.fixture
def example_search_location(example_agency, example_unit):
    state = StateNode(name="New York", abbreviation="NY").save()
    county = CountyNode(name="New York County", fips="36061").save()
    city = CityNode(name="New York").save()
    county.state.connect(state)
    city.county.connect(county)
    example_agency.city_node.connect(city)
    example_unit.city_node.connect(city)
    return city


def test_search_filters_by_city_and_state_for_officers(
        client,
        db_session,
        example_officer,
        example_employment,
        example_search_location,
        access_token):
    res = client.get(
        "/api/v1/search?query=john&city=New%20York&state=NY",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert res.json["results"][0]["uid"] == example_officer.uid


def test_search_filters_by_state_for_agencies(
        client,
        db_session,
        example_agency,
        example_search_location,
        access_token):
    res = client.get(
        "/api/v1/search?query=Example%20Agency&state=NY",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert res.json["results"][0]["uid"] == example_agency.uid


def test_search_filters_by_city_uid_for_agencies(
        client,
        db_session,
        example_agency,
        example_search_location,
        access_token):
    other_city = CityNode(name="Buffalo").save()
    unmatched_agency = Agency(
        name="Example Agency West",
        website_url="www.example-west.com",
        hq_state="NY",
        hq_city="Buffalo",
        hq_address="456 Main St",
        hq_zip="14201",
    ).save()
    unmatched_agency.city_node.connect(other_city)

    res = client.get(
        "/api/v1/search"
        f"?query=Example%20Agency"
        f"&city_uid={example_search_location.uid}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    results = res.json["results"]
    assert [item["uid"] for item in results] == [example_agency.uid]


def test_search_filters_by_multiple_city_uids_for_agencies(
        client,
        db_session,
        example_agency,
        example_search_location,
        access_token):
    other_city = CityNode(name="Buffalo").save()
    other_agency = Agency(
        name="Example Agency West",
        website_url="www.example-west.com",
        hq_state="NY",
        hq_city="Buffalo",
        hq_address="456 Main St",
        hq_zip="14201",
    ).save()
    other_agency.city_node.connect(other_city)

    res = client.get(
        "/api/v1/search"
        f"?query=Example%20Agency"
        f"&city_uid={example_search_location.uid}"
        f"&city_uid={other_city.uid}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    results = res.json["results"]
    result_uids = {item["uid"] for item in results}
    assert result_uids == {example_agency.uid, other_agency.uid}
    uncited_result = next(
        item for item in results if item["uid"] == other_agency.uid
    )
    assert uncited_result["source"] == "Unknown Source"


def test_search_returns_no_results_for_unresolved_location(
        client, access_token):
    res = client.get(
        "/api/v1/search?query=john&city=NotARealCity&state=NY",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert res.json == {"message": "No results found matching the query"}


def test_search_rejects_invalid_state_filter(client, access_token):
    res = client.get(
        "/api/v1/search?query=john&state=New%20York",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 400
    assert "Invalid state" in res.get_data(as_text=True)


def test_search_returns_no_results_for_unknown_city_uid(client, access_token):
    res = client.get(
        "/api/v1/search?query=john&city_uid=not-a-real-city-uid",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert res.json == {"message": "No results found matching the query"}


def test_search_filters_by_source_name(
        client,
        db_session,
        example_officer,
        access_token):
    other_source = Source(name="Another Source", url="www.other.com").save()
    unmatched_officer = Officer(
        first_name="John",
        last_name="Smith",
    ).save()
    unmatched_officer.citations.connect(other_source, {})

    res = client.get(
        "/api/v1/search?query=john&source=Example%20Source",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    results = res.json["results"]
    assert [item["uid"] for item in results] == [example_officer.uid]


def test_search_filters_by_source_uid(
        client,
        db_session,
        example_agency,
        access_token,
        example_source):
    other_source = Source(
        name="Another Agency Source", url="www.other.com"
    ).save()
    unmatched_agency = Agency(
        name="Example Agency West",
        website_url="www.example-west.com",
        hq_state="NY",
        hq_city="Buffalo",
        hq_address="456 Main St",
        hq_zip="14201",
    ).save()
    unmatched_agency.citations.connect(other_source, {})

    res = client.get(
        "/api/v1/search"
        f"?query=Example%20Agency"
        f"&source_uid={example_source.uid}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    results = res.json["results"]
    assert [item["uid"] for item in results] == [example_agency.uid]


def test_search_filters_units_by_source_name(
        client,
        db_session,
        example_unit,
        access_token):
    other_source = Source(
        name="Different Unit Source", url="www.other.com"
    ).save()
    unmatched_unit = Unit(
        name="Precinct 10",
        hq_state="NY",
    ).save()
    unmatched_unit.citations.connect(other_source, {})

    res = client.get(
        "/api/v1/search?query=Precinct&source=Example%20Source",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    results = res.json["results"]
    assert [item["uid"] for item in results] == [example_unit.uid]


def test_search_returns_no_results_for_unknown_source(client, access_token):
    res = client.get(
        "/api/v1/search?query=john&source=NotARealSource",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert res.json == {"message": "No results found matching the query"}


def test_search_returns_no_results_for_unknown_source_uid(client, access_token):
    res = client.get(
        "/api/v1/search?query=john&source_uid=not-a-real-source-uid",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert res.json == {"message": "No results found matching the query"}


def test_search_filters_by_multiple_source_names(
        client,
        db_session,
        example_officer,
        access_token,
        example_source):
    second_source = Source(name="Another Source", url="www.other.com").save()
    second_officer = Officer(
        first_name="John",
        last_name="Smith",
    ).save()
    second_officer.citations.connect(second_source, {})

    res = client.get(
        "/api/v1/search"
        "?query=john"
        "&source=Example%20Source"
        "&source=Another%20Source",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    results = res.json["results"]
    result_uids = {item["uid"] for item in results}
    assert result_uids == {example_officer.uid, second_officer.uid}


def test_search_filters_by_multiple_source_uids(
        client,
        db_session,
        example_agency,
        access_token,
        example_source):
    second_source = Source(
        name="Another Agency Source", url="www.other.com"
    ).save()
    second_agency = Agency(
        name="Example Agency West",
        website_url="www.example-west.com",
        hq_state="NY",
        hq_city="Buffalo",
        hq_address="456 Main St",
        hq_zip="14201",
    ).save()
    second_agency.citations.connect(second_source, {})

    res = client.get(
        "/api/v1/search"
        f"?query=Example%20Agency"
        f"&source_uid={example_source.uid}"
        f"&source_uid={second_source.uid}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    results = res.json["results"]
    result_uids = {item["uid"] for item in results}
    assert result_uids == {example_agency.uid, second_agency.uid}


def test_build_fulltext_query_applies_prefix_wildcards():
    assert search_queries.build_fulltext_query("john doe") == "john* doe*"


def test_build_fulltext_query_strips_reserved_characters():
    assert (
        search_queries.build_fulltext_query("john + doe:unit/test")
        == "john* doe* unit* test*"
    )


def test_build_fulltext_query_drops_boolean_operators():
    assert search_queries.build_fulltext_query(
        "john AND doe OR unit"
    ) == "john* doe* unit*"


def test_build_fulltext_query_rejects_empty_after_sanitizing():
    with pytest.raises(ValueError, match="Query parameter is required"):
        search_queries.build_fulltext_query("AND :::")


def test_tokenize_query_normalizes_terms():
    assert search_queries.tokenize_query("John   Doe") == ["john", "doe"]


def test_tokenize_query_strips_reserved_characters_and_operators():
    assert search_queries.tokenize_query("John + Doe AND unit/test") == [
        "john",
        "doe",
        "unit",
        "test",
    ]
