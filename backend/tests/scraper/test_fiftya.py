import pytest
from unittest.mock import patch
from backend.scraper.websites.FiftyA.FiftyA import FiftyA


@pytest.fixture
def fiftyA():
    return FiftyA()


@patch.object(FiftyA, "find_urls")
def test_find_officers(mock_find_urls, fiftyA):
    mock_find_urls.return_value = ["/officer1", "/officer2"]
    result = fiftyA._find_officers("/precinct1")
    mock_find_urls.assert_called_once_with(
        f"{fiftyA.SEED}/precinct1", fiftyA.OFFICER_PATTERN
    )
    assert result == ["/officer1", "/officer2"]



