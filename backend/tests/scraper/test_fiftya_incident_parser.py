import pytest
from backend.scraper.websites.FiftyA.FiftyAIncidentParser import (
    FiftyAIncidentParser,
)
from bs4 import BeautifulSoup


@pytest.fixture
def incident_parser():
    return FiftyAIncidentParser()


def test_get_stop_type_with_reason(incident_parser: FiftyAIncidentParser):
    details = [
        "Some details",
        "Reason for contact: Traffic violation",
        "More details",
    ]
    result = incident_parser._get_stop_type(details)
    assert result == "Traffic violation"


def test_get_stop_type_without_reason(incident_parser: FiftyAIncidentParser):
    details = ["Some details", "More details"]
    result = incident_parser._get_stop_type(details)
    assert result is None


def test_get_stop_type_with_multiple_reasons(
    incident_parser: FiftyAIncidentParser,
):
    details = [
        "Some details",
        "Reason for contact: Traffic violation",
        "More details",
        "Reason for contact: Suspicious activity",
    ]
    result = incident_parser._get_stop_type(details)
    assert result == "Traffic violation"


def test_get_location_with_location(incident_parser: FiftyAIncidentParser):
    details_text = "Location: New York"
    expected_location = "New York"
    assert incident_parser._get_location(details_text) == expected_location


def test_get_location_without_location(incident_parser: FiftyAIncidentParser):
    details_text = "No location information available"
    expected_location = None
    assert incident_parser._get_location(details_text) == expected_location


def test_get_location_with_leading_trailing_spaces(
    incident_parser: FiftyAIncidentParser,
):
    details_text = "   Location:   New York   "
    expected_location = "New York"
    assert incident_parser._get_location(details_text) == expected_location


def test_parse_victim_with_valid_soup(incident_parser: FiftyAIncidentParser):
    soup = BeautifulSoup(
        """<html>
            <td class="complainant">
                <td class="complainant">
                Female,&nbsp;<span class="age">55-59</span>
            </td>
        </html>""",
        "html.parser",
    )

    result = incident_parser._parse_victim(soup)

    assert result[0].age == "55"
    assert result[0].gender == "Female"
    assert result[0].ethnicity is None


def test_parse_victim_with_missing_complainant(
    incident_parser: FiftyAIncidentParser,
):
    soup = BeautifulSoup("<html></html>", "html.parser")

    result = incident_parser._parse_victim(soup)

    assert result == []


def test_parse_victim_with_missing_age(incident_parser: FiftyAIncidentParser):
    soup = BeautifulSoup(
        """<html>
            <td class="complainant">
                John Doe
            </td>
        </html>""",
        "html.parser",
    )

    result = incident_parser._parse_victim(soup)

    assert result[0].age is None


def test_parse_victim_with_empty_complainant(
    incident_parser: FiftyAIncidentParser,
):
    soup = BeautifulSoup(
        """<html>
            <td class="complainant"></td>
        </html>""",
        "html.parser",
    )

    result = incident_parser._parse_victim(soup)

    assert result == []
