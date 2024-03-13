from .. import db


class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    accusation_id = db.Column(db.Integer, db.ForeignKey("accusation.id"))
    title = db.Column(db.Text)
    hash = db.Column(db.Text)
    url = db.Column(db.Text)
    filetype = db.Column(db.Text)
