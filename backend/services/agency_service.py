import logging
import json

from backend.database.models.agency import Agency
from backend.database.models.source import Source
from backend.database.models.user import User
from backend.queries.agencies import AgencyQueries
from backend.schemas import add_pagination_wrapper
from backend.serializers.agency_serializer import (
    serialize_agency_profile
)
from backend.serializers.officer_serializer import serialize_officer_rows


class AgencyService:
    def __init__(self):
        self.queries = AgencyQueries()

    def get_agency_profile(self, agency_uid: str, includes: list[str]) -> dict:
        result = self.queries.fetch_agency_profile(agency_uid, includes)
        logging.debug(f"Fetched agency profile result: {result}")
        if result is None:
            raise ValueError("Agency not found")

        return serialize_agency_profile(result, includes)

    def update_agency(
        self,
        agency_uid: str,
        payload: dict,
        source_uid: str | None,
        current_user: User,
    ) -> dict:
        if not source_uid:
            raise ValueError("source_uid is required")

        source = Source.nodes.get_or_none(uid=source_uid)
        if source is None:
            raise ValueError("Source not found")
        if not source.members.is_connected(current_user):
            raise PermissionError(
                "User does not have permission to update this agency for the provided source."
            )

        membership = source.members.relationship(current_user)
        if not membership.may_publish():
            raise PermissionError(
                "User does not have permission to update this agency for the provided source."
            )

        agency = Agency.nodes.get_or_none(uid=agency_uid)
        if agency is None:
            raise LookupError("Agency not found")

        relink_location = bool({"hq_city", "hq_state"} & set(payload.keys()))
        old_values = {
            field: getattr(agency, field, None)
            for field in payload.keys()
        }

        agency = Agency.from_dict(payload, agency_uid)
        agency.refresh()

        location_linked = bool(agency.city_node.all())
        if relink_location:
            agency.city_node.disconnect_all()
            location_linked = Agency.link_location(
                agency,
                state=agency.hq_state,
                city=agency.hq_city,
            )

        changed_fields = {
            field: {
                "old": old_values[field],
                "new": getattr(agency, field, None),
            }
            for field in payload.keys()
            if old_values[field] != getattr(agency, field, None)
        }
        if changed_fields:
            agency.add_citation(
                source,
                current_user,
                json.dumps(changed_fields),
            )

        response = agency.to_dict()
        response["location_linked"] = location_linked
        return response

    def list_agency_officers(
        self,
        agency_uid: str,
        page: int,
        per_page: int,
        includes: list[str],
        filters: dict | None = None,
        term: str | None = None,
    ) -> dict:
        agency = Agency.nodes.get_or_none(uid=agency_uid)
        if not agency:
            raise ValueError("Agency not found")

        include_employment = "employment" in includes
        total = self.queries.count_agency_officers(agency_uid, term, filters)

        if total == 0:
            return {
                "message": "No officers found for this agency"
            }

        skip = (page - 1) * per_page
        if total <= skip:
            raise IndexError("Page number exceeds total results")

        rows = self.queries.fetch_agency_officers(
            agency_uid=agency_uid,
            skip=skip,
            limit=per_page,
            include_employment=include_employment,
            filters=filters,
            term=term,
        )

        officers = serialize_officer_rows(
            rows,
            include_employment=include_employment,
        )

        return add_pagination_wrapper(
            page_data=officers,
            total=total,
            page_number=page,
            per_page=per_page,
        )

    def list_agency_units(
        self,
        agency_uid: str,
        page: int,
        per_page: int,
        includes: list[str],
    ) -> dict:
        agency = Agency.nodes.get_or_none(uid=agency_uid)
        if not agency:
            raise ValueError("Agency not found")

        total = self.queries.count_agency_units(agency_uid)

        if total == 0:
            return {
                "message": "No units found for this agency"
            }

        skip = (page - 1) * per_page
        if total <= skip:
            raise IndexError("Page number exceeds total results")

        rows = self.queries.fetch_agency_units(
            agency_uid=agency_uid,
            skip=skip,
            limit=per_page,
        )

        units = [row[0].to_dict(include_relationships=False) for row in rows]

        return add_pagination_wrapper(
            page_data=units,
            total=total,
            page_number=page,
            per_page=per_page,
        )
