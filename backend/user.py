"""Define the SQL classes for Users."""
from flask_sqlalchemy import SQLAlchemy
from flask_serialize.flask_serialize import FlaskSerialize
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum

db = SQLAlchemy()
fs_mixin = FlaskSerialize(db)


class User(db.Model, UserMixin):
    """The SQL dataclass for an Incident."""

    __tablename__ = "users"

    user_ID = db.Column(db.BigInt, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    privilege_ID = db.Column(db.Integer, nullable=False)
    is_approved = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)