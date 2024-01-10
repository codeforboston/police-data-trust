from unittest.mock import patch, Mock
from backend.scraper.run_scrape import scrape


@patch("backend.scraper.run_scrape.FiftyA")
@patch("backend.scraper.run_scrape.Nypd")
@patch("backend.scraper.run_scrape.ScrapeCacheContainer")
def test_scrape(mock_cache_container: Mock, mock_nypd: Mock, mock_fiftya: Mock):
    # Mock the necessary dependencies
    # mock_cache = mock_cache_container.return_value.get_cache.return_value
    mock_fiftya_instance = mock_fiftya.return_value
    mock_nypd_instance = mock_nypd.return_value

    # Create mock officer objects
    mock_officer1 = Mock()
    mock_officer1.stateId.state = "NY"
    mock_officer1.stateId.value = "912961"
    mock_officer2 = Mock()
    mock_officer2.stateId.state = "NY"
    mock_officer2.stateId.value = "959433"

    incident1 = Mock()
    incident1.source_details.reporting_organization = "FiftyA"
    incident1.case_id = "202201611"
    incident2 = Mock()
    incident2.source_details.reporting_organization = "NYPD"
    incident2.case_id = "202201611"
    incident3 = Mock()
    incident3.source_details.reporting_organization = "FiftyA"
    incident3.case_id = "202201611"
    incident4 = Mock()
    incident4.source_details.reporting_organization = "NYPD"
    incident4.case_id = "202201611"

    # Mock the extract_data method of FiftyA
    mock_fiftya_instance.extract_data.return_value = (
        [mock_officer1, mock_officer2],
        [incident1, incident2],
    )

    # Mock the extract_data method of Nypd
    mock_nypd_instance.extract_data.return_value = (
        [mock_officer1, mock_officer2],
        [incident3, incident4],
    )

    # Call the scrape function
    scrape()

    # Assert that the necessary methods were called with the correct arguments
    mock_fiftya.assert_called_once_with()
    mock_fiftya_instance.extract_data.assert_called_once_with(debug=False)
    mock_nypd.assert_called_once_with()
    mock_nypd_instance.extract_data.assert_called_once_with(debug=False)

    # Assert that the officers and incidents were merged correctly
    assert mock_fiftya_instance.extract_data.call_count == 1
    assert mock_nypd_instance.extract_data.call_count == 1
    assert len(mock_fiftya_instance.extract_data.return_value[0]) == 2
    assert len(mock_fiftya_instance.extract_data.return_value[1]) == 2
    assert len(mock_nypd_instance.extract_data.return_value[0]) == 2
    assert len(mock_nypd_instance.extract_data.return_value[1]) == 2

    # TODO: Add more tests here
