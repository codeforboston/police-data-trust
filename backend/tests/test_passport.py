import pytest
from backend.database.models.passport_request import RequestStatus
from backend.database.models.types.enums import UserRole
from ..database import PassportRequest, User
from .conftest import example_password

def test_create_request(client, db_session, example_user):
    res = client.post(
        "api/v1/passportRequests",
        json={
            "role": UserRole.PASSPORT,
            "user_id": example_user.id,
        },
    )
    print(res)
    db_request = db_session.query(PassportRequest).filter(PassportRequest.user_id == example_user.id).first()
    assert (db_request is not None)
    assert res.status_code == 200

def test_double_request(client, db_session, example_user):
  res = client.post(
      "api/v1/passportRequests",
      json={
          "role": UserRole.PASSPORT,
          "user_id": example_user.id,
      },
  )

  db_count = db_session.query(PassportRequest).filter(PassportRequest.user_id == example_user.id).first()
  assert (db_count is not None)
  assert res.status_code == 200

  res = client.post(
      "api/v1/passportRequests",
      json={
          "role": UserRole.PASSPORT,
          "user_id": example_user.id,
      },
  )

  db_count = db_session.query(PassportRequest).filter(PassportRequest.user_id == example_user.id).count()

  assert db_count == 1
  assert res.status_code == 400

def test_approve_request(client, db_session, example_user, admin_user):
  request = PassportRequest(
    user_id = example_user.id,
    role = UserRole.PASSPORT
  )
  db_session.add(request);
  db_session.commit();

  login_res = client.post(
    "api/v1/auth/login", 
    json = {
      "email": admin_user.email,
      "password": example_password,
    }
  )
  
  res = client.put(
    "api/v1/passportRequests/{}/status".format(request.id),
    json={
      "status": RequestStatus.APPROVED,
    },
    headers={
      "Authorization": "Bearer {0}".format(login_res.json["access_token"])
    },
  )
  
  db_user = User.get(example_user.id)
  assert res.status_code == 200
  assert db_user.role == UserRole.PASSPORT

def test_deny_request(client, db_session, example_user, admin_user):
  request = PassportRequest(
    user_id = example_user.id,
    role = UserRole.PASSPORT
  )
  db_session.add(request);
  db_session.commit();

  login_res = client.post(
    "api/v1/auth/login", 
    json = {
      "email": admin_user.email,
      "password": example_password,
    }
  )
  
  res = client.put(
    "api/v1/passportRequests/{}/status".format(request.id),
    json={
      "status": RequestStatus.DENIED,
    },
    headers={
      "Authorization": "Bearer {0}".format(login_res.json["access_token"])
    },
  )
  
  db_user = User.get(example_user.id)
  assert res.status_code == 200
  assert db_user.role == UserRole.PUBLIC

def test_get_request(db_session, client, admin_user, example_user):
  request = PassportRequest(
    user_id = example_user.id,
    role = UserRole.PASSPORT
  )
  db_session.add(request);
  db_session.commit();

  login_res = client.post(
    "api/v1/auth/login",
    json={
      "email": admin_user.email,
      "password": example_password,
    }
  )

  res = client.get(
    "api/v1/passportRequests/{0}".format(request.id),
    headers={
      "Authorization": "Bearer {0}".format(login_res.json["access_token"])
    },
  )

  assert res.status_code == 200
  assert res.json["user_id"] == example_user.id
  assert res.json["role"] == request.role
  