from backend.database import db


class Attorney(db.model):
    id = db.Column(db.Integer, primary_key=True)
    text_contents = db.Column(db.String)
