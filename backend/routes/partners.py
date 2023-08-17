from backend.auth.jwt import min_role_required
from backend.database.models.user import UserRole
from flask import Blueprint, abort, current_app, request
from flask_jwt_extended.view_decorators import jwt_required

from ..database import Partner, db
from ..schemas import (
    CreatePartnerSchema,
    partner_orm_to_json,
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
