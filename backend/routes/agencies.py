import logging

from operator import and_
from typing import Optional, List
from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.database.models.user import UserRole
from backend.database.models.officer import Officer
from backend.database.models.employment import (
    merge_employment_records,
    Employment
)
from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended.view_decorators import jwt_required
from sqlalchemy.exc import DataError
from pydantic import BaseModel

from ..database import Agency, db, AgencyView, AgencySearch
from ..schemas import (
    CreateAgencySchema,
    agency_orm_to_json,
    officer_orm_to_json,
    employment_to_orm,
    employment_orm_to_json,
    agency_to_orm,
    validate,
)
from sqlalchemy.sql.functions import GenericFunction

bp = Blueprint("agencies_routes", __name__, url_prefix="/api/v1/agencies")


class AddOfficerSchema(BaseModel):
    officer_id: int
    badge_number: str
    agency_id: Optional[int]
    highest_rank: Optional[str]
    earliest_employment: Optional[str]
    latest_employment: Optional[str]
    unit: Optional[str]
    currently_employed: bool = True


class AddOfficerListSchema(BaseModel):
    officers: List[AddOfficerSchema]


# Create agency profile
@bp.route("/", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate(json=CreateAgencySchema)
def create_agency():
    logger = logging.getLogger("create_agency")
    """Create an agency profile.
    User must be a Contributor to create an agency.
    Must include a name and jurisdiction.
    """

    try:
        agency = agency_to_orm(request.context.json)
    except Exception as e:
        logger.error(f"Error, agency_to_orm: {e}")
        abort(400)

    try:
        created = agency.create()
    except DataError as e:
        logger.error(f"DataError: {e}")
        abort(
            400,
            description="Invalid Agency. Please include a valid jurisdiction."
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        abort(400, description="Error creating agency")

    track_to_mp(
        request,
        "create_agency",
        {
            "name": agency.name
        },
    )
    return agency_orm_to_json(created)


# Get agency profile
@bp.route("/<int:agency_id>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_agency(agency_id: int):
    """Get an agency profile.
    """
    agency = db.session.query(Agency).get(agency_id)
    if agency is None:
        abort(404, description="Agency not found")
    try:
        return agency_orm_to_json(agency)
    except Exception as e:
        abort(500, description=str(e))


# Update agency profile
@bp.route("/<int:agency_id>", methods=["PUT"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate()
def update_agency(agency_id: int):
    """Update an agency profile.
    """
    agency = db.session.query(Agency).get(agency_id)
    if agency is None:
        abort(404, description="Agency not found")

    try:
        agency.update(request.context.json)
        db.session.commit()
        track_to_mp(
            request,
            "update_agency",
            {
                "name": agency.name
            }
        )
        return agency_orm_to_json(agency)
    except Exception as e:
        abort(400, description=str(e))


# Delete agency profile
@bp.route("/<int:agency_id>", methods=["DELETE"])
@jwt_required()
@min_role_required(UserRole.ADMIN)
@validate()
def delete_agency(agency_id: int):
    """Delete an agency profile.
    Must be an admin to delete an agency.
    """
    agency = db.session.query(Agency).get(agency_id)
    if agency is None:
        abort(404, description="Agency not found")
    try:
        db.session.delete(agency)
        db.session.commit()
        track_to_mp(
            request,
            "delete_agency",
            {
                "name": agency.name
            },
        )
        return {"message": "Agency deleted successfully"}
    except Exception as e:
        abort(400, description=str(e))


# Get all agencies
@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_all_agencies():
    """Get all agencies.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    all_agencies = db.session.query(Agency)
    pagination = all_agencies.paginate(
        page=q_page, per_page=q_per_page, max_per_page=100
    )

    try:
        return {
            "results": [
                agency_orm_to_json(agency) for agency in pagination.items],
            "page": pagination.page,
            "totalPages": pagination.pages,
            "totalResults": pagination.total,
        }
    except Exception as e:
        abort(500, description=str(e))


# Add officer employment information
@bp.route("/<int:agency_id>/officers", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.CONTRIBUTOR)
@validate(json=AddOfficerListSchema)
def add_officer_to_agency(agency_id: int):
    """Add any number of officer employment records to an agency.
    Must be a Contributor to add officers to an agency.
    """
    agency = db.session.query(Agency).get(agency_id)
    if agency is None:
        abort(404, description="Agency not found")

    records = request.context.json.officers

    created = []
    failed = []
    for record in records:
        try:
            officer = db.session.query(Officer).get(
                record.officer_id)
            if officer is None:
                failed.append({
                    "officer_id": record.officer_id,
                    "reason": "Officer not found"
                })
            else:
                employments = db.session.query(Employment).filter(
                    and_(
                        and_(
                            Employment.officer_id == record.officer_id,
                            Employment.agency_id == agency_id
                        ),
                        Employment.badge_number == record.badge_number
                    )
                )
                if employments is not None:
                    # If the officer already has a records for this agency,
                    # we need to update the earliest and latest employment dates
                    employment = employment_to_orm(record)
                    employment.agency_id = agency_id
                    employment = merge_employment_records(
                        employments.all() + [employment],
                        unit=record.unit,
                        currently_employed=record.currently_employed
                    )

                    # Delete the old records and replace them with the new one
                    employments.delete()
                    created.append(employment.create())
                else:
                    record.agency_id = agency_id
                    employment = employment_to_orm(record)
                    created.append(employment.create())
        except Exception as e:
            failed.append({
                "officer_id": record.officer_id,
                "reason": str(e)
            })
    try:
        track_to_mp(
            request,
            "add_officers_to_agency",
            {
                "agency_id": agency.id,
                "officers_added": len(created),
                "officers_failed": len(failed)
            },
        )
        return {
            "created": [
                employment_orm_to_json(item) for item in created],
            "failed": failed,
            "totalCreated": len(created),
            "totalFailed": len(failed),
        }
    except Exception as e:
        abort(400, description=str(e))


# Get agency officers
@bp.route("/<int:agency_id>/officers", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_agency_officers(agency_id: int):
    """Get all officers for an agency.
    Pagination currently isn't enabled due to the use of an association proxy.
    """
    # args = request.args
    # q_page = args.get("page", 1, type=int)
    # q_per_page = args.get("per_page", 20, type=int)
    # TODO: Add pagination

    try:
        agency = db.session.query(Agency).get(agency_id)

        all_officers = agency.officers

        return {
            "results": [
                officer_orm_to_json(officer) for officer in all_officers],
            "page": 1,
            "totalPages": 1,
            "totalResults": len(all_officers),
        }
    except Exception as e:
        abort(400, description=str(e))


"""
TSRank function ranks the search results
by most relevant in regard to the search term
that is provided.
"""


class TSRank(GenericFunction):
    package = 'full_text'
    name = 'ts_rank'
    inherit_cache = True


DEFAULT_PER_PAGE = 5


"""
Agency search endpoint.
Allows for searching on Agencies by Location (Address, City, Zip)
Returns ranked results relevant to search term.
"""


@min_role_required(UserRole.PUBLIC)
@bp.route("/search", methods=["POST"])
def search():
    # getting request parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', DEFAULT_PER_PAGE))
    search_term = request.args.get('search_term')
    # query to search using location attributes on db
    query = db.session.query(
        db.distinct(AgencyView.agency_id),
        AgencyView.agency_name,
        AgencyView.agency_website_url,
        AgencyView.agency_hq_address,
        AgencyView.agency_hq_city,
        AgencyView.agency_hq_zip,
        AgencyView.agency_jurisdiction,
        db.func.max(db.func.full_text.ts_rank(
            db.func.setweight(
                db.func.coalesce(
                    AgencyView.tsv_agency_hq_address, ''), 'A')
            .concat(
                db.func.setweight(db.func.coalesce(
                    AgencyView.tsv_agency_hq_city, ''), 'A'))
            .concat(
                db.func.setweight(db.func.coalesce(
                    AgencyView.tsv_agency_hq_zip, ''), 'A')
                    ), db.func.to_tsquery(
                        search_term,
                        postgresql_regconfig='english'
                        )
        )).label('rank')
    ).filter(db.or_(
        AgencyView.tsv_agency_hq_address.match(
            search_term,
            postgresql_regconfig='english'),
        AgencyView.tsv_agency_hq_city.match(
            search_term,
            postgresql_regconfig='english'),
        AgencyView.tsv_agency_hq_zip.match(
            search_term,
            postgresql_regconfig='english'),
    )).group_by(
        AgencyView.agency_id,
        AgencyView.agency_name,
        AgencyView.agency_website_url,
        AgencyView.agency_hq_address,
        AgencyView.agency_hq_city,
        AgencyView.agency_hq_zip,
        AgencyView.agency_jurisdiction
    ).order_by(db.text('rank DESC')).all()

    # returning queried results and pagination
    results = []
    for search_result in query:
        result_dict = {
                "name" : search_result.agency_name,
                "url" : search_result.agency_website_url,
                "hq_address" : search_result.agency_hq_address,
                "hq_city" : search_result.agency_hq_city,
                "hq_zipcode" : search_result.agency_hq_zip,
                "jurisdiction" : search_result.agency_jurisdiction,
        }
        results.append(result_dict)
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, len(results))
    paginated_results = results[start_index:end_index]
    response = {
                "page": page,
                "per_page": per_page,
                "total_results": len(results),
                "results": paginated_results
        }
    try:
        return jsonify(response)
    except Exception as e:
        return (500, str(e))


"""
Agency search by location
test API
"""


@min_role_required(UserRole.PUBLIC)
@bp.route("/test_search", methods=["POST"])
def test_agency_search():
    # getting request parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', DEFAULT_PER_PAGE))
    search_term = request.args.get('search_term')
    # query to search using location attributes on db
    query = db.session.query(
        db.distinct(AgencySearch.agency_id),
        AgencySearch.agency_name,
        AgencySearch.agency_website_url,
        AgencySearch.agency_hq_address,
        AgencySearch.agency_hq_city,
        AgencySearch.agency_hq_zip,
        AgencySearch.agency_jurisdiction,
        db.func.max(db.func.full_text.ts_rank(
            db.func.setweight(
                db.func.coalesce(
                    AgencySearch.tsv_agency_hq_address, ''), 'A')
            .concat(
                db.func.setweight(db.func.coalesce(
                    AgencySearch.tsv_agency_hq_city, ''), 'A'))
            .concat(
                db.func.setweight(db.func.coalesce(
                    AgencySearch.tsv_agency_hq_zip, ''), 'A')
                    ), db.func.to_tsquery(
                        search_term,
                        postgresql_regconfig='english'
                        )
        )).label('rank')
    ).filter(db.or_(
        AgencySearch.tsv_agency_hq_address.match(
            search_term,
            postgresql_regconfig='english'),
        AgencySearch.tsv_agency_hq_city.match(
            search_term,
            postgresql_regconfig='english'),
        AgencySearch.tsv_agency_hq_zip.match(
            search_term,
            postgresql_regconfig='english'),
    )).group_by(
        AgencySearch.agency_id,
        AgencySearch.agency_name,
        AgencySearch.agency_website_url,
        AgencySearch.agency_hq_address,
        AgencySearch.agency_hq_city,
        AgencySearch.agency_hq_zip,
        AgencySearch.agency_jurisdiction
    ).order_by(db.text('rank DESC')).all()

    # returning queried results and pagination
    results = []
    for search_result in query:
        result_dict = {
                "name" : search_result.agency_name,
                "url" : search_result.agency_website_url,
                "hq_address" : search_result.agency_hq_address,
                "hq_city" : search_result.agency_hq_city,
                "hq_zipcode" : search_result.agency_hq_zip,
                "jurisdiction" : search_result.agency_jurisdiction,
        }
        results.append(result_dict)
    start_index = (page - 1) * per_page
    end_index = min(start_index + per_page, len(results))
    paginated_results = results[start_index:end_index]
    response = {
                "page": page,
                "per_page": per_page,
                "total_results": len(results),
                "results": paginated_results
        }
    try:
        return jsonify(response)
    except Exception as e:
        return (500, str(e))
