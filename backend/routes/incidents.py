import logging
from datetime import datetime
from typing import Optional

from backend.auth.jwt import min_role_required, contributor_has_partner
from backend.mixpanel.mix import track_to_mp
from mixpanel import MixpanelException
from flask import Blueprint, abort, current_app, request
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended import get_jwt
from pydantic import BaseModel
from typing import Any

from ..database import (
    Incident,
    db,
    Partner,
    PrivacyStatus,
    UserRole,
    MemberRole,
    PartnerMember,
)
from ..schemas import (
    CreateIncidentSchema,
    incident_orm_to_json,
    incident_to_orm,
    validate,
)

bp = Blueprint("incident_routes", __name__, url_prefix="/api/v1/incidents")


@bp.route("/get/<int:incident_id>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_incident(incident_id: int):
    """Get a single incident by ID."""

    return incident_orm_to_json(Incident.get(incident_id))


@bp.route("/create", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@contributor_has_partner()
@validate(json=CreateIncidentSchema)
def create_incident():
    """Create a single incident.

    Cannot be called in production environments
    """
    if current_app.env == "production":
        abort(418)

    try:
        incident = incident_to_orm(request.context.json)
    except Exception:
        abort(400)

    created = incident.create()
    track_to_mp(request, "create_incident", {"source_id": incident.source_id})
    return incident_orm_to_json(created)


class SearchIncidentsSchema(BaseModel):
    location: Optional[str] = None
    dateStart: Optional[str] = None
    dateEnd: Optional[str] = None
    description: Optional[str] = None
    page: Optional[int] = 1
    perPage: Optional[int] = 20

    class Config:
        extra = "forbid"
        schema_extra = {
            "example": {
                "description": "Test description",
                "dateEnd": "2019-12-01",
                "location": "Location 1",
                "dateStart": "2019-09-01",
            }
        }


@bp.route("/search", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate(json=SearchIncidentsSchema)
def search_incidents():
    """Search Incidents."""
    body: SearchIncidentsSchema = request.context.json
    query = db.session.query(Incident)
    logger = logging.getLogger("incidents")

    try:
        if body.location:
            # TODO: Replace with .match, which uses `@@ to_tsquery`
            # for full-text search
            #
            # TODO: eventually replace with geosearch. Geocode
            # records and integrate PostGIS
            query = query.filter(Incident.location.ilike(f"%{body.location}%"))
        if body.dateStart:
            query = query.filter(
                Incident.time_of_incident
                >= datetime.fromisoformat(body.dateStart)
            )
        if body.dateEnd:
            query = query.filter(
                Incident.time_of_incident
                <= datetime.fromisoformat(body.dateEnd)
            )
        if body.description:
            query = query.filter(
                Incident.description.ilike(f"%{body.description}%")
            )
    except Exception as e:
        abort(422, description=str(e))

    results = query.paginate(
        page=body.page, per_page=body.perPage, max_per_page=100
    )

    try:
        track_to_mp(
            request,
            "search_incidents",
            {
                "description": body.description,
                "location": body.location,
                "dateStart": body.dateStart,
                "dateEnd": body.dateEnd,
            },
        )
    except MixpanelException as e:
        logger.error(e)

    try:
        return {
            "results": [
                incident_orm_to_json(result) for result in results.items
            ],
            "page": results.page,
            "totalPages": results.pages,
            "totalResults": results.total,
        }
    except Exception as e:
        abort(500, description=str(e))


@bp.route("/", methods=["GET"])
@jwt_required()  # type: ignore
@min_role_required(UserRole.PUBLIC)
@validate()  # type: ignore
def get_incidents():
    """
    Get a list of incidents. If a partner_id is provided, only incidents
    from that partner will be returned. If no partner_id is provided, all
    incidents will be returned.

    If the user is a member of the partner, they will be able to see
    private incidents. Otherwise, they will only see public incidents.

    :param partner_id: The ID of the partner to filter by.
    :param page: The page number to return.
    :param per_page: The number of incidents to return per page.

    :return: A JSON object containing a list of incidents.
    """
    partner_id = request.args.get("partner_id", type=int)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    partner: Partner | None = None
    if partner_id:
        partner = Partner.get(partner_id, False)
        if not partner:
            return {"message": "Partner not found"}, 404

    # Check if the user has permission to view incidents for this partner
    jwt_decoded: dict[str, str] = get_jwt()
    user_id = jwt_decoded["sub"]

    # Query the Incident table for records with the given partner_id
    # and paginate the results.
    query = Incident.query
    if partner_id:
        query = query.filter_by(source_id=partner_id)
    # If the user is not a member of the partner, they will
    # only see public incidents
    if (
        not partner_id
        or not partner
        or user_id not in [user.id for user in partner.members]
    ):
        query = query.filter_by(privacy_filter=PrivacyStatus.PUBLIC)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    incidents: list[dict[str, Any]] = [
        incident_orm_to_json(incident) for incident in pagination.items
    ]

    # Convert the Incident objects to dictionaries and return them as JSON
    return {
        "results": incidents,
        "page": pagination.page,
        "totalPages": pagination.pages,
        "totalResults": pagination.total,
    }


@bp.route("/<int:incident_id>", methods=["DELETE"])
@jwt_required()  # type: ignore
@min_role_required(UserRole.CONTRIBUTOR)
@validate()  # type: ignore
def delete_incident(incident_id: int):
    """
    Delete an incident by ID. Only users with the role of PUBLISHER or ADMIN
    can delete incidents.

    :param incident_id: The ID of the incident to delete.
    :return: A JSON object containing a message indicating that the incident
    was deleted successfully.
    """
    jwt_decoded: dict[str, str] = get_jwt()
    user_id = jwt_decoded["sub"]

    # Check permissions first for security
    permission = PartnerMember.query.filter(  # type: ignore
        PartnerMember.user_id == user_id,
        PartnerMember.role.in_((MemberRole.PUBLISHER, MemberRole.ADMIN)),
    ).first()
    if not permission:
        abort(403)

    incident = Incident.get(incident_id, False)
    if incident is None:
        abort(404)

    incident.delete()

    return {"message": "Incident deleted successfully"}, 204
