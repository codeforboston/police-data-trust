from backend.database import (
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
    assert res.json["contact_info"]["additional_emails"] == ["lookup-secondary@example.com"]
    assert res.json["social_media"]["linkedin_url"] == "https://linkedin.com/in/lookup-user"


def test_get_user_by_uid_not_found(client, access_token):
    res = client.get(
        "/api/v1/users/not-a-real-user",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert res.status_code == 404
    assert res.json["message"] == "User not found"


def test_update_current_user_preserves_omitted_contact_fields(
    client,
    example_user,
    access_token,
):
    secondary_email = EmailContact.get_or_create("existing-secondary@example.com")
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
    assert {phone.phone_number for phone in example_user.phone_contacts.all()} == {
        "(012) 345-6789",
        "(555) 555-2222",
    }


def test_update_current_user_only_updates_requested_nested_contact_field(
    client,
    example_user,
    access_token,
):
    secondary_email = EmailContact.get_or_create("existing-secondary@example.com")
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
    assert {phone.phone_number for phone in example_user.phone_contacts.all()} == {
        "(012) 345-6789",
        "(555) 555-2222",
    }
