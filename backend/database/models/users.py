"""Define the SQL classes for Users."""

import bcrypt
from backend.database.core import db
from flask_login import LoginManager
from flask_serialize.flask_serialize import FlaskSerialize
from flask_user import SQLAlchemyAdapter
from flask_user import UserManager
from flask_user import UserMixin
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import String, TypeDecorator


fs_mixin = FlaskSerialize(db)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"


# Creating this class as NOCASE collation is not compatible with ordinary
# SQLAlchemy Strings
class CI_String(TypeDecorator):
    """ Case-insensitive String subclass definition"""

    impl = String

    def __init__(self, length, **kwargs):
        if kwargs.get("collate"):
            if kwargs["collate"].upper() not in ["BINARY", "NOCASE", "RTRIM"]:
                raise TypeError(
                    "%s is not a valid SQLite collation" % kwargs["collate"]
                )
            self.collation = kwargs.pop("collate").upper()
        super(CI_String, self).__init__(length=length, **kwargs)


@compiles(CI_String, "sqlite")
def compile_ci_string(element, compiler, **kwargs):
    base_visit = compiler.visit_string(element, **kwargs)
    if element.collation:
        return "%s COLLATE %s" % (base_visit, element.collation)
    else:
        return base_visit


# Define the User data-model.
class Users(db.Model, UserMixin):
    """The SQL dataclass for an Incident."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(
        "is_active", db.Boolean(), nullable=False, server_default="1"
    )

    # User authentication information. The collation="NOCASE" is required
    # to search case insensitively when USER_IFIND_MODE is "nocase_collation".
    email = db.Column(
        CI_String(255, collate="NOCASE"), nullable=False, unique=True
    )
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default="")

    # User information
    first_name = db.Column(
        CI_String(100, collate="NOCASE"), nullable=False, server_default=""
    )
    last_name = db.Column(
        CI_String(100, collate="NOCASE"), nullable=False, server_default=""
    )

    # Define the relationship to Role via UserRoles
    roles = db.relationship("Role", secondary="user_roles")

    def verify_password(self, pw):
        return bcrypt.checkpw(pw.encode("utf8"), self.password.encode("utf8"))


db_adapter = SQLAlchemyAdapter(db, Users)
user_manager = UserManager(db_adapter)


# Define the Role data-model
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(
        db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE")
    )
    role_id = db.Column(
        db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE")
    )
