from __future__ import annotations
import pytest
import math
from datetime import date, datetime
from backend.database import (
    Officer, Unit, Agency
)
from neomodel import db


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

mock_units = {
    "unit_alpha": {
        "name": "Unit Alpha",
        "website_url": "https://agency.gov/unit-alpha",
        "phone": "(555) 123-4567",
        "email": "alpha@agency.gov",
        "description": "Responsible for general investigations and field operations.",
        "address": "100 Alpha Ave",
        "city": "Chicago",
        "state": "MI",
        "zip": "60001",
        "agency_url": "https://agency.gov",
        "officers_url": "https://agency.gov/unit-alpha/officers",
        "date_established": date(2001, 5, 14)
    },
    "unit_bravo": {
        "name": "Unit Bravo",
        "website_url": "https://agency.gov/unit-bravo",
        "phone": "(555) 234-5678",
        "email": "bravo@agency.gov",
        "description": "Handles specialized enforcement and tactical operations.",
        "address": "200 Bravo Blvd",
        "city": "NYC",
        "state": "NY",
        "zip": "75001",
        "agency_url": "https://agency.gov",
        "officers_url": "https://agency.gov/unit-bravo/officers",
        "date_established": date(1998, 9, 3)
    },
    "unit_charlie": {
        "name": "Unit Charlie",
        "website_url": "https://agency.gov/unit-charlie",
        "phone": "(555) 345-6789",
        "email": "charlie@agency.gov",
        "description": "Focuses on community outreach and civilian safety programs.",
        "address": "300 Charlie Rd",
        "city": "Oakridge",
        "state": "OH",
        "zip": "43001",
        "agency_url": "https://agency.gov",
        "officers_url": "https://agency.gov/unit-charlie/officers",
        "date_established": date(2010, 2, 28)
    }
}

mock_unit_memberships = {
    "john": {
        "earliest_date": datetime.strptime("2015-03-04 00:00:00", "%Y-%m-%d %H:%M:%S").date(),
        "latest_date": datetime.strptime("2020-03-04 00:00:00", "%Y-%m-%d %H:%M:%S").date(),
        "badge_number": "1234",
        "highest_rank": 'Officer'
    },
    "hazel": {
        "earliest_date": datetime.strptime("2018-08-12 00:00:00", "%Y-%m-%d %H:%M:%S").date(),
        "latest_date": datetime.strptime("2021-04-04 00:00:00", "%Y-%m-%d %H:%M:%S").date(),
        "badge_number": "5678",
        "highest_rank": 'Sergeant',
    },
    "frank": {
        "earliest_date": datetime.strptime("2019-05-03 00:00:00", "%Y-%m-%d %H:%M:%S").date(),
        "latest_date": datetime.strptime("2025-05-04 00:00:00", "%Y-%m-%d %H:%M:%S").date(),
        "badge_number": "1234",
        "highest_rank": 'Lieutenant'
    }
}

mock_sources = {
    "cpdp": {"name": "Citizens Police Data Project"}
}


@pytest.fixture
def example_officers():
    # Create Officers in the database
    officers = {}
    for name, mock in mock_officers.items():
        o = Officer(**mock).save()
        officers[name] = o
    return officers


def test_create_officer(
        client,
        contributor_access_token,
        example_agency
        ):

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


def test_get_officer(client, example_officer, access_token):
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
    source_publisher: User,
    example_source: Source,
    example_incidents_private_public: list[Incident],
):
    \"""
    Test that a source member can delete an incident.
    \"""

    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": source_publisher.email,
            "password": "my_password",
        },
    ).json["access_token"]

    # Make a request to delete the incident
    res = client.delete(
        f"/api/v1/officers/{example_incidents_private_public[0].id}"
        + f"?source_uid={example_source.id}",
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

@pytest.fixture
def create_officers_units_agencies():
    # Create Officers in the database
    officers = {}
    for name, mock in mock_officers.items():
        officers[name] = Officer(**mock).save()

    # Create Units in the database
    units = {}
    for key, mock in mock_units.items():
        units[key] = Unit(**mock).save()

    # Create Agencies in the database
    agencies = {}
    for key, mock in mock_agencies.items():
        agencies[key] = Agency(**mock).save()

    # Link officers to existing unit objects
    units["unit_alpha"].officers.connect(officers["john"], mock_unit_memberships["john"])
    units["unit_bravo"].officers.connect(officers["hazel"], mock_unit_memberships["hazel"])
    units["unit_charlie"].officers.connect(officers["frank"], mock_unit_memberships["frank"])


    # # Link units to agencies (one direction is enough)
    units["unit_alpha"].agency.connect(agencies["cpd"])
    units["unit_bravo"].agency.connect(agencies["nypd"])

    return officers



def test_get_officers_with_unit(client, db_session, access_token, create_officers_units_agencies):  

    results, meta = db.cypher_query("""
        MATCH (o:Officer)
        MATCH (o)-[:MEMBER_OF_UNIT]->(u:Unit)
        where u.name = "Unit Alpha"
        RETURN o
    """)
    officers_with_unit = [Officer.inflate(row[0]) for row in results]

    res = client.get(
        "/api/v1/officers/?unit=Unit Alpha",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )
    print(officers_with_unit[0])
    print(f"len results is {len(res.json['results'])}")
    assert res.status_code == 200
    assert res.json["results"][0]["first_name"] is not None
    assert res.json["results"][0]["last_name"] is not None
    assert res.json["page"] == 1
    assert res.json["total"] == len(officers_with_unit)


def test_get_officers_with_unit_and_agency(client, 
            db_session, access_token, create_officers_units_agencies):

    results, meta = db.cypher_query("""
        MATCH (o:Officer)
        MATCH (o)-[:MEMBER_OF_UNIT]->(u:Unit)
        MATCH (u)-[:ESTABLISHED_BY]-(a:Agency)
        where a.name = "Chicago Police Department"
        RETURN o
    """)
    officers_with_unit = [Officer.inflate(row[0]) for row in results]

    res = client.get(
        "/api/v1/officers/?agency=Chicago Police Department",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )
    assert officers_with_unit is not None
    assert res.json is not None
    print(f"len results is {len(res.json['results'])}")
    assert res.status_code == 200
    assert res.json["results"][0]["first_name"] is not None
    assert res.json["results"][0]["last_name"] is not None
    assert res.json["page"] == 1
    assert res.json["total"] == len(officers_with_unit)


def test_get_officers_with_date(client, db_session, access_token, create_officers_units_agencies):
    res = client.get(
        "/api/v1/officers/?active_after=2018-01-01",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )
    assert res.json != []
    print(res.json)
    print(f"len results is {len(res.json['results'])}")
    assert res.status_code == 200
    assert res.json["results"][0]["first_name"] is not None
    assert res.json["results"][0]["last_name"] is not None
    assert res.json["page"] == 1

    res = client.get(
        "/api/v1/officers/?active_before=2022-01-01",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )
    assert res.json != []
    print(res.json)
    print(f"len results is {len(res.json['results'])}")
    assert res.status_code == 200
    assert res.json["results"][0]["first_name"] is not None
    assert res.json["results"][0]["last_name"] is not None
    assert res.json["page"] == 1

    res = client.get(
        "/api/v1/officers/?active_before=2010-01-01",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )
    assert res.json == []

    res = client.get(
        "/api/v1/officers/?active_after=2035-01-01",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )
    assert res.json == []


def test_get_officers_with_rank(client, db_session, access_token, create_officers_units_agencies):
    res = client.get(
        "/api/v1/officers/?rank=Officer",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )
    assert res.json != []
    assert res.status_code == 200
    assert res.json["results"][0]["first_name"] is not None
    assert res.json["results"][0]["last_name"] is not None

    res = client.get(
        "/api/v1/officers/?rank=Officer&agency=Chicago Police Department",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )
    assert res.json != []
    assert res.status_code == 200
    assert res.json["results"][0]["first_name"] is not None
    assert res.json["results"][0]["last_name"] is not None

    res = client.get(
        "/api/v1/officers/?rank=Lieutenant",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )
    assert res.json != []
    assert res.status_code == 200
    assert res.json["results"][0]["first_name"] is not None
    assert res.json["results"][0]["last_name"] is not None


def test_filter_by_ethnicity(client, db_session, access_token, create_officers_units_agencies):
    res = client.get(
        "/api/v1/officers/?ethnicity=White",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert res.status_code == 200
    assert res.json != []
    for officer in res.json["results"]:
        assert officer["ethnicity"] == "White"
