from .. import db


class ResultOfStop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    result = db.Column(db.Text)
