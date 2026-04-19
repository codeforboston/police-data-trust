from backend.database import (
    MemberRole,
    Source,
    User,
    EmailContact,
    PhoneContact,
    SocialMediaContact,
)
from backend.database.models.user import UserRole


def test_get_user_by_uid(client, access_token):
    user = User.create_user(
        email="lookup@example.com",
        password="my_password",
        role=UserRole.PUBLIC.value,
        first_name="Lookup",
        last_name="User",
        phone_number="(555) 555-1111",
    )
    user.website = "https://example.com"
    user.city = "Brooklyn"
    user.state = "NY"
    user.organization = "NPDC"
    user.title = "Researcher"
    user.biography = "Profile lookup test user"
    user.profile_image = "/tmp/profile.png"
    user.save()

    secondary_email = EmailContact.get_or_create("lookup-secondary@example.com")
    user.secondary_emails.connect(secondary_email)

    social = user.social_media_contacts.single() or SocialMediaContact().save()
    social.linkedin_url = "https://linkedin.com/in/lookup-user"
    social.save()

    res = client.get(
        f"/api/v1/users/{user.uid}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert res.status_code == 200
    assert res.json["uid"] == user.uid
    assert res.json["first_name"] == "Lookup"
    assert res.json["last_name"] == "User"
    assert res.json["website"] == "https://example.com"
    assert res.json["location"] == {"city": "Brooklyn", "state": "NY"}
    assert res.json["employment"] == {"employer": "NPDC", "title": "Researcher"}
    assert res.json["bio"] == "Profile lookup test user"
    assert res.json["primary_email"] == "lookup@example.com"
    assert res.json["contact_info"]["additional_emails"] == [
        "lookup-secondary@example.com"
    ]
    assert (
        res.json["social_media"]["linkedin_url"]
        == "https://linkedin.com/in/lookup-user"
    )
    assert "memberships" not in res.json


def test_get_user_by_uid_not_found(client, access_token):
    res = client.get(
        "/api/v1/users/not-a-real-user",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert res.status_code == 404
    assert res.json["message"] == "User not found"


def test_get_current_user_with_memberships_include(
    client,
    example_user,
    access_token,
):
    source = Source(
        name="Example Affiliation",
        url="https://example.org",
        description="An affiliated source",
    ).save()
    source.members.connect(
        example_user,
        {
            "role": MemberRole.ADMIN.value,
            "is_active": True,
        }
    )

    res = client.get(
        "/api/v1/users/self?include=memberships",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert "memberships" in res.json
    assert len(res.json["memberships"]) == 1
    assert res.json["memberships"][0]["source"] == {
        "uid": source.uid,
        "slug": source.slug,
        "name": "Example Affiliation",
        "description": "An affiliated source",
        "website": "https://example.org",
    }
    assert res.json["memberships"][0]["role"] == MemberRole.ADMIN.value
    assert res.json["memberships"][0]["is_active"] is True
    assert res.json["memberships"][0]["date_joined"] is not None


def test_get_user_by_uid_rejects_invalid_include(client, access_token):
    res = client.get(
        "/api/v1/users/self?include=not-real",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 400


def test_get_people_suggestions(client, example_user, access_token):
    shared_source_a = Source(
        name="Shared Source A",
        url="https://source-a.example.org",
    ).save()
    shared_source_b = Source(
        name="Shared Source B",
        url="https://source-b.example.org",
    ).save()
    unrelated_source = Source(
        name="Unrelated Source",
        url="https://unrelated.example.org",
    ).save()

    shared_source_a.members.connect(
        example_user,
        {
            "role": MemberRole.MEMBER.value,
            "is_active": True,
        }
    )
    shared_source_b.members.connect(
        example_user,
        {
            "role": MemberRole.MEMBER.value,
            "is_active": True,
        }
    )

    strongest_match = User.create_user(
        email="shared-two@example.com",
        password="my_password",
        role=UserRole.PUBLIC.value,
        first_name="Alicia",
        last_name="Nguyen",
    )
    strongest_match.title = "Investigator"
    strongest_match.organization = "NPDC"
    strongest_match.profile_image = "/tmp/alicia.png"
    strongest_match.save()

    shared_source_a.members.connect(
        strongest_match,
        {
            "role": MemberRole.ADMIN.value,
            "is_active": True,
        }
    )
    shared_source_b.members.connect(
        strongest_match,
        {
            "role": MemberRole.MEMBER.value,
            "is_active": True,
        }
    )

    second_match = User.create_user(
        email="shared-one@example.com",
        password="my_password",
        role=UserRole.PUBLIC.value,
        first_name="Brandon",
        last_name="Young",
    )
    second_match.title = "Analyst"
    second_match.organization = "Civic Labs"
    second_match.save()

    shared_source_a.members.connect(
        second_match,
        {
            "role": MemberRole.MEMBER.value,
            "is_active": True,
        }
    )

    inactive_match = User.create_user(
        email="inactive@example.com",
        password="my_password",
        role=UserRole.PUBLIC.value,
        first_name="Inactive",
        last_name="Member",
    )
    shared_source_a.members.connect(
        inactive_match,
        {
            "role": MemberRole.MEMBER.value,
            "is_active": False,
        }
    )

    unrelated_match = User.create_user(
        email="unrelated@example.com",
        password="my_password",
        role=UserRole.PUBLIC.value,
        first_name="Una",
        last_name="Related",
    )
    unrelated_source.members.connect(
        unrelated_match,
        {
            "role": MemberRole.MEMBER.value,
            "is_active": True,
        }
    )

    res = client.get(
        "/api/v1/users/self/suggestions/people?limit=2",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert res.status_code == 200
    assert [item["uid"] for item in res.json["results"]] == [
        strongest_match.uid,
        second_match.uid,
    ]
    assert res.json["results"][0] == {
        "uid": strongest_match.uid,
        "first_name": "Alicia",
        "last_name": "Nguyen",
        "title": "Investigator",
        "organization": "NPDC",
        "profile_image": "/tmp/alicia.png",
        "shared_source_count": 2,
        "shared_sources": [
            {
                "uid": shared_source_a.uid,
                "slug": shared_source_a.slug,
                "name": "Shared Source A",
            },
            {
                "uid": shared_source_b.uid,
                "slug": shared_source_b.slug,
                "name": "Shared Source B",
            },
        ],
    }
    assert res.json["results"][1]["shared_source_count"] == 1


def test_update_current_user_preserves_omitted_contact_fields(
    client,
    example_user,
    access_token,
):
    secondary_email = EmailContact.get_or_create(
        "existing-secondary@example.com"
    )
    example_user.secondary_emails.connect(secondary_email)

    phone_contact = PhoneContact.get_or_create("(555) 555-2222")
    example_user.phone_contacts.connect(phone_contact)

    res = client.patch(
        "/api/v1/users/self",
        json={
            "website": "https://updated.example.com",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    example_user.refresh()

    assert res.status_code == 200
    assert res.json["website"] == "https://updated.example.com"
    assert res.json["contact_info"]["additional_emails"] == [
        "existing-secondary@example.com"
    ]
    assert set(res.json["contact_info"]["phone_numbers"]) == {
        "(012) 345-6789",
        "(555) 555-2222",
    }
    assert [email.email for email in example_user.secondary_emails.all()] == [
        "existing-secondary@example.com"
    ]
    assert {
        phone.phone_number for phone in example_user.phone_contacts.all()
    } == {
        "(012) 345-6789",
        "(555) 555-2222",
    }


def test_update_current_user_only_updates_requested_nested_contact_field(
    client,
    example_user,
    access_token,
):
    secondary_email = EmailContact.get_or_create(
        "existing-secondary@example.com"
    )
    example_user.secondary_emails.connect(secondary_email)

    example_user.phone_contacts.connect(
        PhoneContact.get_or_create("(555) 555-2222")
    )

    res = client.patch(
        "/api/v1/users/self",
        json={
            "contact_info": {
                "additional_emails": ["new-secondary@example.com"],
            },
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    example_user.refresh()

    assert res.status_code == 200
    assert res.json["contact_info"]["additional_emails"] == [
        "new-secondary@example.com"
    ]
    assert set(res.json["contact_info"]["phone_numbers"]) == {
        "(012) 345-6789",
        "(555) 555-2222",
    }
    assert [email.email for email in example_user.secondary_emails.all()] == [
        "new-secondary@example.com"
    ]
    assert {
        phone.phone_number for phone in example_user.phone_contacts.all()
    } == {
        "(012) 345-6789",
        "(555) 555-2222",
    }
