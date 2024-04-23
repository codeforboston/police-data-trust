from sqlalchemy.sql.functions import GenericFunction
from ..database import SearchView, db


class TSRank(GenericFunction):
    package = 'full_text'
    name = 'ts_rank'
    inherit_cache = True


"""
TODO:
Convert search function to endpoint,
Pagination support,
API request:return specifications,
"""


def search(search_term):
    return db.session.query(
        db.distinct(SearchView.id),
        SearchView.officer_first_name,
        SearchView.officer_middle_name,
        SearchView.officer_last_name,
        SearchView.agency_name,
        db.func.max(db.func.full_text.ts_rank(
                db.func.setweight(db.func.coalesce(
                    SearchView.tsv_officer_first_name, ''), 'A').concat(
                    db.func.setweight(db.func.coalesce(
                        SearchView.tsv_officer_middle_name, ''), 'A')
                ).concat(
                    db.func.setweight(db.func.coalesce(
                        SearchView.tsv_officer_last_name, ''), 'A')
                ).concat(
                    db.func.setweight(db.func.coalesce(
                        SearchView.tsv_agency_name, ''), 'A')
                ), db.func.to_tsquery(search_term,
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
        SearchView.agency_name
    ).order_by(db.text('rank DESC')).all()
