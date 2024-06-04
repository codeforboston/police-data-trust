from ..core import db
from sqlalchemy.ext.associationproxy import association_proxy


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'))
    agency = db.relationship("Agency", back_populates="units")

    officer_association = db.relationship('Employment', back_populates='unit')
    officers = association_proxy('officer_association', 'officer')

    def __repr__(self):
        return f"<Unit {self.name}>"
