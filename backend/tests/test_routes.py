from datetime import datetime

import pytest

from backend.database import Incident


@pytest.mark.parametrize(
    ("page", "expected_status_code"),
    [("/", 200)],
)
def test_simple_routes(client, page, expected_status_code):
    assert client.get(page).status_code == expected_status_code


def test_create_incident(client, db_session):
    res = client.post(
        "/api/v1/incidents/create",
        json={"time_of_incident": "2021-03-14 01:05:09"}
    )
    incident_id = res.json["id"]

    incident_obj = db_session \
        .query(Incident) \
        .filter(Incident.id == incident_id) \
        .first()

    assert incident_obj.time_of_incident == datetime(2021, 3, 14, 1, 5, 9)


def test_get_incident(app, client, db_session):
    # Create an incident in the database
    incident_date = datetime(1969, 7, 16, 13, 32, 0)
    incident_date_str = app.json_encoder().encode(incident_date)[1:-1]

    obj = Incident(time_of_incident=incident_date)
    db_session.add(obj)
    db_session.commit()

    # Test that we can get it
    res = client.get(f"/api/v1/incidents/get/{obj.id}")
    assert res.json["time_of_incident"] == incident_date_str
