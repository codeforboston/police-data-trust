from unittest import TestCase


class TestRoutes(TestCase):
    def test_routes(self, client):
        for page, expected_status_code in {
            "/": 200,
            "/api/v1/healthcheck": 200,
        }.items():
            self.assertEqual(client.get(page).status_code, expected_status_code)
