import logging

from backend.auth.jwt import min_role_required
from backend.dto.search import SearchQueryParams
from backend.database.models.user import UserRole
from backend.services.search_service import SearchService
from flask import Blueprint, abort, request
from flask_jwt_extended.view_decorators import jwt_required
from flask import jsonify


bp = Blueprint("search_routes", __name__, url_prefix="/api/v1/search")
search_service = SearchService()


# Text Search Endpoint
@bp.route("", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def text_search():
    """Text Search
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    try:
        query_params = SearchQueryParams(**request.args)
    except Exception as e:
        logging.debug(f"Invalid query params: {e}")
        abort(400, description=str(e))

    response, status_code = search_service.search_text(
        query=query_params.term,
        page=query_params.page,
        per_page=query_params.per_page,
    )
    return jsonify(response), status_code
