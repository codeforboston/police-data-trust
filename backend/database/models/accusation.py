from .. import db


class Accusation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    perpetrator_id = db.Column(db.Integer, db.ForeignKey("perpetrator.id"))
    officer_id = db.Column(db.Integer, db.ForeignKey("officer.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date_created = db.Column(db.Text)
    basis = db.Column(db.Text)

    attachments = db.relationship("Attachment", backref="accusation")
    perpetrator = db.relationship("Perpetrator", back_populates="suspects")
    officer = db.relationship("Officer", back_populates="accusations")

    def __repr__(self):
        return f"<Employment {self.id}>"
