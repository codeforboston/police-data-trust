from backend.database import db


class OfficerAtIncident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Relationships, fields?
