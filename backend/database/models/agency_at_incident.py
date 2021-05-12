from backend.database import db


class AgencyAtIncident(db.model):
    id = db.Column(db.Integer, primary_key=True)
