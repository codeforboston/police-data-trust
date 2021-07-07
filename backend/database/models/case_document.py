from .. import db


class CaseDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    legal_case_id = db.Column(db.Integer, db.ForeignKey('legal_case.id'))
    text_contents = db.Column(db.String)
