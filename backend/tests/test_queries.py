from backend.database.queries.queries import officer_exists, incident_exists
from backend.database import Officer, StateID, Incident
from typing import Any


def test_officer_exists(db_session: Any):
    # Create a test officer with a state ID value
    state_id_value = "ABC123"
    officer = Officer(**{"first_name": "Test Officer"})
    state_id = StateID(**{"value": state_id_value, "state": "NY"})
    officer.stateId = state_id  # type: ignore
    db_session.add(officer)
    db_session.commit()

    # test manually that the officer exists
    assert (
        db_session.query(Officer)
        .join(StateID)
        .filter(
            StateID.value == state_id.value and StateID.state == state_id.state
        )
        .first()
        is not None
    )

    # Test that the officer exists
    assert officer_exists(db_session, state_id)

    # Test that a non-existing officer returns False
    assert not officer_exists(
        db_session, StateID(**{"value": "DEF456", "state": "NY"})
    )


def test_incident_exists(db_session: Any):
    # Create a test incident with a case ID value
    case_id_value = "123456"
    incident = Incident(**{"case_id": case_id_value})
    db_session.add(incident)
    db_session.commit()

    # test manually that the incident exists
    assert (
        db_session.query(Incident)
        .filter(Incident.case_id == case_id_value)
        .first()
        is not None
    )

    # Test that the incident exists
    assert incident_exists(db_session, case_id_value)

    # Test that a non-existing incident returns False
    assert not incident_exists(db_session, "654321")
