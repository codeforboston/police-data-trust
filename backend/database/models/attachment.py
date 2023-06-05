from .. import db


class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    title = db.Column(db.Text)
    hash = db.Column(db.Text)
    location = db.Column(db.Text)
    filetype = db.Column(db.Text)
