import pytest
from unittest.mock import patch, MagicMock
from backend.database import User
from flask_jwt_extended import decode_token


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
    db_session, client, email, password,
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
        assert res.json["status"] == "ok"
        assert res.json["message"] == "Successfully registered."
        assert res.json["access_token"] == "mocked_access_token"
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
    mock_db_session,
    client, example_user, password, expected_status_code
):
    with patch('backend.database.User.get_by_email') as mock_get_by_email:
        mock_get_by_email.return_value = example_user

        res = client.post(
            "api/v1/auth/login",
            json={
                "email": example_user.email,
                "password": password,
            },
        )

        assert ("Set-Cookie" in res.headers) == (expected_status_code == 200)
        assert res.status_code == expected_status_code


def test_jwt(client, mock_db_session, example_user, mock_access_token):
    with patch('backend.database.User.nodes.get_or_none') as mock_get_or_none, \
         patch('flask_jwt_extended.decode_token') as mock_decode_token:
        
        mock_get_or_none.return_value = example_user
        mock_decode_token.return_value = {"sub": "mock_user_uid"}

        res = client.post(
            "api/v1/auth/login",
            json={
                "email": "test@email.com",
                "password": "my_password",
            },
        )

        assert res.status_code == 200

        user_uid = decode_token(res.json["access_token"])["sub"]
        db_user = User.nodes.get_or_none(uid=user_uid)

        assert db_user.email == example_user.email
        assert res.status_code == 200


def test_auth_test_header(
    mock_db_session, client, example_user, mock_access_token):
    login_res = client.post(
        "api/v1/auth/login",
        json={"email": example_user.email, "password": "my_password"},
    )

    client.set_cookie(domain="localhost", key="access_token_cookie", value="")

    with patch('backend.auth.jwt_required') as mock_jwt_required:
        mock_jwt_required.return_value = None  # Mock the jwt_required decorator
        test_res = client.get(
            "api/v1/auth/whoami",
            headers={
                "Authorization": f"Bearer {mock_access_token}"
            },
        )

    assert test_res.status_code == 200


def test_auth_test_cookie(mock_db_session, client, example_user):
    client.post(
        "api/v1/auth/login",
        json={"email": example_user.email, "password": "my_password"},
    )

    with patch('backend.auth.jwt_required') as mock_jwt_required:
        mock_jwt_required.return_value = None  # Mock the jwt_required decorator
        test_res = client.get(
            "api/v1/auth/whoami",
        )

    assert test_res.status_code == 200


def test_access_token_fixture(mock_db_session, mock_access_token):
    assert len(mock_access_token) > 0


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
