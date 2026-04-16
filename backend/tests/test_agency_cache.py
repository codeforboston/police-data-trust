from backend.services.agency_cache_service import AgencyCacheService


class StubAgencyCacheQueries:
    def __init__(self, rows):
        self.rows = rows
        self.update_calls = []

    def fetch_agency_metrics_inputs(self):
        return self.rows

    def update_agency_metrics_cache(self, updates):
        self.update_calls.append(updates)
        return len(updates)


def test_refresh_agency_metrics_cache_batches_updates():
    queries = StubAgencyCacheQueries(
        [
            ("a-1", 2, 10, 4, 7),
            ("a-2", 1, 3, 1, 2),
            ("a-3", 0, 0, 0, 0),
        ]
    )
    service = AgencyCacheService(queries=queries)

    result = service.refresh_agency_metrics_cache(batch_size=2)

    assert result["agencies_seen"] == 3
    assert result["agencies_updated"] == 3
    assert len(queries.update_calls) == 2
    assert queries.update_calls[0] == [
        {
            "agency_uid": "a-1",
            "unit_count_cached": 2,
            "officer_count_cached": 10,
            "complaint_count_cached": 4,
            "allegation_count_cached": 7,
            "metrics_updated_at": result["metrics_updated_at"],
        },
        {
            "agency_uid": "a-2",
            "unit_count_cached": 1,
            "officer_count_cached": 3,
            "complaint_count_cached": 1,
            "allegation_count_cached": 2,
            "metrics_updated_at": result["metrics_updated_at"],
        },
    ]
    assert queries.update_calls[1] == [
        {
            "agency_uid": "a-3",
            "unit_count_cached": 0,
            "officer_count_cached": 0,
            "complaint_count_cached": 0,
            "allegation_count_cached": 0,
            "metrics_updated_at": result["metrics_updated_at"],
        },
    ]
