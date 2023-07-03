from ..core import db, CrudMixin


class Source(db.Model, CrudMixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    contact_email = db.Column(db.Text)
    reported_incidents = db.relationship(
        'Incident', backref='source', lazy="select")
