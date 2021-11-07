from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended.utils import get_jwt_identity
from ..auth import role_required
from ..database import User, PassportRequest, RequestStatus, UserRole, db
from ..schemas import UserSchema, validate, PassportRequestSchema
from sqlalchemy.inspection import inspect
from pydantic import BaseModel
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("passport", __name__, url_prefix="/api/v1/passportRequests")


class PassportRequestDTO(BaseModel):
    user_id: int
    role: UserRole


class StatusUpdateDTO(BaseModel):
    status: RequestStatus


# NOTE: Should users only be able to make requests for themselves? If so, then we can get the user_id
# ... from the token
@bp.route("", methods=["POST"])
@validate(json=PassportRequestDTO)
def request_upgrade():
    body: PassportRequestDTO = request.context.json
    # NOTE: Do we want users to be able to send requests for multiple different roles?
    query = db.session.query(PassportRequest).filter(
        PassportRequest.user_id == body.user_id
    )
    request_exists = db.session.query(query.exists()).scalar()
    if request_exists:
        return {
            "message": "Error. Request already exists",
        }, 400
    passportRequest = PassportRequest(
        user=User.get(body.user_id),
        status=RequestStatus.PENDING,
        role=body.role,
    )
    passportRequest = passportRequest.create()
    response = PassportRequestSchema.from_orm(passportRequest).dict()
    return response, 200


@bp.route("", methods=["GET"])
@role_required(UserRole.ADMIN)
def list_requests():
    query = db.session.query(PassportRequest)
    mapper = inspect(PassportRequest)
    for key in request.args.keys():
        if key in mapper.attrs:
            query = query.filter(
                getattr(PassportRequest, key) == request.args[key]
            )
    passportRequests = query.all()
    passports = [
        PassportRequestSchema.from_orm(x).dict() for x in passportRequests
    ]
    print(passports)
    return {"passports": passports}, 200


@bp.route("/<requestId>/status", methods=["PUT"])
@role_required(UserRole.ADMIN)
@jwt_required()
@validate(json=StatusUpdateDTO)
def update_status(requestId: int):
    statusUpdate: StatusUpdateDTO = request.context.json
    passportRequest = PassportRequest.get(requestId)
    if statusUpdate.status == RequestStatus.APPROVED:
        user = passportRequest.user
        user.role = passportRequest.role
    passportRequest.status = statusUpdate.status
    passportRequest.admin_id = get_jwt_identity()
    db.session.commit()
    return PassportRequestSchema.from_orm(passportRequest).dict()


@bp.route("/<requestId>", methods=["GET"])
@role_required(UserRole.ADMIN)
def get_single_request(requestId: int):
    return PassportRequestSchema.from_orm(PassportRequest.get(requestId)).dict()
