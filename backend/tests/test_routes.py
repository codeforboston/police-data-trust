import pytest


@pytest.mark.parametrize(
    ("page", "expected_status_code"),
    [
        ("/incidents", 200),
    ],
)
def test_routes(client, page, expected_status_code):
    assert client.get(page).status_code == expected_status_code
