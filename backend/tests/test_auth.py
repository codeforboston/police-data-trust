import pytest
from backend.database import User, UserRole
from backend.auth import user_manager
from flask_jwt_extended import decode_token

@pytest.fixture
def example_user(db_session):
    user = User(
        email="test@email.com",
        password=user_manager.hash_password("my_password"),
        role=UserRole.PUBLIC,
        first_name="first",
        last_name="last",
    )
    db_session.add(user)
    db_session.commit()
    return user

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

    assert (db_user == None) == (expected_status_code != 200)
    assert res.status_code == expected_status_code


@pytest.mark.parametrize(
    ("password", "expected_status_code"),
    [("my_password", 200), ("bad_password", 401), (None, 400)],
)
def test_login(client, example_user, db_session, password, expected_status_code):
    res = client.post(
        "api/v1/auth/login",
        json={
            "email": example_user.email,
            "password": password,
        },
    )

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

def test_auth_test(client, example_user):
    login_res = client.post(
        'api/v1/auth/login',
        json={
            "email": example_user.email,
            "password": "my_password"
        }
    )
    print(login_res.json["access_token"])

    test_res = client.get(
        'api/v1/auth/test',
        headers={
            "Authorization": "Bearer {0}".format(login_res.json["access_token"])
        }
    )

    assert test_res.status_code == 200
