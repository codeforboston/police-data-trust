import pytest
from backend.database import User, UserRole
from backend.auth import user_manager
from flask_jwt_extended import decode_token


@pytest.mark.parametrize(
    ("email", "password", "expected_status_code"),
    [
        ("test@email.com", "my_password", 200),
        ("bad_email", "bad_password", 400),
        (None, None, 400),
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
    [("my_password", 200), ("bad_password", 401), (None, 400)],
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
        "api/v1/auth/test",
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
        "api/v1/auth/test",
    )

    assert test_res.status_code == 200


def test_access_token_fixture(access_token):
    assert len(access_token) > 0
