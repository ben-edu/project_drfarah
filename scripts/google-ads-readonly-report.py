#!/usr/bin/env python3
"""Run bounded read-only Google Ads reports from an authenticated operator environment."""
import argparse
import json
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "api"))
from app.services.google_ads_reporting import CUSTOMER_ID, GoogleAdsReadError, read_report

def main(argv=None):
    parser = argparse.ArgumentParser(description="Google Ads v26 read-only reporting")
    parser.add_argument("--report", required=True, choices=[
        "account", "campaigns", "budgets", "schedules", "recommendations", "daily", "ad_groups", "search_terms", "changes"
    ])
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--customer-id", default=os.getenv("GOOGLE_ADS_CUSTOMER_ID", CUSTOMER_ID))
    parser.add_argument("--login-customer-id", default=os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"))
    args = parser.parse_args(argv)
    try:
        rows = read_report(
            report=args.report, start=args.start, end=args.end,
            ads_customer_id=args.customer_id, login_customer_id=args.login_customer_id,
        )
    except (GoogleAdsReadError, ValueError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2
    print(json.dumps({
        "source": "Google Ads API v26", "report": args.report,
        "row_count": len(rows), "rows": rows,
        "note": "costMicros is served cost, not billed cost; conversions are not completed patient visits",
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
