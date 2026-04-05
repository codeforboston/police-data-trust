import logging

from backend.database import db

UNIT_BASE_MATCH = """
MATCH (u:Unit {uid: $uid})-[]-(a:Agency)
"""

OFFICER_COUNT_SUBQUERY = """
CALL (u) {
  OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(o:Officer)
  RETURN count(DISTINCT o) AS total_officers
}
"""

COMPLAINT_SUBQUERY = """
CALL (u) {
  OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(:Officer)
      -[:ACCUSED_OF]->(allege:Allegation)-[:ALLEGED]-(c:Complaint)
  RETURN
    count(DISTINCT c) AS total_complaints,
    count(DISTINCT allege) AS total_allegations
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

    OFFICER_INCLUDE_SPECS = {
      "employment": {

      }
    }

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

    def count_unit_officers(self, unit_uid: str) -> int:
        query = """
        MATCH (u:Unit {uid: $unit_uid})<-[]-(:Employment)-[]->(o:Officer)
        RETURN count(DISTINCT o) AS total_officers
        """
        rows, _ = db.cypher_query(query, {"unit_uid": unit_uid})
        return rows[0][0] if rows else 0

    def fetch_unit_officers(
        self,
        unit_uid: str,
        skip: int,
        limit: int,
        include_employment: bool = False,
    ) -> list[dict]:
        params = {
            "unit_uid": unit_uid,
            "skip": skip,
            "limit": limit,
        }

        if include_employment:
            query = """
            MATCH (u:Unit {uid: $unit_uid})<-[:IN_UNIT]-
            (e:Employment)-[:HELD_BY]->(o:Officer)
            WITH o, e
            ORDER BY coalesce(e.latest_date, e.earliest_date) DESC
            WITH
                o,
                collect(e) AS employment
            WITH
                o,
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
                    rank: most_recent.highest_rank
                } AS employment
            SKIP $skip
            LIMIT $limit
            """
        else:
            query = """
            MATCH (u:Unit {uid: $unit_uid})-[:IN_UNIT]-
            (:Employment)-[:HELD_BY]-(o:Officer)
            RETURN o
            SKIP $skip
            LIMIT $limit
            """

        logging.debug(
            "Executing Cypher query: {} with params: {}".format(
                query, params)
        )

        rows, _ = db.cypher_query(query, params, resolve_objects=True)
        logging.debug(
            "Cypher query for unit officers returned rows: {}".format(rows))
        return rows
