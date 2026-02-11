from __future__ import annotations
import pytest
from backend.database import (
    Officer
)


mock_officers = {
    "john": {
        "first_name": "John",
        "last_name": "Doe",
        "ethnicity": "White",
        "gender": "Male"
    },
    "hazel": {
        "first_name": "Hazel",
        "last_name": "Nutt",
        "ethnicity": "White",
        "gender": "Female"
    },
    "frank": {
        "first_name": "Frank",
        "last_name": "Furter",
        "ethnicity": "Black/African American",
        "gender": "Male"
    }
}


@pytest.fixture
def example_officers():
    # Create Officers in the database
    officers = {}
    for name, mock in mock_officers.items():
        o = Officer(**mock).save()
        officers[name] = o
    return officers


def test_get_employment_history(
        client, example_officer, example_employment, access_token):
    # Test that we can get it
    res = client.get(
        f"/api/v1/officers/{example_officer.uid}",
        query_string={
            "include": ["employment"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert res.status_code == 200
    assert "employment_history" in res.json
    assert res.json["employment_history"][0].get(
        "badge_number") == example_employment.badge_number
    assert res.json["employment_history"][0].get(
        "earliest_date") == example_employment.earliest_date.isoformat()


def test_get_allegation_summary(
        client, example_officer, example_complaint, access_token):
    # Test that we can get officer allegation summary from metrics endpoint
    res = client.get(
        f"/api/v1/officers/{example_officer.uid}",
        query_string={
            "include": ["allegations"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert res.status_code == 200
    assert "allegation_summary" in res.json


def test_get_complaint_history(
        client, example_officer, example_complaint,
        example_allegation, access_token):
    # Test that we can get officer complaint history from metrics endpoint
    res = client.get(
        f"/api/v1/officers/{example_officer.uid}/metrics",
        query_string={
            "include": ["complaint_history"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    c_year = example_complaint.incident_date.year
    assert example_allegation.accused.is_connected(example_officer)
    assert example_allegation.complaint.is_connected(example_complaint)

    assert res.status_code == 200
    assert "officer_uid" in res.json
    assert res.json["officer_uid"] == example_officer.uid
    assert "complaint_history" in res.json

    history = res.json["complaint_history"]
    for year_data in history:
        assert "year" in year_data
        assert "complaint_count" in year_data
        assert "closed_count" in year_data
        if year_data["year"] == c_year:
            assert year_data.get("complaint_count", 0) == 1
            assert year_data.get("closed_count", 0) == 1
            break


def test_get_allegation_types(
        client, example_officer, example_allegation, access_token):
    # Test that we can get officer complaint history from metrics endpoint
    res = client.get(
        f"/api/v1/officers/{example_officer.uid}/metrics",
        query_string={
            "include": ["allegation_types"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert res.status_code == 200
    assert "officer_uid" in res.json
    assert res.json["officer_uid"] == example_officer.uid
    assert "allegation_types" in res.json
    type_list = res.json["allegation_types"].get("top_types", [])
    assert any(at["type"] == example_allegation.type for at in type_list)


def test_get_allegation_outcomes(
        client, example_officer, example_allegation, access_token):
    # Test that we can get officer complaint history from metrics endpoint
    res = client.get(
        f"/api/v1/officers/{example_officer.uid}/metrics",
        query_string={
            "include": ["allegation_outcomes"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert res.status_code == 200
    assert "officer_uid" in res.json
    assert res.json["officer_uid"] == example_officer.uid
    assert "allegation_outcomes" in res.json


def test_get_complainant_demo(
        client, example_officer, example_allegation, access_token):
    # Test that we can get officer complaint history from metrics endpoint
    res = client.get(
        f"/api/v1/officers/{example_officer.uid}/metrics",
        query_string={
            "include": ["complainant_demographics"]
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert res.status_code == 200
    assert "officer_uid" in res.json
    assert res.json["officer_uid"] == example_officer.uid
    assert "complainant_demographics" in res.json
