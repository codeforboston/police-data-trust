import pandas as pd
from backend.scraper.data_scrapers.scraper_utils import (
    cols,
    isnan,
    map_cols,
    nan_to_none,
    parse_int,
    strip_nan,
)

test_dataset = {"Original_Column_Name": "test"}
test_df = pd.DataFrame([test_dataset])
test_m = {
    "Original_Column_Name": "target_column_name",
}


def test_map_cols():
    result = map_cols(test_df, test_m)
    assert result.columns == "target_column_name"


def test_cols():
    result = []
    result.append(cols())
    test_columns = [
        "source_id",
        "victim_name",
        "victim_gender",
        "victim_race",
        "victim_age",
        "victim_image_url",
        "manner_of_injury",
        "incident_date",
        "address",
        "city",
        "state",
        "zip",
        "county",
        "latitude",
        "longitude",
        "description",
        "officer_outcomes",
        "department",
        "criminal_charges",
        "source_link",
        "off_duty_killing",
        "encounter_type_draft",
        "encounter_reason_draft",
        "officer_names_draft",
        "officer_races_draft",
        "officer_known_past_shootings_draft",
        "call_for_service_draft",
    ]
    dataset = cols()
    assert dataset == test_columns


def test_isnan():
    x = float("nan")
    assert isnan(x) is True
    assert isnan(1.5) is False


def test_nan_to_none():
    x = float("nan")
    assert nan_to_none(x) is None


def test_strip():
    x = float("nan")
    test_list = [1, 2, 3, 4, x]
    assert strip_nan(test_list) == [1, 2, 3, 4]


def test_map_df(df, mapper):
    return [mapper(strip_nan(r)) for r in df.itertuples(index=False)]


def test_parse_int():
    assert parse_int("test_str") is None
