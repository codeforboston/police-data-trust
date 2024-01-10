import pytest
from bs4 import BeautifulSoup
from backend.scraper.websites.FiftyA.FiftyAOfficerParser import (
    FiftyAOfficerParser,
)


@pytest.fixture
def officer_parser():
    return FiftyAOfficerParser()


def test_parse_officer_with_invalid_soup(officer_parser: FiftyAOfficerParser):
    soup = BeautifulSoup("<html></html>", "html.parser")

    result = officer_parser.parse_officer(soup)

    assert result is None


def test_parse_officer_with_valid_soup(officer_parser: FiftyAOfficerParser):
    soup = BeautifulSoup(
        """<html>
            <h1 class="title name">John Doe</h1>
            <span class="desc">White Male 30</span>
            <span class="taxid">Tax #12345</span>
            <a href='/complaint/1'>Complaint 1</a>
            <a href='/complaint/2'>Complaint 2</a>
        </html>""",
        "html.parser",
    )

    result = officer_parser.parse_officer(soup)
    assert result is not None
    assert result.officer.date_of_birth == "1994-01-01"
    assert result.officer.first_name == "John"
    assert result.officer.last_name == "Doe"
    assert result.officer.stateId.id_name == "Tax ID Number"
    assert result.officer.stateId.state == "NY"
    assert result.officer.stateId.value == "12345"
    assert result.complaints == ["/complaint/1", "/complaint/2"]


def test_parse_officer_with_missing_title(officer_parser: FiftyAOfficerParser):
    soup = BeautifulSoup(
        """<html>
            <span class="desc">White Male 30</span>
            <span class="taxid">Tax #12345</span>
        </html>""",
        "html.parser",
    )

    result = officer_parser.parse_officer(soup)

    assert result is None


def test_parse_officer_with_missing_tax_id(officer_parser: FiftyAOfficerParser):
    soup = BeautifulSoup(
        """<html>
            <h1 class="title name">John Doe</h1>
            <span class="desc">White Male 30</span>
        </html>""",
        "html.parser",
    )

    result = officer_parser.parse_officer(soup)

    assert result is None


def test_get_work_history_with_valid_soup(officer_parser: FiftyAOfficerParser):
    soup = BeautifulSoup(
        """<html>
            <div class="commandhistory">
                <a href='/command/precinct1'>Precinct 1</a>
                <a href='/command/precinct2'>Precinct 2</a>
            </div>
        </html>""",
        "html.parser",
    )

    expected_result = ["Precinct 1", "Precinct 2"]

    result = officer_parser._get_work_history(soup)

    assert result == expected_result


def test_get_work_history_with_missing_div(officer_parser: FiftyAOfficerParser):
    soup = BeautifulSoup("<html></html>", "html.parser")

    expected_result = []

    result = officer_parser._get_work_history(soup)

    assert result == expected_result


def test_get_work_history_with_missing_links(
    officer_parser: FiftyAOfficerParser,
):
    soup = BeautifulSoup(
        """<html>
            <div class="commandhistory">
            </div>
        </html>""",
        "html.parser",
    )

    expected_result = []

    result = officer_parser._get_work_history(soup)

    assert result == expected_result
