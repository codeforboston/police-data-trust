import pytest
from backend.dto import RegisterUserDTO
from backend.database import User
from backend.auth import user_manager
from flask_jwt_extended import decode_token

@pytest.mark.parametrize(
    ("email", "password", "expected_status_code"),
    [("test@email.com", "password", 200),
    ("bad_email", "bad_password", 400),
    (None, None, 400)]
)
def test_register(client, email, password, expected_status_code):
  res = client.post(
    "api/v1/auth/register",
    json={
      "email": email,
      "password": password,
    },
  )
  assert res.status_code == expected_status_code

@pytest.mark.parametrize(
    ("password", "expected_status_code"),
    [("password", 200),
    ("bad_password", 401),
    (None, 400)]
)
def test_login(client, db_session, password, expected_status_code):
  test_user = User(email="test2@email.com", password=user_manager.hash_password("password"), first_name="first", last_name="last")
  db_session.add(test_user)
  db_session.commit()

  res = client.post(
    "api/v1/auth/login",
    json={
      "email": "test2@email.com",
      "password": password,
    }
  )

  assert res.status_code == expected_status_code

def test_jwt(client, db_session):
  test_user = User(email="test3@email.com", password=user_manager.hash_password("password"), first_name="first", last_name="last")
  db_session.add(test_user)
  db_session.commit()

  res = client.post(
    "api/v1/auth/login",
    json={
      "email": "test3@email.com",
      "password": "password",
    }
  )

  assert res.status_code == 200

  user_id = decode_token(res.json["access_token"])["sub"]
  db_user = db_session.query(User).filter(user_id == User.id).first()

  assert db_user.email == test_user.email
  assert res.status_code == 200

