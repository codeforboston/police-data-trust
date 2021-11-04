from flask import Blueprint
from flask import jsonify
from flask import request
from ..auth import role_required
from ..database import User, PassportRequest, RequestStatus, UserRole
from ..schemas import UserSchema, validate, sqlalchemy_to_pydantic
from pydantic import BaseModel


bp = Blueprint("passport", __name__, url_prefix="/api/v1/passportRequests")

class PassportRequestDTO(BaseModel):
  user_id: int
  role: UserRole  

class StatusUpdateDTO(BaseModel):
  status: RequestStatus

@bp.route("/", methods=["POST"])
@validate(json=PassportRequestDTO)
def request_upgrade():
  body: PassportRequestDTO = request.context.json;
  # NOTE: Do we want users to be able to send requests for multiple different roles?
  request_exists = PassportRequest.query.join(User, User.id==body.user_id).count()
  print(request_exists)
  if (request_exists):
    return {
      "message": "Error. Request already exists",
    }, 400
  passportRequest = PassportRequest(
    user = User.get(body.user_id),
    status = RequestStatus.PENDING,
    request_role = body.role
  )
  passportRequest = passportRequest.create();
  PassportRequestSchema = sqlalchemy_to_pydantic(PassportRequest)
  response = PassportRequestSchema(
    user = User.get(body.user_id),
    status = RequestStatus.PENDING,
    request_role = body.role,
    id = passportRequest.id,
    user_id = passportRequest.user_id
  )
  return {
    "request": response,
  }, 200

@bp.route("/", methods=["GET"])
@role_required(UserRole.ADMIN)
@validate()
def list_requests():
  return PassportRequest.query.filterBy(status=request.args["status"], role=request.args["role"]);

@bp.route("/:requestId/status", methods=["PUT"])
@role_required(UserRole.ADMIN)
@validate(json=StatusUpdateDTO)
def update_status(requestId: int):
  statusUpdate: StatusUpdateDTO = request.context.json;
  passportRequest = PassportRequest.get(requestId);
  if (statusUpdate == RequestStatus.APPROVED):
    user = passportRequest.user;
    user.role = passportRequest.request_role;
  passportRequest.status = statusUpdate;
  db.session.commit();
  return passportRequest;
  
  

@bp.route("/<requestId>")
@role_required(UserRole.ADMIN)
def get_single_request(requestId: int):
  return PassportRequest.query.filterBy(id=requestId);