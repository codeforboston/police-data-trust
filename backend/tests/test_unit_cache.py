from backend.services.unit_cache_service import UnitCacheService


class StubUnitCacheQueries:
    def __init__(self, rows):
        self.rows = rows
        self.update_calls = []

    def fetch_unit_metrics_inputs(self):
        return self.rows

    def update_unit_metrics_cache(self, updates):
        self.update_calls.append(updates)
        return len(updates)


def test_refresh_unit_metrics_cache_batches_updates():
    queries = StubUnitCacheQueries(
        [
            ("u-1", 10, 4, 7),
            ("u-2", 3, 1, 2),
            ("u-3", 0, 0, 0),
        ]
    )
    service = UnitCacheService(queries=queries)

    result = service.refresh_unit_metrics_cache(batch_size=2)

    assert result["units_seen"] == 3
    assert result["units_updated"] == 3
    assert len(queries.update_calls) == 2
    assert queries.update_calls[0] == [
        {
            "unit_uid": "u-1",
            "officer_count_cached": 10,
            "complaint_count_cached": 4,
            "allegation_count_cached": 7,
            "metrics_updated_at": result["metrics_updated_at"],
        },
        {
            "unit_uid": "u-2",
            "officer_count_cached": 3,
            "complaint_count_cached": 1,
            "allegation_count_cached": 2,
            "metrics_updated_at": result["metrics_updated_at"],
        },
    ]
    assert queries.update_calls[1] == [
        {
            "unit_uid": "u-3",
            "officer_count_cached": 0,
            "complaint_count_cached": 0,
            "allegation_count_cached": 0,
            "metrics_updated_at": result["metrics_updated_at"],
        },
    ]
