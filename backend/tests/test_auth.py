import pytest
from backend.database.models.user import User, UserRole

mock_user = {
    "email": "existing@email.com",
    "password_hash": User.hash_password("my_password"),
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "role": UserRole.PUBLIC.value,
}


@pytest.fixture
def existing_user():
    user = User(**mock_user)
    user.save()
    return user


@pytest.mark.parametrize(
    (
        "email", "password", "firstname", "lastname",
        "phone_number", "expected_status_code"
    ),
    [
        ("new_user@email.com", "my_password", "John", "Doe", "1234567890", 200),
        ("existing@email.com", "my_password", "John", "Doe", "1234567890", 409),
        ("bad_email", "bad_password", None, None, None, 422),
        (None, None, None, None, None, 422),
    ],
)
def test_register(
    client, existing_user, email, password,
    firstname, lastname, phone_number,
    expected_status_code
):
    res = client.post(
        "api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "firstname": firstname,
            "lastname": lastname,
            "phone_number": phone_number,
        }
    )

    assert res.status_code == expected_status_code

    if expected_status_code == 200:
        assert res.json["status"] == "OK"
        assert res.json["message"] == "Successfully registered."
        assert "Set-Cookie" in res.headers
    elif expected_status_code == 409 and email == "existing@email.com":
        assert res.json["status"] == "Conflict"
        assert res.json["message"] == "Error. Email matches existing account."
    elif expected_status_code == 422:
        assert res.json["status"] == "Unprocessable Entity"
        assert "Invalid request body" in res.json["message"]
    else:
        assert res.json["status"] == "ok"
        assert "Failed to register" in res.json["message"]


@pytest.mark.parametrize(
    ("password", "expected_status_code"),
    [("my_password", 200), ("bad_password", 401), (None, 422)],
)
def test_login(
    db_session,
    client, example_user, password, expected_status_code
):
    res = client.post(
        "api/v1/auth/login",
        json={
            "email": example_user.email,
            "password": password,
        },
    )

    assert ("Set-Cookie" in res.headers) == (expected_status_code == 200)
    assert res.status_code == expected_status_code


# @pytest.mark.parametrize(("use_correct_email"), [(True), (False)])
# def test_forgot_email(mocker, client, example_user, use_correct_email):
#     mock_send_reset_password_email = mocker.spy(
#         flask_user.UserManager, "send_reset_password_email"
#     )
#     mock_send_forgot_password_email = mocker.spy(
#         flask_user.emails, "send_forgot_password_email"
#     )
#     email: str
#     if use_correct_email:
#         email = example_user.email
#     else:
#         email = "fake@email.com"
#     res = client.post("api/v1/auth/forgotPassword", json={"email": email})
#     mock_send_reset_password_email.assert_called_once_with(mock.ANY, email)
#     if use_correct_email:
#         mock_send_forgot_password_email.assert_called_once_with(
#             example_user, mock.ANY, mock.ANY
#         )
#     else:
#         mock_send_forgot_password_email.assert_not_called()
#     assert res.status_code == 200


# @pytest.mark.parametrize(("use_correct_token"), [(True), (False)])
# def test_reset_password(client, example_user, use_correct_token):
#     login_res = client.post(
#         "api/v1/auth/login",
#         json={"email": example_user.email, "password": "my_password"},
#     )
#     token = ""
#     if use_correct_token:
#         token = login_res.json["access_token"]

#     client.post(
#         "api/v1/auth/resetPassword",
#         headers={"Authorization": "Bearer {0}".format(token)},
#         json={
#             "password": "newPassword",
#         },
#     )

#     login_res = client.post(
#         "api/v1/auth/login",
#         json={"email": example_user.email, "password": "newPassword"},
#     )

#     assert (login_res.status_code == 200) == use_correct_token
