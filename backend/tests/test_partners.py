import pytest
from backend.database import Partner


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

mock_members = {
    "user": {
        "email": "user@email.com",
        "password": "my_password",
    },
    "publisher": {},
    "admin": {},
    "member": {},
    "subscriber": {}
}


@pytest.fixture
def example_partners(client, access_token):
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


@pytest.fixture
def example_members(client, access_token, example_partners):
    # partners = example_partners
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


def test_get_partner(client, db_session, access_token):
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


def test_get_all_partners(client, example_partners):
    # Create partners in the database
    created = example_partners

    # Test that we can get partners
    res = client.get("/api/v1/partners/")
    assert res.json["results"].__len__() == created.__len__()


def test_partner_pagination(client, example_partners, access_token):
    per_page = 1
    expected_total_pages = len(example_partners)
    actual_ids = set()
    for page in range(1, expected_total_pages + 1):
        res = client.get(
            f"/api/v1/partners/?per_page={per_page}&page={page}",
            headers={"Authorization": "Bearer {0}".format(access_token)},
        )

        assert res.status_code == 200
        assert res.json["page"] == page
        assert res.json["totalPages"] == expected_total_pages
        assert res.json["totalResults"] == expected_total_pages

        incidents = res.json["results"]
        assert len(incidents) == per_page
        actual_ids.add(incidents[0]["id"])

    assert actual_ids == set(i["id"] for i in example_partners.values())

    res = client.get(
        (
            f"/api/v1/partners/?per_page={per_page}"
            f"&page={expected_total_pages + 1}"
        ),
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 404

# def test_add_member_to_partner(client, example_partners, access_token):

# def test_remove_member_from_partner(client, example_partners, access_token):

# def test_get_partner_members(client, example_partners, access_token):
