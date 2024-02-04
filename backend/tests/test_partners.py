import pytest
from backend.auth import user_manager
from backend.database import Partner, PartnerMember, MemberRole, Incident
from backend.database.models.user import User, UserRole
from typing import Any, List

publisher_email = "pub@partner.com"
inactive_email = "lurker@partner.com"
admin_email = "leader@partner.com"
member_email = "joe@partner.com"
example_password = "my_password"

mock_partners = {
    "cpdp": {
        "name": "Citizens Police Data Project",
        "url": "https://cpdp.co",
        "contact_email": "tech@invisible.institute",
    },
    "mpv": {
        "name": "Mapping Police Violence",
        "url": "https://mappingpoliceviolence.us",
        "contact_email": "samswey1@gmail.com",
    },
    "fe": {
        "name": "Fatal Encounters",
        "url": "https://fatalencounters.org",
        "contact_email": "d.brian@fatalencounters.org",
    },
}

mock_users = {
    "publisher": {
        "email": publisher_email,
        "password": example_password,
    },
    "inactive": {
        "email": inactive_email,
        "password": example_password,
    },
    "admin": {
        "email": admin_email,
        "password": example_password,
    },
    "member": {
        "email": member_email,
        "password": example_password,
    },
}

mock_members = {
    "publisher": {
        "user_email": publisher_email,
        "role": MemberRole.PUBLISHER,
        "is_active": True,
    },
    "inactive": {
        "user_email": inactive_email,
        "role": MemberRole.PUBLISHER,
        "is_active": False,
    },
    "admin": {
        "user_email": publisher_email,
        "role": MemberRole.ADMIN,
        "is_active": True,
    },
    "member": {
        "user_email": publisher_email,
        "role": MemberRole.MEMBER,
        "is_active": True,
    },
}


@pytest.fixture
def example_partners(client, access_token):
    created = {}

    for id, mock in mock_partners.items():
        res = client.post(
            "/api/v1/partners/create",
            json=mock,
            headers={"Authorization": "Bearer {0}".format(access_token)},
        )
        assert res.status_code == 200
        created[id] = res.json
    return created


@pytest.fixture
def example_members(client, db_session, example_partner, p_admin_access_token):
    created = {}
    users = {}

    for id, mock in mock_users.items():
        user = User(
            email=mock["email"],
            password=user_manager.hash_password(example_password),
            role=UserRole.PUBLIC,
            first_name=id,
            last_name="user",
            phone_number="(278) 555-7890",
        )
        db_session.add(user)
        db_session.commit()
        users[id] = user

    partner_obj = (
        db_session.query(Partner).filter(Partner.name == example_partner.name).first()
    )

    for id, mock in mock_members.items():
        user_obj = (
            db_session.query(User).filter(User.email == mock["user_email"]).first()
        )

        req = {
            "partner_id": partner_obj.id,
            "user_id": user_obj.id,
            "role": mock["role"],
            "is_active": mock["is_active"],
        }

        res = client.post(
            f"/api/v1/partners/{partner_obj.id}/members/add",
            json=req,
            headers={"Authorization": "Bearer {0}".format(p_admin_access_token)},
        )
        assert res.status_code == 200
        created[id] = res.json
    return created


def test_create_partner(db_session, example_user, example_partners):
    created = example_partners["mpv"]

    partner_obj = (
        db_session.query(Partner).filter(Partner.name == created["name"]).first()
    )

    user_obj = db_session.query(User).filter(User.email == example_user.email).first()

    association_obj = (
        db_session.query(PartnerMember)
        .filter(
            PartnerMember.partner_id == partner_obj.id,
            PartnerMember.user_id == user_obj.id,
        )
        .first()
    )

    assert partner_obj.name == created["name"]
    assert partner_obj.url == created["url"]
    assert partner_obj.contact_email == created["contact_email"]
    assert association_obj is not None
    assert association_obj.is_administrator() is True


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
        (f"/api/v1/partners/?per_page={per_page}" f"&page={expected_total_pages + 1}"),
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 404


def test_add_member_to_partner(db_session, example_members):
    created = example_members["publisher"]

    partner_member_obj = (
        db_session.query(PartnerMember)
        .filter(PartnerMember.id == created["id"])
        .first()
    )

    assert partner_member_obj.partner_id == created["partner_id"]
    assert partner_member_obj.user_id == created["user_id"]
    assert partner_member_obj.role == created["role"]


def test_get_partner_members(
    db_session, client, example_partner, example_user, admin_user, access_token
):
    # Create partners in the database
    users = []
    partner_obj = (
        db_session.query(Partner).filter(Partner.name == example_partner.name).first()
    )

    member_obj = db_session.query(User).filter(User.email == example_user.email).first()

    admin_obj = db_session.query(User).filter(User.email == admin_user.email).first()

    users.append(member_obj)
    users.append(admin_obj)

    for user in users:
        association_obj = PartnerMember(partner_id=partner_obj.id, user_id=user.id)
        db_session.add(association_obj)
        db_session.commit()

    # Test that we can get partners
    res = client.get(
        f"/api/v1/partners/{partner_obj.id}/members/",
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )

    assert res.status_code == 200
    assert res.json["results"].__len__() == users.__len__()
    # assert res.json["results"][0]["user"]["email"] == member_obj.email


def test_get_partner_users(
    client: Any,
    example_partner: Partner,
    example_members: PartnerMember,
    access_token: str,
) -> None:
    # Test that we can get partner users
    res: Any = client.get(
        f"/api/v1/partners/{example_partner.id}/users",
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 200
    data = res.get_json()

    # Verify the response structure
    assert "results" in data
    assert "page" in data
    assert "totalPages" in data
    assert "totalResults" in data

    # Verify the results
    assert len(data["results"]) == len(mock_users) + 1

    # Verify the page number
    assert data["page"] == 1

    # Verify the total pages
    assert data["totalPages"] == 1

    # Verify the total results
    assert data["totalResults"] == len(mock_users) + 1


def test_get_partner_users_error(
    client: Any,
    access_token: str,
) -> None:
    # Test that we can get partner users
    res: Any = client.get(
        f"/api/v1/partners/{1234}/users",
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 404


def test_get_incidents(
    client: Any,
    access_token: str,
    example_partner: Partner,
    example_incidents: List[Incident],
):
    # Make a request to get the incidents
    res = client.get(
        f"/api/v1/partners/{example_partner.id}/incidents",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 200
    data = res.json

    # Verify the response structure
    assert "results" in data
    assert "page" in data
    assert "totalPages" in data
    assert "totalResults" in data

    # Verify the results
    assert len(data["results"]) == len(example_incidents)

    # Verify the page number
    assert data["page"] == 1

    # Verify the total pages
    assert data["totalPages"] == 1

    # Verify the total results
    assert data["totalResults"] == len(example_incidents)


def test_get_incidents_unauthorized(client: Any, example_partner: Partner):
    # Create a partner in the database
    partner_id = example_partner.id

    # Make a request to get the incidents without a valid access token
    res = client.get(f"/api/v1/partners/{partner_id}/incidents")
    assert res.status_code == 401


def test_get_incidents_pagination(
    client: Any,
    access_token: str,
    example_partner_member: Partner,
    example_incidents_private_public: List[Incident],
):
    # Make a request to get the incidents with pagination
    per_page = 2
    page = 1
    res = client.get(
        f"/api/v1/partners/{example_partner_member.id}/incidents?per_page={per_page}&page={page}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 200
    data = res.json

    # Verify the response structure
    assert "results" in data
    assert "page" in data
    assert "totalPages" in data
    assert "totalResults" in data

    # Verify the results
    assert len(data["results"]) == per_page

    # Verify the page number
    assert data["page"] == page

    # Verify the total pages
    assert data["totalPages"] == len(example_incidents_private_public) // per_page

    # Verify the total results
    assert data["totalResults"] == len(example_incidents_private_public)


def test_get_incidents_no_association(
    client: Any, access_token: str, example_partner: Partner
):
    # Make a request to get the incidents without a partner member association
    res = client.get(
        f"/api/v1/partners/{example_partner.id}/incidents",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 200
    data = res.json

    # Verify that only public incidents are returned
    assert len(data["results"]) == 0


def test_get_incidents_not_admin(
    client: Any,
    access_token: str,
    example_partner: Partner,
    example_user: User,
    example_incidents: List[Incident],
):
    # Make a request to get the incidents
    res = client.get(
        f"/api/v1/partners/{example_partner.id}/incidents",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 200
    data = res.json

    # Verify that only public incidents are returned
    assert len(data["results"]) == len(example_incidents)
