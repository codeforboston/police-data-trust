import logging
# from typing import Optional, List
from backend.auth.jwt import min_role_required
from backend.schemas import (
    validate_request, add_pagination_wrapper, ordered_jsonify,
    args_to_dict,
    NodeConflictException)
from backend.mixpanel.mix import track_to_mp
from backend.database.models.user import UserRole, User
from backend.database.models.agency import Agency
from backend.serializers.search_serializer import (
    build_agency_result,
    fetch_details,
)
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from backend.dto.agency import (
    AgencyQueryParams, GetAgencyParams, GetAgencyOfficersParams,
    CreateAgency, UpdateAgency,
    GetAgencyUnitsParams)
from backend.services.agency_service import AgencyService
from backend.queries.filter_resolver import FilterResolver


bp = Blueprint("agencies_routes", __name__, url_prefix="/api/v1/agencies")
agency_service = AgencyService()
filter_resolver = FilterResolver()


# Create agency profile
@bp.route("", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate_request(CreateAgency)
def create_agency():
    """Create an agency profile.
    User must be a Contributor to create an agency.
    Must include a name and jurisdiction.
    """
    body: CreateAgency = request.validated_body
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])
    payload = body.model_dump(exclude={"source_uid"})

    try:
        response = agency_service.create_agency(
            payload=payload,
            source_uid=body.source_uid,
            current_user=current_user,
        )
        track_to_mp(
            request,
            "create_agency",
            {
                "name": response.get("name")
            },
        )
        return ordered_jsonify(response), 201
    except NodeConflictException:
        abort(409, description="Agency already exists")
    except PermissionError as e:
        abort(403, description=str(e))
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        logging.getLogger("create_agency").error(f"Error creating agency: {e}")
        abort(400, description=str(e))


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
        logging.debug(f"Invalid query params: {e}")
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
    body: UpdateAgency = request.validated_body
    jwt_decoded = get_jwt()
    current_user = User.get(jwt_decoded["sub"])
    payload = body.model_dump(exclude_unset=True, exclude={"source_uid"})

    try:
        response = agency_service.update_agency(
            agency_uid=agency_uid,
            payload=payload,
            source_uid=body.source_uid,
            current_user=current_user,
        )
        track_to_mp(
            request,
            "update_agency",
            {
                "name": response.get("name")
            }
        )
        return ordered_jsonify(response)
    except LookupError as e:
        abort(404, description=str(e))
    except PermissionError as e:
        abort(403, description=str(e))
    except ValueError as e:
        abort(400, description=str(e))
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
@bp.route("", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_all_agencies():
    """Get all agencies.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    term: filter on agency name
    hq_city: filter on agency city
    hq_state: filter on agency state
    hq_zip: filter on agency zipcode
    jurisdiction: filter on agency jurisdiction
    """
    logging.debug(request.args)
    # --- Validate query parameters ---
    try:
        params = AgencyQueryParams(**args_to_dict(
            request.args,
            always_list={"city", "city_uid", "state", "source", "source_uid", "jurisdiction"},
        ))
    except Exception as e:
        logging.debug(f"Invalid query params: {e}")
        abort(400, description=str(e))

    # preprocess query
    if params.term:
        search_term = Agency.preprocess_query(params.term)
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

    city_uids = filter_resolver.resolve_city_uids(
        city=params.city,
        city_uid=params.city_uid,
        state=params.state,
    )
    if (params.city or params.city_uid or params.state) and not city_uids:
        return jsonify({"message": "No results found matching the query"}), 200

    source_uids = filter_resolver.resolve_source_uids(
        source=params.source,
        source_uid=params.source_uid,
    )
    if (params.source or params.source_uid) and not source_uids:
        return jsonify({"message": "No results found matching the query"}), 200

    # --- Count total matches ---
    row_count = Agency.search(
        query=search_term,
        filters=filters,
        city_uids=city_uids,
        source_uids=source_uids,
        count=True
    )
    logging.debug(f"requested page: {params.page}")
    logging.debug(f"Agency search found {row_count} results")
    if row_count == 0:
        return jsonify({"message": "No results found matching the query"}), 200
    if row_count <= params.skip:
        return jsonify({"message": "Page number exceeds total results"}), 400

    # --- Fetch paginated results ---
    results = Agency.search(
        query=search_term,
        filters=filters,
        city_uids=city_uids,
        source_uids=source_uids,
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
        logging.debug(f"Invalid query params: {e}")
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
        "type": request.args.getlist("type"),
        "status": request.args.getlist("status"),
        "rank": request.args.getlist("rank"),
        "include": request.args.getlist("include"),
    }
    try:
        params = GetAgencyOfficersParams(**raw)
    except Exception as e:
        logging.debug(f"Invalid query params: {e}")
        abort(400, description=str(e))

    filters = {
        "type": params.type or [],
        "status": params.status or [],
        "rank": params.rank or [],
    }

    try:
        result = agency_service.list_agency_officers(
            agency_uid=agency_uid,
            page=params.page,
            per_page=params.per_page,
            includes=params.include or [],
            filters=filters,
            term=params.term,
        )
        return ordered_jsonify(result), 200
    except IndexError:
        return jsonify({"message": "Page number exceeds total results"}), 400
    except ValueError:
        abort(404, description="Agency not found")
