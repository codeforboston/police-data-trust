from backend.database import db


class Multimedia(db.model):
    id = db.Column(db.Integer, primary_key=True)
