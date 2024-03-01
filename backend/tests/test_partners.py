import pytest
from backend.auth import user_manager
from backend.database import Partner, PartnerMember, MemberRole, Invitation
from backend.database.models.user import User, UserRole
from datetime import datetime


publisher_email = "pub@partner.com"
inactive_email = "lurker@partner.com"
admin_email = "leader@partner.com"
admin2_email = "leader2@partner.com"
member_email = "joe@partner.com"
member2_email = "jack@partner.com"
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
    "admin2" : {
        "email" : admin2_email,
        "password" : example_password
    },
    "member2" : {
        "email" : member2_email,
        "password" : example_password
    }
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
    "admin2" : {
        "user_email": admin_email,
        "role": MemberRole.ADMIN,
        "is_active": True,
    },
    "member2" : {
        "user_email": member2_email,
        "role" : MemberRole.MEMBER,
        "is_active" : True
    }
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
        db_session.query(Partner)
        .filter(Partner.name == example_partner.name)
        .first()
    )

    for id, mock in mock_members.items():
        user_obj = (
            db_session.query(User)
            .filter(User.email == mock["user_email"])
            .first()
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
            headers={
                "Authorization": "Bearer {0}".format(p_admin_access_token)
            },
        )
        assert res.status_code == 200
        created[id] = res.json
    return created


def test_create_partner(db_session, example_user, example_partners):
    created = example_partners["mpv"]

    partner_obj = (
        db_session.query(Partner)
        .filter(Partner.name == created["name"])
        .first()
    )

    user_obj = (
        db_session.query(User).filter(User.email == example_user.email).first()
    )

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
        (
            f"/api/v1/partners/?per_page={per_page}"
            f"&page={expected_total_pages + 1}"
        ),
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 404


# def test_add_member_to_partner(db_session, example_members):
    # created = example_members["publisher"]

    # partner_member_obj = (
    #     db_session.query(PartnerMember)
    #     .filter(PartnerMember.id == created["id"])
    #     .first()
    # )

    # assert partner_member_obj.partner_id == created["partner_id"]
    # assert partner_member_obj.email == created["email"]
    # assert partner_member_obj.role == created["role"]
    """
    Write tests for inviting users/adding members to partners after
    establishing permanent mail server
    """


def test_get_partner_members(
    db_session, client, example_partner, example_user, admin_user, access_token
):
    # Create partners in the database
    users = []
    partner_obj = (
        db_session.query(Partner)
        .filter(Partner.name == example_partner.name)
        .first()
    )

    member_obj = (
        db_session.query(User).filter(User.email == example_user.email).first()
    )

    admin_obj = (
        db_session.query(User).filter(User.email == admin_user.email).first()
    )

    users.append(member_obj)
    users.append(admin_obj)

    for user in users:
        association_obj = PartnerMember(
            partner_id=partner_obj.id, user_id=user.id
        )
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


def test_join_organization(
    client,
    partner_publisher: User,
    example_partner: Partner,
    example_members,
    db_session
):
    """
    Two test scenarios
    User already in the organization
    User not in the organization
    """
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_publisher.email,
            "password": example_password
        },
    ).json["access_token"]
    """
    Join Endpoint requires the Invitation
    Table to populated using the /invite endpoint
    Adding a record to the Invitation Table manually
    """
    invite = Invitation(
        partner_id=example_partner.id,
        user_id=example_members["publisher"]["user_id"],
        role="Member"

    )
    db_session.add(invite)
    db_session.commit()

    """
    Deleting existing PartnerMember record
    for "user_id=example_members["publisher"]["user_id"],
     partner_id=example_partner.id" as it
    has already been added to the PartnerMember
    Table using the "example_members function above

    In theory, records should only be added to
    PartnerMember table using the /invite endpoint,
    and after users have accepted their invites.
    """
    db_session.query(PartnerMember).filter_by(
        user_id=example_members["publisher"]["user_id"],
        partner_id=example_partner.id
    ).delete()
    db_session.commit()
    res = client.post(
        "/api/v1/partners/join",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : example_members["publisher"]["user_id"],
            "partner_id": example_partner.id,
            "role": "Member",
            "date_joined": datetime.now(),
            "is_active" : True
        }
    )

    # verify status code
    assert res.status_code == 200

    """
    Verify record has been added to
    Partner Member table after /join endpoint
    """
    partner_member_obj = PartnerMember.query.filter_by(
        user_id=example_members["publisher"]["user_id"],
        partner_id=example_partner.id
    ).first()

    assert partner_member_obj.user_id == example_members["publisher"]["user_id"]
    assert partner_member_obj.partner_id == example_partner.id

    """
    Record in Invitation Table has to
    be deleted after /join endpoint
    Verifying that this is happening correctly
    """
    invitation_check = Invitation.query.filter_by(
        partner_id=example_partner.id,
        user_id=example_members["publisher"]["user_id"]
    ).first()

    assert invitation_check is None


"""
Test for when a user is trying to
join an organization but they are already
added to the organization
"""


def test_join_organization_user_exists(
    client,
    partner_publisher: User,
    example_partner: Partner,
    example_members,
    db_session
):
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_publisher.email,
            "password": example_password
        },
    ).json["access_token"]

    res = client.post(
        "/api/v1/partners/join",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : example_members["publisher"]["user_id"],
            "partner_id": example_partner.id,
            "role": "Member",
            "date_joined": datetime.now(),
            "is_active" : True
        }
    )

    # verify status code
    assert res.status_code == 400


def test_leave_endpoint(
    client,
    partner_publisher: User,
    example_partner: Partner,
    example_members,
    db_session
):
    """
    Can leave org user is already part
    of
    """
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_publisher.email,
            "password": example_password
        },
    ).json["access_token"]

    res = client.delete(
        "/api/v1/partners/leave",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : example_members["publisher"]["user_id"],
            "partner_id": example_partner.id,
        }
    )
    assert res.status_code == 200
    # verify item has been deleted using endpoint
    deleted = PartnerMember.query.filter_by(
        user_id=example_members["publisher"]["user_id"],
        partner_id=example_partner.id
    ).first()
    assert deleted is None

    """
    Cannot leave org one hasnot joined
    """
    res = client.delete(
        "/api/v1/partners/leave",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : example_members["publisher"]["user_id"],
            "partner_id": example_partner.id,
        }
    )

    assert res.status_code == 400

# test:only admin can remove members


def test_remove_member_admin(
    client,
    example_members,
    example_partner,
    partner_admin,
    db_session
):
    """
    Test cases:
    1)Only Admins can remove members
    2)Handle Members in the Partner Org
    assert DB changes
    3)Handle Members not in the Parter Org
    assert DB changes

    """
    # log in as admin
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_admin.email,
            "password": example_password
        },
    ).json["access_token"]

    # use remove_member endpoint as admin
    res = client.delete(
        "/api/v1/partners/remove_member",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : example_members["publisher"]["user_id"],
            "partner_id": example_partner.id,
        }
    )
    assert res.status_code == 200
    removed = PartnerMember.query.filter_by(
        user_id=example_members["publisher"]["user_id"],
        partner_id=example_partner.id
    ).first()
    assert removed is None

# test admins cannot remove other admins


def test_remove_member_admin2(
    client,
    example_members,
    example_partner,
    partner_admin,
    db_session
):
    # log in as admin
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_admin.email,
            "password": example_password
        },
    ).json["access_token"]

    # use remove_member endpoint as admin\
    # trying to remove admin as well
    res = client.delete(
        "/api/v1/partners/remove_member",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : example_members["admin2"]["user_id"],
            "partner_id": example_partner.id,
        }
    )
    assert res.status_code == 400
    removed = PartnerMember.query.filter_by(
        user_id=example_members["admin2"]["user_id"],
        partner_id=example_partner.id,
    ).first()
    assert removed is not None

# admins trying to remove records that don't exist


def test_remove_member_admin3(
    client,
    partner_admin,
):
    # log in as admin
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_admin.email,
            "password": example_password
        },
    ).json["access_token"]

    # use remove_member endpoint as admin\
    # trying to remove record that does not\
    # exist
    res = client.delete(
        "/api/v1/partners/remove_member",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : 99999999,
            "partner_id": 9999999,
        }
    )

    assert res.status_code == 400
    removed = PartnerMember.query.filter_by(
        user_id=99999999,
        partner_id=99999999,
    ).first()
    assert removed is None


"""
withdrawing invitations that exist
"""


def test_withdraw_invitation(
        client,
        partner_admin,
        db_session,
        example_partner,
        example_members,
):
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_admin.email,
            "password": example_password
        },
    ).json["access_token"]

    invite = Invitation(
        partner_id=example_partner.id,
        user_id=example_members["member2"]["user_id"],
        role="Member"

    )
    db_session.add(invite)
    db_session.commit()

    res = client.delete(
        "/api/v1/partners/withdraw_invitation",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : example_members["member2"]["user_id"],
            "partner_id": example_partner.id,
        }
    )
    assert res.status_code == 200
    query = db_session.query(Invitation).filter_by(
        user_id=example_members["member2"]["user_id"],
        partner_id=example_partner.id
    ).first()
    assert query is None


"""
withdrawing invitations that don't exist
"""


def test_withdraw_invitation1(
        client,
        partner_admin,
        db_session,
        example_members,
        example_partner,
):
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_admin.email,
            "password": example_password
        },
    ).json["access_token"]

    res = client.delete(
        "/api/v1/partners/withdraw_invitation",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : example_members["member2"]["user_id"],
            "partner_id": example_partner.id,
        }
    )
    assert res.status_code == 400
    query = db_session.query(Invitation).filter_by(
        user_id=example_members["member2"]["user_id"],
        partner_id=example_partner.id
    ).first()
    assert query is None

# normal:all conditions met


def test_role_change(
        client,
        partner_admin,
        example_partner,
        example_members
):
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_admin.email,
            "password": example_password
        },
    ).json["access_token"]

    res = client.patch(
        "/api/v1/partners/role_change",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : example_members["member2"]["user_id"],
            "partner_id": example_partner.id,
            "role": "Publisher"
        }
    )
    assert res.status_code == 200
    role_change = PartnerMember.query.filter_by(
        user_id=example_members["member2"]["user_id"],
        partner_id=example_partner.id,
    ).first()
    assert role_change.role == "Publisher" and role_change is not None


"""
admin cannot change the role
of another admin
"""


def test_role_change5(
        client,
        partner_admin,
        example_partner,
        example_members
):
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_admin.email,
            "password": example_password
        },
    ).json["access_token"]

    res = client.patch(
        "/api/v1/partners/role_change",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : example_members["admin2"]["user_id"],
            "partner_id": example_partner.id,
            "role": "Publisher"
        }
    )
    assert res.status_code == 400
    role_change = PartnerMember.query.filter_by(
        user_id=example_members["admin2"]["user_id"],
        partner_id=example_partner.id,
    ).first()
    assert role_change.role != "Publisher" and role_change is not None


"""
Rest of the role change tests
are for requests where the partner_id/
user_id is not found
"""


def test_role_change1(
        client,
        partner_admin,
        example_partner,
):
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_admin.email,
            "password": example_password
        },
    ).json["access_token"]

    res = client.patch(
        "/api/v1/partners/role_change",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : float("inf"),
            "partner_id": example_partner.id,
            "role": "Publisher"
        }
    )
    assert res.status_code == 400
    role_change_instance = PartnerMember.query.filter_by(
        user_id=float("inf"),
        partner_id=example_partner.id,
    ).first()
    assert role_change_instance is None


def test_role_change2(
        client,
        partner_admin,
        example_members
):
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_admin.email,
            "password": example_password
        },
    ).json["access_token"]

    res = client.patch(
        "/api/v1/partners/role_change",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : example_members["member2"]["user_id"],
            "partner_id": -1,
            "role": "Publisher"
        }
    )
    assert res.status_code == 400
    role_change_instance = PartnerMember.query.filter_by(
        user_id=example_members["member2"]["user_id"],
        partner_id=-1,
    ).first()
    assert role_change_instance is None


def test_role_change3(
        client,
        partner_admin,
):
    access_token = res = client.post(
        "api/v1/auth/login",
        json={
            "email": partner_admin.email,
            "password": example_password
        },
    ).json["access_token"]

    res = client.patch(
        "/api/v1/partners/role_change",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "user_id" : -1,
            "partner_id": -1,
            "role": "Publisher"
        }
    )
    assert res.status_code == 400
    role_change_instance = PartnerMember.query.filter_by(
        user_id=-1,
        partner_id=-1,
    ).first()
    assert role_change_instance is None
