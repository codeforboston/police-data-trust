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
        db_session.query(Partner).filter(Partner.name == created["name"]
                                         ).first()
    )

    assert partner_obj.name == created["name"]
    assert partner_obj.url == created["url"]
    assert partner_obj.contact_email == created["contact_email"]


def test_get_partner(app, client, db_session, access_token):
    # Create a partner in the database
    partner_name = "Test Partner"
    partner_url = "https://testpartner.com"

    obj = Partner(name=partner_name, url=partner_url)
    db_session.add(obj)
    db_session.commit()
    assert obj.id is not None

    # Test that we can get it
    res = client.get(f"/api/v1/partners/{obj.id}")
    assert res.json["name"] == partner_name
    assert res.json["url"] == partner_url
