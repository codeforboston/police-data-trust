from flask import Blueprint
from flask import jsonify
from flask import request
from ..auth import role_required
from ..database import User, PassportRequest, RequestStatus, UserRole
from ..dto import RoleUpdateDTO

bp = Blueprint("passport", __name__, url_prefix="/api/v1/passportRequests")

@bp.route("/", methods=["POST"])
@validate
def request_upgrade(body: PassportRequestDTO):
  # NOTE: Do we want users to be able to send requests for multiple different roles?
  request_exists = PassportRequest.query.exists(PassportRequest.user.id.has(body.id))
  if (request_exists):
    return {
      "message": "Error. Request already exists",
    }, 400
  passportRequest = PassportRequest(
    user = User.get(body.user_id),
    status = RequestStatus.PENDING,
    role = body.role
  )
  return {
    "request": request,
  }, 200

@bp.route("/", methods=["GET"])
@role_required(UserRole.ADMIN)
def list_requests():
  return PassportRequest.query.filterBy(status=request.args["status"], role=request.args["role"]);

@bp.route("/:requestId/status", methods=["PUT"])
@role_required(UserRole.ADMIN)
def update_status(body: RoleUpdateDTO):
  

@bp.route("/")