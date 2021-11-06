import enum

from ..core import db
from ..core import CrudMixin
from .types.enums import UserRole


class RequestStatus(str, enum.Enum):
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    PENDING = "PENDING"


class PassportRequest(db.Model, CrudMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    user = db.relationship("User", uselist=False, foreign_keys=[user_id])
    request_role = db.Column(db.Enum(UserRole), nullable=False)
    status = db.Column(db.Enum(RequestStatus), default=RequestStatus.PENDING)
    admin = db.relationship("User", uselist=False, foreign_keys=[admin_id])
