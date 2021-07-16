from .. import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(
        db.Integer, db.ForeignKey("incident.id"), nullable=False
    )
    term = db.Column(db.Text)
