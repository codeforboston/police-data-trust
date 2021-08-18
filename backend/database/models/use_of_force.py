from .. import db


class UseOfForce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    item = db.Column(db.Text())
