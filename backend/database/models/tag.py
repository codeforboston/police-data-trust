from .. import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.Text)
