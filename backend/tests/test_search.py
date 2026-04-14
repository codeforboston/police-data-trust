import urllib.parse
import pytest

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
