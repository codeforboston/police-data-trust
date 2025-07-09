import logging
from typing import Optional, List

from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.schemas import validate_request, ordered_jsonify, paginate_results
from backend.database.models.user import UserRole, User
from backend.database.models.complaint import Complaint, Penalty
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
    officer_uid = allegation_data.pop("accused_uid", None)
    complainant_data = allegation_data.pop("complainant", None)

    # Create Officer for Allegation
    if officer_uid:
        officer = Officer.nodes.get_or_none(uid=officer_uid)
        if officer is None:
            # Raise an error if the officer is not found
            raise ValueError(f"Officer with UID {officer_uid} not found")
    else:
        # If no officer UID is provided, we assume the allegation is not linked to an officer
        raise ValueError("Officer UID is required for the allegation") 

    try:
        allegation = CreateAllegation(**allegation_data)
        allegation.accused.connect(officer)
        allegation.complaint.connect(complaint)
        complaint.allegations.connect(allegation)
        allegation.save()
        logging.info(f"Allegation {allegation.uid} created for Complaint {complaint.uid}")
    except Exception as e:
        logging.error(f"Error creating allegation: {e}")
        if allegation:
            # If the allegation was created but failed to connect, delete it
            logging.error(f"Deleting allegation {allegation.uid} due to error")
            allegation.delete()

    # Connect complainant to allegation
    if complainant_data:
        try:
            complainant = CreateCivilian(**complainant_data)
            allegation.complainant.connect(complainant)
        except Exception as e:
            logging.error(f"Error connecting complainant to allegation: {e}")
            if complainant:
                # If the complainant was created but failed to connect, delete it
                logging.error(f"Deleting complainant {complainant.uid} due to error")
                complainant.delete()


def create_penalty(complaint, penalty_data):
    officer_uid = penalty_data.pop("officer_uid", None)
    if officer_uid:
        officer = Officer.nodes.get_or_none(uid=officer_uid)
        if officer is None:
            # Raise an error if the officer is not found
            raise ValueError(f"Officer with UID {officer_uid} not found")
    else:
        # If no officer UID is provided, we assume the penalty is not linked to an officer
        raise ValueError("Officer UID is required for the penalty")
    try:
        penalty = Penalty(**penalty_data)
        complaint.penalties.connect(penalty)
        penalty.officer.connect(officer)
        penalty.complaint.connect(complaint)
        penalty.save()
        logging.info(f"Penalty {penalty.uid} created for Complaint {complaint.uid}")
    except Exception as e:
        logging.error(f"Error creating penalty: {e}")
        if penalty:
            # If the penalty was created but failed to connect, delete it
            logging.error(f"Deleting penalty {penalty.uid} due to error")
            penalty.delete()


def create_investigation(complaint, investigation_data):
    investigator_uid = investigation_data.pop("investigator_uid", None)
    try:
        investigation = CreateInvestigation(**investigation_data)
        complaint.investigations.connect(investigation)
        investigation.complaint.connect(complaint)
        investigation.save()
        logging.info(f"Investigation {investigation.uid} created for Complaint {complaint.uid}")
    except Exception as e:
        logging.error(f"Error creating investigation: {e}")
        if investigation:
            # If the investigation was created but failed to connect, delete it
            logging.error(f"Deleting investigation {investigation.uid} due to error")
            investigation.delete()
        return
    if investigator_uid:
        investigator = Officer.nodes.get_or_none(uid=investigator_uid)
        if investigator:
            investigation.investigator.connect(investigator)


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
                create_allegation(complaint, allegation)
            except ValueError as ve:
                logger.error(f"Error creating allegation: {ve}")

    # Add Penalties
    if penalties:
        for penalty in penalties:
            try:
                create_penalty(complaint, penalty)
            except ValueError as ve:
                logger.error(f"Error creating penalty: {ve}")

    # Add Investigations
    if investigations:
        for investigation in investigations:
            try:
                create_investigation(complaint, investigation)
            except ValueError as ve:
                logger.error(f"Error creating investigation: {ve}")

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
