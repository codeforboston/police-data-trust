from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.database.models.user import User, UserRole
from flask import Blueprint, abort, current_app, request
from flask_jwt_extended import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from flask_sqlalchemy import Pagination
from ..database import Partner, PartnerMember, MemberRole, db
from ..schemas import (
    CreatePartnerSchema,
    AddMemberSchema,
    partner_orm_to_json,
    partner_member_orm_to_json,
    user_orm_to_json,
    partner_member_to_orm,
    partner_to_orm,
    validate,
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
@validate()
def get_partner_members(partner_id: int):
    """Get all members of a partner.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    # partner = Partner.get(partner_id)
    all_members = db.session.query(PartnerMember).filter(
        PartnerMember.partner_id == partner_id
    )
    results = all_members.paginate(
        page=q_page, per_page=q_per_page, max_per_page=100
    )

    return {
        "results": [
            partner_member_orm_to_json(member) for member in results.items
        ],
        "page": results.page,
        "totalPages": results.pages,
        "totalResults": results.total,
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


@bp.route("/<int:partner_id>/users", methods=["GET"])
@jwt_required()  # type: ignore
@min_role_required(UserRole.PUBLIC)
@validate()  # type: ignore
def get_partner_users(partner_id: int):
    # Get the page number from the query parameters (default to 1)
    page = request.args.get("page", 1, type=int)

    # Get the number of items per page from the query parameters (default to 20)
    per_page = request.args.get("per_page", 20, type=int)

    # Query the PartnerMember table for records with
    # the given partner_id and paginate the results
    pagination: Pagination = PartnerMember.query.filter_by(
        partner_id=partner_id
    ).paginate(page=page, per_page=per_page, error_out=False)

    # If the partner_id is invalid, return a 404 error
    if pagination.total == 0:
        return {"message": "Partner not found"}, 404

    # Get the User objects associated with the members on the current page
    users: list[User] = [
        User.query.get(member.user_id) for member in pagination.items
    ]  # type: ignore

    # Convert the User objects to dictionaries and return them as JSON

    return {
        "results": [user_orm_to_json(user) for user in users],
        "page": pagination.page,
        "totalPages": pagination.pages,
        "totalResults": pagination.total,
    }


@bp.route("/<int:partner_id>/members/add", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate(json=AddMemberSchema)
def add_member_to_partner(partner_id: int):
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
