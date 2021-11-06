from flask import Blueprint
from flask import jsonify
from flask import request
from ..auth import role_required
from ..database import User, UserRole, db
from ..schemas import validate
from pydantic import BaseModel

bp = Blueprint("user", __name__, url_prefix="/api/v1/users")

class RoleUpdateDTO(BaseModel):
  role: UserRole

@bp.route("/<userId>/role", methods=["PUT"])
@role_required(UserRole.ADMIN)
@validate(json=RoleUpdateDTO)
def update_role(userId: int):
  updatedRole: RoleUpdateDTO = request.context.json;
  user = User.get(userId);
  user.role = updatedRole.role;
  db.session.commit()
  return user;