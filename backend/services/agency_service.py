import logging

from backend.database.models.agency import Agency
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
