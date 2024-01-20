from .. import Officer, StateID, Incident
from sqlalchemy.orm import Session
from typing import Optional


def officer_exists(db: Session, stateID: StateID) -> Optional[Officer]:
    return (
        db.query(Officer)
        .join(StateID)
        .filter(
            StateID.value == stateID.value and StateID.state == stateID.state
        )
        .first()
    )


def incident_exists(db: Session, incident: Incident) -> Optional[Incident]:
    return (
        db.query(Incident).filter(Incident.case_id == incident.case_id).first()
    )
