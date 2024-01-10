import pytest
import requests_mock
import re
from backend.scraper.mixins.Scraper import ScraperMixin


@pytest.fixture
def scraper():
    return ScraperMixin()


def test_init(scraper):
    assert scraper.rate_limit == 5


def test_fetch(scraper):
    url = "http://test.com"
    with requests_mock.Mocker() as m:
        m.get(url, text="response")
        result = scraper.fetch(url)
        assert result == "response"


def test_fetch_error(scraper):
    url = "http://test.com"
    with requests_mock.Mocker() as m:
        m.get(url, status_code=404)
        result = scraper.fetch(url)
        assert result is None


def test_fetch_retries(scraper):
    url = "http://test.com"
    with requests_mock.Mocker() as m:
        m.get(url, [{"status_code": 500}, {"status_code": 200, "text": "response"}])
        result = scraper.fetch(url)
        assert result == "response"


def test_find_urls(scraper):
    url = "http://test.com"
    pattern = re.compile(r"^\/page\/\w+$")
    with requests_mock.Mocker() as m:
        m.get(url, text='<a href="/page/page1"></a><a href="/page/page2"></a>')
        result = scraper.find_urls(url, pattern)
        assert result == ["/page/page1", "/page/page2"]
