import pytest


@pytest.mark.parametrize(
    ("page", "expected_status_code"),
    [("/", 200), ("/api/v1/healthcheck", 200)],
)
def test_simple_routes(client, page, expected_status_code):
    assert client.get(page).status_code == expected_status_code
