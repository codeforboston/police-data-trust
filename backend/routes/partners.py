from datetime import datetime
from typing import Optional

from backend.auth.jwt import min_role_required, contributor_has_partner
from backend.database.models.user import UserRole
from flask import Blueprint, abort, current_app, request
from flask_jwt_extended.view_decorators import jwt_required
from pydantic import BaseModel

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

    return Partner.get(partner_id).schema_json()


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
