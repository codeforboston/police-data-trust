from ..core import db

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publication_name = db.column(db.text)
    publication_date = db.column(db.date)
    author = db.column(db.text)
    URL = db.column(db.text)
    incidents = db.relationship("incident", backref = "source")
    