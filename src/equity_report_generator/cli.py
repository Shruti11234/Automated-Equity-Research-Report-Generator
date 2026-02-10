from __future__ import annotations

import argparse
from pathlib import Path

from .compliance import compliance_footer
from .data_pipeline import fetch_company_snapshot, fetch_financial_trend, to_metric_table
from .report_sections import build_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automated Equity Research Report Generator")
    parser.add_argument("--company", required=True, help="Company name for report heading")
    parser.add_argument("--ticker", required=True, help="Primary ticker symbol (e.g., AAPL)")
    parser.add_argument("--peers", nargs="*", default=[], help="Optional peer tickers")
    parser.add_argument("--output", default="report.md", help="Output markdown path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    subject = fetch_company_snapshot(args.ticker, args.company)
    trend = fetch_financial_trend(args.ticker)

    peer_tickers = [t.upper() for t in args.peers if t.upper() != subject.ticker]
    peers = [fetch_company_snapshot(t) for t in peer_tickers]
    peers_table = to_metric_table([subject, *peers])

    report = build_report(
        subject=subject,
        financial_trend=trend,
        peers_table=peers_table,
        compliance_note=compliance_footer(),
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Report generated at: {output_path}")


if __name__ == "__main__":
    main()
