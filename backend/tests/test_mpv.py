import pandas as pd
from backend.scraper.data_scrapers.scraper_utils import (
    isnan,
    map_cols,
    nan_to_none,
    parse_int,
)

test_dataset = {"Original_Column_Name": "test"}
test_df = pd.DataFrame([test_dataset])
test_m = {
    "Original_Column_Name": "target_column_name",
}


def test_map_cols():
    result = map_cols(test_df, test_m)
    assert result.columns == "target_column_name"


def test_isnan():
    x = float("nan")
    assert isnan(x) is True
    assert isnan(1.5) is False


def test_nan_to_none():
    x = float("nan")
    assert nan_to_none(x) is None


def test_parse_int():
    assert parse_int("test_str") is None
