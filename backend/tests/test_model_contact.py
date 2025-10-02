from backend.database.models.contact import EmailContact, PhoneContact


def test_get_or_create_email():
    email_address = "test@example.com"
    email_contact = EmailContact.get_or_create(email_address)
    assert email_contact is not None
    assert email_contact.email == email_address


def test_get_or_create_phone():
    phone_number = "(123) 456-7890"
    phone_contact = PhoneContact.get_or_create(phone_number)
    assert phone_contact is not None
    assert phone_contact.phone_number == phone_number
