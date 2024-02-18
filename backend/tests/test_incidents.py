from __future__ import annotations
from datetime import datetime

import pytest
from backend.database import Incident, Partner, PrivacyStatus, User
from typing import Any

mock_partners = {
    "cpdp": {"name": "Citizens Police Data Project"},
    "mpv": {"name": "Mapping Police Violence"},
}

mock_incidents = {
    "domestic": {
        "time_of_incident": "2021-03-14 01:05:09",
        "description": "Domestic disturbance",
        "perpetrators": [
            {"first_name": "Susie", "last_name": "Suserson"},
            {"first_name": "Lisa", "last_name": "Wong"},
        ],
        "use_of_force": [{"item": "Injurious restraint"}],
        "source": "Citizens Police Data Project",
        "location": "123 Right St Chicago, IL",
    },
    "traffic": {
        "time_of_incident": "2021-10-01 00:00:00",
        "description": "Traffic stop",
        "perpetrators": [
            {"first_name": "Ronda", "last_name": "Sousa"},
        ],
        "use_of_force": [{"item": "verbalization"}],
        "source": "Mapping Police Violence",
        "location": "Park St and Boylston Boston",
    },
    "firearm": {
        "time_of_incident": "2021-10-05 00:00:00",
        "description": "Robbery",
        "perpetrators": [
            {"first_name": "Dale", "last_name": "Green"},
        ],
        "use_of_force": [{"item": "indirect firearm"}],
        "source": "Citizens Police Data Project",
        "location": "CHICAGO ILLINOIS",
    },
    "missing_fields": {
        "description": "Robbery",
        "perpetrators": [
            {"first_name": "Dale", "last_name": "Green"},
        ],
        "source": "Citizens Police Data Project",
    },
}


@pytest.fixture
def example_incidents(db_session, client, contributor_access_token):
    for id, mock in mock_partners.items():
        db_session.add(Partner(**mock))
        db_session.commit()

    created = {}
    for name, mock in mock_incidents.items():
        res = client.post(
            "/api/v1/incidents/create",
            json=mock,
            headers={
                "Authorization": "Bearer {0}".format(contributor_access_token)
            },
        )
        assert res.status_code == 200
        created[name] = res.json
    return created


def test_create_incident(db_session, example_incidents):
    # TODO: test that the User actually has permission to create an
    # incident for the partner
    # expected = mock_incidents["domestic"]
    created = example_incidents["domestic"]

    incident_obj = (
        db_session.query(Incident).filter(Incident.id == created["id"]).first()
    )

    assert incident_obj.time_of_incident == datetime(2021, 3, 14, 1, 5, 9)
    for i in [0, 1]:
        assert (
            incident_obj.perpetrators[i].id == created["perpetrators"][i]["id"]
        )
    assert incident_obj.use_of_force[0].id == created["use_of_force"][0]["id"]
    # assert incident_obj.source == expected["source"]


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
                "dateStart": "2021-09-30",
                "dateEnd": "2021-10-02",
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


def test_incident_pagination(client, example_incidents, access_token):
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


def test_get_incidents(client: Any, access_token: str):
    res = client.get(
        "/api/v1/incidents/",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )

    assert res.status_code == 200
    assert res.json["results"] == []
    assert res.json["page"] == 1
    assert res.json["totalPages"] == 0
    assert res.json["totalResults"] == 0


def test_get_incidents_pulic(
    client: Any,
    access_token: str,
    example_incidents_private_public: list[Incident],
):
    """
    Test that a regular user can see public incidents.
    """

    res = client.get(
        "/api/v1/incidents/",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )

    public_incidents_count = len(
        [
            i
            for i in example_incidents_private_public
            if i.privacy_filter == PrivacyStatus.PUBLIC
        ]
    )
    assert res.status_code == 200
    assert len(res.json["results"]) == public_incidents_count
    assert res.json["page"] == 1
    assert res.json["totalPages"] == 1
    assert res.json["totalResults"] == public_incidents_count


def test_get_incidents_pulic_pagination(
    client: Any,
    access_token: str,
    example_incidents_private_public: list[Incident],
):
    """
    Test that pagination works for public incidents.
    """
    res = client.get(
        "/api/v1/incidents/?per_page=1",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )

    public_incidents_count = len(
        [
            i
            for i in example_incidents_private_public
            if i.privacy_filter == PrivacyStatus.PUBLIC
        ]
    )

    assert res.status_code == 200
    assert len(res.json["results"]) == 1
    assert res.json["page"] == 1
    assert res.json["totalPages"] == public_incidents_count
    assert res.json["totalResults"] == public_incidents_count

    res = client.get(
        "/api/v1/incidents/?per_page=1&page=2",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )

    assert res.status_code == 200
    assert len(res.json["results"]) == 0
    assert res.json["page"] == 2
    assert res.json["totalPages"] == public_incidents_count
    assert res.json["totalResults"] == public_incidents_count


def test_get_incidents_private(
    client: Any,
    access_token: str,
    example_partner_member: Partner,
    example_incidents_private_public: list[Incident],
):
    """
    Test that a partner member can see private incidents.
    """
    res = client.get(
        f"/api/v1/incidents/?partner_id={example_partner_member.id}",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )

    assert res.status_code == 200
    assert len(res.json["results"]) == len(example_incidents_private_public)
    assert res.json["page"] == 1
    assert res.json["totalPages"] == 1
    assert res.json["totalResults"] == len(example_incidents_private_public)


def test_get_incidents_unauthorized(client: Any):
    res = client.get("/api/v1/incidents/")
    assert res.status_code == 401


def test_get_invalid_partner_id(client: Any, access_token: str):
    res = client.get(
        "/api/v1/incidents/?partner_id=999999",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 404
    assert res.json["message"] == "Partner not found"


def test_delete_incident(
    client: Any,
    partner_publisher: User,
    example_partner: Partner,
    example_incidents_private_public: list[Incident],
):
    """
    Test that a partner member can delete an incident.
    """

    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_publisher.email,
            "password": "my_password",
        },
    ).json["access_token"]

    # Make a request to delete the incident
    res = client.delete(
        f"/api/v1/incidents/{example_incidents_private_public[0].id}"
        + f"?partner_id={example_partner.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 204

    # Verify that the incident is deleted
    deleted_incident = Incident.query.get(
        example_incidents_private_public[0].id
    )
    assert deleted_incident is None


def test_delete_incident_no_user_role(
    client: Any,
    access_token: str,
):
    """
    Test that a user without atlest CONTRIBUTOR role
    can't delete an incident.
    """
    # Make a request to delete the incident
    res = client.delete(
        "/api/v1/incidents/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 403


def test_delete_incident_nonexsitent_incident(
    client: Any,
    partner_publisher: User,
):
    """
    Test that a partner member can't delete an incident
    with a invalid incident id.
    """
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_publisher.email,
            "password": "my_password",
        },
    ).json["access_token"]

    # Make a request to delete the incident
    res = client.delete(
        f"/api/v1/incidents/{999}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 404
