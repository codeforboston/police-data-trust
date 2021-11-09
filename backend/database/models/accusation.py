from .. import db


class Accusation(db.Model):
    """Models CPDP `complaints-accused` table"""

    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    officer_id = db.Column(db.Integer, db.ForeignKey("officer.id"))
    category = db.Column(db.Text)
    category_code = db.Column(db.Text)
    finding = db.Column(db.Text)
    outcome = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint("incident_id", "officer_id", name="accusation_uc"),
    )
