import flask_user
from backend.database import User
from flask_jwt_extended import decode_token
from unittest import mock, TestCase


class TestAuth(TestCase):
    def test_register(self, client, db_session):
        for case in [
            ("test@email.com", "my_password", 200),
            ("bad_email", "bad_password", 422),
            (None, None, 422),
        ]:
            email, password, expected_status_code = case

            res = client.post(
                "api/v1/auth/register",
                json={
                    "email": email,
                    "password": password,
                },
            )

            db_user = db_session.query(User).filter(email == User.email).first()
            self.assertTrue(("Set-Cookie" in res.headers) is (expected_status_code == 200))
            self.assertTrue((db_user is not None) is (expected_status_code == 200))
            self.assertEqual(res.status_code, expected_status_code)

    def test_login(self, client, example_user):
        for password, expected_status_code in {
            "my_password": 200,
            "bad_password": 401,
            None: 422,
        }.items():
            res = client.post(
                "api/v1/auth/login",
                json={
                    "email": example_user.email,
                    "password": password,
                },
            )

            self.assertTrue(("Set-Cookie" in res.headers) is (expected_status_code == 200))
            self.assertEqual(res.status_code, expected_status_code)

    def test_jwt(self, client, db_session, example_user):
        res = client.post(
            "api/v1/auth/login",
            json={
                "email": "test@email.com",
                "password": "my_password",
            },
        )

        self.assertEqual(res.status_code, 200)

        user_id = decode_token(res.json["access_token"])["sub"]
        db_user = db_session.query(User).filter(user_id == User.id).first()

        self.assertEqual(db_user.email, example_user.email)
        self.assertEqual(res.status_code, 200)

    def test_auth_test_header(self, client, example_user):
        login_res = client.post(
            "api/v1/auth/login",
            json={"email": example_user.email, "password": "my_password"},
        )

        client.set_cookie(domain="localhost", key="access_token_cookie", value="")

        test_res = client.get(
            "api/v1/auth/whoami",
            headers={
                "Authorization": f"Bearer {login_res.json['access_token']}"
            },
        )

        self.assertEqual(test_res.status_code, 200)

    def test_auth_test_cookie(self, client, example_user):
        client.post(
            "api/v1/auth/login",
            json={"email": example_user.email, "password": "my_password"},
        )

        test_res = client.get(
            "api/v1/auth/whoami",
        )

        self.assertEqual(test_res.status_code, 200)

    def test_forgot_email(self, mocker, client, example_user):
        mock_send_reset_password_email = mocker.spy(
            flask_user.UserManager, "send_reset_password_email"
        )
        mock_send_forgot_password_email = mocker.spy(
            flask_user.emails, "send_forgot_password_email"
        )
        email: str
        for use_correct_email in {True, False}:
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
            self.assertEqual(res.status_code, 200)

    def test_reset_password(self, client, example_user):
        login_res = client.post(
            "api/v1/auth/login",
            json={"email": example_user.email, "password": "my_password"},
        )
        token = ""
        for use_correct_token in {True, False}:
            if use_correct_token:
                token = login_res.json["access_token"]

            client.post(
                "api/v1/auth/resetPassword",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "password": "newPassword",
                },
            )

            login_res = client.post(
                "api/v1/auth/login",
                json={"email": example_user.email, "password": "newPassword"},
            )

            self.assertTrue((login_res.status_code == 200) is use_correct_token)

    def test_access_token_fixture(self, access_token):
        self.assertGreater(len(access_token), 0)
