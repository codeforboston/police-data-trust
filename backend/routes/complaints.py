import logging
from typing import Optional, List

from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.schemas import validate_request, ordered_jsonify, paginate_results
from backend.database.models.user import UserRole, User
from backend.database.models.complaint import Complaint
from backend.database.models.source import Source
from backend.database.models.attachment import Attachment
from backend.database.models.civilian import Civilian
from backend.database.models.officer import Officer
from .tmp.pydantic.complaints import (
    CreateComplaint, UpdateComplaint, CreateComplaintSource, 
    CreateAllegation, CreateInvestigation, CreatePenalty, 
    CreateLocation, CreateCivilian)
from flask import Blueprint, abort, request
from flask_jwt_extended import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from pydantic import BaseModel
from neomodel import db


bp = Blueprint("complaint_routes", __name__, url_prefix="/api/v1/complaints")

def create_allegation(complaint, allegation_data):
    try:
        allegation = CreateAllegation(**allegation_data)
        complaint.allegations.connect(allegation.to_allegation())
    except Exception as e:
        abort(400, description=str(e))


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

    complaint_data = body.model_dump(exclude_unset=True)

    # Extract child objects from the body
    source_details = complaint_data.pop("source_details", {})
    location = complaint_data.pop("location", None)
    attachments = complaint_data.pop("attachments", [])
    allegations = complaint_data.pop("allegations", [])
    investigations = complaint_data.pop("investigations", [])
    penalties = complaint_data.pop("penalties", [])
    civilian_witnesses = complaint_data.pop("civilian_witnesses", [])
    police_witnesses = complaint_data.pop("police_witnesses", [])
    source_uid = complaint_data.pop("source_uid", None)

    source = Source.nodes.get_or_none(uid=source_uid)
    if source is None:
        abort(404, description="Invalid Complaint: Source not found")
    # Verify that the user is a member of the source
    # Need to also verify that the user is a Publisher or Higher
    if not source.is_member(current_user):
        abort(
            403,
            description="User does not have permission to "
            "create a complaint for this source.")
  
    try:
        complaint = Complaint.from_dict(complaint_data)
        complaint.source_org.connect(source, source_details)
    except Exception as e:
        logger.error(f"Error creating complaint: {e}")
        abort(400, description=str(e))

    # Add locations
    if location:
        try:
            loc = CreateLocation(**location)
            complaint.location.connect(loc.to_location())
        except Exception as e:
            logger.error(f"Error linking location: {e}")
            abort(400, description=str(e))
    # Add attachments
    if attachments:
        for attachment in attachments:
            try:
                a = Attachment.from_dict(attachment.model_dump())
                complaint.attachments.connect(attachment.to_attachment())
            except Exception as e:
                logger.error(f"Error linking attachment: {e}")
                abort(400, description=str(e))

    # Add allegations
    if allegations:
        for allegation in allegations:
            try:
                a = CreateAllegation(**allegation)
                complaint.allegations.connect(a.to_allegation())
            except Exception as e:
                logger.error(f"Error linking allegation: {e}")
                abort(400, description=str(e))

    # Add investigations
    if investigations:
        for investigation in investigations:
            try:
                i = CreateInvestigation(**investigation)
                complaint.investigations.connect(i.to_investigation())
            except Exception as e:
                logger.error(f"Error linking investigation: {e}")
                abort(400, description=str(e))

    # Add penalties
    if penalties:
        for penalty in penalties:
            try:
                p = CreatePenalty(**penalty)
                complaint.penalties.connect(p.to_penalty())
            except Exception as e:
                logger.error(f"Error linking penalty: {e}")
                abort(400, description=str(e))

    # Add civilian witnesses
    if civilian_witnesses:
        for civilian in civilian_witnesses:
            try:
                c = CreateCivilian(**civilian)
                civilian_instance = c.to_civilian()
                complaint.civilian_witnesses.connect(civilian_instance)
            except Exception as e:
                logger.error(f"Error linking civilian witness: {e}")
                abort(400, description=str(e))
    
    # Add police witnesses
    if police_witnesses:
        for officer in police_witnesses:
            try:
                o = Officer.nodes.get_or_none(uid=officer)
                if o is None:
                    abort(404, description=f"Officer {officer} not found")
                complaint.police_witnesses.connect(o)
            except Exception as e:
                logger.error(f"Error linking police witness: {e}")
                abort(400, description=str(e))



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
    # logger = logging.getLogger("get_all_complaints")
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
