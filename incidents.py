"""Define the SQL classes for Users."""

from flask_sqlalchemy import SQLAlchemy
from flask_serialize.flask_serialize import FlaskSerialize

db = SQLAlchemy()
fs_mixin = FlaskSerialize(db)

class Incidents(db.Model, fs_mixin):
		"""The SQL dataclass for an Incident."""

		__tablename__ = "incident"

		incident_id = db.Column(db.Unicode(512), primary_key=True)
		occurence_date = db.Column(db.DateTime)  # noqa: N815
		state_abbv = db.Column(db.Unicode(512))
		city = db.Column(db.Unicode(512))
		address_1 = db.Column(db.Unicode(512))
		address_2 = db.Column(db.Unicode(512))
		zip_code = db.Column(db.Unicode(512))
		stop_type = db.Column(db.Unicode(512))
		call_type = db.Column(db.Unicode(512))
		has_multimedia = db.Column(db.Boolean)
		from_report = db.Column(db.Boolean)
		race = db.Column(db.Boolean)
		neighborhood = db.Column(db.Unicode(512))

		# role = db.relationship("RoleTable", backref=db.backref("incidents", lazy=True))
		