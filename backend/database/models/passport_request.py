import enum

from ..core import db
from ..core import CrudMixin
from .types.enums import UserRole

class RequestStatus(enum.Enum):
  APPROVED = 1
  DECLINED = 2
  PENDING = 3

class PassportRequest(db.Model, CrudMixin):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  user = db.relationship("User", uselist=False, foreign_keys=[user_id])
  request_role = db.Enum(UserRole)
  status = db.Enum(RequestStatus)
  admin = db.relationship("User")
 