"""Regression tests for the SCM Jenkins Google Ads read-only reporting runner."""
from __future__ import annotations

import ast
import io
import runpy
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = ROOT / "scripts" / "google-ads-report-runner.py"
JENKINSFILE_PATH = ROOT / "jenkins" / "google-ads" / "Jenkinsfile"
RUNNER = runpy.run_path(str(RUNNER_PATH))


def test_runner_syntax_and_scm_separation():
    # Regression: the old Groovy sh heredoc translated Python string escapes
    # and caused a SyntaxError before any Google Ads query ran.
    ast.parse(RUNNER_PATH.read_text(encoding="utf-8"))
    pipeline = JENKINSFILE_PATH.read_text(encoding="utf-8")
    assert "python - <<'PY'" not in pipeline
    assert "python /app/google-ads-report-runner.py" in pipeline
    assert "-v \"$PWD/scripts/google-ads-report-runner.py:/app/google-ads-report-runner.py:ro\"" in pipeline
    assert "ADS_OUTPUT_FORMAT" in pipeline
    assert "checkout scm" in pipeline


def test_full_audit_summary_prints_paid_terms_and_budget():
    calls = []

    def fake_run(cmd, **kwargs):
        assert kwargs == {"capture_output": True, "text": True}
        calls.append(cmd)
        kind = cmd[cmd.index("--report") + 1]
        if kind == "search_terms":
            rows = [
                {
                    "metrics": {"costMicros": "7300000", "clicks": "2", "impressions": "6", "conversions": 0},
                    "campaign": {"id": "24414014329"},
                    "adGroup": {"id": "199388744537"},
                    "searchTermView": {"searchTerm": "urgent care beverly hills"},
                },
                {
                    "metrics": {"costMicros": "0", "clicks": "0", "impressions": "3"},
                    "searchTermView": {"searchTerm": "nonpaid query"},
                },
            ]
        elif kind == "changes":
            rows = [{"changeEvent": {"changeResourceType": "CAMPAIGN_BUDGET", "changeResourceName": "budget-id"}}]
        else:
            rows = [{"campaignBudget": {"amountMicros": "10000000"}}]
        import json
        return SimpleNamespace(returncode=0, stderr="", stdout=json.dumps({"rows": rows, "report": kind}))

    output = io.StringIO()
    with redirect_stdout(output):
        status = RUNNER["main"](
            {"REPORT_KIND": "full_audit", "ADS_OUTPUT_FORMAT": "summary"},
            run=fake_run, today=date(2026, 11, 22),
        )
    text = output.getvalue()
    assert status == 0
    assert len(calls) == 9
    assert "REPORT_WINDOW=2026-11-16..2026-11-22" in text
    assert "SEARCH_TERMS_SUMMARY: rows=2 paid_rows=1 clicks=2 impressions=9 cost_usd=7.30" in text
    assert "PAID_TERM cost_usd=7.30" in text
    assert "term=urgent care beverly hills" in text
    assert "term=nonpaid query" not in text
    assert '"amountMicros": "10000000"' in text
    assert any("--report" in cmd and cmd[cmd.index("--report") + 1] == "schedules" for cmd in calls)
    assert '"CAMPAIGN_BUDGET": 1' in text
    assert "Google Ads API read-only reports SUCCESS" in text
    dates = [cmd for cmd in calls if "--report" in cmd and cmd[cmd.index("--report") + 1] == "search_terms"]
    assert dates[0][-4:] == ["--start", "2026-11-16", "--end", "2026-11-22"]


def test_raw_and_crlf_search_terms():
    import json

    def fake_run(cmd, **kwargs):
        return SimpleNamespace(
            returncode=0, stderr="",
            stdout=json.dumps({"rows": [{
                "metrics": {"costMicros": "5000000", "clicks": "1", "impressions": "2"},
                "searchTermView": {"searchTerm": "clinic\nname\rtest"},
            }]}),
        )

    output = io.StringIO()
    with redirect_stdout(output):
        status = RUNNER["main"](
            {"REPORT_KIND": "search_terms", "ADS_OUTPUT_FORMAT": "summary"},
            run=fake_run, today=date(2026, 11, 22),
        )
    assert status == 0
    assert "term=clinic name test" in output.getvalue()

    output = io.StringIO()
    with redirect_stdout(output):
        status = RUNNER["main"](
            {"REPORT_KIND": "search_terms", "ADS_OUTPUT_FORMAT": "raw"},
            run=fake_run, today=date(2026, 11, 22),
        )
    assert status == 0
    assert '"rows":' in output.getvalue()
    assert "PAID_TERM " not in output.getvalue()


def test_rejects_invalid_dates_without_invoking_api():
    calls = []
    stderr = io.StringIO()

    def fail_if_called(*args, **kwargs):
        calls.append(args)
        raise AssertionError("The API must not be called")

    with redirect_stderr(stderr):
        code = RUNNER["main"](
            {"REPORT_KIND": "full_audit", "ADS_END_DATE": "2026-11-23"},
            run=fail_if_called, today=date(2026, 11, 22),
        )
    assert code == 2
    assert calls == []
    assert "future" in stderr.getvalue()


def test_rejects_invalid_output_format():
    stderr = io.StringIO()
    with redirect_stderr(stderr):
        code = RUNNER["main"](
            {"REPORT_KIND": "campaigns", "ADS_OUTPUT_FORMAT": "unsafe"},
            today=date(2026, 11, 22),
        )
    assert code == 2
    assert "Invalid output format" in stderr.getvalue()


def test_weekday_schedule_compliance_summary():
    from contextlib import redirect_stdout
    days = ("MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY")
    rows = [
        {
            "campaign": {"id": campaign_id},
            "campaignCriterion": {
                "status": "ENABLED",
                "adSchedule": {
                    "dayOfWeek": day, "startHour": "8", "startMinute": "THIRTY",
                    "endHour": "16", "endMinute": "THIRTY",
                },
            },
        }
        for campaign_id in ("24414014329", "24404901753", "23637947414")
        for day in days
    ]
    output = io.StringIO()
    with redirect_stdout(output):
        RUNNER["summarize"]("schedules", {"rows": rows})
    assert "SCHEDULE_COMPLIANCE=PASS" in output.getvalue()
    assert output.getvalue().count("SCHEDULE campaign_id=") == 15

    rows[0]["campaignCriterion"]["adSchedule"]["endHour"] = "17"
    output = io.StringIO()
    with redirect_stdout(output):
        RUNNER["summarize"]("schedules", {"rows": rows})
    assert "SCHEDULE_COMPLIANCE=DRIFT_OR_INCOMPLETE" in output.getvalue()




def test_keyword_recommendation_detail_with_text_and_match_type():
    import json

    def fake_run(cmd, **kwargs):
        assert cmd[cmd.index("--report") + 1] == "recommendation_keywords"
        return SimpleNamespace(
            returncode=0,
            stderr="",
            stdout=json.dumps({"rows": [{
                "recommendation": {
                    "resourceName": "customers/6525103588/recommendations/example",
                    "campaign": "customers/6525103588/campaigns/24414014329",
                    "adGroup": "customers/6525103588/adGroups/199388744537",
                    "keywordRecommendation": {
                        "keyword": {"text": "urgent care clinic", "matchType": "PHRASE"},
                        "recommendedCpcBidMicros": "4000000",
                    },
                },
            }]}),
        )

    output = io.StringIO()
    with redirect_stdout(output):
        status = RUNNER["main"](
            {"REPORT_KIND": "recommendation_keywords", "ADS_OUTPUT_FORMAT": "summary"},
            run=fake_run, today=date(2026, 11, 23),
        )
    assert status == 0
    assert "RECOMMENDATION_KEYWORDS total=1" in output.getvalue()
    assert '"matchType": "PHRASE"' in output.getvalue()
    assert '"text": "urgent care clinic"' in output.getvalue()

if __name__ == "__main__":
    # Runs in a Python 3.12 container without external dependencies or API credentials.
    # Kept outside api/tests because root Jenkins' API pytest container mounts only api/.
    completed = 0
    for name, fn in sorted(list(globals().items())):
        if name.startswith("test_") and callable(fn):
            fn()
            print("PASS " + name, flush=True)
            completed += 1
    if completed < 5:
        raise SystemExit("Too few Google Ads runner regression tests discovered")
    print(f"PASS Google Ads runner tests: {completed}", flush=True)
