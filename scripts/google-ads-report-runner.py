#!/usr/bin/env python3
"""Jenkins operator entry point for bounded, read-only Google Ads reporting.

Keep Python outside of Groovy sh strings: Jenkins/Groovy escape processing can
turn Python "\\n" string literals into real newlines before Python parses them.
Only subprocesses the separately tested Google Ads SearchStream read-only CLI.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

ALLOWED_REPORTS = (
    "full_audit", "account", "budgets", "schedules", "campaigns", "daily",
    "ad_groups", "search_terms", "changes",
)
FULL_AUDIT = (
    "account", "budgets", "schedules", "campaigns", "daily",
    "ad_groups", "search_terms", "changes",
)
DATED_REPORTS = {"daily", "ad_groups", "search_terms", "changes"}


def parse_date(value: str, fallback: date) -> date:
    value = value.strip()
    if not value:
        return fallback
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Dates must be YYYY-MM-DD") from exc
    if parsed.isoformat() != value:
        raise ValueError("Dates must be YYYY-MM-DD")
    return parsed


def report_window(env: dict[str, str], today: date | None = None) -> tuple[date, date]:
    if today is None:
        today = datetime.now(ZoneInfo("America/Los_Angeles")).date()
    end = parse_date(env.get("ADS_END_DATE", ""), today)
    start = parse_date(env.get("ADS_START_DATE", ""), end - timedelta(days=6))
    if start > end or end > today:
        raise ValueError("Date range must be ordered and must not extend into the future")
    if (end - start).days >= 30:
        raise ValueError("Choose a date range under 30 days for Change Events compatibility")
    return start, end


def _number(value: object) -> int:
    return int(value or 0)


def summarize(item: str, payload: dict[str, object]) -> None:
    rows = payload.get("rows")
    if not isinstance(rows, list):
        raise ValueError("Google Ads report rows are not a list")
    print(f"ROWS={len(rows)}", flush=True)

    if item == "search_terms":
        paid = sorted(
            (row for row in rows if _number(row.get("metrics", {}).get("costMicros")) > 0),
            key=lambda row: _number(row.get("metrics", {}).get("costMicros")),
            reverse=True,
        )
        clicks = sum(_number(row.get("metrics", {}).get("clicks")) for row in rows)
        impressions = sum(_number(row.get("metrics", {}).get("impressions")) for row in rows)
        micros = sum(_number(row.get("metrics", {}).get("costMicros")) for row in rows)
        print(
            f"SEARCH_TERMS_SUMMARY: rows={len(rows)} paid_rows={len(paid)} "
            f"clicks={clicks} impressions={impressions} cost_usd={micros / 1_000_000:.2f}",
            flush=True,
        )
        for row in paid[:20]:
            metrics = row.get("metrics", {})
            term = str(row.get("searchTermView", {}).get("searchTerm", ""))
            term = term.replace(chr(10), " ").replace(chr(13), " ")
            print(
                f"PAID_TERM cost_usd={_number(metrics.get('costMicros')) / 1_000_000:.2f}"
                f" clicks={metrics.get('clicks', 0)}"
                f" conversions={metrics.get('conversions', 0)}"
                f" campaign_id={row.get('campaign', {}).get('id', '')}"
                f" ad_group_id={row.get('adGroup', {}).get('id', '')}"
                f" term={term}",
                flush=True,
            )
        print(
            f"PAID_TERMS_NOT_SHOWN={max(0, len(paid) - 20)} "
            f"ZERO_COST_ROWS_NOT_SHOWN={len(rows) - len(paid)}",
            flush=True,
        )
    elif item == "changes":
        counts = Counter(
            row.get("changeEvent", {}).get("changeResourceType", "UNKNOWN")
            for row in rows
        )
        print("CHANGE_TYPES=" + json.dumps(dict(counts), sort_keys=True), flush=True)
        for row in rows[:8]:
            event = row.get("changeEvent", {})
            print(
                "CHANGE time=" + str(event.get("changeDateTime", ""))
                + " type=" + str(event.get("changeResourceType", ""))
                + " client=" + str(event.get("clientType", ""))
                + " resource=" + str(event.get("changeResourceName", "")),
                flush=True,
            )
        print(f"CHANGE_EVENTS_NOT_SHOWN={max(0, len(rows) - 8)}", flush=True)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2), flush=True)


def main(env: dict[str, str] | None = None, run=subprocess.run, today: date | None = None) -> int:
    if env is None:
        env = os.environ
    report = env.get("REPORT_KIND", "full_audit")
    output_format = env.get("ADS_OUTPUT_FORMAT", "summary") or "summary"
    if report not in ALLOWED_REPORTS:
        print("Invalid report selection", file=sys.stderr)
        return 2
    if output_format not in ("summary", "raw"):
        print("Invalid output format (use summary or raw)", file=sys.stderr)
        return 2
    try:
        start, end = report_window(env, today=today)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    reports = FULL_AUDIT if report == "full_audit" else (report,)
    print(f"REPORT_WINDOW={start.isoformat()}..{end.isoformat()} (America/Los_Angeles)", flush=True)
    for item in reports:
        print(f"===== {item.upper()} =====", flush=True)
        cmd = [sys.executable, "/app/google-ads-readonly-report.py", "--report", item]
        if item in DATED_REPORTS:
            cmd += ["--start", start.isoformat(), "--end", end.isoformat()]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode:
            print((result.stderr or "Google Ads reporting command failed").strip(), file=sys.stderr)
            return result.returncode
        if output_format == "raw":
            print(result.stdout, flush=True)
            continue
        try:
            payload = json.loads(result.stdout)
            if not isinstance(payload, dict):
                raise ValueError("Google Ads report returned unexpected JSON")
            summarize(item, payload)
        except (ValueError, TypeError, KeyError) as exc:
            print(f"Invalid Google Ads report output: {exc}", file=sys.stderr)
            return 2
    print("Google Ads API read-only reports SUCCESS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
