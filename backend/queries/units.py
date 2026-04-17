import logging

from backend.database import db

UNIT_BASE_MATCH = """
MATCH (u:Unit {uid: $uid})-[]-(a:Agency)
"""

OFFICER_COUNT_SUBQUERY = """
CALL (u) {
  RETURN coalesce(u.officer_count_cached, 0) AS total_officers
}
"""

COMPLAINT_SUBQUERY = """
CALL (u) {
  RETURN
    coalesce(u.complaint_count_cached, 0) AS total_complaints,
    coalesce(u.allegation_count_cached, 0) AS total_allegations
}
"""

ALLEGATION_SUBQUERY = """
CALL (u) {
  OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(:Officer)
      -[:ACCUSED_OF]->(allege:Allegation)
  MATCH (allege)-[:ALLEGED]-(c:Complaint)
  WITH
    CASE
      WHEN allege.type IS NULL OR trim(allege.type) = "" THEN "Unknown"
      ELSE allege.type
    END AS type,
    count(*) AS occurrences,
    sum(
      CASE
        WHEN toLower(trim(coalesce(allege.finding, ""))) = "substantiated"
        THEN 1 ELSE 0
      END
    ) AS substantiated_count,
    min(c.incident_date) AS earliest_incident_date,
    max(c.incident_date) AS latest_incident_date
  ORDER BY occurrences DESC, type ASC
  RETURN collect({
    type: type,
    occurrences: occurrences,
    substantiated_count: substantiated_count,
    earliest_incident_date: earliest_incident_date,
    latest_incident_date: latest_incident_date
  }) AS allegation_summary
}
"""

REPORTED_OFFICER_SUBQUERY = """
CALL (u) {
  MATCH (u)<-[]-(:Employment)-[]->(o:Officer)
    -[:ACCUSED_OF]->(allege:Allegation)-[:ALLEGED]-(c:Complaint)
  WITH
    o,
    count(DISTINCT c) AS complaint_count,
    count(DISTINCT allege) AS allegation_count
  ORDER BY complaint_count DESC, allegation_count DESC
  LIMIT 3
  RETURN collect(o) AS most_reported_officers
}
"""

LOCATION_SUBQUERY = """
CALL (u) {
  OPTIONAL MATCH (u)-[]-(:Agency)-[]-(city:CityNode)
    -[]-(:CountyNode)-[]-(state:StateNode)
  RETURN {
    coords: city.coordinates,
    city: city.name,
    state: state.name
  } AS location
}
"""


class UnitQueries:
    INCLUDE_SPECS = {
        "officers": {
            "subquery": OFFICER_COUNT_SUBQUERY,
            "return_fields": ["total_officers"],
        },
        "complaints": {
            "subquery": COMPLAINT_SUBQUERY,
            "return_fields": ["total_complaints", "total_allegations"],
        },
        "allegations": {
            "subquery": ALLEGATION_SUBQUERY,
            "return_fields": ["allegation_summary"],
        },
        "reported_officers": {
            "subquery": REPORTED_OFFICER_SUBQUERY,
            "return_fields": ["most_reported_officers"],
        },
        "location": {
            "subquery": LOCATION_SUBQUERY,
            "return_fields": ["location"],
        }
    }

    def _normalize_officer_filters(self, filters: dict | None) -> dict:
        filters = filters or {}
        return {
            "ranks": filters.get("rank") or [],
            "statuses": filters.get("status") or [],
            "types": filters.get("type") or [],
        }

    def _classify_officer_term(self, term: str | None) -> str:
        if not term or not term.strip():
            return "none"

        t = term.strip()

        has_space = " " in t
        has_alpha = any(c.isalpha() for c in t)
        has_digit = any(c.isdigit() for c in t)

        if has_digit and not has_alpha and not has_space:
            return "badge"

        if has_alpha and not has_digit:
            return "name"

        return "ambiguous"

    def _build_officer_search_query(
        self,
        unit_uid: str,
        term: str | None = None,
        filters: dict | None = None,
    ) -> tuple[str, dict]:
        normalized = self._normalize_officer_filters(filters)
        strategy = self._classify_officer_term(term)

        params = {
            "unit_uid": unit_uid,
            "term": term.strip() if term else None,
            **normalized,
        }

        if strategy == "none":
            cypher = """
            MATCH (u:Unit {uid: $unit_uid})<-[:IN_UNIT]-(e:Employment)
            -[:HELD_BY]->(o:Officer)
            WHERE (coalesce($ranks, []) = [] OR e.highest_rank IN $ranks)
            AND (coalesce($statuses, []) = [] OR e.status IN $statuses)
            AND (coalesce($types, []) = [] OR e.type IN $types)
            WITH o, e, u, 0.0 AS score
            """
            return cypher, params

        if strategy == "name":
            cypher = """
            CALL () {
                CALL db.index.fulltext.queryNodes("officerNames", $term)
                YIELD node, score
                RETURN node AS o, score
            }
            MATCH (o)<-[:HELD_BY]-(e:Employment)-[:IN_UNIT]->(u:Unit)
            WHERE u.uid = $unit_uid
            AND (coalesce($ranks, []) = [] OR e.highest_rank IN $ranks)
            AND (coalesce($statuses, []) = [] OR e.status IN $statuses)
            AND (coalesce($types, []) = [] OR e.type IN $types)
            WITH o, e, u, score
            """
            return cypher, params

        if strategy == "badge":
            cypher = """
            CALL () {
                CALL db.index.fulltext.queryNodes("officerBadgeNumbers", $term)
                YIELD node, score
                RETURN node AS e, score
            }
            MATCH (e)-[:HELD_BY]->(o:Officer)
            MATCH (e)-[:IN_UNIT]->(u:Unit)
            WHERE u.uid = $unit_uid
            AND (coalesce($ranks, []) = [] OR e.highest_rank IN $ranks)
            AND (coalesce($statuses, []) = [] OR e.status IN $statuses)
            AND (coalesce($types, []) = [] OR e.type IN $types)
            WITH o, e, u, score
            """
            return cypher, params

        cypher = """
        CALL () {
            CALL db.index.fulltext.queryNodes("officerNames", $term)
            YIELD node, score
            RETURN node AS o, null AS e, score

            UNION

            CALL db.index.fulltext.queryNodes("officerBadgeNumbers", $term)
            YIELD node, score
            MATCH (node)-[:HELD_BY]->(o:Officer)
            RETURN o, node AS e, score
        }
        MATCH (o)<-[:HELD_BY]-(all_e:Employment)-[:IN_UNIT]->(u:Unit)
        WHERE u.uid = $unit_uid
        AND (coalesce($ranks, []) = [] OR all_e.highest_rank IN $ranks)
        AND (coalesce($statuses, []) = [] OR all_e.status IN $statuses)
        AND (coalesce($types, []) = [] OR all_e.type IN $types)
        AND (e IS NULL OR all_e = e)
        WITH o, all_e AS e, score
        """
        return cypher, params

    def fetch_unit_profile(self, uid: str, includes: list[str]):
        subqueries = []
        return_fields = ["u", "a"]

        for include in includes:
            spec = self.INCLUDE_SPECS.get(include)
            if not spec:
                continue
            subqueries.append(spec["subquery"])
            return_fields.extend(spec["return_fields"])

        cypher = (
            UNIT_BASE_MATCH
            + "\n"
            + "\n".join(subqueries)
            + "\nRETURN "
            + ", ".join(return_fields)
        )
        logging.debug(f"Executing Cypher query for unit profile: {cypher}")

        rows, _ = db.cypher_query(cypher, {"uid": uid}, resolve_objects=True)
        if not rows:
            raise ValueError("Unit not found")
        logging.debug(f"Cypher query  rows: {rows[0]}")

        row = rows[0]
        return {field: row[idx] for idx, field in enumerate(return_fields)}

    def count_unit_officers(
            self,
            unit_uid: str,
            term: str | None = None,
            filters: dict | None = None
    ) -> int:
        base_query, params = self._build_officer_search_query(
            unit_uid=unit_uid,
            term=term,
            filters=filters,
        )

        query = (
            base_query
            + """
            RETURN count(DISTINCT o) AS total_officers
            """
        )
        logging.warning(
            f"Counting unit officers: {query} with params: {params}")
        rows, _ = db.cypher_query(query, params)
        return rows[0][0] if rows else 0

    def fetch_unit_officers(
        self,
        unit_uid: str,
        skip: int,
        limit: int,
        include_employment: bool = False,
        term: str | None = None,
        filters: dict | None = None,
    ):
        base_query, params = self._build_officer_search_query(
            unit_uid=unit_uid,
            term=term,
            filters=filters,
        )
        params.update({
            "skip": skip,
            "limit": limit,
        })

        if include_employment:
            query = (
                base_query
                + """
                WITH o, e, score
                ORDER BY coalesce(e.latest_date, e.earliest_date) DESC
                WITH
                    o,
                    max(score) AS score,
                    collect(e) AS employment
                WITH
                    o,
                    score,
                    employment,
                    head(employment) AS most_recent,
                    reduce(min_date = null, stint IN employment |
                        CASE
                            WHEN min_date IS NULL THEN stint.earliest_date
                            WHEN stint.earliest_date IS NULL THEN min_date
                            WHEN stint.earliest_date < min_date
                            THEN stint.earliest_date
                            ELSE min_date
                        END
                    ) AS earliest_date,
                    reduce(max_date = null, stint IN employment |
                        CASE
                            WHEN stint.latest_date IS NULL THEN null
                            WHEN max_date IS NULL THEN stint.latest_date
                            WHEN stint.latest_date > max_date
                            THEN stint.latest_date
                            ELSE max_date
                        END
                    ) AS latest_date
                RETURN
                    o,
                    {
                        uid: most_recent.uid,
                        earliest_date: earliest_date,
                        latest_date: latest_date,
                        badge_number: most_recent.badge_number,
                        rank: most_recent.highest_rank,
                        status: most_recent.status,
                        type: most_recent.type
                    } AS employment
                ORDER BY score DESC, o.last_name ASC, o.first_name ASC
                SKIP $skip
                LIMIT $limit
                """
            )
        else:
            query = (
                base_query
                + """
                WITH o, max(score) AS score
                RETURN o
                ORDER BY score DESC, o.last_name ASC, o.first_name ASC
                SKIP $skip
                LIMIT $limit
                """
            )

        logging.debug(
            "Executing Cypher query: {} with params: {}".format(
                query, params)
        )

        rows, _ = db.cypher_query(query, params, resolve_objects=True)
        logging.debug(
            "Cypher query for unit officers returned rows: {}".format(rows))
        return rows
