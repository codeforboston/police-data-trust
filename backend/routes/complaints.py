import logging
from functools import wraps

from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.schemas import validate_request, ordered_jsonify, paginate_results
from backend.database.models.user import UserRole, User
from backend.database.models.complaint import (
    Complaint, Penalty, Allegation, Investigation)
from backend.database.models.source import Source
from backend.dto.complaint import (
    CreateComplaint, UpdateComplaint,
    CreateAllegation, CreateInvestigation, CreatePenalty)
from backend.services.complaint_service import ComplaintService
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask_jwt_extended.view_decorators import jwt_required


bp = Blueprint("complaint_routes", __name__, url_prefix="/api/v1/complaints")
complaint_service = ComplaintService()


def verify_edit_allowed_or_abort(c_uid: str):
    """
    Check if the current user is allowed to edit the complaint.
    Returns True if allowed, False otherwise.
    """
    verify_jwt_in_request()
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])
    c = Complaint.nodes.get_or_none(uid=c_uid)
    if c is None:
        abort(404, description="Complaint not found")
    source = c.source_org.single()
    if (
        not source
        or not source.members.is_connected(current_user)
        or not source.members.relationship(current_user).may_publish()
    ):
        abort(403, description="User does not have permission"
              " to edit this complaint.")
        return False
    return True


def edit_permission_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(complaint_uid: str, *args, **kwargs):
            if verify_edit_allowed_or_abort(complaint_uid):
                return fn(complaint_uid, *args, **kwargs)
        return decorator
    return wrapper


# Create a complaint
@bp.route("", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreateComplaint)
def create_complaint():
    """Create a complaint.
    """
    body: CreateComplaint = request.validated_body
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])

    try:
        response = complaint_service.create_complaint(
            payload=body.model_dump(exclude_unset=True),
            current_user=current_user,
        )
    except LookupError as e:
        abort(404, description=str(e))
    except PermissionError as e:
        abort(403, description=str(e))
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        logging.getLogger("create_complaint").error(
            f"Error creating complaint: {e}")
        abort(400, description=str(e))

    logging.getLogger("create_complaint").info(
        f"Complaint {response.get('uid')} created by User {current_user.uid}"
    )
    track_to_mp(
        request,
        "create_complaint",
        {
            "complaint_uid": response.get("uid")
        },
    )
    return ordered_jsonify(response), 201


# Get a complaint record
@bp.route("/<complaint_uid>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_complaint(complaint_uid: str):
    """Get a complaint record.
    """
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")
    return c.to_json()


# Get all complaints
@bp.route("", methods=["GET"])
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
@bp.route("/<complaint_uid>", methods=["PATCH"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(UpdateComplaint)
def update_complaint(complaint_uid: str):
    """Update a complaint record.
    """
    body: UpdateComplaint = request.validated_body
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])
    try:
        response = complaint_service.update_complaint(
            complaint_uid=complaint_uid,
            payload=body.model_dump(exclude_unset=True),
            current_user=current_user,
        )
    except LookupError as e:
        abort(404, description=str(e))
    except PermissionError as e:
        abort(403, description=str(e))
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        abort(400, description=str(e))

    track_to_mp(
        request,
        "update_complaint",
        {
            "complaint_uid": response.get("uid")
        },
    )
    return ordered_jsonify(response)


# Delete a complaint record
@bp.route("/<complaint_uid>", methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
def delete_complaint(complaint_uid: str):
    """Delete a complaint record.
    Must be an admin to delete a complaint.
    """
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])
    source = c.source_org.single()
    if not source.members.is_connected(current_user):
        abort(403, description="User does not have permission"
              " to delete this complaint.")
    if not source.members.relationship(current_user).is_administrator():
        abort(
            403,
            description="User does not have permission"
            " to delete this complaint.")

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
        return jsonify({"message": "Complaint deleted successfully"}), 204
    except Exception as e:
        abort(400, description=str(e))


"""
##############################################################
######----         Complaint Allegations            ----######
##############################################################
"""


# Get all allegations for a complaint
@bp.route("/<complaint_uid>/allegations", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_complaint_allegations(complaint_uid: str):
    """Get all allegations for a complaint.
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    allegations = c.allegations.all()
    results = paginate_results(allegations, q_page, q_per_page)
    if not results:
        abort(404, description="No allegations found for this complaint.")

    return ordered_jsonify(results), 200


# Create an allegation for a complaint
@bp.route("/<complaint_uid>/allegations", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreateAllegation)
@edit_permission_required()
def create_complaint_allegation(complaint_uid: str):
    """Create an allegation for a complaint.
    """
    body: CreateAllegation = request.validated_body
    try:
        allegation = complaint_service.create_allegation_record(
            complaint_uid=complaint_uid,
            allegation_input=body,
        )
    except LookupError as e:
        abort(404, description=str(e))
    except ValueError as ve:
        abort(400, description=str(ve))
    except AttributeError as ae:
        abort(400, description=str(ae))

    track_to_mp(
        request,
        "create_complaint_allegation",
        {
            "complaint_uid": complaint_uid,
            "allegation_uid": allegation.uid
        },
    )
    return allegation.to_json(), 201


# Get a specific allegation for a complaint
@bp.route("/<complaint_uid>/allegations/<allegation_uid>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_complaint_allegation(complaint_uid: str, allegation_uid: str):
    """Get a specific allegation for a complaint.
    """
    try:
        allegation = complaint_service.get_allegation_record(
            complaint_uid=complaint_uid,
            allegation_uid=allegation_uid,
        )
        return allegation.to_json(), 200
    except LookupError as e:
        abort(404, description=str(e))


# Update an allegation for a complaint
@bp.route("/<complaint_uid>/allegations/<allegation_uid>", methods=["PATCH"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreateAllegation)
@edit_permission_required()
def update_complaint_allegation(complaint_uid: str, allegation_uid: str):
    """Update an allegation for a complaint.
    """
    body: CreateAllegation = request.validated_body
    try:
        allegation = complaint_service.update_allegation_record(
            complaint_uid=complaint_uid,
            allegation_uid=allegation_uid,
            allegation_input=body,
        )
    except LookupError as e:
        abort(404, description=str(e))
    except Exception as e:
        abort(400, description=str(e))

    track_to_mp(
        request,
        "update_complaint_allegation",
        {
            "complaint_uid": complaint_uid,
            "allegation_uid": allegation.uid
        },
    )
    return allegation.to_json()


# Delete an allegation for a complaint
@bp.route("/<complaint_uid>/allegations/<allegation_uid>", methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@edit_permission_required()
def delete_complaint_allegation(complaint_uid: str, allegation_uid: str):
    """Delete an allegation for a complaint.
    Must be an admin to delete an allegation.
    """
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")
    allegation = Allegation.nodes.get_or_none(uid=allegation_uid)
    if allegation is None:
        abort(404, description="Allegation not found")

    try:
        uid = allegation.uid
        allegation.delete()
        track_to_mp(
            request,
            "delete_complaint_allegation",
            {
                "complaint_uid": c.uid,
                "allegation_uid": uid
            },
        )
        return {"message": "Allegation deleted successfully"}, 204
    except Exception as e:
        abort(400, description=str(e))


"""
##############################################################
######----         Complaint Investigations         ----######
##############################################################
"""


# Get all investigations for a complaint
@bp.route("/<complaint_uid>/investigations", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_complaint_investigations(complaint_uid: str):
    """Get all investigations for a complaint.
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    investigations = c.investigations.all()
    results = paginate_results(investigations, q_page, q_per_page)
    if not results:
        abort(404, description="No investigations found for this complaint.")

    return ordered_jsonify(results), 200


# Create an investigation for a complaint
@bp.route("/<complaint_uid>/investigations", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreateInvestigation)
@edit_permission_required()
def create_complaint_investigation(complaint_uid: str):
    """Create an investigation for a complaint.
    """
    body: CreateInvestigation = request.validated_body
    try:
        investigation = complaint_service.create_investigation_record(
            complaint_uid=complaint_uid,
            investigation_input=body,
        )
    except LookupError as e:
        abort(404, description=str(e))
    except ValueError as ve:
        abort(400, description=str(ve))
    except AttributeError as ae:
        abort(400, description=str(ae))

    track_to_mp(
        request,
        "create_complaint_investigation",
        {
            "complaint_uid": complaint_uid,
            "investigation_uid": investigation.uid
        },
    )
    return investigation.to_json(), 201


# Get a specific investigation for a complaint
@bp.route("/<complaint_uid>/investigations/<investigation_uid>",
          methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_complaint_investigation(complaint_uid: str, investigation_uid: str):
    """Get a specific investigation for a complaint.
    """
    try:
        investigation = complaint_service.get_investigation_record(
            complaint_uid=complaint_uid,
            investigation_uid=investigation_uid,
        )
        return investigation.to_json(), 200
    except LookupError as e:
        abort(404, description=str(e))


# Update an investigation for a complaint
@bp.route("/<complaint_uid>/investigations/<investigation_uid>",
          methods=["PATCH"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreateInvestigation)
@edit_permission_required()
def update_complaint_investigation(complaint_uid: str, investigation_uid: str):
    """Update an investigation for a complaint.
    """
    body: CreateInvestigation = request.validated_body
    try:
        investigation = complaint_service.update_investigation_record(
            complaint_uid=complaint_uid,
            investigation_uid=investigation_uid,
            investigation_input=body,
        )
    except LookupError as e:
        abort(404, description=str(e))
    except Exception as e:
        abort(400, description=str(e))

    track_to_mp(
        request,
        "update_complaint_investigation",
        {
            "complaint_uid": complaint_uid,
            "investigation_uid": investigation.uid
        },
    )
    return investigation.to_json()


# Delete an investigation for a complaint
@bp.route("/<complaint_uid>/investigations/<investigation_uid>",
          methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@edit_permission_required()
def delete_complaint_investigation(complaint_uid: str, investigation_uid: str):
    """Delete an investigation for a complaint.
    Must be an admin to delete an investigation.
    """
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    investigation = Investigation.nodes.get_or_none(uid=investigation_uid)
    if investigation is None:
        abort(404, description="Investigation not found")

    try:
        uid = investigation.uid
        investigation.delete()
        track_to_mp(
            request,
            "delete_complaint_investigation",
            {
                "complaint_uid": c.uid,
                "investigation_uid": uid
            },
        )
        return {"message": "Investigation deleted successfully"}, 204
    except Exception as e:
        abort(400, description=str(e))


"""
##############################################################
######----         Complaint Penalties              ----######
##############################################################
"""


# Get all penalties for a complaint
@bp.route("/<complaint_uid>/penalties", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_complaint_penalties(complaint_uid: str):
    """Get all penalties for a complaint.
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    penalties = c.penalties.all()
    results = paginate_results(penalties, q_page, q_per_page)
    if not results:
        abort(404, description="No penalties found for this complaint.")

    return ordered_jsonify(results), 200


# Create a penalty for a complaint
@bp.route("/<complaint_uid>/penalties", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreatePenalty)
@edit_permission_required()
def create_complaint_penalty(complaint_uid: str):
    """Create a penalty for a complaint.
    """
    body: CreatePenalty = request.validated_body
    try:
        penalty = complaint_service.create_penalty_record(
            complaint_uid=complaint_uid,
            penalty_input=body,
        )
    except LookupError as e:
        abort(404, description=str(e))
    except ValueError as ve:
        abort(400, description=str(ve))
    except AttributeError as ae:
        abort(400, description=str(ae))

    track_to_mp(
        request,
        "create_complaint_penalty",
        {
            "complaint_uid": complaint_uid,
            "penalty_uid": penalty.uid
        },
    )
    return penalty.to_json(), 201


# Get a specific penalty for a complaint
@bp.route("/<complaint_uid>/penalties/<penalty_uid>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_complaint_penalty(complaint_uid: str, penalty_uid: str):
    """Get a specific penalty for a complaint.
    """
    try:
        penalty = complaint_service.get_penalty_record(
            complaint_uid=complaint_uid,
            penalty_uid=penalty_uid,
        )
        return penalty.to_json(), 200
    except LookupError as e:
        abort(404, description=str(e))


# Update a penalty for a complaint
@bp.route("/<complaint_uid>/penalties/<penalty_uid>", methods=["PATCH"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreatePenalty)
@edit_permission_required()
def update_complaint_penalty(complaint_uid: str, penalty_uid: str):
    """Update a penalty for a complaint.
    """
    body: CreatePenalty = request.validated_body
    try:
        penalty = complaint_service.update_penalty_record(
            complaint_uid=complaint_uid,
            penalty_uid=penalty_uid,
            penalty_input=body,
        )
    except LookupError as e:
        abort(404, description=str(e))
    except Exception as e:
        abort(400, description=str(e))

    track_to_mp(
        request,
        "update_complaint_penalty",
        {
            "complaint_uid": complaint_uid,
            "penalty_uid": penalty.uid
        },
    )
    return penalty.to_json()


# Delete a penalty for a complaint
@bp.route("/<complaint_uid>/penalties/<penalty_uid>", methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@edit_permission_required()
def delete_complaint_penalty(complaint_uid: str, penalty_uid: str):
    """Delete a penalty for a complaint.
    Must be an admin to delete a penalty.
    """
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    penalty = Penalty.nodes.get_or_none(uid=penalty_uid)
    if penalty is None:
        abort(404, description="Penalty not found")

    try:
        uid = penalty.uid
        penalty.delete()
        track_to_mp(
            request,
            "delete_complaint_penalty",
            {
                "complaint_uid": c.uid,
                "penalty_uid": uid
            },
        )
        return {"message": "Penalty deleted successfully"}, 204
    except Exception as e:
        abort(400, description=str(e))
