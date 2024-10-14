from __future__ import annotations
import pytest
import math
from backend.database import (
    Officer,
)

mock_officers = {
    "john": {
        "first_name": "John",
        "last_name": "Doe",
        "ethnicity": "White",
        "gender": "Male"
    },
    "hazel": {
        "first_name": "Hazel",
        "last_name": "Nutt",
        "ethnicity": "White",
        "gender": "Female"
    },
    "frank": {
        "first_name": "Frank",
        "last_name": "Furter",
        "ethnicity": "Black/African American",
        "gender": "Male"
    }
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
    "john": {
        "agency": "Chicago Police Department",
        "earliest_employment": "2015-03-14 00:00:00",
        "badge_number": "1234",
        "currently_employed": True
    },
    "hazel": {
        "agency": "Chicago Police Department",
        "earliest_employment": "2018-08-12 00:00:00",
        "badge_number": "5678",
        "currently_employed": True
    },
    "frank": {
        "agency": "New York Police Department",
        "earliest_employment": "2019-05-03 00:00:00",
        "badge_number": "1234",
        "currently_employed": True
    }
}

mock_partners = {
    "cpdp": {"name": "Citizens Police Data Project"}
}


@pytest.fixture
def example_officers(db_session):
    # Create Officers in the database
    officers = {}
    for name, mock in mock_officers.items():
        o = Officer(**mock).save()
        officers[name] = o
    return officers


def test_create_officer(
        db_session,
        client,
        contributor_access_token,
        example_agency):

    # Test that we can create an officer without an agency association
    request = {
        "first_name": "Max",
        "last_name": "Payne",
        "ethnicity": "White",
        "gender": "Male"
    }
    res = client.post(
        "/api/v1/officers/",
        json=request,
        headers={
            "Authorization": "Bearer {0}".format(contributor_access_token)
        },
    )
    assert res.status_code == 200
    response = res.json

    officer_obj = (
       Officer.nodes.get(uid=response["uid"])
    )
    assert officer_obj.first_name == request["first_name"]
    assert officer_obj.last_name == request["last_name"]
    assert officer_obj.ethnicity == request["ethnicity"]
    assert officer_obj.gender == request["gender"]


def test_get_officer(client, db_session, example_officer, access_token):
    # Test that we can get it
    res = client.get(f"/api/v1/officers/{example_officer.uid}")

    assert res.status_code == 200
    assert res.json["first_name"] == example_officer.first_name
    assert res.json["last_name"] == example_officer.last_name
    assert res.json["gender"] == example_officer.gender
    assert res.json["ethnicity"] == example_officer.ethnicity


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


def test_get_officers(client, db_session, access_token, example_officers):
    all_officers = Officer.nodes.all()
    res = client.get(
        "/api/v1/officers/",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )

    assert res.status_code == 200
    assert res.json["results"][0]["first_name"] is not None
    assert res.json["results"][0]["last_name"] is not None
    assert res.json["page"] == 1
    assert res.json["total"] == len(all_officers)


def test_officer_pagination(client, db_session, access_token, example_officers):
    # Create Officers in the database
    officers = Officer.nodes.all()
    per_page = 1
    expected_total_pages = math.ceil(len(officers)//per_page)

    for page in range(1, expected_total_pages + 1):
        res = client.get(
            "/api/v1/officers/",
            query_string={"per_page": per_page, "page": page},
            headers={"Authorization": "Bearer {0}".format(access_token)},
        )

        assert res.status_code == 200
        assert res.json["page"] == page
        assert res.json["total"] == len(officers)
        assert len(res.json["results"]) == per_page

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
"""
