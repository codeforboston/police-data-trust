from ..core import db, CrudMixin


class Source(db.Model, CrudMixin):
    id = db.Column(db.Text, primary_key=True)
    publication_name = db.Column(db.Text)
    publication_date = db.Column(db.Date)
    author = db.Column(db.Text)
    URL = db.Column(db.Text)
