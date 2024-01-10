import pytest
from unittest.mock import patch, Mock
from backend.scraper.websites.NYPD.Nypd import Nypd


@pytest.fixture
def nypd():
    return Nypd()


@patch.object(Nypd, "fetch")
def test_find_officers(mock_fetch: Mock, nypd: Nypd):
    mock_fetch.return_value = "officer\nofficer1\nofficer2\nofficer3"
    result = nypd._find_officers() # type: ignore
    mock_fetch.assert_called_once_with(nypd.OFFICER_CSV_PATH)
    assert result == ["officer1", "officer2", "officer3"]


@patch.object(Nypd, "fetch")
def test_find_incidents(mock_fetch: Mock, nypd: Nypd):
    mock_fetch.return_value = "incident\nincident1\nincident2\nincident3"
    result = nypd._find_incidents() # type: ignore
    mock_fetch.assert_called_once_with(nypd.INCIDENTS_CSV_PATH)
    assert result == ["incident1", "incident2", "incident3"]


@patch.object(Nypd, "_find_incidents")
@patch.object(Nypd, "_find_officers")
def test_extract_data(mock_find_officers: Mock, mock_find_incidents: Mock, nypd: Nypd):
    mock_find_officers.return_value = [
        "False,1/2/2024 12:00:00 AM,048210,Richard,Aalbue,912961,POM,Police Officer,H BKLYN,03619,0,0,0",
    ]
    mock_find_incidents.return_value = [
        "1170948,True,1/2/2024 12:00:00 AM,1,011762,Abdelhadi,Aanouz,959433,PO,Police Officer,047 PCT,19427,202201611,3/7/2022 12:00:00 AM,Abuse of Authority,Refusal to provide name,Complaint Withdrawn,2,0,0,,,",
    ]
    officers, incidents = nypd.extract_data()
    assert len(officers) == 1
    assert len(incidents) == 1
    assert officers[0].first_name == "Richard"
    assert officers[0].last_name == "Aalbue"
    assert officers[0].stateId.id_name == "Tax ID Number"
    assert officers[0].stateId.state == "NY"
    assert officers[0].stateId.value == "912961"

    assert incidents[0].date_record_created is None
    assert incidents[0].description == "Refusal to provide name"
    assert incidents[0].location == "047 PCT"
    assert incidents[0].longitude == 40.7128
    assert incidents[0].latitude == 74.006
    assert incidents[0].stop_type == "Abuse of Authority"
    assert incidents[0].call_type == "Abuse of Authority"
    assert incidents[0].has_attachments is False
    assert incidents[0].from_report
    assert incidents[0].was_victim_arrested is False
    assert incidents[0].arrest_id is None
    assert incidents[0].criminal_case_brought is None
    assert incidents[0].case_id == "202201611"
