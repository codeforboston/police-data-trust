from .. import db


class Accusation(db.Model):
    """Models CPDP `complaints-accused` table"""

    id = db.Column(db.Integer, primary_key=True)
    suspect_id = db.Column(db.Integer, db.ForeignKey("suspect.id"))
    officer_id = db.Column(db.Integer, db.ForeignKey("officer.id"))
    category = db.Column(db.Text)
    category_code = db.Column(db.Text)
    finding = db.Column(db.Text)
    outcome = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint("suspect_id", "officer_id", name="accusation_uc"),
    )
