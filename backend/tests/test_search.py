import urllib.parse


def test_search_text(
        client, db_session, example_officer,
        example_agency, example_unit, access_token):
    """Test the search results endpoint."""
    officer = example_officer
    params = {
        "query": "john"
    }

    query_string = urllib.parse.urlencode(params)

    # Perform a search query
    res = client.get(f"/api/v1/search/?{query_string}")

    assert res.status_code == 200
    data = res.get_json()
    results = data["results"]
    assert isinstance(results, list)
    assert len(results) > 0
    assert results[0]["uid"] == officer.uid
    assert results[0]["title"] == officer.full_name
    assert results[0]["content_type"] == "Officer"
    assert results[0]["href"] == f"/api/v1/officers/{officer.uid}"
    assert results[0]["source"] == "Example Source"
    assert "last_updated" in results[0]
