import logging
# from typing import Optional, List
from backend.auth.jwt import min_role_required
from backend.schemas import (
    validate_request, add_pagination_wrapper, ordered_jsonify,
    NodeConflictException)
from backend.mixpanel.mix import track_to_mp
from backend.database.models.user import UserRole
from backend.database.models.agency import Agency
from backend.routes.search import (
    fetch_details, build_agency_result)
from .tmp.pydantic.agencies import CreateAgency, UpdateAgency
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended.view_decorators import jwt_required
from backend.dto.agency import (
    AgencyQueryParams, GetAgencyParams, GetAgencyOfficersParams, GetAgencyUnitsParams)
from backend.services.agency_service import AgencyService


bp = Blueprint("agencies_routes", __name__, url_prefix="/api/v1/agencies")
agency_service = AgencyService()


# Create agency profile
@bp.route("/", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreateAgency)
def create_agency():
    logger = logging.getLogger("create_agency")
    """Create an agency profile.
    User must be a Contributor to create an agency.
    Must include a name and jurisdiction.
    """
    body: CreateAgency = request.validated_body

    try:
        agency = Agency.from_dict(body.model_dump())
    except NodeConflictException:
        abort(409, description="Agency already exists")
    except Exception as e:
        logger.error(f"Error, Agency.from_dict: {e}")
        abort(400)

    try:
        Agency.link_location(agency, state=agency.hq_state, city=agency.hq_city)
    except Exception as e:
        logging.error(f"Error linking location {agency.name}: {e}")
        print(f"Error linking location {agency.name}: {e}")
        return

    track_to_mp(
        request,
        "create_agency",
        {
            "name": agency.name
        },
    )
    return agency.to_json()


# Get agency profile
@bp.route("/<agency_uid>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_agency(agency_uid: str):
    """Get an agency profile.
    Adds optional related data based on 'include' query parameter.
    Allowed include values:
    - units
    - officers
    - complaints
    - allegations
    """
    raw = {
        **request.args,  # copies simple values
        "include": request.args.getlist("include"),
    }
    try:
        params = GetAgencyParams(**raw)
    except Exception as e:
        logging.warning(f"Invalid query params: {e}")
        abort(400, description=str(e))
    try:
        agency_data = agency_service.get_agency_profile(
            agency_uid=agency_uid,
            includes=params.include or [],
        )
        return ordered_jsonify(agency_data), 200
    except ValueError:
        abort(404, description="Agency not found")


# Update agency profile
@bp.route("/<agency_uid>", methods=["PUT"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(UpdateAgency)
def update_agency(agency_uid: str):
    """Update an agency profile.
    """
    # logger = logging.getLogger("update_agency")
    body: UpdateAgency = request.validated_body
    agency = Agency.nodes.get_or_none(uid=agency_uid)
    if agency is None:
        abort(404, description="Agency not found")

    try:
        agency = Agency.from_dict(body.model_dump(), agency_uid)
        agency.refresh()
        track_to_mp(
            request,
            "update_agency",
            {
                "name": agency.name
            }
        )
        return agency.to_json()
    except Exception as e:
        abort(400, description=str(e))


# Delete agency profile
@bp.route("/<agency_id>", methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.ADMIN)
def delete_agency(agency_id: str):
    """Delete an agency profile.
    Must be an admin to delete an agency.
    """
    agency = Agency.nodes.get_or_none(uid=agency_id)
    if agency is None:
        abort(404, description="Agency not found")
    try:
        name = agency.name
        agency.delete()
        track_to_mp(
            request,
            "delete_agency",
            {
                "name": name
            }
        )
        return {"message": "Agency deleted successfully"}
    except Exception as e:
        abort(400, description=str(e))


# Get all agencies
@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_all_agencies():
    """Get all agencies.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    name: filter on agency name
    hq_city: filter on agency city
    hq_state: filter on agency state
    hq_zip: filter on agency zipcode
    jurisdiction: filter on agency jurisdiction
    """
    logging.warning(request.args)
    # --- Validate query parameters ---
    try:
        params = AgencyQueryParams(**request.args)
    except Exception as e:
        logging.warning(f"Invalid query params: {e}")
        abort(400, description=str(e))

    # preprocess query
    if params.name:
        search_term = Agency.preprocess_query(params.name)
    else:
        search_term = None

    # # --- Pagination ---
    # skip = (params.page - 1) * params.per_page

    # --- Extract filters ---
    filters = {
        k: v for k, v in {
            "hq_city": params.hq_city,
            "hq_state": params.hq_state,
            "hq_zip": params.hq_zip,
            "jurisdiction": params.jurisdiction,
        }.items() if v
    }

    # --- Count total matches ---
    row_count = Agency.search(
        query=search_term,
        filters=filters,
        count=True
    )
    logging.warning(f"requested page: {params.page}")
    logging.warning(f"Agency search found {row_count} results")
    if row_count == 0:
        return jsonify({"message": "No results found matching the query"}), 200
    if row_count <= params.skip:
        return jsonify({"message": "Page number exceeds total results"}), 400

    # --- Fetch paginated results ---
    results = Agency.search(
        query=search_term,
        filters=filters,
        skip=params.skip,
        limit=params.limit,
    )

    # --- Optional searchResult output ---
    if params.searchResult:
        details = fetch_details(
            [row.get("uid") for row in results], "Agency")
        agencies = [build_agency_result(
            row, details.get(row.get("uid"), {})) for row in results]
        page = [item.model_dump() for item in agencies if item]
        return_func = jsonify
    else:
        page = [row._properties for row in results]
        return_func = ordered_jsonify

    # Add pagination wrapper
    response = add_pagination_wrapper(
        page_data=page,
        total=row_count,
        page_number=params.page,
        per_page=params.per_page
    )

    return return_func(response), 200


# List agency units
@bp.route("/<agency_uid>/units", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_agency_units(agency_uid):
    """Get all units for an agency."""
    raw = {
        **request.args,
        "include": request.args.getlist("include"),
    }
    try:
        params = GetAgencyUnitsParams(**raw)
    except Exception as e:
        logging.warning(f"Invalid query params: {e}")
        abort(400, description=str(e))

    try:
        result = agency_service.list_agency_units(
            agency_uid=agency_uid,
            page=params.page,
            per_page=params.per_page,
            includes=params.include or [],
        )
        return ordered_jsonify(result), 200
    except IndexError:
        return jsonify({"message": "Page number exceeds total results"}), 400
    except ValueError:
        abort(404, description="Agency not found")


# Get agency officers
@bp.route("/<agency_uid>/officers", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_agency_officers(agency_uid):
    """Get all officers for an agency."""
    raw = {
        **request.args,
        "include": request.args.getlist("include"),
    }
    try:
        params = GetAgencyOfficersParams(**raw)
    except Exception as e:
        logging.warning(f"Invalid query params: {e}")
        abort(400, description=str(e))

    try:
        result = agency_service.list_agency_officers(
            agency_uid=agency_uid,
            page=params.page,
            per_page=params.per_page,
            includes=params.include or [],
        )
        return ordered_jsonify(result), 200
    except IndexError:
        return jsonify({"message": "Page number exceeds total results"}), 400
    except ValueError:
        abort(404, description="Agency not found")
