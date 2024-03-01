
from datetime import datetime
from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.database.models.user import User, UserRole
from flask import Blueprint, abort, current_app, request, jsonify
from flask_jwt_extended import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from flask_sqlalchemy import Pagination
from sqlalchemy.orm import joinedload

from ..database import (
    Partner,
    PartnerMember,
    MemberRole,
    db,
    Invitation,
    StagedInvitation,
)
from ..dto import InviteUserDTO
from flask_mail import Message
from ..config import TestingConfig
from ..schemas import (
    CreatePartnerSchema,
    partner_orm_to_json,
    partner_member_orm_to_json,
    partner_to_orm,
    validate,
    AddMemberSchema,
    partner_member_to_orm
)


bp = Blueprint("partner_routes", __name__, url_prefix="/api/v1/partners")


@bp.route("/<int:partner_id>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_partners(partner_id: int):
    """Get a single partner by ID."""

    return partner_orm_to_json(Partner.get(partner_id))


@bp.route("/create", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate(json=CreatePartnerSchema)
def create_partner():
    """Create a contributing partner.

    Cannot be called in production environments
    """
    if current_app.env == "production":
        abort(418)

    try:
        partner = partner_to_orm(request.context.json)
    except Exception:
        abort(400)

    created = partner.create()
    make_admin = PartnerMember(
        partner_id=created.id,
        user_id=get_jwt()["sub"],
        role=MemberRole.ADMIN,
    )
    make_admin.create()

    track_to_mp(
        request,
        "create_partner",
        {
            "partner_name": partner.name,
            "partner_contact": partner.contact_email,
        },
    )
    return partner_orm_to_json(created)


@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_all_partners():
    """Get all partners.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    all_partners = db.session.query(Partner)
    results = all_partners.paginate(
        page=q_page, per_page=q_per_page, max_per_page=100
    )

    return {
        "results": [partner_orm_to_json(partner) for partner in results.items],
        "page": results.page,
        "totalPages": results.pages,
        "totalResults": results.total,
    }


@bp.route("/<int:partner_id>/members/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()  # type: ignore
def get_partner_members(partner_id: int):
    """Get all members of a partner.
    Accepts Query ParaFmeters for pagination:
    per_page: number of results per page
    page: page number
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    # partner = Partner.get(partner_id)
    members: Pagination = (
        PartnerMember.query.options(
            joinedload(PartnerMember.user)  # type: ignore
        )
        .filter_by(partner_id=partner_id)
        .paginate(page=q_page, per_page=q_per_page, max_per_page=100)
    )

    return {
        "results": [
            partner_member_orm_to_json(member) for member in members.items
        ],
        "page": members.page,
        "totalPages": members.pages,
        "totalResults": members.total,
    }


""" This class currently doesn't work with the `partner_member_to_orm`
    class AddMemberSchema(BaseModel):
    user_email: str
    role: Optional[MemberRole] = PartnerMember.get_default_role()
    is_active: Optional[bool] = True

    class Config:
        extra = "forbid"
        schema_extra = {
            "example": {
                "user_email": "member@partner.org",
                "role": "ADMIN",
            }
        } """

# inviting anyone to NPDC


@bp.route("/invite", methods=["POST"])
@jwt_required()
@min_role_required(MemberRole.ADMIN)
@validate(auth=True, json=InviteUserDTO)
def add_member_to_partner():
    body: InviteUserDTO = request.context.json
    jwt_decoded = get_jwt()

    current_user = User.get(jwt_decoded["sub"])
    association = db.session.query(PartnerMember).filter(
        PartnerMember.user_id == current_user.id,
        PartnerMember.partner_id == body.partner_id,
    ).first()
    if (
        association is None
        or not association.is_administrator()
        or not association.partner_id == body.partner_id
    ):
        abort(403)
    mail = current_app.extensions.get('mail')
    user = User.query.filter_by(email=body.email).first()
    if user is not None:
        invitation_exists = Invitation.query.filter_by(
            partner_id=body.partner_id, user_id=user.id).first()
        if invitation_exists:
            return {
                "status": "error",
                "message": "Invitation already sent to this user!"
            }, 500
        else:
            try:
                new_invitation = Invitation(
                    partner_id=body.partner_id, user_id=user.id, role=body.role)
                db.session.add(new_invitation)
                db.session.commit()

                msg = Message("Invitation to join NPDC partner organization!",
                              sender=TestingConfig.MAIL_USERNAME,
                              recipients=[body.email])
                msg.body = """You are a registered user of NPDC and were invited
                to a partner organization. Please log on to accept or decline
                the invitation at https://dev.nationalpolicedata.org/."""
                mail.send(msg)
                return {
                    "status": "ok",
                    "message": "User notified of their invitation!"
                }, 200

            except Exception:
                return {
                    "status": "error",
                    "message": "Something went wrong! Please try again!"
                }, 500
    else:
        try:

            new_staged_invite = StagedInvitation(
                partner_id=body.partner_id, email=body.email, role=body.role)
            db.session.add(new_staged_invite)
            db.session.commit()
            msg = Message("Invitation to join NPDC index!",
                          sender=TestingConfig.MAIL_USERNAME,
                          recipients=[body.email])
            msg.body = """You are not a registered user of NPDC and were
                        invited to a partner organization. Please register
                        with NPDC index at
                        https://dev.nationalpolicedata.org/."""
            mail.send(msg)

            return {
                "status": "ok",
                "message": """User is not registered with the NPDC index.
                 Email sent to user notifying them to register."""
            }, 200

        except Exception:
            return {
                "status": "error",
                "message": "Something went wrong! Please try again!"
            }, 500
# user can join org they were invited to


@bp.route("/join", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def join_organization():
    try:
        body = request.get_json()
        user_exists = PartnerMember.query.filter_by(
            user_id=body["user_id"],
            partner_id=body["partner_id"]).first()
        if user_exists:
            return {
                "status" : "Error",
                "message": "User already in the organization"
            }, 400
        else:
            new_member = PartnerMember(
                user_id=body["user_id"],
                partner_id=body["partner_id"],
                role=body["role"],
                date_joined=datetime.now(),
                is_active=True
            )
            db.session.add(new_member)
            db.session.commit()
            Invitation.query.filter_by(
                user_id=body["user_id"],
                partner_id=body["partner_id"]).delete()
            db.session.commit()
            return {
                "status": "ok",
                "message": "Successfully joined partner organization"
            } , 200
    except Exception:
        db.session.rollback()
        return {
            "status": "Error",
            "message": "Something went wrong!"
        }, 500
    finally:
        db.session.close()

# user can leave org they already joined


@bp.route("/leave", methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def leave_organization():
    """
    remove from PartnerMember table
    """
    try:
        body = request.get_json()
        result = PartnerMember.query.filter_by(
            user_id=body["user_id"], partner_id=body["partner_id"]).delete()
        db.session.commit()
        if result > 0:
            return {
                "status": "ok",
                "message": "Succesfully left organization"
            }, 200
        else:
            return {
                "status": "Error",
                "message": "Not a member of this organization"
            }, 400
    except Exception:
        db.session.rollback()
        return {
            "status": "Error",
            "message": "Something went wrong!"
        }
    finally:
        db.session.close()

# admin can remove any member from a partner organization


@bp.route("/remove_member", methods=['DELETE'])
@jwt_required()
@min_role_required(MemberRole.ADMIN)
def remove_member():
    body = request.get_json()
    try:
        user_found = PartnerMember.query.filter_by(
            user_id=body["user_id"],
            partner_id=body["partner_id"]
            ).first()
        if user_found and user_found.role != MemberRole.ADMIN:
            PartnerMember.query.filter_by(
                user_id=body["user_id"],
                partner_id=body["partner_id"]).delete()
            db.session.commit()
            return {
                "status" : "ok",
                "message" : "Member successfully deleted from Organization"
            } , 200
        else:
            return {
                "status" : "Error",
                "message" : "Member is not part of the Organization"

            } , 400
    except Exception as e:
        db.session.rollback()
        return str(e)
    finally:
        db.session.close()


# admin can withdraw invitations that have been sent out
@bp.route("/withdraw_invitation", methods=['DELETE'])
@jwt_required()
@min_role_required(MemberRole.ADMIN)
def withdraw_invitation():
    body = request.get_json()
    try:
        user_found = Invitation.query.filter_by(
            user_id=body["user_id"],
            partner_id=body["partner_id"]
            ).first()
        if user_found:
            Invitation.query.filter_by(
                user_id=body["user_id"],
                partner_id=body["partner_id"]
            ).delete()
            db.session.commit()
            return {
                "status" : "ok",
                "message" : "Member's invitation withdrawn from Organization"
            } , 200
        else:
            return {
                "status" : "Error",
                "message" : "Member is not invited to the Organization"

            } , 400
    except Exception as e:
        db.session.rollback()
        return str(e)
    finally:
        db.session.close()


# admin can change roles of any user
@bp.route("/role_change", methods=["PATCH"])
@jwt_required()
@min_role_required(MemberRole.ADMIN)
def role_change():
    body = request.get_json()
    try:
        user_found = PartnerMember.query.filter_by(
            user_id=body["user_id"],
            partner_id=body["partner_id"]
            ).first()
        if user_found and user_found.role != "Administrator":
            user_found.role = body["role"]
            db.session.commit()
            return {
                "status" : "ok",
                "message" : "Role has been updated!"
            }, 200
        else:
            return {
                "status" : "Error",
                "message" : "User not found in this organization"
            }, 400
    except Exception as e:
        db.session.rollback
        return str(e)
    finally:
        db.session.close()


# view invitations table
@bp.route("/invitations", methods=["GET"])
@jwt_required()
@validate()
# only defined for testing environment
def get_invitations():
    if current_app.env == "production":
        abort(418)
    try:
        all_records = Invitation.query.all()
        records_list = [record.serialize() for record in all_records]
        return jsonify(records_list)

    except Exception as e:
        return str(e)


# view staged invitations table

@bp.route("/stagedinvitations", methods=["GET"])
@jwt_required()
@validate()
# only defined for testing environment
def stagedinvitations():
    if current_app.env == "production":
        abort(418)
    staged_invitations = StagedInvitation.query.all()
    invitations_data = [
        {
            'id': staged_invitation.id,
            'email': staged_invitation.email,
            'role': staged_invitation.role,
            'partner_id': staged_invitation.partner_id,
        }
        for staged_invitation in staged_invitations
    ]

    return jsonify({'staged_invitations': invitations_data})


@bp.route("/<int:partner_id>/members/add", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate(json=AddMemberSchema)
def add_member_to_partner_testing(partner_id: int):
    """Add a member to a partner.

    TODO: Allow the API to accept a user email instad of a user id
    TODO: Use the partner ID from the API path instead of the request body
    The `partner_member_to_orm` function seems very picky about the input.
    I wasn't able to get it to accept a dict or a PartnerMember object.

    Cannot be called in production environments
    """
    if current_app.env == "production":
        abort(418)

    # Ensure that the user has premission to add a member to this partner.
    jwt_decoded = get_jwt()

    current_user = User.get(jwt_decoded["sub"])
    association = (
        db.session.query(PartnerMember)
        .filter(
            PartnerMember.user_id == current_user.id,
            PartnerMember.partner_id == partner_id,
        )
        .first()
    )

    if (
        association is None
        or not association.is_administrator()
        or not association.partner_id == partner_id
    ):
        abort(403)

    # TODO: Allow the API to accept a user email instad of a user id
    # user_obj = User.get_by_email(request.context.json.user_email)
    # if user_obj is None:
    #     abort(400)

    # new_member = PartnerMember(
    #     partner_id=partner_id,
    #     user_id=user_obj.id,
    #     role=request.context.json.role,
    # )

    try:
        partner_member = partner_member_to_orm(request.context.json)
    except Exception:
        abort(400)

    created = partner_member.create()

    track_to_mp(
        request,
        "add_partner_member",
        {
            "partner_id": partner_id,
            "user_id": partner_member.user_id,
            "role": partner_member.role,
        },
    )
    return partner_member_orm_to_json(created)
