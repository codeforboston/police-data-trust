from .. import Officer, StateID, Incident
from sqlalchemy.orm import Session


def officer_exists(db: Session, stateID: StateID) -> bool:
    return (
        db.query(Officer)
        .join(StateID)
        .filter(
            StateID.value == stateID.value and StateID.state == stateID.state
        )
        .first()
        is not None
    )


def incident_exists(db: Session, incident: Incident) -> bool:
    return (
        db.query(Incident).filter(Incident.case_id == incident.case_id).first()
        is not None
    )
