import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.config import Config


CURRENT_UNIT_PROFILE_QUERY = """
MATCH (u:Unit {uid: $uid})-[]-(a:Agency)
CALL (u) {
  RETURN coalesce(u.officer_count_cached, 0) AS total_officers
}
CALL (u) {
  RETURN
    coalesce(u.complaint_count_cached, 0) AS total_complaints,
    coalesce(u.allegation_count_cached, 0) AS total_allegations
}
RETURN u.uid AS uid, a.uid AS agency_uid, total_officers, total_complaints, total_allegations
"""

LEGACY_UNIT_PROFILE_QUERY = """
MATCH (u:Unit {uid: $uid})-[]-(a:Agency)
CALL (u) {
  OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(o:Officer)
  RETURN count(DISTINCT o) AS total_officers
}
CALL (u) {
  OPTIONAL MATCH (u)<-[]-(:Employment)-[]->(:Officer)
      -[:ACCUSED_OF]->(allege:Allegation)-[:ALLEGED]-(c:Complaint)
  RETURN
    count(DISTINCT c) AS total_complaints,
    count(DISTINCT allege) AS total_allegations
}
RETURN u.uid AS uid, a.uid AS agency_uid, total_officers, total_complaints, total_allegations
"""

CURRENT_SEARCH_UNIT_DETAILS_QUERY = """
UNWIND $unit_uids AS uid
MATCH (u:Unit {uid: uid})
OPTIONAL MATCH (u)-[]-(a:Agency)
CALL (u) {
    OPTIONAL MATCH (u)-[r:UPDATED_BY]->(s:Source)
    RETURN s, r
    ORDER BY r.timestamp DESC
    LIMIT 1
}
RETURN uid, {
    name: u.name,
    agency_name: a.name,
    officers: coalesce(u.officer_count_cached, 0),
    complaints: coalesce(u.complaint_count_cached, 0),
    source: s.name,
    last_updated: r.timestamp
} AS result
"""

LEGACY_SEARCH_UNIT_DETAILS_QUERY = """
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
RETURN uid, {
    name: u.name,
    agency_name: a.name,
    officers: officers,
    complaints: complaints,
    source: s.name,
    last_updated: r.timestamp
} AS result
"""


@dataclass
class ProfileRun:
    label: str
    query_name: str
    params: dict[str, Any]
    records: int
    available_after_ms: float | None
    consumed_after_ms: float | None
    root_operator: str | None
    db_hits: int
    rows: int
    page_cache_hits: int
    page_cache_misses: int
    identifiers: list[str]
    profile_tree: dict[str, Any] | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Profile cached vs legacy unit-related Neo4j queries.",
    )
    parser.add_argument(
        "--unit-id",
        action="append",
        dest="unit_ids",
        default=[],
        help="Unit UID to profile. Repeat to include multiple units.",
    )
    parser.add_argument(
        "--output-json",
        help="Write raw profiling output to a JSON file.",
    )
    return parser.parse_args()


def extract_value(container: Any, key: str, default: Any = None) -> Any:
    if container is None:
        return default
    if isinstance(container, dict):
        return container.get(key, default)
    if hasattr(container, key):
        return getattr(container, key)
    try:
        return container[key]
    except Exception:
        return default


def to_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def normalize_profile_node(node: Any) -> dict[str, Any]:
    children = extract_value(node, "children", []) or []
    normalized_children = [normalize_profile_node(child) for child in children]

    return {
        "operator_type": extract_value(node, "operator_type")
        or extract_value(node, "operatorType"),
        "identifiers": extract_value(node, "identifiers", []) or [],
        "db_hits": to_int(
            extract_value(node, "db_hits", extract_value(node, "dbHits", 0))
        ),
        "rows": to_int(extract_value(node, "rows", 0)),
        "page_cache_hits": to_int(
            extract_value(
                node,
                "page_cache_hits",
                extract_value(node, "pageCacheHits", 0),
            )
        ),
        "page_cache_misses": to_int(
            extract_value(
                node,
                "page_cache_misses",
                extract_value(node, "pageCacheMisses", 0),
            )
        ),
        "children": normalized_children,
    }


def aggregate_profile(node: dict[str, Any] | None) -> dict[str, Any]:
    if not node:
        return {
            "db_hits": 0,
            "rows": 0,
            "page_cache_hits": 0,
            "page_cache_misses": 0,
        }

    totals = {
        "db_hits": node.get("db_hits", 0),
        "rows": node.get("rows", 0),
        "page_cache_hits": node.get("page_cache_hits", 0),
        "page_cache_misses": node.get("page_cache_misses", 0),
    }

    for child in node.get("children", []):
        child_totals = aggregate_profile(child)
        for key, value in child_totals.items():
            totals[key] += value

    return totals


def profile_query(
    driver,
    *,
    label: str,
    query_name: str,
    query: str,
    params: dict[str, Any],
    database: str,
) -> ProfileRun:
    with driver.session(database=database) as session:
        result = session.run(f"PROFILE {query}", params)
        records = list(result)
        summary = result.consume()

    profile = normalize_profile_node(getattr(summary, "profile", None))
    totals = aggregate_profile(profile)

    return ProfileRun(
        label=label,
        query_name=query_name,
        params=params,
        records=len(records),
        available_after_ms=getattr(summary, "result_available_after", None),
        consumed_after_ms=getattr(summary, "result_consumed_after", None),
        root_operator=profile.get("operator_type"),
        db_hits=totals["db_hits"],
        rows=totals["rows"],
        page_cache_hits=totals["page_cache_hits"],
        page_cache_misses=totals["page_cache_misses"],
        identifiers=profile.get("identifiers", []),
        profile_tree=profile,
    )


def print_run(run: ProfileRun) -> None:
    print(f"{run.query_name} [{run.label}]")
    print(
        "  records={} available_after={}ms consumed_after={}ms".format(
            run.records,
            run.available_after_ms,
            run.consumed_after_ms,
        )
    )
    print(
        "  root={} db_hits={} rows={} page_cache_hits={} page_cache_misses={}".format(
            run.root_operator,
            run.db_hits,
            run.rows,
            run.page_cache_hits,
            run.page_cache_misses,
        )
    )


def print_comparison(
    query_name: str,
    cached: ProfileRun,
    legacy: ProfileRun,
) -> None:
    print(f"\nComparison: {query_name}")
    print(
        "  db_hits delta: {:+d}".format(cached.db_hits - legacy.db_hits)
    )
    print(
        "  rows delta: {:+d}".format(cached.rows - legacy.rows)
    )
    if cached.available_after_ms is not None and legacy.available_after_ms is not None:
        print(
            "  available_after delta: {:+.2f}ms".format(
                cached.available_after_ms - legacy.available_after_ms
            )
        )
    if cached.consumed_after_ms is not None and legacy.consumed_after_ms is not None:
        print(
            "  consumed_after delta: {:+.2f}ms".format(
                cached.consumed_after_ms - legacy.consumed_after_ms
            )
        )


def main() -> int:
    args = parse_args()
    if not args.unit_ids:
        print("Provide at least one --unit-id.")
        return 2

    try:
        from neo4j import GraphDatabase
    except ModuleNotFoundError:
        print(
            "The neo4j Python package is required to run this profiler. "
            "Install backend dependencies, then retry."
        )
        return 1

    config = Config()
    driver = GraphDatabase.driver(
        f"bolt://{config.GRAPH_NM_URI}",
        auth=(config.GRAPH_USER, config.GRAPH_PASSWORD),
    )

    all_runs: list[ProfileRun] = []
    try:
        for unit_id in args.unit_ids:
            run_specs = [
                (
                    "unit_profile",
                    "cached",
                    CURRENT_UNIT_PROFILE_QUERY,
                    {"uid": unit_id},
                ),
                (
                    "unit_profile",
                    "legacy",
                    LEGACY_UNIT_PROFILE_QUERY,
                    {"uid": unit_id},
                ),
                (
                    "search_unit_details",
                    "cached",
                    CURRENT_SEARCH_UNIT_DETAILS_QUERY,
                    {"unit_uids": [unit_id]},
                ),
                (
                    "search_unit_details",
                    "legacy",
                    LEGACY_SEARCH_UNIT_DETAILS_QUERY,
                    {"unit_uids": [unit_id]},
                ),
            ]

            print(f"\nUnit {unit_id}")
            unit_runs: dict[tuple[str, str], ProfileRun] = {}
            for query_name, label, query, params in run_specs:
                run = profile_query(
                    driver,
                    label=label,
                    query_name=query_name,
                    query=query,
                    params=params,
                    database=config.GRAPH_DB,
                )
                unit_runs[(query_name, label)] = run
                all_runs.append(run)
                print_run(run)

            print_comparison(
                "unit_profile",
                unit_runs[("unit_profile", "cached")],
                unit_runs[("unit_profile", "legacy")],
            )
            print_comparison(
                "search_unit_details",
                unit_runs[("search_unit_details", "cached")],
                unit_runs[("search_unit_details", "legacy")],
            )
    finally:
        driver.close()

    if args.output_json:
        payload = {
            "database": config.GRAPH_DB,
            "runs": [
                {
                    "label": run.label,
                    "query_name": run.query_name,
                    "params": run.params,
                    "records": run.records,
                    "available_after_ms": run.available_after_ms,
                    "consumed_after_ms": run.consumed_after_ms,
                    "root_operator": run.root_operator,
                    "db_hits": run.db_hits,
                    "rows": run.rows,
                    "page_cache_hits": run.page_cache_hits,
                    "page_cache_misses": run.page_cache_misses,
                    "identifiers": run.identifiers,
                    "profile_tree": run.profile_tree,
                }
                for run in all_runs
            ],
        }
        Path(args.output_json).write_text(json.dumps(payload, indent=2))
        print(f"\nWrote profiling output to {args.output_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
