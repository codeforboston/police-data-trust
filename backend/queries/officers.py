from neomodel import db


EMPLOYMENT_HISTORY_QUERY = """
    MATCH (o:Officer {uid: $uid})-[:HELD_BY]-(e:Employment)-[:IN_UNIT]
    -(u:Unit)-[:ESTABLISHED_BY]-(a:Agency)
    WITH a, u, e
    ORDER BY coalesce(e.latest_date, e.earliest_date) DESC
    WITH
      a,
      u,
      head(collect(e)) AS rep,
      min(e.earliest_date) AS earliest_date,
      max(e.latest_date)   AS latest_date
    RETURN {
      agency_uid:   a.uid,
      agency_name:  a.name,
      state:        a.hq_state,
      unit_uid:     u.uid,
      unit_name:    u.name,
      badge_number: rep.badge_number,
      highest_rank: rep.highest_rank,
      salary:       rep.salary,
      earliest_date: earliest_date,
      latest_date:   latest_date
    } AS item
    LIMIT 20;
    """

ALLEGATION_SUMMARY_QUERY = """
MATCH (o:Officer {uid: $uid})-[:ACCUSED_OF]->(a:Allegation)
MATCH (a)-[:ALLEGED]->(c:Complaint)
WITH
  CASE
    WHEN a.type IS NULL OR trim(a.type) = "" THEN "Unknown"
    ELSE a.type
  END AS type,
  count(*) AS occurrences,
  count(DISTINCT c.uid) AS complaint_count,
  sum(CASE WHEN toLower(
    trim(coalesce(a.finding,""))) = "substantiated" THEN 1 ELSE 0 END)
    AS substantiated_count,
  min(c.incident_date) AS earliest_incident_date,
  max(c.incident_date) AS latest_incident_date
ORDER BY occurrences DESC, type ASC
RETURN
  type,
  complaint_count,
  occurrences,
  substantiated_count,
  earliest_incident_date,
  latest_incident_date
LIMIT 10;
"""

SOURCES_QUERY = """
MATCH (o:Officer {uid: $uid})-[:UPDATED_BY]->(s:Source)
RETURN DISTINCT {
  name: s.name,
  url: s.url,
  contact_email: s.contact_email
} AS source
"""

METRICS_COMPLAINTS_CYPHER = """
MATCH (o:Officer {uid: $uid})-[:ACCUSED_OF]->
(:Allegation)-[:ALLEGED]->(co:Complaint)
WHERE co.incident_date IS NOT NULL
WITH
  co.incident_date.year AS year,
  co
WITH
  year,
  count(DISTINCT co) AS complaint_count,
  count(DISTINCT CASE WHEN co.closed_date IS NOT NULL
  THEN co END) AS closed_count
ORDER BY year DESC
LIMIT 7
RETURN collect({
  year: year,
  complaint_count: complaint_count,
  closed_count: closed_count
}) AS results;
"""


# Last 7 Calendar years of complaint counts
METRICS_COMPLAINT_HISTORY_QUERY = """
WITH range(date().year - 6, date().year) AS years
UNWIND years AS year
OPTIONAL MATCH (o:Officer {uid: $uid})-
[:ACCUSED_OF]->(:Allegation)-[:ALLEGED]->(co:Complaint)
WHERE co.incident_date IS NOT NULL AND co.incident_date.year = year
WITH
  year,
  count(DISTINCT co) AS complaint_count,
  count(DISTINCT CASE WHEN co.closed_date IS NOT NULL
  THEN co END) AS closed_count
ORDER BY year DESC
RETURN collect({
  year: year,
  complaint_count: complaint_count,
  closed_count: closed_count
}) AS results;
"""

METRICS_ALLEGATION_TYPES_QUERY = """
MATCH (o:Officer {uid: $uid})

CALL (o) {
  MATCH (o)-[:ACCUSED_OF]->(al:Allegation)
  RETURN count(al) AS total_allegations
}

CALL (o) {
  MATCH (o)-[:ACCUSED_OF]->(al:Allegation)
  WITH
    trim(coalesce(al.type, "")) AS type,
    trim(coalesce(al.allegation, "")) AS subtype
  WHERE type <> "" AND subtype <> ""
  RETURN type, subtype, count(*) AS pair_count
  ORDER BY pair_count DESC, type ASC, subtype ASC
  LIMIT 6
}

WITH
  total_allegations,
  collect(
    {type: type, subtype: subtype, count: pair_count}) AS top_types
RETURN {
  total_allegations: total_allegations,
  top_types: top_types
} AS result;
"""

METRICS_ALLEGATION_OUTCOMES_QUERY = """
MATCH (o:Officer {uid: $uid})
OPTIONAL MATCH (o)-[:ACCUSED_OF]->(al:Allegation)
WITH
  // keep only non-null / non-blank outcomes
  [x IN collect(trim(al.outcome)) WHERE x IS NOT NULL AND x <> ""] AS outcomes
WITH outcomes, size(outcomes) AS total

// Build per-outcome counts, while still returning a row when total = 0
WITH outcomes, total, CASE WHEN total = 0 THEN [NULL]
ELSE outcomes END AS outcomes2
UNWIND outcomes2 AS outcome
WITH total, outcome, count(*) AS cnt
WITH
  total,
  [r IN collect(CASE WHEN outcome IS NULL THEN NULL
  ELSE {outcome: outcome, count: cnt} END)
   WHERE r IS NOT NULL] AS rows
ORDER BY rows[0].count DESC

// Sort, slice top 5, compute rest
WITH total, rows
UNWIND rows AS r
WITH total, r
ORDER BY r.count DESC, r.outcome ASC
WITH total, collect(r) AS sorted
WITH
  total,
  sorted[0..5] AS top,
  sorted[5..]  AS rest
WITH
  total,
  top,
  size(rest) AS rest_n,
  reduce(s = 0, r IN rest | s + r.count) AS rest_count

RETURN {
  total_outcomes: total,
  top_outcomes: [
    r IN top |
    {
      outcome: r.outcome,
      count: r.count,
      pct: CASE WHEN total = 0 THEN 0
      ELSE round(100.0 * r.count / total, 2) END
    }
  ],
  all_the_rest: CASE
    WHEN rest_n > 0 THEN {
      outcome: "All the rest",
      count: rest_count,
      pct: CASE WHEN total = 0 THEN 0
      ELSE round(100.0 * rest_count / total, 2) END
    }
    ELSE NULL
  END
} AS result;
"""

METRICS_COMPLAINANT_DEMOGRAPHICS_QUERY = """
MATCH (o:Officer {uid: $uid})-[:ACCUSED_OF]->
(:Allegation)-[:REPORTED_BY]-(c:Civilian)
WITH o, collect(DISTINCT c) AS civilians

CALL (civilians) {
  WITH civilians, size(civilians) AS total
  UNWIND (CASE WHEN size(civilians) = 0 THEN [NULL] ELSE civilians END) AS c
  WITH total,
    CASE
      WHEN c IS NULL THEN NULL
      WHEN c.ethnicity IS NULL OR trim(c.ethnicity) = "" THEN NULL
      ELSE trim(c.ethnicity)
    END AS v
  WITH total, v, count(*) AS cnt
  WITH total,
    [r IN collect(CASE WHEN v IS NULL THEN NULL ELSE
    {value: v, count: cnt} END) WHERE r IS NOT NULL] AS rows,
    sum(CASE WHEN v IS NULL THEN 0 ELSE cnt END) AS not_null_total
  UNWIND (CASE WHEN size(rows) = 0 THEN [NULL] ELSE rows END) AS r
  WITH total, not_null_total, r
  ORDER BY
    (CASE WHEN r IS NULL THEN -1 ELSE r.count END) DESC,
    (CASE WHEN r IS NULL THEN "" ELSE r.value END) ASC
  WITH total, not_null_total,
    [x IN collect(
      CASE WHEN r IS NULL THEN NULL ELSE {
        ethnicity: r.value,
        count: r.count,
        pct: CASE WHEN total = 0 THEN 0
        ELSE round(100.0 * r.count / total, 2) END
      } END
    ) WHERE x IS NOT NULL] AS known
  WITH total, not_null_total, known
  WITH total, not_null_total,
    (known + [{
      ethnicity: "Unknown",
      count: total - not_null_total,
      pct: CASE WHEN total = 0 THEN 0
        ELSE round(100.0 * (total - not_null_total) / total, 2) END
    }]) AS ethnicity_breakdown
  RETURN ethnicity_breakdown
}

CALL (civilians) {
  WITH civilians, size(civilians) AS total
  UNWIND (CASE WHEN total = 0 THEN [NULL] ELSE civilians END) AS c
  WITH total,
    CASE
      WHEN c IS NULL THEN NULL
      WHEN c.gender IS NULL OR trim(c.gender) = "" THEN NULL
      ELSE trim(c.gender)
    END AS v
  WITH v, count(*) AS cnt, total
  WITH
    [r IN collect(CASE WHEN v IS NULL THEN NULL
    ELSE {value: v, count: cnt} END) WHERE r IS NOT NULL] AS rows,
    sum(CASE WHEN v IS NULL THEN 0 ELSE cnt END) AS not_null_total,
    total
  UNWIND (CASE WHEN size(rows) = 0 THEN [NULL] ELSE rows END) AS r
  WITH total, not_null_total, r
  ORDER BY
    (CASE WHEN r IS NULL THEN -1 ELSE r.count END) DESC,
    (CASE WHEN r IS NULL THEN "" ELSE r.value END) ASC
  WITH
    total,
    not_null_total,
    [x IN collect(
      CASE WHEN r IS NULL THEN NULL ELSE {
        gender: r.value,
        count: r.count,
        pct: CASE WHEN total = 0 THEN 0
                  ELSE round(100.0 * r.count / total, 2) END
      } END
    ) WHERE x IS NOT NULL] AS known
  WITH total, not_null_total, known
  WITH total, not_null_total,
    (known + [{
      gender: "Unknown",
      count: total - not_null_total,
      pct: CASE WHEN total = 0 THEN 0
        ELSE round(100.0 * (total - not_null_total) / total, 2) END
    }]) AS gender_breakdown
  RETURN gender_breakdown
}

CALL (civilians) {
  WITH civilians, size(civilians) AS total
  UNWIND (CASE WHEN size(civilians) = 0 THEN [NULL] ELSE civilians END) AS c
  WITH total,
    CASE
      WHEN c IS NULL THEN NULL
      WHEN c.age_range IS NULL OR trim(c.age_range) = "" THEN NULL
      ELSE trim(c.age_range)
    END AS v
  WITH total, v, count(*) AS cnt
  WITH total,
    [r IN collect(CASE WHEN v IS NULL THEN NULL
    ELSE {value: v, count: cnt} END) WHERE r IS NOT NULL] AS rows,
    sum(CASE WHEN v IS NULL THEN 0 ELSE cnt END) AS not_null_total
  UNWIND (CASE WHEN size(rows) = 0 THEN [NULL] ELSE rows END) AS r
  WITH total, not_null_total, r
  ORDER BY
    (CASE WHEN r IS NULL THEN -1 ELSE r.count END) DESC,
    (CASE WHEN r IS NULL THEN "" ELSE r.value END) ASC
  WITH total, not_null_total,
    [x IN collect(
      CASE WHEN r IS NULL THEN NULL ELSE {
        age_range: r.value,
        count: r.count,
        pct: CASE WHEN total = 0 THEN 0
        ELSE round(100.0 * r.count / total, 2) END
      } END
    ) WHERE x IS NOT NULL] AS known
  WITH total, not_null_total, known
  WITH total, not_null_total,
    (known + [{
      age_range: "Unknown",
      count: total - not_null_total,
      pct: CASE WHEN total = 0 THEN 0
        ELSE round(100.0 * (total - not_null_total) / total, 2) END
    }]) AS age_range_breakdown
  RETURN age_range_breakdown
}

RETURN {
  civilian_count: size(civilians),

  ethnicity: ethnicity_breakdown,
  gender:    gender_breakdown,
  age_range: age_range_breakdown
} AS result;
"""

class OfficerQueries:
    INCLUDE_SPECS = {
        
    }

    def fetch_officer_sources(self, officer_uid: str):
        rows, _ = db.cypher_query(SOURCES_QUERY, {"uid": officer_uid})
        return [row[0] for row in rows]


    def fetch_officer_employment_history(self, officer_uid: str):
        rows, _ = db.cypher_query(EMPLOYMENT_HISTORY_QUERY, {"uid": officer_uid})
        return [row[0] for row in rows]


    def fetch_officer_allegation_summary(self, officer_uid: str):
        rows, _ = db.cypher_query(ALLEGATION_SUMMARY_QUERY, {"uid": officer_uid})
        return rows


    def fetch_officer_metric_a_types(self, officer_uid: str):
        rows, _ = db.cypher_query(
            METRICS_ALLEGATION_TYPES_QUERY, {"uid": officer_uid})
        return rows[0][0] if rows else {}


    def fetch_officer_metric_a_outcomes(self, officer_uid: str):
        rows, _ = db.cypher_query(
            METRICS_ALLEGATION_OUTCOMES_QUERY, {"uid": officer_uid})
        return rows[0][0] if rows else {}


    def fetch_officer_metric_comp_history(self, officer_uid: str):
        rows, _ = db.cypher_query(
            METRICS_COMPLAINT_HISTORY_QUERY, {"uid": officer_uid})
        return rows[0][0] if rows else []


    def fetch_officer_metric_comp_demo(self, officer_uid: str):
        rows, _ = db.cypher_query(
            METRICS_COMPLAINANT_DEMOGRAPHICS_QUERY, {"uid": officer_uid})
        return rows[0][0] if rows else {}
