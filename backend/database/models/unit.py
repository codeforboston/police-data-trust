from ..core import CrudMixin, db
from sqlalchemy.ext.associationproxy import association_proxy


class Unit(db.Model, CrudMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    website_url = db.Column(db.Text)
    phone = db.Column(db.Text)
    email = db.Column(db.Text)
    description = db.Column(db.Text)
    address = db.Column(db.Text)
    zip = db.Column(db.Text)
    agency_url = db.Column(db.Text)
    officers_url = db.Column(db.Text)

    commander_id = db.Column(db.Integer, db.ForeignKey('officer.id'))
    agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'))

    agency = db.relationship("Agency", back_populates="units")
    officer_association = db.relationship('Employment', back_populates='unit')
    officers = association_proxy('officer_association', 'officer')

    def __repr__(self):
        return f"<Unit {self.name}>"
