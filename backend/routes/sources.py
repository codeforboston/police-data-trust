
import logging
from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.database.models.user import User, UserRole
from ..schemas import (
    validate_request, paginate_results, ordered_jsonify,
    args_to_dict, add_pagination_wrapper,
    NodeConflictException)
from flask import Blueprint, abort, current_app, request
from flask_jwt_extended import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from pydantic import ValidationError

from ..database import (
    Source,
    MemberRole,
    Invitation,
    StagedInvitation,
)
from ..dto import InviteUserDTO
from ..dto.source import SourceFilters, CreatePartner, UpdatePartner
from flask_mail import Message
from ..config import TestingConfig


bp = Blueprint("source_routes", __name__, url_prefix="/api/v1/sources")


def source_query_builder(params: SourceFilters):
    query = Source.nodes
    if params.name is not None:
        query = query.filter(name__icontains=params.name)
    if params.name__in is not None:
        query = query.filter(name__in=params.name__in)
    return query


@bp.route("/slug/<source_slug>", methods=["GET"])
def get_source_by_slug(source_slug: str):
    """Get a single source by slug."""
    p = Source.nodes.get_or_none(slug=source_slug)
    if p is None:
        abort(404, description="Source not found")
    return p.to_json()


@bp.route("/<source_uid>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_source(source_uid: str):
    """Get a single source by UID."""
    p = Source.nodes.get_or_none(uid=source_uid)
    if p is None:
        abort(404, description="Source not found")
    return p.to_json()


@bp.route("/", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate_request(CreatePartner)
def create_source():
    """Create a contributing source."""
    logger = logging.getLogger("create_source")
    body: CreatePartner = request.validated_body
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])

    if (
        body.name is not None
        and body.contact_email is not None
        and body.name != ""
        and body.contact_email != ""
    ):

        # Creates a new instance of the Source and saves it to the DB
        try:
            new_p = Source.create_source(
                name=body.name,
                contact_email=body.contact_email,
                url=body.url,
                slug=body.slug)
        except NodeConflictException:
            abort(409, description="Source already exists")
        except Exception as e:
            abort(
                400,
                description=f"Failed to create source: {e}")
        # Connects the current user to the new source as an admin
        new_p.members.connect(
            current_user,
            {
                "role": MemberRole.ADMIN.value
            }
        )
        # update to UserRole contributor status
        if (current_user.role_enum.get_value()
                < UserRole.CONTRIBUTOR.get_value()):
            current_user.role = UserRole.CONTRIBUTOR.value
            current_user.save()
        logger.info(f"User {current_user.uid} created source {new_p.name}")

        track_to_mp(request, "create_source", {
            "source_name": new_p.name,
            "source_contact": new_p.primary_email.single().email
        })
        return new_p.to_json()
    else:
        return {
                "status": "error",
                "message": "Failed to create source. " +
                           "Please include all of the following"
        }, 400


@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_all_sources():
    """Get all sources.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    q_params = args_to_dict(
        request.args, always_list={"name__in"})
    try:
        params = SourceFilters.model_validate(q_params)
    except ValidationError as e:
        logging.warning(f"Invalid query parameters: {e}")
        abort(400, description=f"Invalid query parameters: {e}")

    q_page = params.page
    q_per_page = params.per_page

    page, count = Source.filter_sources(
        name=params.name,
        name__in=params.name__in,
        page=q_page,
        per_page=q_per_page
    )
    results = add_pagination_wrapper(
        page_data=[page.to_dict() for page in page], total=count,
        page_number=q_page, per_page=q_per_page)
    return ordered_jsonify(results), 200


@bp.route("/<source_uid>", methods=["PATCH"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate_request(UpdatePartner)
def update_source(source_uid: str):
    """Update a source's information."""
    body: UpdatePartner = request.validated_body
    current_user = User.get(get_jwt()["sub"])
    p = Source.nodes.get_or_none(uid=source_uid)
    if p is None:
        abort(404, description="Source not found")

    if p.members.is_connected(current_user):
        rel = p.members.relationship(current_user)
        if not rel.is_administrator():
            abort(403, description="Not authorized to update source")
    else:
        abort(403, description="Not authorized to update source")

    try:
        p.update_source(
            name=body.name,
            contact_email=body.contact_email,
            url=body.url,
            slug=body.slug
        )
    except Exception as e:
        abort(400, description=str(e))

    if body.social_media is not None:
        social = p.social_media.single()
        updates = body.social_media.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(social, key, value)
        social.save()

    return p.to_json()


@bp.route("/<source_uid>/members/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_source_members(source_uid: int):
    """Get all members of a source.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    p = Source.nodes.get_or_none(uid=source_uid)
    if p is None:
        abort(404, description="Source not found")

    all_members = p.members.all()
    results = paginate_results(all_members, q_page, q_per_page)
    return ordered_jsonify(results), 200


""" This class currently doesn't work with the `source_member_to_orm`
    class AddMemberSchema(BaseModel):
    user_email: str
    role: Optional[MemberRole] = SourceMember.get_default_role()
    is_active: Optional[bool] = True

    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "user_email": "member@source.org",
                "role": "ADMIN",
            }
        } """

# inviting anyone to NPDC


@bp.route("/invite", methods=["POST"])
@jwt_required()
@min_role_required(MemberRole.ADMIN)
# @validate(auth=True, json=InviteUserDTO)
def add_member_to_source():
    body: InviteUserDTO = request.context.json
    logger = logging.getLogger("add_member_to_source")
    jwt_decoded = get_jwt()

    current_user = User.get(jwt_decoded["sub"])
    membership = current_user.sources.search(
        uid=body.source_uid).first()

    if (
        membership is None
        or not membership.is_administrator()
    ):
        abort(403)
    mail = current_app.extensions.get('mail')
    invited_user = User.get_by_email(email=body.email)
    source = Source.nodes.get_or_none(uid=body.source_uid)
    if source is None:
        return {
            "status": "error",
            "message": "Source not found!"
        }, 404
    if invited_user is not None:
        invitation_exists = source.invitations.is_connected(
            invited_user)
        if invitation_exists:
            return {
                "status": "error",
                "message": "Invitation already sent to this user!"
            }, 409
        else:
            try:
                new_invitation = Invitation(
                    role=body.role
                ).save()
                source.invitations.connect(new_invitation).save()
                invited_user.received_invitations.connect(new_invitation).save()
                current_user.extended_invitations.connect(new_invitation).save()

                msg = Message("Invitation to join an NPDC source organization!",
                              sender=TestingConfig.MAIL_USERNAME,
                              recipients=[body.email])
                msg.body = "You have been invited to a join a source" + \
                    " organization. Please log on to accept or decline" + \
                    " the invitation at https://dev.nationalpolicedata.org/."
                mail.send(msg)
                return {
                    "status": "ok",
                    "message": "User notified of their invitation!"
                }, 200

            except Exception as e:
                logger.exception(f"Failed to send invitation: {e}")
                return {
                    "status": "error",
                    "message": "Something went wrong! Please try again!"
                }, 500
    else:
        try:
            existing_invitation = source.staged_invitations.search(
                email=body.email
            ).first()
            if existing_invitation is not None:
                return {
                    "status": "error",
                    "message": "Invitation already sent to this user!"
                }, 409
            else:
                new_staged_invite = StagedInvitation(
                    email=body.email, role=body.role).save()
                source.staged_invitations.connect(new_staged_invite).save()
                current_user.extended_staged_invitations.connect(
                    new_staged_invite).save()

                msg = Message(
                    "Invitation to join NPDC index!",
                    sender=TestingConfig.MAIL_USERNAME,
                    recipients=[body.email])
                msg.body = """You have been
                            invited to a source organization. Please register
                            with NPDC index at
                            https://dev.nationalpolicedata.org/."""
                mail.send(msg)

            return {
                "status": "ok",
                "message": """User is not registered with the NPDC index.
                 Email sent to user notifying them to register."""
            }, 200

        except Exception as e:
            logger.exception(f"Failed to send invitation: {e}")
            return {
                "status": "error",
                "message": "Something went wrong! Please try again!"
            }, 500


# user can join org they were invited to
@bp.route("/join", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate_request(CreatePartner)
def join_organization():
    logger = logging.getLogger("join_organization")
    body: CreatePartner = request.validated_body
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])
    source = Source.nodes.get_or_none(uid=body["source_uid"])
    if source is None:
        return {
            "status": "error",
            "message": "Source not found!"
        }, 404

    # invitations = current_user.invitations.all()
    # TODO: Confirm that the user has a valid invitation to this organization.
    # If not, return a 403 error.
    # Note: currently inivtations are implemented as a Node... Perhaps a
    # relationship would be more appropriate.
    try:
        body = request.get_json()
        membership = current_user.sources.search(
            uid=body["source_uid"]
        ).first()
        if membership is not None:
            return {
                "status" : "Conflict",
                "message": "User already in the organization"
            }, 409
        else:
            current_user.sources.connect(
                source,
                {
                    "role": body["role"]
                }
            ).save()

            # TODO: Remove the invitation from the user's list of invitations
            logger.info(f"User {current_user.uid} joined {source.name}")
            return {
                "status": "ok",
                "message": "Successfully joined source organization"
            } , 200
    except Exception as e:
        logger.exception(f"Failed to join organization: {e}")
        return {
            "status": "Error",
            "message": "Something went wrong!"
        }, 500


# user can leave org they already joined
@bp.route("/leave", methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def leave_organization():
    """
    Disconnect the user from the source organization.
    """
    logger = logging.getLogger("leave_organization")
    try:
        body = request.get_json()
        jwt_decoded = get_jwt()
        current_user = User.get(jwt_decoded["sub"])
        source = current_user.sources.search(
            uid=body["source_uid"]
        ).first()
        if source is not None:
            current_user.sources.disconnect(
                source
            ).save()
            logger.info(f"User {current_user.uid} left {source.name}")
            return {
                "status": "ok",
                "message": "Succesfully left organization"
            }, 200
        else:
            return {
                "status": "Error",
                "message": "Not a member of this organization"
            }, 400
    except Exception as e:
        logger.exception(
            f"User {current_user.uid} failed to leave organization: {e}")
        return {
            "status": "Error",
            "message": "Something went wrong!"
        }


# admin can remove any member from a source organization
@bp.route("/remove_member", methods=['DELETE'])
@jwt_required()
@min_role_required(MemberRole.ADMIN)
def remove_member():
    body = request.get_json()
    logger = logging.getLogger("remove_member")
    source = Source.nodes.get_or_none(uid=body["source_uid"])
    current_user = User.get(get_jwt()["sub"])
    user_to_remove = User.get(body["user_id"])
    if source is None:
        return {
            "status": "error",
            "message": "Source not found!"
        }, 404
    if user_to_remove is None:
        return {
            "status": "error",
            "message": "User not found!"
        }, 404
    c_user_membership = current_user.sources.relationship(
        source
    ).first()
    if c_user_membership is None or not c_user_membership.is_administrator():
        return {
            "status": "Unauthorized",
            "message": "Not authorized to remove members!"
        }, 403
    user_membership = user_to_remove.sources.relationship(
        source
    ).first()
    if user_membership is None:
        return {
            "status": "error",
            "message": "User not a member of this organization!"
        }, 404
    try:
        source.members.disconnect(user_to_remove).save()
        user_to_remove.sources.disconnect(source).save()
        return {
            "status" : "ok",
            "message" : "Member successfully deleted from Organization"
        } , 200
    except Exception as e:
        logger.exception(
            "Failed to remove user {} from {}: {}".format(
                user_to_remove.uid,
                source.name,
                e
            ))
        return {
            "status" : "Error",
            "message" : "Something went wrong!"
        }, 500


# # admin can withdraw invitations that have been sent out
# @bp.route("/withdraw_invitation", methods=['DELETE'])
# @jwt_required()
# @min_role_required(MemberRole.ADMIN)
# def withdraw_invitation():
#     body = request.get_json()
#     try:
#         user_found = Invitation.query.filter_by(
#             user_id=body["user_id"],
#             source_uid=body["source_uid"]
#             ).first()
#         if user_found:
#             Invitation.query.filter_by(
#                 user_id=body["user_id"],
#                 source_uid=body["source_uid"]
#             ).delete()
#             db.session.commit()
#             return {
#                 "status" : "ok",
#                 "message" : "Member's invitation withdrawn from Organization"
#             } , 200
#         else:
#             return {
#                 "status" : "Error",
#                 "message" : "Member is not invited to the Organization"

#             } , 400
#     except Exception as e:
#         db.session.rollback()
#         return str(e)
#     finally:
#         db.session.close()


# # admin can change roles of any user
# @bp.route("/role_change", methods=["PATCH"])
# @jwt_required()
# @min_role_required(MemberRole.ADMIN)
# def role_change():
#     body = request.get_json()
#     try:
#         user_found = SourceMember.query.filter_by(
#             user_id=body["user_id"],
#             source_uid=body["source_uid"]
#             ).first()
#         if user_found and user_found.role != "Administrator":
#             user_found.role = body["role"]
#             db.session.commit()
#             return {
#                 "status" : "ok",
#                 "message" : "Role has been updated!"
#             }, 200
#         else:
#             return {
#                 "status" : "Error",
#                 "message" : "User not found in this organization"
#             }, 400
#     except Exception as e:
#         db.session.rollback
#         return str(e)
#     finally:
#         db.session.close()


# # view invitations table
# @bp.route("/invitations", methods=["GET"])
# @jwt_required()
# @validate()
# # only defined for testing environment
# def get_invitations():
#     if current_app.env == "production":
#         abort(418)
#     try:
#         all_records = Invitation.query.all()
#         records_list = [record.serialize() for record in all_records]
#         return jsonify(records_list)

#     except Exception as e:
#         return str(e)


# # view staged invitations table

# @bp.route("/stagedinvitations", methods=["GET"])
# @jwt_required()
# @validate()
# # only defined for testing environment
# def stagedinvitations():
#     if current_app.env == "production":
#         abort(418)
#     staged_invitations = StagedInvitation.query.all()
#     invitations_data = [
#         {
#             'id': staged_invitation.id,
#             'email': staged_invitation.email,
#             'role': staged_invitation.role,
#             'source_uid': staged_invitation.source_uid,
#         }
#         for staged_invitation in staged_invitations
#     ]

#     return jsonify({'staged_invitations': invitations_data})
