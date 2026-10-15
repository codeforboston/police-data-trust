from neomodel import db
from backend.queries.filter_resolver import FilterResolver
from backend.queries.text_search import (
    NAME_RANK_ORDER,
    build_prefix_query,
    name_rank_clauses,
    tokenize,
)

SEARCH_BASE_QUERY = """
CALL () {
    CALL db.index.fulltext.queryNodes('officerNames',$query)  YIELD node, score
    WHERE (
        size($city_uids) = 0 OR EXISTS {
            MATCH (node)<-[]-(:Employment)-[]->(:Unit)-[]-(:Agency)-
            [:LOCATED_IN]->(city:CityNode)
            WHERE city.uid IN $city_uids
        }
    )
    AND (
        size($source_uids) = 0
        OR EXISTS {
            MATCH (node)<-[:CHANGE_TO]-(:Change)-[:ATTRIBUTED_TO]->
            (source:Source)
            WHERE source.uid IN $source_uids
        }
    )
    RETURN node, score
    UNION ALL
    CALL db.index.fulltext.queryNodes('agencyNames',$query)   YIELD node, score
    WHERE (
        size($city_uids) = 0 OR EXISTS {
            MATCH (node)-[:LOCATED_IN]->(city:CityNode)
            WHERE city.uid IN $city_uids
        }
    )
    AND (
        size($source_uids) = 0
        OR EXISTS {
            MATCH (node)<-[:CHANGE_TO]-(:Change)-[:ATTRIBUTED_TO]->
            (source:Source)
            WHERE source.uid IN $source_uids
        }
    )
    RETURN node, score
    UNION ALL
    CALL db.index.fulltext.queryNodes('unitNames',$query)     YIELD node, score
    WHERE (
        size($city_uids) = 0 OR EXISTS {
            MATCH (node)-[:LOCATED_IN]->(city:CityNode)
            WHERE city.uid IN $city_uids
        }
    )
    AND (
        size($source_uids) = 0
        OR EXISTS {
            MATCH (node)<-[:CHANGE_TO]-(:Change)-[:ATTRIBUTED_TO]->
            (source:Source)
            WHERE source.uid IN $source_uids
        }
    )
    RETURN node, score
}
WITH node, max(score) AS score
"""


SEARCH_COUNT_QUERY = SEARCH_BASE_QUERY + """
RETURN count(node) AS totalMatches
"""


SEARCH_RESULTS_QUERY = (
    SEARCH_BASE_QUERY
    + name_rank_clauses("node", "node, score", words="$query_terms")
    + f"""
RETURN node, score
ORDER BY {NAME_RANK_ORDER}, node.uid ASC
SKIP $per_page * ($page - 1)
LIMIT $per_page
"""
)

SEARCH_DETAILS_QUERY = """
CALL () {
    UNWIND $officer_uids AS uid
    MATCH (o:Officer {uid: uid})

    CALL (o) {
        OPTIONAL MATCH (o)<-[]-(e:Employment)-[]-(u:Unit)-[]-(ag:Agency)
        WITH e, u, ag,
             CASE WHEN e.latest_date IS NULL THEN 1 ELSE 0 END AS is_current
        ORDER BY is_current DESC, e.earliest_date DESC
        RETURN e, u, ag
        LIMIT 1
    }

    CALL (o) {
        OPTIONAL MATCH (o)<-[:CHANGE_TO]-(c:Change)-[:ATTRIBUTED_TO]->
        (s:Source)
        RETURN s, c.timestamp AS updated_at
        ORDER BY updated_at DESC
        LIMIT 1
    }

    RETURN "Officer" AS content_type, uid, {
        complaints: coalesce(o.complaint_count_cached, 0),
        allegations: coalesce(o.allegation_count_cached, 0),
        substantiated: coalesce(o.substantiated_count_cached, 0),
        rank: e.highest_rank,
        unit_name: u.name,
        agency_name: ag.name,
        source: s.name,
        last_updated: updated_at
    } AS result

    UNION ALL

    UNWIND $agency_uids AS uid
    MATCH (a:Agency {uid: uid})

    CALL (a) {
        OPTIONAL MATCH (a)<-[:CHANGE_TO]-(c:Change)-[:ATTRIBUTED_TO]->
        (s:Source)
        RETURN s, c.timestamp AS updated_at
        ORDER BY updated_at DESC
        LIMIT 1
    }

    RETURN "Agency" AS content_type, uid, {
        units: coalesce(a.unit_count_cached, 0),
        officers: coalesce(a.officer_count_cached, 0),
        complaints: coalesce(a.complaint_count_cached, 0),
        source: s.name,
        last_updated: updated_at
    } AS result

    UNION ALL

    UNWIND $unit_uids AS uid
    MATCH (u:Unit {uid: uid})
    OPTIONAL MATCH (u)-[]-(a:Agency)

    CALL (u) {
        OPTIONAL MATCH (u)<-[:CHANGE_TO]-(c:Change)-[:ATTRIBUTED_TO]->
        (s:Source)
        RETURN s, c.timestamp AS updated_at
        ORDER BY updated_at DESC
        LIMIT 1
    }

    RETURN "Unit" AS content_type, uid, {
        name: u.name,
        agency_name: a.name,
        officers: coalesce(u.officer_count_cached, 0),
        complaints: coalesce(u.complaint_count_cached, 0),
        source: s.name,
        last_updated: updated_at
    } AS result
}
RETURN content_type, uid, result
"""


class SearchQueries:
    def __init__(self, filter_resolver: FilterResolver | None = None):
        self.filter_resolver = filter_resolver or FilterResolver()

    def tokenize_query(self, raw_query: str) -> list[str]:
        return tokenize(raw_query)

    def build_fulltext_query(self, raw_query: str) -> str:
        return build_prefix_query(raw_query)

    def build_search_params(
        self,
        *,
        query: str,
        page: int,
        per_page: int,
        city_uids: list[str] | None = None,
        source_uids: list[str] | None = None,
    ) -> dict:
        return {
            "query": self.build_fulltext_query(query),
            "query_terms": self.tokenize_query(query),
            "city_uids": city_uids or [],
            "source_uids": source_uids or [],
            "page": page,
            "per_page": per_page,
        }

    def resolve_search_city_uids(
        self,
        *,
        city: str | list[str] | None = None,
        city_uid: str | list[str] | None = None,
        state: str | list[str] | None = None,
    ) -> list[str]:
        return self.filter_resolver.resolve_city_uids(
            city=city,
            city_uid=city_uid,
            state=state,
        )

    def resolve_search_source_uids(
        self,
        *,
        source: str | list[str] | None = None,
        source_uid: str | list[str] | None = None,
    ) -> list[str]:
        return self.filter_resolver.resolve_source_uids(
            source=source,
            source_uid=source_uid,
        )

    def count_search_results(
        self,
        *,
        query: str,
        page: int,
        per_page: int,
        city_uids: list[str] | None = None,
        source_uids: list[str] | None = None,
    ) -> int:
        params = self.build_search_params(
            query=query,
            page=page,
            per_page=per_page,
            city_uids=city_uids,
            source_uids=source_uids,
        )
        rows, _ = db.cypher_query(SEARCH_COUNT_QUERY, params)
        return rows[0][0] if rows else 0

    def fetch_search_results(
        self,
        *,
        query: str,
        page: int,
        per_page: int,
        city_uids: list[str] | None = None,
        source_uids: list[str] | None = None,
    ):
        params = self.build_search_params(
            query=query,
            page=page,
            per_page=per_page,
            city_uids=city_uids,
            source_uids=source_uids,
        )
        rows, _ = db.cypher_query(SEARCH_RESULTS_QUERY, params)
        return rows

    def fetch_search_details(
        self,
        *,
        officer_uids: list[str],
        agency_uids: list[str],
        unit_uids: list[str],
    ) -> dict[str, dict[str, dict]]:
        params = {
            "officer_uids": officer_uids,
            "agency_uids": agency_uids,
            "unit_uids": unit_uids,
        }
        rows, _ = db.cypher_query(SEARCH_DETAILS_QUERY, params)

        details = {
            "Officer": {},
            "Agency": {},
            "Unit": {},
        }
        for content_type, uid, row in rows:
            details.setdefault(content_type, {})[uid] = row or {}

        return details
