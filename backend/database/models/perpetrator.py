from backend.database.models.officer import State
from backend.database.models.employment import Rank
from .. import db
from sqlalchemy.ext.associationproxy import association_proxy


class Perpetrator(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    race = db.Column(db.Text)
    ethnicity = db.Column(db.Text)
    gender = db.Column(db.Text)
    badge = db.Column(db.Text)
    unit = db.Column(db.Text)  # type?
    # Note: rank at time of incident
    rank = db.Column(db.Enum(Rank))
    state_id_val = db.Column(db.Text)
    state_id_state = db.Column(db.Enum(State))
    state_id_name = db.Column(db.Text)
    role = db.Column(db.Text)
    officer_association = db.relationship(
        "Accusation", back_populates="perpetrator"
    )
    suspects = association_proxy("officer_association", "officer")

    def __repr__(self):
        return f"<Perpetrator {self.id}>"
