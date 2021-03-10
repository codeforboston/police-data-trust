"""Define the SQL classes for Users."""
from flask_sqlalchemy import SQLAlchemy
from flask_serialize.flask_serialize import FlaskSerialize

db = SQLAlchemy()
fs_mixin = FlaskSerialize(db)


class Incidents(db.Model, fs_mixin):
    """The SQL dataclass for an Incident."""

    __tablename__ = "incident"

    incident_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    occurence_date = db.Column(db.DateTime)  # noqa: N815
    state_abbv = db.Column(db.Unicode(2))
    city = db.Column(db.Unicode(100))
    address_1 = db.Column(db.Unicode(100))
    address_2 = db.Column(db.Unicode(100))
    zip_code = db.Column(db.Unicode(10))
    stop_type = db.Column(db.Integer)
    call_type = db.Column(db.Integer)
    has_multimedia = db.Column(db.Boolean)
    from_report = db.Column(db.Boolean)
    race = db.Column(db.Boolean)
    neighborhood = db.Column(db.Unicode(50))

    convert_types = [{'type': bool, 'method': lambda v: True if v else False}]

    # role = db.relationship(
    #     "RoleTable",
    #      backref=db.backref("incidents", lazy=True)
    # )
