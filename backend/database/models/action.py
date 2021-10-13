from .. import db


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # action id
    incident_id = db.Column(
        db.Integer, db.ForeignKey("incident.id"), nullable=False
    )
    date = db.Column(db.DateTime)
    action = db.Column(db.Text)  # TODO: Not sure what this is.
    actor = db.Column(db.Text)  # TODO: Not sure what this is.
    notes = db.Column(db.Text)
