import pytest
from backend.scraper.websites.FiftyA.FiftyA import FiftyA
from backend.database import Officer, Incident
from unittest.mock import patch, Mock


@pytest.fixture
def fiftya():
    return FiftyA()


def test_find_officers(fiftya: FiftyA):
    precinct = "/command/123"
    officers = fiftya._find_officers(precinct)
    assert isinstance(officers, list)
    assert all(isinstance(officer, str) for officer in officers)


def test_sample_list(fiftya: FiftyA):
    lst = ["a", "b", "c", "d", "e"]
    num = 3
    sampled_list = fiftya.sample_list(lst, num)
    assert isinstance(sampled_list, list)
    assert len(sampled_list) == min(num, len(lst))


@patch.object(FiftyA, "_find_officers")
@patch.object(FiftyA, "find_urls")
def test_find_officers_in_precincts(
    mock_find_urls: Mock, mock__find_officers: Mock, fiftya: FiftyA
):
    mock_find_urls.return_value = ["/command/1", "/command/2", "/command/3"]
    mock__find_officers.return_value = [
        "/officer/1",
        "/officer/2",
        "/officer/3",
    ]
    officers = fiftya._find_officers_in_precincts(debug=False)
    assert isinstance(officers, list)
    assert all(isinstance(officer, str) for officer in officers)


def test_find_incidents(fiftya: FiftyA):
    complaints = ["/complaint/1", "/complaint/2", "/complaint/3"]
    incidents = fiftya._find_incidents(complaints)
    assert isinstance(incidents, list)
    assert all(isinstance(incident, Incident) for incident in incidents)


def test_find_officer_profile_and_complaints(fiftya: FiftyA):
    officers = ["/officer/1", "/officer/2", "/officer/3"]
    officer_profiles, complaints = fiftya._find_officer_profile_and_complaints(
        officers
    )
    assert isinstance(officer_profiles, list)
    assert all(isinstance(profile, Officer) for profile in officer_profiles)
    assert isinstance(complaints, list)
    assert all(isinstance(complaint, str) for complaint in complaints)


def test_extract_data(fiftya: FiftyA):
    officer_profiles, incidents = fiftya.extract_data(debug=True)
    assert isinstance(officer_profiles, list)
    assert all(isinstance(profile, Officer) for profile in officer_profiles)
    assert isinstance(incidents, list)
    assert all(isinstance(incident, Incident) for incident in incidents)
