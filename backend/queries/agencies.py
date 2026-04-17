import logging

from neomodel import db

AGENCY_BASE_MATCH = """
MATCH (a:Agency {uid: $agency_uid})
"""

UNIT_COUNT_SUBQUERY = """
CALL (a) {
  RETURN coalesce(a.unit_count_cached, 0) AS total_units
}
"""

OFFICER_COUNT_SUBQUERY = """
CALL (a) {
  RETURN coalesce(a.officer_count_cached, 0) AS total_officers
}
"""

COMPLAINT_SUBQUERY = """
CALL (a) {
  RETURN
    coalesce(a.complaint_count_cached, 0) AS total_complaints,
    coalesce(a.allegation_count_cached, 0) AS total_allegations
}
"""

ALLEGATION_SUBQUERY = """
CALL (a) {
  OPTIONAL MATCH (a)-[]-(:Unit)<-[]-(:Employment)-[]->(:Officer)
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

REPORTED_UNIT_SUBQUERY = """
CALL (a) {
  MATCH (a)-[]-(u:Unit)<-[]-(:Employment)-[]->(:Officer)
      -[:ACCUSED_OF]->(:Allegation)-[:ALLEGED]-(c:Complaint)
  WITH
    u,
    count(DISTINCT c) AS complaint_count,
    count(*) AS allegation_count
  ORDER BY complaint_count DESC, allegation_count DESC
  LIMIT 3
  RETURN collect(u) AS most_reported_units
}
"""

LOCATION_SUBQUERY = """
CALL (a) {
  OPTIONAL MATCH (a)-[]-(city:CityNode)-[]-(:CountyNode)-[]-(state:StateNode)
  RETURN {
    coords: city.coordinates,
    city: city.name,
    state: state.name
  } AS location
}
"""

PROFILE_AGENCY_LOOKUP_QUERY = """
MATCH (city:CityNode {name: $city_name})
    -[:WITHIN_COUNTY]->(:CountyNode)-[:WITHIN_STATE]->(state:StateNode)
WHERE state.abbreviation = $state
MATCH (a:Agency)-[:LOCATED_IN]->(city)
WHERE NOT a.uid IN $exclude_uids
RETURN
  a.uid AS uid,
  a.name AS agency_name,
  city.name AS city_name,
  state.abbreviation AS state_abbreviation,
  state.name AS state_name,
  a.jurisdiction AS jurisdiction,
  coalesce(a.officer_count_cached, 0) AS officer_count,
  coalesce(a.complaint_count_cached, 0) AS complaint_count
ORDER BY complaint_count DESC,
    officer_count DESC,
    agency_name ASC
LIMIT $limit
"""

RICH_AGENCY_LOOKUP_QUERY = """
MATCH (city:CityNode)-[:WITHIN_COUNTY]->(:CountyNode)
    -[:WITHIN_STATE]->(state:StateNode)
WHERE
  city.coordinates IS NOT NULL
  AND ($state IS NULL OR state.abbreviation = $state)
WITH
  city,
  state,
  coalesce(city.population, 0) AS population,
  coalesce(city.agency_count_cached, 0) AS agency_count_cached,
  coalesce(city.officer_count_cached, 0) AS officer_count_cached,
  coalesce(city.complaint_count_cached, 0) AS complaint_count_cached,
  coalesce(city.richness_score_cached, 0.0) AS richness_score_cached
ORDER BY richness_score_cached DESC,
    complaint_count_cached DESC,
    officer_count_cached DESC,
    agency_count_cached DESC,
    population DESC,
    city.name ASC
LIMIT $candidate_city_limit
MATCH (a:Agency)-[:LOCATED_IN]->(city)
WHERE NOT a.uid IN $exclude_uids
WITH DISTINCT
  a,
  city,
  state,
  population,
  richness_score_cached,
  complaint_count_cached,
  officer_count_cached,
  agency_count_cached
RETURN
  a.uid AS uid,
  a.name AS agency_name,
  city.name AS city_name,
  state.abbreviation AS state_abbreviation,
  state.name AS state_name,
  a.jurisdiction AS jurisdiction,
  coalesce(a.officer_count_cached, 0) AS officer_count,
  coalesce(a.complaint_count_cached, 0) AS complaint_count,
  population,
  richness_score_cached
ORDER BY complaint_count DESC,
    officer_count DESC,
    richness_score_cached DESC,
    complaint_count_cached DESC,
    officer_count_cached DESC,
    agency_count_cached DESC,
    population DESC,
    agency_name ASC
LIMIT $limit
"""

NEARBY_AGENCY_LOOKUP_QUERY = """
WITH point({
    longitude: $longitude,
    latitude: $latitude,
    crs: 'wgs-84'
}) AS user_point
MATCH (a:Agency)-[:LOCATED_IN]->(city:CityNode)
    -[:WITHIN_COUNTY]->(:CountyNode)-[:WITHIN_STATE]->(state:StateNode)
WHERE city.coordinates IS NOT NULL AND NOT a.uid IN $exclude_uids
WITH DISTINCT
    a,
    city,
    state,
    point.distance(user_point, city.coordinates) AS distance_meters
RETURN
  a.uid AS uid,
  a.name AS agency_name,
  city.name AS city_name,
  state.abbreviation AS state_abbreviation,
  state.name AS state_name,
  a.jurisdiction AS jurisdiction,
  coalesce(a.officer_count_cached, 0) AS officer_count,
  coalesce(a.complaint_count_cached, 0) AS complaint_count,
  distance_meters
ORDER BY distance_meters ASC,
    complaint_count DESC,
    officer_count DESC,
    agency_name ASC
LIMIT $limit
"""


class AgencyQueries:
    INCLUDE_SPECS = {
        "units": {
            "subquery": UNIT_COUNT_SUBQUERY,
            "return_fields": ["total_units"],
        },
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
        "reported_units": {
            "subquery": REPORTED_UNIT_SUBQUERY,
            "return_fields": ["most_reported_units"],
        },
        "location": {
            "subquery": LOCATION_SUBQUERY,
            "return_fields": ["location"],
        },
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

    def _build_agency_officer_search_query(
        self,
        agency_uid: str,
        term: str | None = None,
        filters: dict | None = None,
    ) -> tuple[str, dict]:
        normalized = self._normalize_officer_filters(filters)
        strategy = self._classify_officer_term(term)

        params = {
            "agency_uid": agency_uid,
            "term": term.strip() if term else None,
            **normalized,
        }

        if strategy == "none":
            cypher = """
            MATCH (a:Agency {uid: $agency_uid})-[:ESTABLISHED_BY]-(u:Unit)
                -[:IN_UNIT]-(e:Employment)-[:HELD_BY]-(o:Officer)
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
            MATCH (o)<-[:HELD_BY]-(e:Employment)-[:IN_UNIT]->
            (u:Unit)-[:ESTABLISHED_BY]->(a:Agency)
            WHERE a.uid = $agency_uid
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
            MATCH (e)-[:IN_UNIT]->(u:Unit)-[:ESTABLISHED_BY]->(a:Agency)
            WHERE a.uid = $agency_uid
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
        MATCH (o)<-[:HELD_BY]-(all_e:Employment)-[:IN_UNIT]->
        (u:Unit)-[:ESTABLISHED_BY]->(a:Agency)
        WHERE a.uid = $agency_uid
        AND (coalesce($ranks, []) = [] OR all_e.highest_rank IN $ranks)
        AND (coalesce($statuses, []) = [] OR all_e.status IN $statuses)
        AND (coalesce($types, []) = [] OR all_e.type IN $types)
        AND (e IS NULL OR all_e = e)
        WITH o, all_e AS e, u, score
        """
        return cypher, params

    def fetch_agency_profile(self, agency_uid: str, includes: list[str]):
        subqueries = []
        return_fields = ["a"]

        for include in includes:
            spec = self.INCLUDE_SPECS.get(include)
            if not spec:
                continue
            subqueries.append(spec["subquery"])
            return_fields.extend(spec["return_fields"])

        cypher = (
            AGENCY_BASE_MATCH
            + "\n"
            + "\n".join(subqueries)
            + "\nRETURN "
            + ", ".join(return_fields)
        )

        logging.warning(f"Cypher query: {cypher}")
        rows, _ = db.cypher_query(
            cypher, {"agency_uid": agency_uid}, resolve_objects=True)
        if not rows:
            raise ValueError("Agency not found")

        logging.warning(f"Cypher query rows: {rows[0]}")
        row = rows[0]
        return {field: row[idx] for idx, field in enumerate(return_fields)}

    def count_agency_officers(
        self,
        agency_uid: str,
        term: str | None = None,
        filters: dict | None = None
    ) -> int:
        base_query, params = self._build_agency_officer_search_query(
            agency_uid=agency_uid,
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
            f"Counting agency officers: {query} with params {params}")
        rows, _ = db.cypher_query(query, params)
        return rows[0][0] if rows else 0

    def count_agency_units(self, agency_uid: str) -> int:
        query = """
        MATCH (a:Agency {uid: $agency_uid})-[:ESTABLISHED_BY]-(u:Unit)
        RETURN count(DISTINCT u) AS total_units
        """
        rows, _ = db.cypher_query(query, {"agency_uid": agency_uid})
        return rows[0][0] if rows else 0

    def fetch_agency_officers(
        self,
        agency_uid: str,
        skip: int,
        limit: int,
        include_employment: bool,
        term: str | None = None,
        filters: dict | None = None
    ):
        base_query, params = self._build_agency_officer_search_query(
            agency_uid=agency_uid,
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
                WITH o, e, u, score
                ORDER BY coalesce(e.latest_date, e.earliest_date) DESC

                WITH
                    o,
                    max(score) AS score,
                    collect({employment: e, unit: u}) AS rows

                WITH
                    o,
                    score,
                    rows,
                    head(rows) AS most_recent,
                    reduce(min_date = null, row IN rows |
                        CASE
                            WHEN min_date IS NULL
                              THEN row.employment.earliest_date
                            WHEN row.employment.earliest_date IS NULL
                              THEN min_date
                            WHEN row.employment.earliest_date < min_date
                            THEN row.employment.earliest_date
                            ELSE min_date
                        END
                    ) AS earliest_date,
                    reduce(max_date = null, row IN rows |
                        CASE
                            WHEN row.employment.latest_date IS NULL THEN null
                            WHEN max_date IS NULL
                              THEN row.employment.latest_date
                            WHEN row.employment.latest_date > max_date
                            THEN row.employment.latest_date
                            ELSE max_date
                        END
                    ) AS latest_date

                RETURN
                    o,
                    {
                        uid: most_recent.employment.uid,
                        earliest_date: earliest_date,
                        latest_date: latest_date,
                        badge_number: most_recent.employment.badge_number,
                        rank: most_recent.employment.highest_rank,
                        status: most_recent.employment.status,
                        type: most_recent.employment.type,
                        unit: {
                            uid: most_recent.unit.uid,
                            name: most_recent.unit.name
                        }
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

        logging.warning(
            f"Cypher query for fetching officers: {query} with params {params}"
        )
        rows, _ = db.cypher_query(query, params, resolve_objects=True)
        return rows

    def fetch_agency_units(
        self,
        agency_uid: str,
        skip: int,
        limit: int,
    ):
        params = {
            "agency_uid": agency_uid,
            "skip": skip,
            "limit": limit,
        }

        query = """
        MATCH (a:Agency {uid: $agency_uid})-[:ESTABLISHED_BY]-(u:Unit)
        RETURN u
        SKIP $skip
        LIMIT $limit
        """

        rows, _ = db.cypher_query(query, params, resolve_objects=True)
        return rows

    def fetch_profile_agencies(
        self,
        *,
        city_name: str,
        state: str,
        exclude_uids: list[str] | None = None,
        limit: int = 5,
    ):
        params = {
            "city_name": " ".join(city_name.split()),
            "state": state.strip().upper(),
            "exclude_uids": exclude_uids or [],
            "limit": limit,
        }
        rows, _ = db.cypher_query(PROFILE_AGENCY_LOOKUP_QUERY, params)
        return rows

    def fetch_rich_agencies(
        self,
        *,
        state: str | None = None,
        exclude_uids: list[str] | None = None,
        limit: int = 5,
        candidate_city_limit: int = 100,
    ):
        params = {
            "state": state.strip().upper() if state else None,
            "exclude_uids": exclude_uids or [],
            "limit": limit,
            "candidate_city_limit": candidate_city_limit,
        }
        rows, _ = db.cypher_query(RICH_AGENCY_LOOKUP_QUERY, params)
        return rows

    def fetch_nearby_agencies(
        self,
        *,
        latitude: float,
        longitude: float,
        exclude_uids: list[str] | None = None,
        limit: int = 5,
    ):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "exclude_uids": exclude_uids or [],
            "limit": limit,
        }
        rows, _ = db.cypher_query(NEARBY_AGENCY_LOOKUP_QUERY, params)
        return rows
