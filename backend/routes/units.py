import logging
from backend.auth.jwt import min_role_required
from backend.schemas import (
    add_pagination_wrapper, ordered_jsonify)
from backend.database.models.user import UserRole
from backend.database.models.agency import Unit, State
from backend.routes.search import create_unit_result
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended.view_decorators import jwt_required
# from neomodel import db
# from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


bp = Blueprint("unit_routes", __name__, url_prefix="/api/v1/units")


class UnitQueryParams(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1)
    searchResult: bool = Field(default=False)

    @validator("state")
    def validate_state(cls, v):
        if v and v not in State.choices():
            raise ValueError(f"Invalid state: {v}")
        return v


@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_all_units():
    """Get all units.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    name: filter on unit name
    city: filter on unit city
    state: filter on unit state
    """
    try:
        params = UnitQueryParams(**request.args)
    except Exception as e:
        logging.warning(f"Invalid query params: {e}")
        abort(400, description=str(e))

    # Pagination
    skip = (params.page - 1) * params.per_page

    # Extract filters
    search_term = params.name
    filters = {k: v for k, v in {"city": params.city,
                                 "state": params.state}.items() if v}

    # --- Count total matches ---
    row_count = Unit.search(query=search_term, filters=filters, count=True)

    if row_count == 0:
        return jsonify({"message": "No results found matching the query"}), 200
    if row_count < skip:
        return jsonify({"message": "Page number exceeds total results"}), 400

    # --- Fetch paginated results ---
    results = Unit.search(
        query=search_term,
        filters=filters,
        skip=skip,
        limit=params.per_page)

    # Optional searchResult format
    if params.searchResult:
        units = [create_unit_result(row) for row in results]
        page = [item.model_dump() for item in units if item]
        return_func = jsonify

    else:
        page = [row._properties for row in results]
        return_func = ordered_jsonify

    response = add_pagination_wrapper(
        page_data=page,
        total=row_count,
        page_number=params.page,
        per_page=params.per_page
    )
    # logging.warning(response)
    return return_func(response), 200
