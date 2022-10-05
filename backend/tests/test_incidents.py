from datetime import datetime

import pytest
from backend.database import Incident, Source

mock_incidents = {
    "domestic": {
        "time_of_incident": "2021-03-14 01:05:09",
        "description": "Domestic disturbance",
        "officers": [
            {"first_name": "Susie", "last_name": "Suserson"},
            {"first_name": "Lisa", "last_name": "Wong"},
        ],
        "use_of_force": [{"item": "Injurious restraint"}],
        "source": "cpdp",
        "location": "123 Right St Chicago, IL",
    },
    "traffic": {
        "time_of_incident": "2021-10-01 00:00:00",
        "description": "Traffic stop",
        "officers": [
            {"first_name": "Ronda", "last_name": "Sousa"},
        ],
        "use_of_force": [{"item": "verbalization"}],
        "source": "mpv",
        "location": "Park St and Boylston Boston",
    },
    "firearm": {
        "time_of_incident": "2021-10-05 00:00:00",
        "description": "Robbery",
        "officers": [
            {"first_name": "Dale", "last_name": "Green"},
        ],
        "use_of_force": [{"item": "indirect firearm"}],
        "source": "cpdp",
        "location": "CHICAGO ILLINOIS",
    },
    "missing_fields": {
        "description": "Robbery",
        "officers": [
            {"first_name": "Dale", "last_name": "Green"},
        ],
        "source": "cpdp",
    },
}

mock_sources = {
    "cpdp": {"publication_name": "chicago police data project"},
    "mpv": {"publication_name": "Mapping Police Violence"},
}


@pytest.fixture
def example_incidents(db_session, client, access_token):
    for id, mock in mock_sources.items():
        db_session.add(Source(id=id, **mock))
        db_session.commit()

    created = {}
    for name, mock in mock_incidents.items():
        res = client.post(
            "/api/v1/incidents/create",
            json=mock,
            headers={"Authorization": "Bearer {0}".format(access_token)},
        )
        assert res.status_code == 200
        created[name] = res.json
    return created


def test_create_incident(db_session, example_incidents):
    expected = mock_incidents["domestic"]
    created = example_incidents["domestic"]

    incident_obj = (
        db_session.query(Incident).filter(Incident.id == created["id"]).first()
    )

    assert incident_obj.time_of_incident == datetime(2021, 3, 14, 1, 5, 9)
    for i in [0, 1]:
        assert incident_obj.officers[i].id == created["officers"][i]["id"]
    assert incident_obj.use_of_force[0].id == created["use_of_force"][0]["id"]
    assert incident_obj.source == expected["source"]


def test_get_incident(app, client, db_session, access_token):
    # Create an incident in the database
    incident_date = datetime(1969, 7, 16, 13, 32, 0)
    incident_date_str = app.json_encoder().encode(incident_date)[1:-1]

    obj = Incident(time_of_incident=incident_date)
    db_session.add(obj)
    db_session.commit()

    # Test that we can get it
    res = client.get(f"/api/v1/incidents/get/{obj.id}")
    assert res.json["time_of_incident"] == incident_date_str


@pytest.mark.parametrize(
    ("query", "expected_incident_names"),
    [
        (
            {},
            ["domestic", "traffic", "firearm", "missing_fields"],
        ),
        (
            {"location": "Chicago"},
            ["domestic", "firearm"],
        ),
        (
            {
                "startTime": "2021-09-30 00:00:00",
                "endTime": "2021-10-02 00:00:00",
            },
            ["traffic"],
        ),
        (
            {
                "description": "traffic",
            },
            ["traffic"],
        ),
    ],
)
def test_search_incidents(
    client, example_incidents, access_token, query, expected_incident_names
):
    res = client.post(
        "/api/v1/incidents/search",
        json=query,
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 200

    # Match the results to the known dataset and assert that all the expected
    # results are present
    actual_incidents = res.json["results"]

    def incident_name(incident):
        return next(
            (
                k
                for k, v in example_incidents.items()
                if v["id"] == incident["id"]
            ),
            None,
        )

    actual_incident_names = list(
        filter(None, map(incident_name, actual_incidents))
    )
    assert set(actual_incident_names) == set(expected_incident_names)

    assert res.json["page"] == 1
    assert res.json["totalPages"] == 1
    assert res.json["totalResults"] == len(expected_incident_names)


def test_pagination(client, example_incidents, access_token):
    per_page = 1
    expected_total_pages = len(example_incidents)
    actual_ids = set()
    for page in range(1, expected_total_pages + 1):
        res = client.post(
            "/api/v1/incidents/search",
            json={"perPage": per_page, "page": page},
            headers={"Authorization": "Bearer {0}".format(access_token)},
        )

        assert res.status_code == 200
        assert res.json["page"] == page
        assert res.json["totalPages"] == expected_total_pages
        assert res.json["totalResults"] == expected_total_pages

        incidents = res.json["results"]
        assert len(incidents) == per_page
        actual_ids.add(incidents[0]["id"])

    assert actual_ids == set(i["id"] for i in example_incidents.values())

    res = client.post(
        "/api/v1/incidents/search",
        json={"perPage": per_page, "page": expected_total_pages + 1},
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 404
