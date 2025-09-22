import pytest
from backend.database.models.user import User, UserRole

def test_get_by_email(example_user):
    user = example_user
    fetched_user = user.get_by_email(user.email)
    assert fetched_user is not None
    assert fetched_user.email == user.email

def test_create_user():
    email = "test@example.com"
    user = User.create_user(
        password="password",
        role=UserRole.PUBLIC.value,
        first_name="Test",
        last_name="User",
        email=email,
        phone_number="123-456-7890"
    )
    assert user is not None
    assert user.email == email