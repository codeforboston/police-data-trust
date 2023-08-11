from datetime import datetime

import flask_user
import pytest
from backend.database import User, Partner
from flask_jwt_extended import decode_token
from unittest import mock


mock_partners = {
    "cpdp": {
        "name": "Citizens Police Data Project",
        "url": "https://cpdp.co",
        "contact_email": "tech@invisible.institute"
    },
    "mpv": {
        "name": "Mapping Police Violence",
        "url": "https://mappingpoliceviolence.us",
        "contact_email": "samswey1@gmail.com"
    },
    "fe": {
        "name": "Fatal Encounters",
        "url": "https://fatalencounters.org",
        "contact_email": "d.brian@fatalencounters.org"
    }
}


@pytest.fixture
def example_partners(db_session, client, access_token):
    created = {}

    for id, mock in mock_partners.items():
        res = client.post(
            "/api/v1/partners/create",
            json=mock,
            headers={"Authorization":
                     "Bearer {0}".format(access_token)},
        )
        assert res.status_code == 200
        created[id] = res.json
    return created


def test_create_partner(db_session, example_partners):
    # sample = mock_partners["mpv"]
    created = example_partners["mpv"]

    partner_obj = (
        db_session.query(Partner).filter(Partner.id == created["id"]).first()
    )

    assert partner_obj.name == created["name"]
    assert partner_obj.url == created["url"]
    assert partner_obj.contact_email == created["contact_email"]
    # assert partner_obj.source == expected["source"]


""" def test_get_partner(app, client, db_session, access_token):
    # Create an incident in the database
    incident_date = datetime(1969, 7, 16, 13, 32, 0)
    incident_date_str = app.json_encoder().encode(incident_date)[1:-1]

    obj = Incident(time_of_incident=incident_date)
    db_session.add(obj)
    db_session.commit()

    # Test that we can get it
    res = client.get(f"/api/v1/incidents/get/{obj.id}")
    assert res.json["time_of_incident"] == incident_date_str


def test_pagination(client, example_partners, access_token):
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
 """