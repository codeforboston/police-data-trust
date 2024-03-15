from .. import db


class Attorney(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_contents = db.Column(db.String)
