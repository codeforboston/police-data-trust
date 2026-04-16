from backend.services.officer_cache_service import OfficerCacheService


class StubOfficerCacheQueries:
    def __init__(self, rows):
        self.rows = rows
        self.update_calls = []

    def fetch_officer_metrics_inputs(self):
        return self.rows

    def update_officer_metrics_cache(self, updates):
        self.update_calls.append(updates)
        return len(updates)


def test_refresh_officer_metrics_cache_batches_updates():
    queries = StubOfficerCacheQueries(
        [
            ("o-1", 4, 7, 2),
            ("o-2", 1, 2, 0),
            ("o-3", 0, 0, 0),
        ]
    )
    service = OfficerCacheService(queries=queries)

    result = service.refresh_officer_metrics_cache(batch_size=2)

    assert result["officers_seen"] == 3
    assert result["officers_updated"] == 3
    assert len(queries.update_calls) == 2
    assert queries.update_calls[0] == [
        {
            "officer_uid": "o-1",
            "complaint_count_cached": 4,
            "allegation_count_cached": 7,
            "substantiated_count_cached": 2,
            "metrics_updated_at": result["metrics_updated_at"],
        },
        {
            "officer_uid": "o-2",
            "complaint_count_cached": 1,
            "allegation_count_cached": 2,
            "substantiated_count_cached": 0,
            "metrics_updated_at": result["metrics_updated_at"],
        },
    ]
    assert queries.update_calls[1] == [
        {
            "officer_uid": "o-3",
            "complaint_count_cached": 0,
            "allegation_count_cached": 0,
            "substantiated_count_cached": 0,
            "metrics_updated_at": result["metrics_updated_at"],
        },
    ]
