from unittest.mock import patch, Mock
import pytest
from backend.scraper.run_scrape import add_to_database


@pytest.fixture
def cache():
    cache = Mock()
    cache.get_json.return_value = {"model": "data"}
    return cache


@pytest.fixture
def model():
    model = Mock()
    model.__getstate__ = Mock(return_value={"model": "data"})
    return model


@pytest.fixture
def uid():
    return "123"


@pytest.fixture
def table():
    return "officer"


def test_add_to_database_existing_in_cache(
    cache: Mock, model: Mock, uid: str, table: str
):
    # Calling the function
    add_to_database(model, cache, uid, table)

    # Assertions
    cache.get_json.assert_called_once_with(uid, table)
    model.create.assert_not_called()
    cache.set_json.assert_not_called()


@patch("backend.scraper.run_scrape.officer_exists")
def test_add_to_database_existing_in_database(
    mock_officer_exists: Mock,
    cache: Mock,
    model: Mock,
    uid: str,
    table: str,
):
    cache.get_json.return_value = None
    mock_officer_exists.return_value = True

    # Calling the function
    add_to_database(model, cache, uid, table)

    # Assertions
    cache.get_json.assert_called_once_with(uid, table)
    model.delete.assert_called_once()
    model.create.assert_called_once()
    cache.set_json.assert_called_once()
    mock_officer_exists.assert_called_once()


@patch("backend.scraper.run_scrape.officer_exists")
def test_add_to_database_new_model(
    mock_officer_exists: Mock, cache: Mock, model: Mock, uid: str, table: str
):
    cache.get_json.return_value = None
    mock_officer_exists.return_value = model

    # Calling the function
    add_to_database(model, cache, uid, table)

    # Assertions
    cache.get_json.assert_called_once_with(uid, table)
    model.create.assert_called_once()
    cache.set_json.assert_called_once_with(uid, model.__getstate__(), table)
    mock_officer_exists.assert_called_once()


def test_add_to_database_invalid_table(cache: Mock, model: Mock, uid: str):
    table = "invalid_table"

    # Calling the function
    try:
        add_to_database(model, cache, uid, table)
    except ValueError as e:
        # Assertion
        assert str(e) == "Invalid table invalid_table"
