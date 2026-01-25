import logging
# from typing import Optional, List
from backend.auth.jwt import min_role_required
from backend.schemas import (
    validate_request, add_pagination_wrapper, ordered_jsonify, paginate_results,
    NodeConflictException)
from backend.mixpanel.mix import track_to_mp
from backend.database.models.user import UserRole
from backend.database.models.agency import Agency
from backend.routes.search import fetch_details, build_agency_result
from flask import Blueprint, abort, request, jsonify
from flask_jwt_extended.view_decorators import jwt_required
from neomodel import db
from backend.dto.agency import (
    AgencyQueryParams, GetAgencyParams, CreateAgency, UpdateAgency)

bp = Blueprint("agencies_routes", __name__, url_prefix="/api/v1/agencies")

UNIT_CYPHER = """
CALL (a) {
  OPTIONAL MATCH (a:Agency)-[]-(u:Unit)
  RETURN count(DISTINCT u) AS total_units
}
"""

OFFICER_CYPHER = """
CALL (a) {
  OPTIONAL MATCH (a)-[]-(:Unit)<-[]-(:Employment)-[]->(o:Officer)
  WITH count(DISTINCT o) AS total_officers
  RETURN total_officers
}
"""

COMPLAINT_CYPHER = """
CALL (a) {
  OPTIONAL MATCH (a)-[]-(:Unit)<-[]-(:Employment)-[]->(:Officer)
      -[:ACCUSED_OF]->(:Allegation)-[:ALLEGED]-(c:Complaint)
  WITH count(c) AS total_complaints
  RETURN total_complaints
}
"""

ALLEGATION_CYPHER = """
CALL (a) {
  OPTIONAL MATCH (a)-[]-(:Unit)<-[]-(:Employment)
  -[]->(:Officer)-[:ACCUSED_OF]->(allege:Allegation)
  MATCH (allege)-[:ALLEGED]-(c:Complaint)
  WITH
  CASE
      WHEN allege.type IS NULL OR trim(allege.type) = "" THEN "Unknown"
      ELSE allege.type
  END AS type,
  count(*) AS occurrences,
  sum(CASE WHEN toLower(
      trim(coalesce(allege.finding,""))) = "substantiated" THEN 1 ELSE 0 END)
      AS substantiated_count,
  min(c.incident_date) AS earliest_incident_date,
  max(c.incident_date) AS latest_incident_date
  ORDER BY occurrences DESC, type ASC
  RETURN {
      type: type,
      occurrences: occurrences,
      substantiated_count: substantiated_count,
      earliest_incident_date: earliest_incident_date,
      latest_incident_date: latest_incident_date
  } AS type_summary
}
"""


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
    match_clause = "MATCH (a:Agency {uid: $agency_uid})"
    return_clause = "RETURN a"
    subqueries = ""
    if params.include:
        if "units" in params.include:
            subqueries += UNIT_CYPHER
            return_clause += ", total_units"
        if "officers" in params.include:
            subqueries += OFFICER_CYPHER
            return_clause += ", total_officers"
        if "complaints" in params.include:
            subqueries += COMPLAINT_CYPHER
            return_clause += ", total_complaints"
        if "allegations" in params.include:
            subqueries += ALLEGATION_CYPHER
            return_clause += ", collect(type_summary) AS allegation_summary"
    cy = match_clause + subqueries + return_clause

    rows, _ = db.cypher_query(cy, {"agency_uid": agency_uid})
    if not rows:
        abort(404, description="Agency not found")
    row = rows[0]
    agency_data = row[0]._properties
    if params.include:
        idx = 1
        if "units" in params.include:
            agency_data["total_units"] = row[idx]
            idx += 1
        if "officers" in params.include:
            agency_data["total_officers"] = row[idx]
            idx += 1
        if "complaints" in params.include:
            agency_data["total_complaints"] = row[idx]
            idx += 1
        if "allegations" in params.include:
            agency_data["allegation_summary"] = row[idx]
            idx += 1
    return ordered_jsonify(agency_data)


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


# # Add officer employment information
# @bp.route("/<int:agency_id>/officers", methods=["POST"])
# @jwt_required()
# @min_role_required(UserRole.CONTRIBUTOR)
# @validate(json=AddOfficerListSchema)
# def add_officer_to_agency(agency_id: int):
#     """Add any number of officer employment records to an agency.
#     Must be a Contributor to add officers to an agency.
#     """
#     agency = Agency.nodes.get_or_none(uid=agency_id)
#     if agency is None:
#         abort(404, description="Agency not found")

#     records = request.context.json.officers

#     created = []
#     failed = []
#     for record in records:
#         try:
#             officer = db.session.query(Officer).get(
#                 record.officer_id)
#             if officer is None:
#                 failed.append({
#                     "officer_id": record.officer_id,
#                     "reason": "Officer not found"
#                 })
#             else:
#                 employments = db.session.query(Employment).filter(
#                     and_(
#                         and_(
#                             Employment.officer_id == record.officer_id,
#                             Employment.agency_id == agency_id
#                         ),
#                         Employment.badge_number == record.badge_number
#                     )
#                 )
#                 if employments is not None:
#                     # If the officer already has a records for this agency,
#                     # we need to update the earliest and
#                     # latest employment dates
#                     employment = employment_to_orm(record)
#                     employment.agency_id = agency_id
#                     employment = merge_employment_records(
#                         employments.all() + [employment],
#                         currently_employed=record.currently_employed
#                     )

#                     # Delete the old records and replace them with the new one
#                     employments.delete()
#                     created.append(employment.create())
#                 else:
#                     record.agency_id = agency_id
#                     employment = employment_to_orm(record)
#                     created.append(employment.create())
#         except Exception as e:
#             failed.append({
#                 "officer_id": record.officer_id,
#                 "reason": str(e)
#             })
#     try:
#         track_to_mp(
#             request,
#             "add_officers_to_agency",
#             {
#                 "agency_id": agency.id,
#                 "officers_added": len(created),
#                 "officers_failed": len(failed)
#             },
#         )
#         return {
#             "created": [
#                 employment_orm_to_json(item) for item in created],
#             "failed": failed,
#             "totalCreated": len(created),
#             "totalFailed": len(failed),
#         }
#     except Exception as e:
#         abort(400, description=str(e))


# Get agency officers
@bp.route("/<agency_id>/officers", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def get_agency_officers(agency_id):
    """Get all officers for an agency.
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    try:
        query = f"""
                MATCH (a:Agency)-[]-(u:Unit)-[]-(:Employment)-[]-(o:Officer)
                WHERE a.uid='{agency_id}'
                RETURN o
                """
        res, meta = db.cypher_query(query, resolve_objects=True)
        officers = [record[0] for record in res]

        result = paginate_results(officers, q_page, q_per_page)
        return ordered_jsonify(result), 200

    except Exception as e:
        abort(400, description=str(e))
