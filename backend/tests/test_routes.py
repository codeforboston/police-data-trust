from datetime import datetime

import pytest

from backend.database import Incident


@pytest.mark.parametrize(
    ("page", "expected_status_code"),
    [("/", 200)],
)
def test_simple_routes(client, page, expected_status_code):
    assert client.get(page).status_code == expected_status_code


def test_create_incident(client, db_session, access_token):
    expected = {
        "time_of_incident": "2021-03-14 01:05:09",
        "stop_type": "Domestic disturbance",
        "officers": [
            {"first_name": "Susie", "last_name": "Suserson"},
            {"first_name": "Lisa", "last_name": "Wong"},
        ],
        "use_of_force": [{"item": "Injurious restraint"}],
        "source": "clkpdp",
    }
    res = client.post(
        "/api/v1/incidents/create",
        json=expected,
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )

    assert res.status_code == 200
    data = res.json

    incident_obj = (
        db_session.query(Incident).filter(Incident.id == data["id"]).first()
    )

    assert incident_obj.time_of_incident == datetime(2021, 3, 14, 1, 5, 9)
    for i in [0, 1]:
        assert incident_obj.officers[i].id == data["officers"][i]["id"]
    assert incident_obj.use_of_force[0].id == data["use_of_force"][0]["id"]
    assert incident_obj.source == expected["source"]


def test_get_incident(app, client, db_session, access_token):
    # Create an incident in the database
    incident_date = datetime(1969, 7, 16, 13, 32, 0)
    incident_date_str = app.json_encoder().encode(incident_date)[1:-1]

    obj = Incident(time_of_incident=incident_date)
    db_session.add(obj)
    db_session.commit()

    # Test that we can get it
    res = client.get(f"/api/v1/incidents/get/{obj.id}")
    assert res.json["time_of_incident"] == incident_date_str


def test_search_incidents(client, access_token):
    res = client.get(
        "/api/v1/incidents/search",
        json={
            "location": "boston",
            "start_time": "2021-03-14 01:05:09",
            "end_time": "2021-03-14 01:05:09",
            "incident_type": "traffic",
        },
    )

    assert res.status_code == 200
    assert res.json["location"] == "boston"


@pytest.fixture
def example_incidents(db_session):
    incident = Incident()
    db_session.add(incident)
    db_session.commit()
    return incident
