import logging
from typing import Optional, List

from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.schemas import validate_request, ordered_jsonify, paginate_results
from backend.database.models.user import UserRole, User
from backend.database.models.complaint import Complaint
from .tmp.pydantic.complaints import CreateComplaint, UpdateComplaint
from flask import Blueprint, abort, request
from flask_jwt_extended import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from pydantic import BaseModel
from neomodel import db


bp = Blueprint("complaint_routes", __name__, url_prefix="/api/v1/complaints")


# Create a complaint
@bp.route("/", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreateComplaint)
def create_complaint():
    """Create a complaint.
    """
    logger = logging.getLogger("create_complaint")
    body: CreateComplaint = request.validated_body
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])

    # try:
    complaint = Complaint.from_dict(body.model_dump())
    # except Exception as e:
    #     abort(400, description=str(e))

    logger.info(f"Complaint {complaint.uid} created by User {current_user.uid}")
    track_to_mp(
        request,
        "create_complaint",
        {
            "complaint_uid": complaint.uid
        },
    )
    return complaint.to_json()


# Get a complaint record
@bp.route("/<complaint_uid>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_complaint(complaint_uid: int):
    """Get a complaint record.
    """
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")
    return c.to_json()



# Get all complaints
@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_all_complaints():
    """Get all complaints.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    logger = logging.getLogger("get_all_complaints")
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    all_complaints = Complaint.nodes.all()
    results = paginate_results(all_complaints, q_page, q_per_page)
    if not results:
        abort(404, description="No complaints found")
    return ordered_jsonify(results), 200


# Update a complaint record
@bp.route("/<complaint_uid>", methods=["PUT"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(UpdateComplaint)
def update_complaint(complaint_uid: str):
    """Update a complaint record.
    """
    body: UpdateComplaint = request.validated_body
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    try:
        c = Complaint.from_dict(body.model_dump(), complaint_uid)
        c.refresh()
    except Exception as e:
        abort(400, description=str(e))

    track_to_mp(
        request,
        "update_complaint",
        {
            "complaint_uid": c.uid
        },
    )
    return c.to_json()


# Delete a complaint record
@bp.route("/<complaint_uid>", methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.ADMIN)
def delete_complaint(complaint_uid: str):
    """Delete a complaint record.
    Must be an admin to delete a complaint.
    """
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")
    try:
        uid = c.uid
        c.delete()
        track_to_mp(
            request,
            "delete_complaint",
            {
                "complaint_uid": uid
            },
        )
        return {"message": "Complaint deleted successfully"}
    except Exception as e:
        abort(400, description=str(e))
