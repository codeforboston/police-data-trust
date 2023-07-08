from .. import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.Text)

    def __repr__(self):
        return f"<Tag {self.id}: {self.term}>"
