from backend.database import db

UNIT_BASE_QUERY = """
MATCH (u:Unit {uid: $uid})-[]-(a:Agency)
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

MOST_REPORTED_OFFICER_SUBQUERY = """
CALL (u) {
  MATCH (u)<-[]-(:Employment)-[]->(o:Officer)
    -[:ACCUSED_OF]->(a:Allegation)-[:ALLEGED]-(c:Complaint)
  WITH
    o,
    count(DISTINCT c) AS complaint_count,
    count(DISTINCT a) AS allegation_count
  ORDER BY complaint_count DESC, allegation_count DESC
  LIMIT 3
  RETURN collect(o) AS most_reported_officers
}
"""

TOTAL_OFFICER_SUBQUERY = """
CALL (u) {
  OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(o:Officer)
  RETURN count(DISTINCT o) AS total_officers
}
"""

COMPLAINT_SUBQUERY = """
CALL (u) {
  OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(:Officer)
      -[:ACCUSED_OF]->(a:Allegation)-[:ALLEGED]-(c:Complaint)
  RETURN
    count(DISTINCT c) AS total_complaints,
    count(DISTINCT a) AS total_allegations
}
"""

UNIT_INCLUDE_SPECS = {
    "reported_officers": {
        "subquery": MOST_REPORTED_OFFICER_SUBQUERY,
        "return_fields": ["most_reported_officers"],
    },
    "total_officers": {
        "subquery": TOTAL_OFFICER_SUBQUERY,
        "return_fields": ["total_officers"],
    },
    "total_complaints": {
        "subquery": COMPLAINT_SUBQUERY,
        "return_fields": ["total_complaints", "total_allegations"],
    },
    "location": {
        "subquery": LOCATION_SUBQUERY,
        "return_fields": ["location"],
    },
}


def fetch_unit_detail(uid: str, includes: list[str]):
    subqueries = []
    return_fields = ["u", "a"]

    for include in includes:
        spec = UNIT_INCLUDE_SPECS.get(include)
        if not spec:
            continue
        subqueries.append(spec["subquery"])
        return_fields.extend(spec["return_fields"])

    cypher = (
        UNIT_BASE_QUERY
        + "\n"
        + "\n".join(subqueries)
        + "\nRETURN "
        + ", ".join(return_fields)
    )

    rows, _ = db.cypher_query(cypher, {"uid": uid}, resolve_objects=True)
    if not rows:
        return None

    row = rows[0]
    return {field: row[idx] for idx, field in enumerate(return_fields)}
