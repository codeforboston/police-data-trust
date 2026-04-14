import pytest

from backend.database.models.infra.locations import CityNode, CountyNode, StateNode


@pytest.fixture
def example_city_nodes():
    ny_state = StateNode(name="New York", abbreviation="NY").save()
    il_state = StateNode(name="Illinois", abbreviation="IL").save()

    ny_county = CountyNode(name="New York County", fips="36061").save()
    il_county = CountyNode(name="Sangamon County", fips="17167").save()

    ny_county.state.connect(ny_state)
    il_county.state.connect(il_state)

    springfield_il = CityNode(
        name="Springfield",
        sm_id="springfield-il",
    ).save()
    springfield_ny = CityNode(
        name="Springfield",
        sm_id="springfield-ny",
    ).save()
    new_york = CityNode(
        name="New York",
        sm_id="new-york-ny",
    ).save()

    springfield_il.county.connect(il_county)
    springfield_ny.county.connect(ny_county)
    new_york.county.connect(ny_county)

    return {
        "springfield_il": springfield_il,
        "springfield_ny": springfield_ny,
        "new_york": new_york,
    }


def test_city_lookup_returns_state_context(
    client, access_token, example_city_nodes
):
    res = client.get(
        "/api/v1/locations/cities?term=Springfield",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert len(res.json["results"]) == 2
    assert {row["state"]["abbreviation"] for row in res.json["results"]} == {
        "IL",
        "NY",
    }
    assert {row["sm_id"] for row in res.json["results"]} == {
        "springfield-il",
        "springfield-ny",
    }


def test_city_lookup_filters_by_state(
    client, access_token, example_city_nodes
):
    res = client.get(
        "/api/v1/locations/cities?term=Springfield&state=IL",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert len(res.json["results"]) == 1
    assert res.json["results"][0]["state"]["abbreviation"] == "IL"
    assert res.json["results"][0]["sm_id"] == "springfield-il"


def test_city_lookup_returns_empty_results_when_no_match(
    client, access_token
):
    res = client.get(
        "/api/v1/locations/cities?term=NotARealCity",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert res.json == {
        "results": [],
        "page": 1,
        "per_page": 20,
        "total": 0,
        "pages": 0,
    }


def test_city_lookup_rejects_invalid_state(client, access_token):
    res = client.get(
        "/api/v1/locations/cities?term=Springfield&state=Illinois",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 400
    assert "Invalid state" in res.get_data(as_text=True)


def test_county_lookup_returns_state_context(
    client, access_token, example_city_nodes
):
    res = client.get(
        "/api/v1/locations/counties?term=County",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert len(res.json["results"]) == 2
    assert {row["state"]["abbreviation"] for row in res.json["results"]} == {
        "IL",
        "NY",
    }


def test_county_lookup_filters_by_state(
    client, access_token, example_city_nodes
):
    res = client.get(
        "/api/v1/locations/counties?term=County&state=NY",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert len(res.json["results"]) == 1
    assert res.json["results"][0]["state"]["abbreviation"] == "NY"
    assert res.json["results"][0]["name"] == "New York County"


def test_county_lookup_rejects_invalid_state(client, access_token):
    res = client.get(
        "/api/v1/locations/counties?term=County&state=Illinois",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 400
    assert "Invalid state" in res.get_data(as_text=True)


def test_state_lookup_returns_matching_states(
    client, access_token, example_city_nodes
):
    res = client.get(
        "/api/v1/locations/states?term=New",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert len(res.json["results"]) == 1
    assert res.json["results"][0]["name"] == "New York"
    assert res.json["results"][0]["abbreviation"] == "NY"


def test_state_lookup_matches_abbreviation(
    client, access_token, example_city_nodes
):
    res = client.get(
        "/api/v1/locations/states?term=IL",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert len(res.json["results"]) == 1
    assert res.json["results"][0]["abbreviation"] == "IL"


def test_state_lookup_returns_empty_results_when_no_match(
    client, access_token
):
    res = client.get(
        "/api/v1/locations/states?term=NotARealState",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert res.json == {
        "results": [],
        "page": 1,
        "per_page": 20,
        "total": 0,
        "pages": 0,
    }
