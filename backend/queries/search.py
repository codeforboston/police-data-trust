import re

from neomodel import db

LUCENE_RESERVED_PATTERN = re.compile(r'[+\-!(){}\[\]^"~*?:\\/|&]+')
LUCENE_BOOLEAN_OPERATORS = {"AND", "OR", "NOT"}

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
        size($source_uids) = 0 OR EXISTS {
            MATCH (node)-[:UPDATED_BY]->(source:Source)
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
        size($source_uids) = 0 OR EXISTS {
            MATCH (node)-[:UPDATED_BY]->(source:Source)
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
        size($source_uids) = 0 OR EXISTS {
            MATCH (node)-[:UPDATED_BY]->(source:Source)
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


SEARCH_RESULTS_QUERY = SEARCH_BASE_QUERY + """
WITH node, score,
CASE
    WHEN 'Officer' IN labels(node) THEN trim(
        coalesce(node.first_name, '') + ' ' +
        coalesce(node.middle_name, '') + ' ' +
        coalesce(node.last_name, '') + ' ' +
        coalesce(node.suffix, '')
    )
    ELSE coalesce(node.name, '')
END AS display_name
RETURN node, score
ORDER BY
CASE
    WHEN toLower(display_name) = $raw_query_normalized THEN 0
    WHEN toLower(display_name) STARTS WITH $raw_query_normalized THEN 1
    WHEN size($query_terms) > 0
        AND all(term IN $query_terms WHERE toLower(display_name) CONTAINS term)
        THEN 2
    ELSE 3
END ASC,
score DESC,
node.uid ASC
SKIP $per_page * ($page - 1)
LIMIT $per_page
"""

SEARCH_DETAILS_QUERY = """
CALL () {
    UNWIND $officer_uids AS uid
    MATCH (o:Officer {uid: uid})
    OPTIONAL MATCH (o)-[:ACCUSED_OF]->(al:Allegation)-[:ALLEGED]->(co:Complaint)
    WITH
        uid,
        o,
        count(DISTINCT co) AS complaint_count,
        count(DISTINCT al) AS allegation_count,
        sum(
            CASE
                WHEN toLower(trim(coalesce(al.finding, ""))) = "substantiated"
                THEN 1 ELSE 0
            END
        ) AS substantiated_count

    CALL (o) {
        OPTIONAL MATCH (o)<-[]-(e:Employment)-[]-(u:Unit)-[]-(ag:Agency)
        WITH e, u, ag,
             CASE WHEN e.latest_date IS NULL THEN 1 ELSE 0 END AS is_current
        ORDER BY is_current DESC, e.earliest_date DESC
        RETURN e, u, ag
        LIMIT 1
    }

    CALL (o) {
        OPTIONAL MATCH (o)-[r:UPDATED_BY]->(s:Source)
        RETURN s, r
        ORDER BY r.timestamp DESC
        LIMIT 1
    }

    RETURN "Officer" AS content_type, uid, {
        complaints: complaint_count,
        allegations: allegation_count,
        substantiated: substantiated_count,
        rank: e.highest_rank,
        unit_name: u.name,
        agency_name: ag.name,
        source: s.name,
        last_updated: r.timestamp
    } AS result

    UNION ALL

    UNWIND $agency_uids AS uid
    MATCH (a:Agency {uid: uid})
    OPTIONAL MATCH (a)-[]-(u:Unit)
    OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(o:Officer)
    OPTIONAL MATCH (o)-[]-(:Allegation)-[]-(c:Complaint)

    WITH
        a,
        uid,
        count(DISTINCT u) AS units,
        count(DISTINCT o) AS officers,
        count(DISTINCT c) AS complaints

    CALL (a) {
        OPTIONAL MATCH (a)-[r:UPDATED_BY]->(s:Source)
        RETURN s, r
        ORDER BY r.timestamp DESC
        LIMIT 1
    }

    RETURN "Agency" AS content_type, uid, {
        units: units,
        officers: officers,
        complaints: complaints,
        source: s.name,
        last_updated: r.timestamp
    } AS result

    UNION ALL

    UNWIND $unit_uids AS uid
    MATCH (u:Unit {uid: uid})
    OPTIONAL MATCH (u)-[]-(a:Agency)
    OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(o:Officer)
    OPTIONAL MATCH (o)-[]-(:Allegation)-[]-(c:Complaint)

    WITH
        uid,
        u,
        a,
        count(DISTINCT o) AS officers,
        count(DISTINCT c) AS complaints

    CALL (u) {
        OPTIONAL MATCH (u)-[r:UPDATED_BY]->(s:Source)
        RETURN s, r
        ORDER BY r.timestamp DESC
        LIMIT 1
    }

    RETURN "Unit" AS content_type, uid, {
        name: u.name,
        agency_name: a.name,
        officers: officers,
        complaints: complaints,
        source: s.name,
        last_updated: r.timestamp
    } AS result
}
RETURN content_type, uid, result
"""


class SearchQueries:
    def _as_list(self, value: str | list[str] | None) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    def tokenize_query(self, raw_query: str) -> list[str]:
        sanitized = LUCENE_RESERVED_PATTERN.sub(" ", raw_query)
        tokens = []
        for term in sanitized.split():
            if term.upper() in LUCENE_BOOLEAN_OPERATORS:
                continue
            tokens.append(term.lower())

        return tokens

    def build_fulltext_query(self, raw_query: str) -> str:
        terms = [f"{term}*" for term in self.tokenize_query(raw_query)]

        if not terms:
            raise ValueError("Query parameter is required")

        return " ".join(terms)

    def build_search_params(
        self,
        *,
        query: str,
        page: int,
        per_page: int,
        city_uids: list[str] | None = None,
        source_uids: list[str] | None = None,
    ) -> dict:
        query_terms = self.tokenize_query(query)
        return {
            "query": self.build_fulltext_query(query),
            "raw_query_normalized": " ".join(query_terms),
            "query_terms": query_terms,
            "city_uids": city_uids or [],
            "source_uids": source_uids or [],
            "page": page,
            "per_page": per_page,
        }

    def resolve_search_city_uids(
        self,
        *,
        city: str | None = None,
        state: str | None = None,
    ) -> list[str]:
        if not city and not state:
            return []

        if city and state:
            query = """
            MATCH (city:CityNode)-[:WITHIN_COUNTY]->(:CountyNode)-[:WITHIN_STATE]
                ->(state:StateNode {abbreviation: $state})
            WHERE toLower(city.name) = toLower($city)
            RETURN DISTINCT city.uid
            """
            params = {"city": city, "state": state}
        elif city:
            query = """
            MATCH (city:CityNode)
            WHERE toLower(city.name) = toLower($city)
            RETURN DISTINCT city.uid
            """
            params = {"city": city}
        else:
            query = """
            MATCH (city:CityNode)-[:WITHIN_COUNTY]->(:CountyNode)-[:WITHIN_STATE]
                ->(state:StateNode {abbreviation: $state})
            RETURN DISTINCT city.uid
            """
            params = {"state": state}

        rows, _ = db.cypher_query(query, params)
        return [row[0] for row in rows]

    def resolve_search_source_uids(
        self,
        *,
        source: str | list[str] | None = None,
        source_uid: str | list[str] | None = None,
    ) -> list[str]:
        source_uid_values = self._as_list(source_uid)
        source_name_values = self._as_list(source)

        resolved_uids: list[str] = []

        if source_uid_values:
            query = """
            MATCH (s:Source)
            WHERE s.uid IN $source_uids
            RETURN DISTINCT s.uid
            """
            rows, _ = db.cypher_query(query, {"source_uids": source_uid_values})
            resolved_uids.extend(row[0] for row in rows)

        if source_name_values:
            query = """
            MATCH (s:Source)
            WHERE toLower(s.name) IN $source_names
            RETURN DISTINCT s.uid
            """
            rows, _ = db.cypher_query(
                query,
                {"source_names": [value.lower() for value in source_name_values]},
            )
            resolved_uids.extend(row[0] for row in rows)

        return list(dict.fromkeys(resolved_uids))

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
