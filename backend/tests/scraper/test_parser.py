import pytest
from bs4 import BeautifulSoup
from backend.scraper.mixins.Parser import ParserMixin


@pytest.fixture
def parser():
    return ParserMixin()

def test__find_and_extract_with_element(parser):
    soup = BeautifulSoup("<div class='test'>Hello, World!</div>", "html.parser")
    result = parser._find_and_extract(soup, "div", "test", "Element not found")
    assert result == "Hello, World!"

def test__find_and_extract_without_element(parser, caplog):
    soup = BeautifulSoup("<div>Hello, World!</div>", "html.parser")
    result = parser._find_and_extract(soup, "div", "test", "Element not found")
    assert result is None
    assert "Element not found" in caplog.text

def test__find_and_extract_with_replace_text(parser):
    soup = BeautifulSoup("<div class='test'>Hello, World!</div>", "html.parser")
    result = parser._find_and_extract(soup, "div", "test", "Element not found", replace_text="Hello, ")
    assert result == "World!"

def test__find_and_extract_without_replace_text(parser):
    soup = BeautifulSoup("<div class='test'>Hello, World!</div>", "html.parser")
    result = parser._find_and_extract(soup, "div", "test", "Element not found")
    assert result == "Hello, World!"