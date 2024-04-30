from sqlalchemy.sql.functions import GenericFunction
from ..database import SearchView, db
from flask import Blueprint, jsonify, request
from flask_jwt_extended.view_decorators import jwt_required


class TSRank(GenericFunction):
    package = 'full_text'
    name = 'ts_rank'
    inherit_cache = True


bp = Blueprint("search_route", __name__, url_prefix="/api/v1/search")
"""
TODO:
Convert search function to endpoint,
Pagination support,
API request:return specifications,
"""


DEFAULT_PER_PAGE = 5


@bp.route("/", methods=["POST"])
@jwt_required()
def search():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', DEFAULT_PER_PAGE))
    search_term = request.args.get('search_term')
    query = db.session.query(
        db.distinct(SearchView.id),
        SearchView.officer_first_name,
        SearchView.officer_middle_name,
        SearchView.officer_last_name,
        SearchView.agency_name,
        SearchView.agency_hq_city,
        SearchView.agency_jurisdiction,
        db.func.max(db.func.full_text.ts_rank(
            db.func.setweight(
                db.func.coalesce(
                    SearchView.tsv_officer_first_name, ''), 'A')
            .concat(
                db.func.setweight(db.func.coalesce(
                    SearchView.tsv_officer_middle_name, ''), 'A'))
            .concat(
                db.func.setweight(db.func.coalesce(
                    SearchView.tsv_officer_last_name, ''), 'A'))
            .concat(
                db.func.setweight(db.func.coalesce(
                    SearchView.tsv_agency_name, ''), 'A')), db.func.to_tsquery(
                        search_term,
                        postgresql_regconfig='english')
        )).label('rank')
    ).filter(db.or_(
        SearchView.tsv_officer_first_name.match(
            search_term,
            postgresql_regconfig='english'),
        SearchView.tsv_officer_last_name.match(
            search_term,
            postgresql_regconfig='english'),
        SearchView.tsv_officer_middle_name.match(
            search_term,
            postgresql_regconfig='english'),
        SearchView.tsv_agency_name.match(
            search_term,
            postgresql_regconfig='english')
    )).group_by(
        SearchView.id,
        SearchView.officer_first_name,
        SearchView.officer_middle_name,
        SearchView.officer_last_name,
        SearchView.agency_name,
        SearchView.agency_hq_city,
        SearchView.agency_jurisdiction
    ).order_by(db.text('rank DESC')).all()
    results = []
    for search_result in query:
        if search_result.agency_name is None:
            result_dict = {
                "first_name" : search_result.officer_first_name,
                "middle_name" : search_result.officer_middle_name,
                "last_name" : search_result.officer_last_name,
                }
        elif search_result.first_name is None:
            result_dict = {
                "agency_name" : search_result.agency_name ,
                "agency_hq_city" : search_result.agency_hq_city,
                "agency_jurisdiction" : search_result.agency_jurisdiction
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
