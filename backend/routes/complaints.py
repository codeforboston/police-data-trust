import logging
from functools import wraps

from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.schemas import validate_request, ordered_jsonify, paginate_results
from backend.database.models.user import UserRole, User
from backend.database.models.complaint import (
    Complaint, Penalty, Allegation, Investigation, Location)
from backend.database.models.source import Source
from backend.database.models.attachment import Attachment
from backend.database.models.civilian import Civilian
from backend.database.models.officer import Officer
from .tmp.pydantic.complaints import (
    CreateComplaint, UpdateComplaint,
    CreateAllegation, CreateInvestigation, CreatePenalty,
    CreateCivilian)
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask_jwt_extended.view_decorators import jwt_required


bp = Blueprint("complaint_routes", __name__, url_prefix="/api/v1/complaints")


def create_allegation(
        complaint: Complaint,
        allegation_input: CreateAllegation,
        civilian: Civilian = None):
    """
    Create an allegation for a complaint and the required connections.
    Returns the created Allegation instance.
    """
    a_data = allegation_input.model_dump(exclude_unset=True)
    officer_uid = a_data.pop("accused_uid", None)
    complainant_data = a_data.pop("complainant", None)

    # Officer is required
    if not officer_uid:
        raise ValueError("Officer UID is required for the allegation")

    officer = Officer.nodes.get_or_none(uid=officer_uid)
    if officer is None:
        raise ValueError(f"Officer with UID {officer_uid} not found")

    allegation = None
    try:
        allegation = Allegation(**a_data).save()
        allegation.accused.connect(officer)
        allegation.complaint.connect(complaint)
        logging.info(
            f"Allegation {allegation.uid} created for Complaint {complaint.uid}"
        )
    except Exception as e:
        logging.error(f"Error creating allegation: {e}")
        if allegation:
            allegation.delete()
        raise AttributeError(f"Failed to create allegation: {e}")

    # Handle complainant
    try:
        if civilian:
            # Civilian already looked up
            allegation.complainant.connect(civilian)

        elif complainant_data:
            civ_id = complainant_data.get("civ_id")
            if not civ_id:
                raise ValueError(
                    "civ_id must be provided in complainant_data"
                )

            new_civilian = Civilian(**complainant_data).save()
            allegation.complainant.connect(new_civilian)

    except Exception as e:
        logging.error(f"Error connecting complainant to allegation: {e}")
        if not civilian and "new_civilian" in locals():
            new_civilian.delete()
        raise

    return allegation


def update_allegation(
        allegation: Allegation, allegation_input: CreateAllegation):
    """
    Update an existing allegation with new data.
    """
    a_data = allegation_input.model_dump(exclude_unset=True)
    officer_uid = a_data.pop("accused_uid", None)
    complainant_data = a_data.pop("complainant", None)

    # Update Officer for Allegation
    if officer_uid:
        officer = Officer.nodes.get_or_none(uid=officer_uid)
        if officer is None:
            # Raise an error if the officer is not found
            raise ValueError(f"Officer with UID {officer_uid} not found")
        else:
            allegation.accused.replace(officer)

    if complainant_data:
        # See if there is a complainant already connected
        complainant = allegation.complainant.single()
        if complainant:
            # If a complainant is already connected, update their information
            for key, value in complainant_data.items():
                setattr(complainant, key, value)
            complainant.save()
        else:
            # If no complainant is connected, create a new one
            complainant = Civilian(**complainant_data)
            allegation.complainant.connect(complainant)

    try:
        Allegation.from_dict(a_data, allegation.uid)
        logging.info(f"Allegation {allegation.uid} updated")
    except Exception as e:
        logging.error(f"Error updating allegation: {e}")
        raise AttributeError(
            f"Failed to update allegation: {e}")
    return allegation


def create_penalty(
        complaint: Complaint, penalty_input: CreatePenalty):
    """
    Create a penalty for a complaint and the required connections.
    Returns the created Penalty instance or False if an error occurs.
    """
    p_data = penalty_input.model_dump(exclude_unset=True)
    officer_uid = p_data.pop("officer_uid", None)
    if officer_uid:
        officer = Officer.nodes.get_or_none(uid=officer_uid)
        if officer is None:
            # Raise an error if the officer is not found
            raise ValueError(f"Officer with UID {officer_uid} not found")
    else:
        raise ValueError("Officer UID is required for the penalty")
    try:
        penalty = Penalty(**p_data).save()
        penalty.complaint.connect(complaint)
        penalty.officer.connect(officer)
        logging.info(
            f"Penalty {penalty.uid} created for Complaint {complaint.uid}")
    except Exception as e:
        logging.error(f"Error creating penalty: {e}")
        if penalty:
            # If the penalty was created but failed to connect, delete it
            logging.error(f"Deleting penalty {penalty.uid} due to error")
            penalty.delete()
        return AttributeError(
            f"Failed to create penalty: {e}")
    return penalty


def update_penalty(
        penalty: Penalty, penalty_input: CreatePenalty):
    """
    Update an existing penalty with new data.
    """
    p_data = penalty_input.model_dump(exclude_unset=True)
    officer_uid = p_data.pop("officer_uid", None)
    if officer_uid:
        officer = Officer.nodes.get_or_none(uid=officer_uid)
        if officer is None:
            # Raise an error if the officer is not found
            raise ValueError(f"Officer with UID {officer_uid} not found")
        else:
            penalty.officer.reconnect(
                penalty.officer.single(),
                officer)
    try:
        Penalty.from_dict(p_data, penalty.uid)
        logging.info(
            f"Penalty {penalty.uid} updated")
    except Exception as e:
        logging.error(f"Error updating penalty: {e}")
        raise AttributeError(
            f"Failed to update penalty: {e}")
    return penalty


def create_investigation(
        complaint: Complaint, investigation_input: CreateInvestigation):
    """
    Create an investigation for a complaint and the required connections.
    Returns the created Investigation instance or False if an error occurs.
    """
    i_data = investigation_input.model_dump(exclude_unset=True)
    investigator_uid = i_data.pop("investigator_uid", None)
    try:
        investigation = Investigation(**i_data).save()
        investigation.complaint.connect(complaint)
        logging.info(
            f"Investigation {investigation.uid} created "
            f"for Complaint {complaint.uid}")
    except Exception as e:
        logging.error(f"Error creating investigation: {e}")
        return AttributeError(
            f"Failed to create investigation: {e}")
    if investigator_uid:
        investigator = Officer.nodes.get_or_none(uid=investigator_uid)
        if investigator:
            investigation.investigator.connect(investigator)
    return investigation


def update_investigation(
        investigation: Investigation, investigation_input: CreateInvestigation):
    """
    Update an existing investigation with new data.
    """
    i_data = investigation_input.model_dump(exclude_unset=True)
    investigator_uid = i_data.pop("investigator_uid", None)

    if investigator_uid:
        investigator = Officer.nodes.get_or_none(uid=investigator_uid)
        if investigator:
            investigation.investigator.replace(investigator)
        else:
            raise ValueError(
                f"Officer with UID {investigator_uid} not found")
    try:
        Investigation.from_dict(i_data, investigation.uid)
        logging.info(
            f"Investigation {investigation.uid} updated")
    except Exception as e:
        logging.error(f"Error updating investigation: {e}")
        raise AttributeError(
            f"Failed to update investigation: {e}")
    return investigation


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
    source_details = complaint_data.pop("source_details", None)
    location_data = complaint_data.pop("location", None)
    attachments = complaint_data.pop("attachments", [])
    allegations = complaint_data.pop("allegations", [])
    investigations = complaint_data.pop("investigations", [])
    penalties = complaint_data.pop("penalties", [])
    civilian_witnesses = complaint_data.pop("civilian_witnesses", [])
    police_witnesses = complaint_data.pop("police_witnesses", [])
    source_uid = complaint_data.pop("source_uid", None)

    source = Source.nodes.get_or_none(uid=source_uid)
    if source is None:
        abort(400, description="Invalid Complaint: Source not found")
    if source_details is None:
        abort(400, description="Invalid Complaint: Source details are required")
    # Verify that the user is a member of the source
    # Need to also verify that the user is a Publisher or Higher
    if not source.members.is_connected(current_user):
        abort(
            403,
            description="User does not have permission to "
            "create a complaint for this source.")
    if not source.members.relationship(current_user).may_publish():
        abort(403, description="User does not have permission to "
              "create a complaint for this source.")
    if not location_data:
        abort(400, description="Invalid Complaint: Location is required")
    else:
        loc = Location.from_dict(location_data)

    try:
        complaint = Complaint.from_dict(complaint_data)
        complaint.location.connect(loc)
        complaint.source_org.connect(source, source_details)
    except Exception as e:
        logger.error(f"Error creating complaint: {e}")
        abort(400, description=str(e))

    # Add attachments
    if attachments:
        for attachment in attachments:
            try:
                a = Attachment.from_dict(attachment)
                complaint.attachments.connect(a)
            except Exception as e:
                logger.error(f"Error linking attachment: {e}")
                abort(400, description=str(e))

    # Add allegations
    if allegations:
        civ_map = {}  # external civ_id -> Civilian node
        for allegation in allegations:
            complainant_data = allegation.get("complainant")
            civilian_node = None

            if complainant_data:
                ext_civ_id = complainant_data.get("civ_id")
                if ext_civ_id in civ_map:
                    # Reuse existing Civilian
                    civilian_node = civ_map[ext_civ_id]
                else:
                    # Create a new Civilian node and track it
                    civ_count = len(civ_map) + 1
                    internal_civ_id = f"{complaint.uid}-{civ_count}"
                    complainant_data["civ_id"] = internal_civ_id
                    civilian_node = Civilian(**complainant_data).save()
                    if ext_civ_id:
                        civ_map[ext_civ_id] = civilian_node

            try:
                a_model = CreateAllegation(**allegation)
                create_allegation(complaint, a_model, civilian_node)
            except ValueError as ve:
                logger.error(f"Error creating allegation: {ve}")
            except AttributeError as ae:
                logger.error(f"Error creating allegation: {ae}")

    # Add Penalties
    if penalties:
        for penalty in penalties:
            try:
                p_model = CreatePenalty(**penalty)
                create_penalty(complaint, p_model)
            except ValueError as ve:
                logger.error(f"Error creating penalty: {ve}")
            except AttributeError as ae:
                logger.error(f"Error creating penalty: {ae}")

    # Add Investigations
    if investigations:
        for investigation in investigations:
            try:
                i_model = CreateInvestigation(**investigation)
                create_investigation(complaint, i_model)
            except ValueError as ve:
                logger.error(f"Error creating investigation: {ve}")
            except AttributeError as ae:
                logger.error(f"Error creating investigation: {ae}")

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
    return complaint.to_json(), 201


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
@bp.route("/<complaint_uid>", methods=["PATCH"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(UpdateComplaint)
@edit_permission_required()
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
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    civilian = None
    complainant_data: CreateCivilian = body.complainant

    if complainant_data:
        civ_id = complainant_data.civ_id  # use attribute access
        if civ_id:
            # Lookup existing civilian
            civilian = Civilian.nodes.get_or_none(civ_id=civ_id)
            if civilian is None:
                abort(404,
                      description=f"Civilian with civ_id {civ_id} not found")
        else:
            # Manufacture a new civ_id using complaint uid + complainant count
            civ_count = len(c.complainants.all())
            # Use Pydantic copy/update instead of item assignment
            complainant_data = complainant_data.model_copy(update={
                "civ_id": f"{c.uid}-{civ_count + 1}"
            })
            body.complainant = complainant_data

    try:
        allegation = create_allegation(c, body, civilian)
    except ValueError as ve:
        abort(400, description=str(ve))
    except AttributeError as ae:
        abort(400, description=str(ae))
    if allegation is False:
        abort(400, description="Failed to create allegation.")

    track_to_mp(
        request,
        "create_complaint_allegation",
        {
            "complaint_uid": c.uid,
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
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    allegation = Allegation.nodes.get_or_none(uid=allegation_uid)
    if allegation is None:
        abort(404, description="Allegation not found")

    if allegation not in c.allegations:
        abort(404, description="Allegation not found for this complaint")

    return allegation.to_json(), 200


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
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    allegation = Allegation.nodes.get_or_none(uid=allegation_uid)
    if allegation is None:
        abort(404, description="Allegation not found")

    try:
        allegation = update_allegation(
            allegation, body)
        allegation.refresh()
    except Exception as e:
        abort(400, description=str(e))

    track_to_mp(
        request,
        "update_complaint_allegation",
        {
            "complaint_uid": c.uid,
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
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    try:
        investigation = create_investigation(c, body)
    except ValueError as ve:
        abort(400, description=str(ve))
    except AttributeError as ae:
        abort(400, description=str(ae))

    track_to_mp(
        request,
        "create_complaint_investigation",
        {
            "complaint_uid": c.uid,
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
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    investigation = Investigation.nodes.get_or_none(uid=investigation_uid)
    if investigation is None:
        abort(404, description="Investigation not found")

    if investigation not in c.investigations:
        abort(404, description="Investigation not found for this complaint")

    return investigation.to_json(), 200


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
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    investigation = Investigation.nodes.get_or_none(uid=investigation_uid)
    if investigation is None:
        abort(404, description="Investigation not found")

    try:
        investigation = Investigation.from_dict(
            body.model_dump(), investigation_uid)
        investigation.refresh()
    except Exception as e:
        abort(400, description=str(e))

    track_to_mp(
        request,
        "update_complaint_investigation",
        {
            "complaint_uid": c.uid,
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
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    try:
        penalty = create_penalty(c, body)
    except ValueError as ve:
        abort(400, description=str(ve))
    except AttributeError as ae:
        abort(400, description=str(ae))

    track_to_mp(
        request,
        "create_complaint_penalty",
        {
            "complaint_uid": c.uid,
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
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    penalty = Penalty.nodes.get_or_none(uid=penalty_uid)
    if penalty is None:
        abort(404, description="Penalty not found")

    if penalty not in c.penalties:
        abort(404, description="Penalty not found for this complaint")

    return penalty.to_json(), 200


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
    c = Complaint.nodes.get_or_none(uid=complaint_uid)
    if c is None:
        abort(404, description="Complaint not found")

    penalty = Penalty.nodes.get_or_none(uid=penalty_uid)
    if penalty is None:
        abort(404, description="Penalty not found")

    try:
        penalty = Penalty.from_dict(body.model_dump(), penalty_uid)
        penalty.refresh()
    except Exception as e:
        abort(400, description=str(e))

    track_to_mp(
        request,
        "update_complaint_penalty",
        {
            "complaint_uid": c.uid,
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
