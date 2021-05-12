from backend.database import db


class ParticipantAtIncident(db.model):
    id = db.Column(db.Integer, primary_key=True)
