from __future__ import annotations

import pytest
from backend.database import (
    Officer,
    Agency,
    Accusation,
    Incident,
    Partner
)
from typing import Any

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

mock_employment = {
    "severe": {
        "agency": "Chicago Police Department",
        "earliest_employment": "2015-03-14 00:00:00",
        "badge_number": "1234",
        "currently_employed": True
    },
    "light": {
        "agency": "Chicago Police Department",
        "earliest_employment": "2018-08-12 00:00:00",
        "badge_number": "5678",
        "currently_employed": True
    },
    "none": {
        "agency": "New York Police Department",
        "earliest_employment": "2019-05-03 00:00:00",
        "badge_number": "1234",
        "currently_employed": True
    }

}

mock_incidents = {
    "domestic": {
        "time_of_incident": "2021-03-14 01:05:09",
        "description": "Domestic disturbance",
        "perpetrators": [
            {"first_name": "Decent", "last_name": "Cop"},
        ],
        "use_of_force": [{"item": "Injurious restraint"}],
        "source": "Citizens Police Data Project",
        "location": "123 Right St Chicago, IL",
    },
    "traffic": {
        "time_of_incident": "2021-10-01 00:00:00",
        "description": "Traffic stop",
        "perpetrators": [
            {"first_name": "Bad", "last_name": "Cop"},
        ],
        "use_of_force": [{"item": "verbalization"}],
        "source": "Mapping Police Violence",
        "location": "Park St and Boylston Boston",
    },
    "firearm": {
        "time_of_incident": "2021-10-05 00:00:00",
        "description": "Robbery",
        "perpetrators": [
            {"first_name": "Bad", "last_name": "Cop"},
        ],
        "use_of_force": [{"item": "indirect firearm"}],
        "source": "Citizens Police Data Project",
        "location": "CHICAGO ILLINOIS",
    },
}

mock_partners = {
    "cpdp": {"name": "Citizens Police Data Project"}
}

mock_accusations = {
    "domestic": {
        "officer": "light",
        "date_created": "2023-03-14 01:05:09",
        "basis": "Name Match"
    },
    "traffic": {
        "officer": "severe",
        "date_created": "2023-10-01 00:00:00",
        "basis": "Name Match"
    },
    "firearm": {
        "officer": "severe",
        "date_created": "2023-10-05 00:00:00",
        "basis": "Name Match"
    },
}


@pytest.fixture
def example_officers(db_session, client, contributor_access_token):
    agencies = {}
    for name, mock in mock_agencies.items():
        db_session.add(Agency(**mock))
        db_session.commit()
        agencies[name] = db_session.query(
            Agency).filter(Agency.name == mock["name"]).first()

    created = {}
    for name, mock in mock_officers.items():
        mock["known_employers"].append(mock_employment[name])
        res = client.post(
            "/api/v1/officers/create",
            json=mock,
            headers={
                "Authorization": "Bearer {0}".format(contributor_access_token)
            },
        )
        assert res.status_code == 200
        created[name] = res.json

    return created, agencies


@pytest.fixture
def example_employment(db_session, example_officers):
    for id, officer in example_officers.items():
        officer_obj = (
            db_session.query(Officer).filter(Incident.id == id).first()
        )
        officer_obj.known_employers.append()
        db_session.commit()


@pytest.fixture
def example_accusations(db_session, client,
                        contributor_access_token, example_officers):
    officers, agencies = example_officers
    incidents = {}
    accusations = {}
    perpetrators = {}

    for id, mock in mock_partners.items():
        db_session.add(Partner(**mock))
        db_session.commit()

    for id, mock in mock_incidents.items():
        obj = Incident(**mock)
        db_session.add(obj)
        db_session.commit()
        incidents[id] = obj
        perpetrators[id] = obj.perpetrators[0].id

    for id, mock in mock_accusations.items():
        obj = Accusation(**mock)
        obj.perpetrator_id = perpetrators[id]
        obj.officer_id = officers[id]["id"]
        db_session.add(obj)
        db_session.commit()
        accusations[id] = obj

    return incidents, accusations


def test_create_officer(db_session, example_officers):
    officers, agencies = example_officers
    created = officers["severe"]

    officer_obj = (
        db_session.query(Officer).filter(Officer.id == created["id"]).first()
    )
    assert officer_obj.first_name == created["first_name"]
    assert officer_obj.last_name == created["last_name"]
    assert officer_obj.race == created["race"]
    assert officer_obj.ethnicity == created["ethnicity"]
    assert len(officer_obj.known_employers) == 1


def test_get_officer(app, client, db_session, access_token):
    # Create an officer in the database
    fname = "John"
    lname = "Doe"

    obj = Officer(
        first_name=fname,
        last_name=lname
    )
    db_session.add(obj)
    db_session.commit()

    # Test that we can get it
    res = client.get(f"/api/v1/officers/{obj.id}")

    assert res.status_code == 200
    assert res.json["first_name"] == fname
    assert res.json["last_name"] == lname


"""
@pytest.mark.parametrize(
    ("query", "expected_officer_names"),
    [
        (
            {},
            ["severe", "light", "none"],
        ),
        (
            {"location": "New York"},
            ["none"],
        ),
        (
            {
                "badgeNumber": "1234"
            },
            ["severe", "none"],
        ),
        (
            {
                "name": "Decent",
            },
            ["light"],
        ),
    ],
)
def test_search_officers(
    client, example_officers, access_token, query, expected_officer_names
):
    res = client.post(
        "/api/v1/officers/search",
        json=query,
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 200

    # Match the results to the known dataset and assert that all the expected
    # results are present
    actual_officers = res.json["results"]

    def officer_name(officer):
        return next(
            (
                k
                for k, v in example_officers.items()
                if v["id"] == officer["id"]
            ),
            None,
        )

    actual_incident_names = list(
        filter(None, map(officer_name, actual_officers))
    )
    assert set(actual_incident_names) == set(expected_officer_names)

    assert res.json["page"] == 1
    assert res.json["totalPages"] == 1
    assert res.json["totalResults"] == len(expected_officer_names)
 """


def test_get_officers(client: Any, access_token: str):
    res = client.get(
        "/api/v1/officers/",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )

    assert res.status_code == 200
    assert res.json["results"] == []
    assert res.json["page"] == 1
    assert res.json["totalPages"] == 0
    assert res.json["totalResults"] == 0


def test_officer_pagination(client, example_officers, access_token):
    per_page = 1
    created, agencies = example_officers
    expected_total_pages = len(created)
    actual_ids = set()
    for page in range(1, expected_total_pages + 1):
        res = client.get(
            "/api/v1/officers/",
            query_string={"per_page": per_page, "page": page},
            headers={"Authorization": "Bearer {0}".format(access_token)},
        )

        assert res.status_code == 200
        assert res.json["page"] == page
        assert res.json["totalPages"] == expected_total_pages
        assert res.json["totalResults"] == len(created)

        officers = res.json["results"]
        assert len(officers) == per_page
        actual_ids.add(officers[0]["id"])

    assert actual_ids == set(i["id"] for i in created.values())

    res = client.get(
        "/api/v1/officers/",
        query_string={"perPage": per_page, "page": expected_total_pages + 1},
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 404


"""
def test_get_accusations(client: Any, access_token: str):
    res = client.get(
        "/api/v1/officers/",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )

    assert res.status_code == 200
    assert res.json["results"] == []
    assert res.json["page"] == 1
    assert res.json["totalPages"] == 0
    assert res.json["totalResults"] == 0


def test_get_accusations_pagination(
    client: Any,
    access_token: str,
    example_incidents_private_public: list[Incident],
):
    \"""
    Test that pagination works for public incidents.
    \"""
    res = client.get(
        "/api/v1/officers/?per_page=1",
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
        "/api/v1/officers/?per_page=1&page=2",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )

    assert res.status_code == 200
    assert len(res.json["results"]) == 0
    assert res.json["page"] == 2
    assert res.json["totalPages"] == public_incidents_count
    assert res.json["totalResults"] == public_incidents_count


def test_get_employers(
    client: Any,
    access_token: str,
    example_incidents_private_public: list[Incident],
):
    \"""
    Test that a regular user can see public incidents.
    \"""

    res = client.get(
        "/api/v1/officers/",
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


def test_get_employers_pagination(
    client: Any,
    access_token: str,
    example_incidents_private_public: list[Incident],
):
    \"""
    Test that pagination works for public incidents.
    \"""
    res = client.get(
        "/api/v1/officers/?per_page=1",
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
        "/api/v1/officers/?per_page=1&page=2",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )

    assert res.status_code == 200
    assert len(res.json["results"]) == 0
    assert res.json["page"] == 2
    assert res.json["totalPages"] == public_incidents_count
    assert res.json["totalResults"] == public_incidents_count


def test_delete_officer(
    client: Any,
    partner_publisher: User,
    example_partner: Partner,
    example_incidents_private_public: list[Incident],
):
    \"""
    Test that a partner member can delete an incident.
    \"""

    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_publisher.email,
            "password": "my_password",
        },
    ).json["access_token"]

    # Make a request to delete the incident
    res = client.delete(
        f"/api/v1/officers/{example_incidents_private_public[0].id}"
        + f"?partner_id={example_partner.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 204

    # Verify that the incident is deleted
    deleted_incident = Incident.query.get(
        example_incidents_private_public[0].id
    )
    assert deleted_incident is None


def test_delete_officer_no_user_role(
    client: Any,
    access_token: str,
):
    \"""
    Test that a user without atlest CONTRIBUTOR role
    can't delete an incident.
    \"""
    # Make a request to delete the incident
    res = client.delete(
        "/api/v1/officers/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 403


def test_delete_officer_nonexsitent_officer(
    client: Any,
    partner_publisher: User,
):
    \"""
    Test that a partner member can't delete an incident
    with a invalid incident id.
    \"""
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_publisher.email,
            "password": "my_password",
        },
    ).json["access_token"]

    # Make a request to delete the officer
    res = client.delete(
        f"/api/v1/officers/{999}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 404 """
