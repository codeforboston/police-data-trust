from flask import abort
from backend.database.models.officer import Officer
from backend.database.models.source import Source
from backend.database.models.user import User
from backend.queries.officers import OfficerQueries
from backend.serializers.officer_serializer import (
    serialize_officer_sources,
    serialize_employment_history,
    serialize_allegation_summary,
    serialize_officer_profile,
    serialize_officer_list,
    serialize_officer_search_results,
)
from backend.schemas import add_pagination_wrapper
from backend.utils.citations import make_citation_diff


class OfficerService:
    def __init__(self):
        self.queries = OfficerQueries()
        self.METRIC_FETCHERS = {
            "allegation_types": self.queries.fetch_metric_a_types,
            "allegation_outcomes": self.queries.fetch_metric_a_outcomes,
            "complaint_history": self.queries.fetch_metric_comp_history,
            "complainant_demographics": self.queries.fetch_metric_comp_demo,
        }

    def _get_source_with_publish_access(
        self,
        source_uid: str | None,
        current_user: User,
        action: str,
    ) -> Source:
        if not source_uid:
            raise ValueError("source_uid is required")

        source = Source.nodes.get_or_none(uid=source_uid)
        if source is None:
            raise ValueError("Source not found")
        if not source.members.is_connected(current_user):
            raise PermissionError(
                f"User does not have permission to {action} "
                f"this officer for the provided source."
            )

        membership = source.members.relationship(current_user)
        if not membership.may_publish():
            raise PermissionError(
                f"User does not have permission to {action} "
                f"this officer for the provided source."
            )

        return source

    def create_officer(
        self,
        payload: dict,
        source_uid: str | None,
        current_user: User,
    ) -> dict:
        source = self._get_source_with_publish_access(
            source_uid=source_uid,
            current_user=current_user,
            action="create",
        )

        officer = Officer.from_dict(payload)

        created_values = {
            field: getattr(officer, field, None)
            for field in payload.keys()
            if getattr(officer, field, None) is not None
        }
        diff = make_citation_diff({}, created_values)
        if diff:
            officer.add_citation(
                source,
                current_user,
                diff,
            )

        return officer.to_dict()

    def update_officer(
        self,
        officer_uid: str,
        payload: dict,
        source_uid: str | None,
        current_user: User,
    ) -> dict:
        source = self._get_source_with_publish_access(
            source_uid=source_uid,
            current_user=current_user,
            action="update",
        )

        officer = Officer.nodes.get_or_none(uid=officer_uid)
        if officer is None:
            raise LookupError("Officer not found")

        old_values = {
            field: getattr(officer, field, None)
            for field in payload.keys()
        }

        officer = Officer.from_dict(payload, officer_uid)
        officer.refresh()

        new_values = {
            field: getattr(officer, field, None)
            for field in payload.keys()
        }
        diff = make_citation_diff(old_values, new_values)
        if diff:
            officer.add_citation(
                source,
                current_user,
                diff,
            )

        return officer.to_dict()

    def get_officer(self, officer_uid: str, includes: list[str]) -> dict:
        officer = Officer.nodes.get_or_none(uid=officer_uid)
        if officer is None:
            abort(404, description="Officer not found")

        sources = serialize_officer_sources(
            self.queries.fetch_sources(officer_uid)
        )

        employment_history = None
        allegation_summary = None

        if "employment" in includes:
            employment_history = serialize_employment_history(
                self.queries.fetch_emp_history(officer_uid)
            )

        if "allegations" in includes:
            allegation_summary = serialize_allegation_summary(
                self.queries.fetch_alleg_summary(officer_uid)
            )

        return serialize_officer_profile(
            officer=officer,
            sources=sources,
            employment_history=employment_history,
            allegation_summary=allegation_summary,
        )

    def list_officers(self, params):
        row_count = Officer.search(
            name=params.officer_name,
            rank=params.officer_rank,
            unit=params.unit,
            agency=params.agency,
            badge_number=params.badge_number,
            ethnicity=params.ethnicity,
            active_after=params.active_after,
            active_before=params.active_before,
            count=True,
        )

        if row_count == 0:
            return {
                "message": "No results found matching the query"}, 200, False

        if row_count <= params.skip:
            return {
                "message": "Page number exceeds total results"}, 400, False

        results = Officer.search(
            name=params.officer_name,
            rank=params.officer_rank,
            unit=params.unit,
            agency=params.agency,
            badge_number=params.badge_number,
            ethnicity=params.ethnicity,
            active_after=params.active_after,
            active_before=params.active_before,
            skip=params.skip,
            limit=params.limit,
            inflate=not params.searchResult,
        )

        if params.searchResult:
            page = serialize_officer_search_results(results)
            use_ordered = False
        else:
            page = serialize_officer_list(results)
            use_ordered = True

        response = add_pagination_wrapper(
            page_data=page,
            total=row_count,
            page_number=params.page,
            per_page=params.per_page,
        )
        return response, 200, use_ordered

    def get_officer_employment(self, officer_uid: str) -> list[dict]:
        officer = Officer.nodes.get_or_none(uid=officer_uid)
        if officer is None:
            abort(404, description="Officer not found")

        employment_history = serialize_employment_history(
            self.queries.fetch_emp_history(officer_uid)
        )
        response = {
            "officer_uid": officer_uid,
            "employment_history": employment_history,
            "total_records": len(employment_history)
        }
        return response

    def get_officer_metrics(
            self, officer_uid: str, includes: list[str]) -> dict:
        officer = Officer.nodes.get_or_none(uid=officer_uid)
        if officer is None:
            abort(404, description="Officer not found")

        if not includes:
            abort(400, description="Include parameter is required.")

        response = {"officer_uid": officer_uid}

        for include in includes:
            fetcher = self.METRIC_FETCHERS.get(include)
            if not fetcher:
                continue
            response[include] = fetcher(officer_uid)

        return response
