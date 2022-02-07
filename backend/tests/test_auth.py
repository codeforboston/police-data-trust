import flask_user
import pytest
from backend.database import User
from flask_jwt_extended import decode_token
from unittest import mock


@pytest.mark.parametrize(
    ("email", "password", "expected_status_code"),
    [
        ("test@email.com", "my_password", 200),
        ("bad_email", "bad_password", 422),
        (None, None, 422),
    ],
)
def test_register(client, db_session, email, password, expected_status_code):
    res = client.post(
        "api/v1/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    db_user = db_session.query(User).filter(email == User.email).first()
    assert ("Set-Cookie" in res.headers) == (expected_status_code == 200)
    assert (db_user is not None) == (expected_status_code == 200)
    assert res.status_code == expected_status_code


@pytest.mark.parametrize(
    ("password", "expected_status_code"),
    [("my_password", 200), ("bad_password", 401), (None, 422)],
)
def test_login(
    client, example_user, db_session, password, expected_status_code
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


def test_jwt(client, db_session, example_user):
    res = client.post(
        "api/v1/auth/login",
        json={
            "email": "test@email.com",
            "password": "my_password",
        },
    )

    assert res.status_code == 200

    user_id = decode_token(res.json["access_token"])["sub"]
    db_user = db_session.query(User).filter(user_id == User.id).first()

    assert db_user.email == example_user.email
    assert res.status_code == 200


def test_auth_test_header(client, example_user):
    login_res = client.post(
        "api/v1/auth/login",
        json={"email": example_user.email, "password": "my_password"},
    )

    client.set_cookie("localhost", "access_token_cookie", value="")

    test_res = client.get(
        "api/v1/auth/whoami",
        headers={
            "Authorization": "Bearer {0}".format(login_res.json["access_token"])
        },
    )

    assert test_res.status_code == 200


def test_auth_test_cookie(client, example_user):
    client.post(
        "api/v1/auth/login",
        json={"email": example_user.email, "password": "my_password"},
    )

    test_res = client.get(
        "api/v1/auth/whoami",
    )

    assert test_res.status_code == 200


@pytest.mark.parametrize(("use_correct_email"), [(True), (False)])
def test_forgot_email(mocker, client, example_user, use_correct_email):
    mock_send_reset_password_email = mocker.spy(
        flask_user.UserManager, "send_reset_password_email"
    )
    mock_send_forgot_password_email = mocker.spy(
        flask_user.emails, "send_forgot_password_email"
    )
    email: str
    if use_correct_email:
        email = example_user.email
    else:
        email = "fake@email.com"
    res = client.post("api/v1/auth/forgotPassword", json={"email": email})
    mock_send_reset_password_email.assert_called_once_with(mock.ANY, email)
    if use_correct_email:
        mock_send_forgot_password_email.assert_called_once_with(
            example_user, mock.ANY, mock.ANY
        )
    else:
        mock_send_forgot_password_email.assert_not_called()
    assert res.status_code == 200


@pytest.mark.parametrize(("use_correct_token"), [(True), (False)])
def test_reset_password(client, example_user, use_correct_token):
    login_res = client.post(
        "api/v1/auth/login",
        json={"email": example_user.email, "password": "my_password"},
    )
    token = ""
    if use_correct_token:
        token = login_res.json["access_token"]

    client.post(
        "api/v1/auth/resetPassword",
        headers={"Authorization": "Bearer {0}".format(token)},
        json={
            "password": "newPassword",
        },
    )

    login_res = client.post(
        "api/v1/auth/login",
        json={"email": example_user.email, "password": "newPassword"},
    )

    assert (login_res.status_code == 200) == use_correct_token


def test_access_token_fixture(access_token):
    assert len(access_token) > 0
