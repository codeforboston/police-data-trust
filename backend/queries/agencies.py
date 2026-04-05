import logging

from neomodel import db

AGENCY_BASE_MATCH = """
MATCH (a:Agency {uid: $agency_uid})
"""

UNIT_COUNT_SUBQUERY = """
CALL (a) {
  OPTIONAL MATCH (a)-[]-(u:Unit)
  RETURN count(DISTINCT u) AS total_units
}
"""

OFFICER_COUNT_SUBQUERY = """
CALL (a) {
  OPTIONAL MATCH (a)-[]-(:Unit)<-[]-(:Employment)-[]->(o:Officer)
  RETURN count(DISTINCT o) AS total_officers
}
"""

COMPLAINT_SUBQUERY = """
CALL (a) {
  OPTIONAL MATCH (a)-[]-(:Unit)<-[]-(:Employment)-[]->(:Officer)
      -[:ACCUSED_OF]->(allege:Allegation)-[:ALLEGED]-(c:Complaint)
  RETURN
    count(DISTINCT c) AS total_complaints,
    count(DISTINCT allege) AS total_allegations
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

        logging.debug(f"Cypher query: {cypher}")
        rows, _ = db.cypher_query(
            cypher, {"agency_uid": agency_uid}, resolve_objects=True)
        if not rows:
            raise ValueError("Agency not found")

        logging.debug(f"Cypher query rows: {rows[0]}")
        row = rows[0]
        return {field: row[idx] for idx, field in enumerate(return_fields)}

    def count_agency_officers(self, agency_uid: str) -> int:
        query = """
        MATCH (a:Agency {uid: $agency_uid})-[:ESTABLISHED_BY]-(u:Unit)
            -[:IN_UNIT]-(:Employment)-[:HELD_BY]-(o:Officer)
        RETURN count(DISTINCT o) AS total_officers
        """
        rows, _ = db.cypher_query(query, {"agency_uid": agency_uid})
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
    ):
        params = {
            "agency_uid": agency_uid,
            "skip": skip,
            "limit": limit,
        }

        if include_employment:
            query = """
            MATCH (a:Agency {uid: $agency_uid})-[:ESTABLISHED_BY]-(u:Unit)
                -[:IN_UNIT]-(e:Employment)-[:HELD_BY]-(o:Officer)
            WITH o, u, e
            ORDER BY coalesce(e.latest_date, e.earliest_date) DESC
            WITH
                o,
                collect({employment: e, unit: u}) AS rows
            WITH
                o,
                rows,
                head(rows) AS most_recent,
                reduce(min_date = null, row IN rows |
                    CASE
                        WHEN min_date IS NULL THEN row.employment.earliest_date
                        WHEN row.employment.earliest_date IS NULL THEN min_date
                        WHEN row.employment.earliest_date < min_date
                          THEN row.employment.earliest_date
                        ELSE min_date
                    END
                ) AS earliest_date,
                reduce(max_date = null, row IN rows |
                    CASE
                        WHEN row.employment.latest_date IS NULL THEN null
                        WHEN max_date IS NULL THEN row.employment.latest_date
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
                    unit: {
                        uid: most_recent.unit.uid,
                        name: most_recent.unit.name
                    }
                } AS employment
            SKIP $skip
            LIMIT $limit
            """
        else:
            query = """
            MATCH (a:Agency {uid: $agency_uid})-[:ESTABLISHED_BY]-(u:Unit)
                -[:IN_UNIT]-(:Employment)-[:HELD_BY]-(o:Officer)
            WITH DISTINCT o
            RETURN o
            SKIP $skip
            LIMIT $limit
            """

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
