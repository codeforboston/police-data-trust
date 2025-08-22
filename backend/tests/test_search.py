import urllib.parse
import pytest


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
    res = client.get(f"/api/v1/search/?{query_string}")

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
