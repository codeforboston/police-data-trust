import pytest
import math
from flask_jwt_extended import decode_token
from backend.database import Source, MemberRole
from backend.database.models.user import User, UserRole


publisher_email = "pub@source.com"
inactive_email = "lurker@source.com"
admin_email = "leader@source.com"
admin2_email = "leader2@source.com"
member_email = "joe@source.com"
member2_email = "jack@source.com"
example_password = "my_password"

mock_sources = {
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

mock_members = {
    "publisher": {
        "user_email": publisher_email,
        "user_role": UserRole.CONTRIBUTOR.value,
        "source_member": {
            "role": MemberRole.PUBLISHER.value,
            "is_active": True,
        }
    },
    "inactive": {
        "user_email": inactive_email,
        "user_role": UserRole.PUBLIC.value,
        "source_member": {
            "role": MemberRole.MEMBER.value,
            "is_active": False
        }
    },
    "admin": {
        "user_email": publisher_email,
        "user_role": UserRole.CONTRIBUTOR.value,
        "source_member": {
            "role": MemberRole.ADMIN.value,
            "is_active": True
        }
    },
    "member": {
        "user_email": publisher_email,
        "user_role": UserRole.PUBLIC.value,
        "source_member": {
            "role": MemberRole.MEMBER.value,
            "is_active": True
        }
    },
    "admin2" : {
        "user_email": admin_email,
        "user_role": UserRole.CONTRIBUTOR.value,
        "source_member": {
            "role": MemberRole.ADMIN.value,
            "is_active": True
        }
    },
    "member2" : {
        "user_email": member2_email,
        "user_role": UserRole.PUBLIC.value,
        "source_member": {
            "role" : MemberRole.MEMBER.value,
            "is_active" : True
        }
    }
}


@pytest.fixture
def example_sources():
    created = {}

    for name, mock in mock_sources.items():
        p = Source(**mock).save()
        created[name] = p
    return created


@pytest.fixture
def example_members(example_source):
    users = {}

    for name, mock in mock_members.items():
        u = User(
            email=mock["user_email"],
            password_hash=User.hash_password(example_password),
            role=mock["user_role"],
            first_name=name,
            last_name="user",
            phone_number="(278) 555-7890",
        ).save()
        example_source.members.connect(
            u, mock['source_member'])
        users[name] = u
    return users


def test_create_source(client, access_token):
    request = {
        "name": "New Source",
        "url": "newsource.com",
        "contact_email": "admin@newsource.com"
    }

    res = client.post(
        "/api/v1/sources/",
        json=request,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert res.status_code == 200
    response = res.json

    source_obj = (
        Source.nodes.get(uid=response["uid"])
    )
    assert source_obj.name == request["name"]
    assert source_obj.url == request["url"]
    assert source_obj.contact_email == request["contact_email"]
    jwt_decoded = decode_token(access_token)
    user_obj = User.get(jwt_decoded["sub"])

    assert user_obj.role_enum.get_value() >= UserRole.CONTRIBUTOR.get_value()
    assert source_obj.members.is_connected(user_obj)
    assert source_obj.members.relationship(user_obj).is_administrator()


def test_get_source(client, example_source, access_token):
    res = client.get(
        f"/api/v1/sources/{example_source.uid}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert res.status_code == 200
    assert res.json["name"] == example_source.name
    assert res.json["url"] == example_source.url
    assert res.json["contact_email"] == example_source.contact_email


def test_get_all_sources(client, example_sources, access_token):
    all_sources = Source.nodes.all()
    res = client.get(
        "/api/v1/sources/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert res.status_code == 200
    assert res.json['results'][0]["name"] is not None
    assert res.json['results'][0]["contact_email"] is not None
    assert res.json["results"].__len__() == all_sources.__len__()


def test_source_pagination(client, example_sources, access_token):
    all_sources = Source.nodes.all()
    per_page = 1
    expected_total_pages = math.ceil(len(all_sources)//per_page)

    for page in range(1, expected_total_pages + 1):
        res = client.get(
            "/api/v1/sources/",
            query_string={"per_page": per_page, "page": page},
            headers={"Authorization": "Bearer {0}".format(access_token)},
        )

        assert res.status_code == 200
        assert res.json["page"] == page
        assert res.json["total"] == expected_total_pages

        sources = res.json["results"]
        assert len(sources) == per_page

    res = client.get(
        (
            f"/api/v1/sources/?per_page={per_page}"
            f"&page={expected_total_pages + 1}"
        ),
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 404


# def test_add_member_to_source(db_session, example_members):
    # created = example_members["publisher"]

    # source_member_obj = (
    #     db_session.query(SourceMember)
    #     .filter(SourceMember.id == created["id"])
    #     .first()
    # )

    # assert source_member_obj.source_uid == created["source_uid"]
    # assert source_member_obj.email == created["email"]
    # assert source_member_obj.role == created["role"]
    """
    Write tests for inviting users/adding members to sources after
    establishing permanent mail server
    """


def test_get_source_members(
        client, example_source, example_members, access_token):
    members = example_source.members.all()
    res = client.get(
        f"/api/v1/sources/{example_source.uid}/members/",
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )

    assert res.status_code == 200
    assert len(res.json["results"]) == len(members)
    # assert res.json["results"][0]["user"]["email"] == member_obj.email


# def test_join_organization(
#     client,
#     source_publisher: User,
#     example_source: Source,
#     example_members,
#     db_session
# ):
#     """
#     Two test scenarios
#     User already in the organization
#     User not in the organization
#     """
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_publisher.email,
#             "password": example_password
#         },
#     ).json["access_token"]
#     """
#     Join Endpoint requires the Invitation
#     Table to populated using the /invite endpoint
#     Adding a record to the Invitation Table manually
#     """
#     invite = Invitation(
#         source_uid=example_source.id,
#         user_id=example_members["publisher"]["user_id"],
#         role="Member"

#     )
#     db_session.add(invite)
#     db_session.commit()

#     """
#     Deleting existing SourceMember record
#     for "user_id=example_members["publisher"]["user_id"],
#      source_uid=example_source.id" as it
#     has already been added to the SourceMember
#     Table using the "example_members function above

#     In theory, records should only be added to
#     SourceMember table using the /invite endpoint,
#     and after users have accepted their invites.
#     """
#     db_session.query(SourceMember).filter_by(
#         user_id=example_members["publisher"]["user_id"],
#         source_uid=example_source.id
#     ).delete()
#     db_session.commit()
#     res = client.post(
#         "/api/v1/sources/join",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : example_members["publisher"]["user_id"],
#             "source_uid": example_source.id,
#             "role": "Member",
#             "date_joined": datetime.now(),
#             "is_active" : True
#         }
#     )

#     # verify status code
#     assert res.status_code == 200

#     """
#     Verify record has been added to
#     Source Member table after /join endpoint
#     """
#     source_member_obj = SourceMember.query.filter_by(
#         user_id=example_members["publisher"]["user_id"],
#         source_uid=example_source.id
#     ).first()

#     assert source_member_obj.user_id ==
#           example_members["publisher"]["user_id"]
#     assert source_member_obj.source_uid == example_source.id

#     """
#     Record in Invitation Table has to
#     be deleted after /join endpoint
#     Verifying that this is happening correctly
#     """
#     invitation_check = Invitation.query.filter_by(
#         source_uid=example_source.id,
#         user_id=example_members["publisher"]["user_id"]
#     ).first()

#     assert invitation_check is None


# """
# Test for when a user is trying to
# join an organization but they are already
# added to the organization
# """


# def test_join_organization_user_exists(
#     client,
#     source_publisher: User,
#     example_source: Source,
#     example_members,
#     db_session
# ):
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_publisher.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     res = client.post(
#         "/api/v1/sources/join",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : example_members["publisher"]["user_id"],
#             "source_uid": example_source.id,
#             "role": "Member",
#             "date_joined": datetime.now(),
#             "is_active" : True
#         }
#     )

#     # verify status code
#     assert res.status_code == 400


# def test_leave_endpoint(
#     client,
#     source_publisher: User,
#     example_source: Source,
#     example_members,
#     db_session
# ):
#     """
#     Can leave org user is already part
#     of
#     """
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_publisher.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     res = client.delete(
#         "/api/v1/sources/leave",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : example_members["publisher"]["user_id"],
#             "source_uid": example_source.id,
#         }
#     )
#     assert res.status_code == 200
#     # verify item has been deleted using endpoint
#     deleted = SourceMember.query.filter_by(
#         user_id=example_members["publisher"]["user_id"],
#         source_uid=example_source.id
#     ).first()
#     assert deleted is None

#     """
#     Cannot leave org one hasnot joined
#     """
#     res = client.delete(
#         "/api/v1/sources/leave",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : example_members["publisher"]["user_id"],
#             "source_uid": example_source.id,
#         }
#     )

#     assert res.status_code == 400

# # test:only admin can remove members


# def test_remove_member_admin(
#     client,
#     example_members,
#     example_source,
#     source_admin,
#     db_session
# ):
#     """
#     Test cases:
#     1)Only Admins can remove members
#     2)Handle Members in the Source Org
#     assert DB changes
#     3)Handle Members not in the Parter Org
#     assert DB changes

#     """
#     # log in as admin
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_admin.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     # use remove_member endpoint as admin
#     res = client.delete(
#         "/api/v1/sources/remove_member",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : example_members["publisher"]["user_id"],
#             "source_uid": example_source.id,
#         }
#     )
#     assert res.status_code == 200
#     removed = SourceMember.query.filter_by(
#         user_id=example_members["publisher"]["user_id"],
#         source_uid=example_source.id
#     ).first()
#     assert removed is None

# # test admins cannot remove other admins


# def test_remove_member_admin2(
#     client,
#     example_members,
#     example_source,
#     source_admin,
#     db_session
# ):
#     # log in as admin
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_admin.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     # use remove_member endpoint as admin\
#     # trying to remove admin as well
#     res = client.delete(
#         "/api/v1/sources/remove_member",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : example_members["admin2"]["user_id"],
#             "source_uid": example_source.id,
#         }
#     )
#     assert res.status_code == 400
#     removed = SourceMember.query.filter_by(
#         user_id=example_members["admin2"]["user_id"],
#         source_uid=example_source.id,
#     ).first()
#     assert removed is not None

# # admins trying to remove records that don't exist


# def test_remove_member_admin3(
#     client,
#     source_admin,
# ):
#     # log in as admin
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_admin.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     # use remove_member endpoint as admin\
#     # trying to remove record that does not\
#     # exist
#     res = client.delete(
#         "/api/v1/sources/remove_member",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : 99999999,
#             "source_uid": 9999999,
#         }
#     )

#     assert res.status_code == 400
#     removed = SourceMember.query.filter_by(
#         user_id=99999999,
#         source_uid=99999999,
#     ).first()
#     assert removed is None


# """
# withdrawing invitations that exist
# """


# def test_withdraw_invitation(
#         client,
#         source_admin,
#         db_session,
#         example_source,
#         example_members,
# ):
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_admin.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     invite = Invitation(
#         source_uid=example_source.id,
#         user_id=example_members["member2"]["user_id"],
#         role="Member"

#     )
#     db_session.add(invite)
#     db_session.commit()

#     res = client.delete(
#         "/api/v1/sources/withdraw_invitation",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : example_members["member2"]["user_id"],
#             "source_uid": example_source.id,
#         }
#     )
#     assert res.status_code == 200
#     query = db_session.query(Invitation).filter_by(
#         user_id=example_members["member2"]["user_id"],
#         source_uid=example_source.id
#     ).first()
#     assert query is None


# """
# withdrawing invitations that don't exist
# """


# def test_withdraw_invitation1(
#         client,
#         source_admin,
#         db_session,
#         example_members,
#         example_source,
# ):
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_admin.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     res = client.delete(
#         "/api/v1/sources/withdraw_invitation",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : example_members["member2"]["user_id"],
#             "source_uid": example_source.id,
#         }
#     )
#     assert res.status_code == 400
#     query = db_session.query(Invitation).filter_by(
#         user_id=example_members["member2"]["user_id"],
#         source_uid=example_source.id
#     ).first()
#     assert query is None

# # normal:all conditions met


# def test_role_change(
#         client,
#         source_admin,
#         example_source,
#         example_members
# ):
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_admin.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     res = client.patch(
#         "/api/v1/sources/role_change",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : example_members["member2"]["user_id"],
#             "source_uid": example_source.id,
#             "role": "Publisher"
#         }
#     )
#     assert res.status_code == 200
#     role_change = SourceMember.query.filter_by(
#         user_id=example_members["member2"]["user_id"],
#         source_uid=example_source.id,
#     ).first()
#     assert role_change.role == "Publisher" and role_change is not None


# """
# admin cannot change the role
# of another admin
# """


# def test_role_change5(
#         client,
#         source_admin,
#         example_source,
#         example_members
# ):
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_admin.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     res = client.patch(
#         "/api/v1/sources/role_change",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : example_members["admin2"]["user_id"],
#             "source_uid": example_source.id,
#             "role": "Publisher"
#         }
#     )
#     assert res.status_code == 400
#     role_change = SourceMember.query.filter_by(
#         user_id=example_members["admin2"]["user_id"],
#         source_uid=example_source.id,
#     ).first()
#     assert role_change.role != "Publisher" and role_change is not None


# """
# Rest of the role change tests
# are for requests where the source_uid/
# user_id is not found
# """


# def test_role_change1(
#         client,
#         source_admin,
#         example_source,
# ):
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_admin.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     res = client.patch(
#         "/api/v1/sources/role_change",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : float("inf"),
#             "source_uid": example_source.id,
#             "role": "Publisher"
#         }
#     )
#     assert res.status_code == 400
#     role_change_instance = SourceMember.query.filter_by(
#         user_id=float("inf"),
#         source_uid=example_source.id,
#     ).first()
#     assert role_change_instance is None


# def test_role_change2(
#         client,
#         source_admin,
#         example_members
# ):
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_admin.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     res = client.patch(
#         "/api/v1/sources/role_change",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : example_members["member2"]["user_id"],
#             "source_uid": -1,
#             "role": "Publisher"
#         }
#     )
#     assert res.status_code == 400
#     role_change_instance = SourceMember.query.filter_by(
#         user_id=example_members["member2"]["user_id"],
#         source_uid=-1,
#     ).first()
#     assert role_change_instance is None


# def test_role_change3(
#         client,
#         source_admin,
# ):
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_admin.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     res = client.patch(
#         "/api/v1/sources/role_change",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "user_id" : -1,
#             "source_uid": -1,
#             "role": "Publisher"
#         }
#     )
#     assert res.status_code == 400
#     role_change_instance = SourceMember.query.filter_by(
#         user_id=-1,
#         source_uid=-1,
#     ).first()
#     assert role_change_instance is None


# """
# Test for creating a new source
# and adding existing source already created
# """


# def test_create_new_source(
#         client,
#         source_admin

# ):
#     # test for creating new source
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_admin.email,
#             "password": example_password
#         },
#     ).json["access_token"]

#     res = client.post(
#         "/api/v1/sources/create",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "name": "Citizens Police Data Project",
#             "url": "https://cpdp.co",
#             "contact_email": "tech@invisible.institute",
#         }
#     )
#     assert res.status_code == 200
#     source_obj = Source.query.filter_by(
#         url="https://cpdp.co"
#     ).first()
#     assert source_obj.name == "Citizens Police Data Project"
#     assert source_obj.url == "https://cpdp.co"
#     assert source_obj.contact_email == "tech@invisible.institute"

#     # test for adding duplicate source that already exists
#     res = client.post(
#         "/api/v1/sources/create",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "name": "Citizens Police Data Project",
#             "url": "https://cpdp.co",
#             "contact_email": "tech@invisible.institute",
#         }
#     )
#     assert res.status_code == 400


# """
# Validation tests for creating
# new sources
# """


# def test_create_source_validation(
#         client,
#         source_admin
# ):
#     # adding source with blank fields
#     access_token = res = client.post(
#         "api/v1/auth/login",
#         json={
#             "email": source_admin.email,
#             "password": example_password
#         },
#     ).json["access_token"]
#     res = client.post(
#         "/api/v1/sources/create",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "name": "",
#             "url": "https://cpdp.co",
#             "contact_email": "tech@invisible.institute",
#         }
#     )
#     assert res.status_code == 400
#     res = client.post(
#         "/api/v1/sources/create",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "name": "Citizens Police Data Project",
#             "url": "",
#             "contact_email": "tech@invisible.institute",
#         }
#     )
#     assert res.status_code == 400

#     res = client.post(
#         "/api/v1/sources/create",
#         headers={"Authorization": f"Bearer {access_token}"},
#         json={
#             "name": "Citizens Police Data Project",
#             "url": None ,
#             "contact_email": "tech@invisible.institute",
#         }
#     )
#     assert res.status_code == 400
