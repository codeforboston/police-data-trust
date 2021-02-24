"""Define the SQL classes for Users."""

from api import db
from flask_sqlalchemy import SQLAlchemy

class Incidents(SQLAlchemy.Model):
		"""The SQL dataclass for an Incident."""

		__tablename__ = "incidents"

		Incident_ID = db.Column(db.Unicode(512), primary_key=True)
		Occurence_Date = db.Column(db.DateTime)  # noqa: N815
		State_Abbv = db.Column(db.Unicode(512))
		City = db.Column(db.Unicode(512))
		Address_1 = db.Column(db.Unicode(512))
		Address_2 = db.Column(db.Unicode(512))
		Zip_Code = db.Column(db.Unicode(512))
		Stop_Type = db.Column(db.Unicode(512))
		Call_Type = db.Column(db.Unicode(512))
		Has_Multimedia = db.Column(db.Boolean)
		From_Report = db.Column(db.Boolean)
		Race = db.Column(db.Boolean)
		Neighborhood = db.Column(db.Unicode(512))

		role = db.relationship("RoleTable", backref=db.backref("incidents", lazy=True))