from unittest import TestCase

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


class TestMpv(TestCase):
    def test_map_cols(self):
        result = map_cols(test_df, test_m)
        self.assertEqual(result.columns, "target_column_name")

    def test_isnan(self):
        self.assertTrue(isnan(float("nan")))
        self.assertFalse(isnan(1.5))

    def test_nan_to_none(self):
        self.assertIsNone(nan_to_none(float("nan")))

    def test_parse_int(self):
        self.assertIsNone(parse_int("test_str"))
