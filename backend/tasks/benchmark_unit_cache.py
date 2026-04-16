import argparse
import json
import statistics
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib import error, parse, request


DEFAULT_UNIT_PROFILE_INCLUDES = [
    "officers",
    "reported_officers",
    "complaints",
    "location",
]


@dataclass
class RequestResult:
    scenario: str
    url: str
    status_code: int
    duration_ms: float
    response_bytes: int
    ok: bool
    error: str | None = None


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]

    ordered = sorted(values)
    index = (len(ordered) - 1) * pct
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def summarize_results(results: list[RequestResult]) -> dict[str, Any]:
    durations = [result.duration_ms for result in results]
    response_bytes = [result.response_bytes for result in results]
    ok_count = sum(1 for result in results if result.ok)
    status_codes: dict[str, int] = {}

    for result in results:
        key = str(result.status_code)
        status_codes[key] = status_codes.get(key, 0) + 1

    return {
        "request_count": len(results),
        "ok_count": ok_count,
        "error_count": len(results) - ok_count,
        "status_codes": status_codes,
        "mean_ms": round(statistics.fmean(durations), 2) if durations else 0.0,
        "p50_ms": round(percentile(durations, 0.50), 2),
        "p95_ms": round(percentile(durations, 0.95), 2),
        "min_ms": round(min(durations), 2) if durations else 0.0,
        "max_ms": round(max(durations), 2) if durations else 0.0,
        "mean_response_bytes": round(
            statistics.fmean(response_bytes), 2
        ) if response_bytes else 0.0,
    }


def compare_summaries(
    baseline: dict[str, Any],
    current: dict[str, Any],
) -> dict[str, Any]:
    baseline_ms = baseline.get("mean_ms", 0.0) or 0.0
    current_ms = current.get("mean_ms", 0.0) or 0.0
    baseline_p95 = baseline.get("p95_ms", 0.0) or 0.0
    current_p95 = current.get("p95_ms", 0.0) or 0.0

    def pct_change(old: float, new: float) -> float | None:
        if old == 0:
            return None
        return round(((new - old) / old) * 100, 2)

    return {
        "mean_ms_delta": round(current_ms - baseline_ms, 2),
        "mean_ms_pct": pct_change(baseline_ms, current_ms),
        "p95_ms_delta": round(current_p95 - baseline_p95, 2),
        "p95_ms_pct": pct_change(baseline_p95, current_p95),
        "error_count_delta": current.get("error_count", 0)
        - baseline.get("error_count", 0),
    }


def build_url(base_url: str, path: str, query: list[tuple[str, str]]) -> str:
    encoded = parse.urlencode(query, doseq=True)
    return f"{base_url.rstrip('/')}{path}?{encoded}" if encoded else (
        f"{base_url.rstrip('/')}{path}"
    )


def request_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    json_body: dict[str, Any] | None = None,
    timeout: float = 30.0,
) -> tuple[int, bytes]:
    data = None
    final_headers = headers.copy() if headers else {}
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        final_headers["Content-Type"] = "application/json"

    req = request.Request(
        url,
        data=data,
        headers=final_headers,
        method=method,
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            return response.status, response.read()
    except error.HTTPError as exc:
        return exc.code, exc.read()


def get_access_token(args: argparse.Namespace) -> str:
    if args.token:
        return args.token

    if not args.email or not args.password:
        raise SystemExit(
            "Provide either --token or both --email and --password."
        )

    login_url = build_url(args.base_url, "/api/v1/auth/login", [])
    status, body = request_json(
        login_url,
        method="POST",
        json_body={"email": args.email, "password": args.password},
        timeout=args.timeout,
    )
    if status != 200:
        raise SystemExit(
            f"Login failed with status {status}: {body.decode('utf-8', 'ignore')}"
        )

    payload = json.loads(body.decode("utf-8"))
    token = payload.get("access_token")
    if not token:
        raise SystemExit("Login response did not include access_token.")
    return token


def run_scenario(
    name: str,
    url: str,
    *,
    headers: dict[str, str],
    warmup: int,
    repeats: int,
    timeout: float,
) -> list[RequestResult]:
    for _ in range(warmup):
        request_json(url, headers=headers, timeout=timeout)

    results: list[RequestResult] = []
    for _ in range(repeats):
        start = time.perf_counter()
        status, body = request_json(url, headers=headers, timeout=timeout)
        duration_ms = (time.perf_counter() - start) * 1000
        results.append(
            RequestResult(
                scenario=name,
                url=url,
                status_code=status,
                duration_ms=duration_ms,
                response_bytes=len(body),
                ok=200 <= status < 300,
                error=None if 200 <= status < 300 else body.decode(
                    "utf-8", "ignore"
                )[:300],
            )
        )
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark unit-heavy API endpoints before/after cache changes.",
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:5000",
        help="Base API URL, e.g. http://localhost:5000",
    )
    parser.add_argument(
        "--token",
        help="JWT access token. If omitted, the script logs in with --email/--password.",
    )
    parser.add_argument("--email", help="Login email for fetching a token.")
    parser.add_argument("--password", help="Login password for fetching a token.")
    parser.add_argument(
        "--unit-id",
        action="append",
        dest="unit_ids",
        default=[],
        help="Unit UID to benchmark. Repeat this flag to benchmark multiple units.",
    )
    parser.add_argument(
        "--search-term",
        action="append",
        dest="search_terms",
        default=[],
        help="Search term to benchmark against /api/v1/search. Repeat as needed.",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=20,
        help="Measured requests per scenario.",
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=3,
        help="Warmup requests per scenario before timing starts.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-request timeout in seconds.",
    )
    parser.add_argument(
        "--search-per-page",
        type=int,
        default=10,
        help="per_page for search benchmarks.",
    )
    parser.add_argument(
        "--officers-per-page",
        type=int,
        default=25,
        help="per_page for unit officers benchmarks.",
    )
    parser.add_argument(
        "--output-json",
        help="Write full benchmark output to this JSON file.",
    )
    parser.add_argument(
        "--compare-json",
        help="Path to a previous benchmark JSON file to compare against.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.unit_ids and not args.search_terms:
        print(
            "Provide at least one --unit-id or --search-term to benchmark.",
            file=sys.stderr,
        )
        return 2

    token = get_access_token(args)
    headers = {"Authorization": f"Bearer {token}"}

    scenario_results: dict[str, list[RequestResult]] = {}

    for unit_id in args.unit_ids:
        profile_query = [("include", value) for value in DEFAULT_UNIT_PROFILE_INCLUDES]
        profile_url = build_url(
            args.base_url,
            f"/api/v1/units/{unit_id}",
            profile_query,
        )
        scenario_results[f"unit_profile:{unit_id}"] = run_scenario(
            f"unit_profile:{unit_id}",
            profile_url,
            headers=headers,
            warmup=args.warmup,
            repeats=args.repeats,
            timeout=args.timeout,
        )

        officers_url = build_url(
            args.base_url,
            f"/api/v1/units/{unit_id}/officers",
            [("page", "1"), ("per_page", str(args.officers_per_page))],
        )
        scenario_results[f"unit_officers:{unit_id}"] = run_scenario(
            f"unit_officers:{unit_id}",
            officers_url,
            headers=headers,
            warmup=args.warmup,
            repeats=args.repeats,
            timeout=args.timeout,
        )

    for search_term in args.search_terms:
        search_url = build_url(
            args.base_url,
            "/api/v1/search",
            [
                ("term", search_term),
                ("page", "1"),
                ("per_page", str(args.search_per_page)),
            ],
        )
        scenario_results[f"search:{search_term}"] = run_scenario(
            f"search:{search_term}",
            search_url,
            headers=headers,
            warmup=args.warmup,
            repeats=args.repeats,
            timeout=args.timeout,
        )

    summary = {
        name: summarize_results(results)
        for name, results in scenario_results.items()
    }

    output: dict[str, Any] = {
        "base_url": args.base_url,
        "repeats": args.repeats,
        "warmup": args.warmup,
        "scenarios": {
            name: {
                "summary": summary[name],
                "requests": [asdict(result) for result in results],
            }
            for name, results in scenario_results.items()
        },
    }

    if args.compare_json:
        baseline = json.loads(Path(args.compare_json).read_text())
        comparisons: dict[str, Any] = {}
        for name, current_summary in summary.items():
            baseline_summary = (
                baseline.get("scenarios", {})
                .get(name, {})
                .get("summary")
            )
            if baseline_summary:
                comparisons[name] = compare_summaries(
                    baseline_summary,
                    current_summary,
                )
        output["comparisons"] = comparisons

    for name, current_summary in summary.items():
        print(name)
        print(
            "  requests={request_count} ok={ok_count} errors={error_count} "
            "mean={mean_ms}ms p50={p50_ms}ms p95={p95_ms}ms "
            "min={min_ms}ms max={max_ms}ms".format(**current_summary)
        )
        print(
            "  statuses={} mean_bytes={}".format(
                current_summary["status_codes"],
                current_summary["mean_response_bytes"],
            )
        )
        if args.compare_json:
            comparison = output.get("comparisons", {}).get(name)
            if comparison:
                print(
                    "  delta mean={:+.2f}ms ({}) p95={:+.2f}ms ({}) errors={:+d}".format(
                        comparison["mean_ms_delta"],
                        (
                            f"{comparison['mean_ms_pct']}%"
                            if comparison["mean_ms_pct"] is not None
                            else "n/a"
                        ),
                        comparison["p95_ms_delta"],
                        (
                            f"{comparison['p95_ms_pct']}%"
                            if comparison["p95_ms_pct"] is not None
                            else "n/a"
                        ),
                        comparison["error_count_delta"],
                    )
                )

    if args.output_json:
        Path(args.output_json).write_text(json.dumps(output, indent=2))
        print(f"\nWrote benchmark output to {args.output_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
