from __future__ import annotations

from typing import Iterable

import pandas as pd

from .compliance import neutral_language_wrap
from .data_pipeline import CompanySnapshot


def _fmt_number(value: float | None, pct: bool = False) -> str:
    if value is None:
        return "N/A"
    if pct:
        return f"{value * 100:.2f}%"
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    return f"{value:,.2f}"


def business_overview(subject: CompanySnapshot) -> str:
    return (
        f"### 1) Business Overview\n"
        f"{subject.company_name} ({subject.ticker}) operates in the "
        f"{subject.sector or 'undisclosed sector'} sector and "
        f"{subject.industry or 'undisclosed industry'} segment. "
        f"The company has an estimated market capitalization of {_fmt_number(subject.market_cap)}."
    )


def financial_performance(subject: CompanySnapshot, financial_trend: pd.DataFrame) -> str:
    summary = (
        f"Key ratio snapshot: P/E {_fmt_number(subject.trailing_pe)}, "
        f"P/B {_fmt_number(subject.price_to_book)}, "
        f"Revenue Growth {_fmt_number(subject.revenue_growth, pct=True)}, "
        f"ROE {_fmt_number(subject.return_on_equity, pct=True)}, "
        f"Debt/Equity {_fmt_number(subject.debt_to_equity)}."
    )

    if financial_trend.empty:
        trend_text = "Historical income statement trend was unavailable from source data."
    else:
        latest_year = int(financial_trend.index.max())
        latest = financial_trend.loc[latest_year]
        trend_text = (
            f"For {latest_year}, reported values include Total Revenue "
            f"{_fmt_number(latest.get('Total Revenue'))}, Operating Income "
            f"{_fmt_number(latest.get('Operating Income'))}, and Net Income "
            f"{_fmt_number(latest.get('Net Income'))}."
        )

    return f"### 2) Financial Performance\n{summary}\n{trend_text}"


def peer_comparison(subject: CompanySnapshot, peers_table: pd.DataFrame) -> str:
    if peers_table.empty:
        return "### 3) Peer Comparison\nPeer data could not be retrieved."

    cols = ["Ticker", "P/E", "P/B", "Revenue Growth", "ROE", "Debt/Equity"]
    available_cols = [c for c in cols if c in peers_table.columns]
    preview = peers_table[available_cols].to_markdown(index=False)
    return f"### 3) Peer Comparison\nComparative valuation and performance snapshot:\n\n{preview}"


def key_risks(subject: CompanySnapshot) -> str:
    risks = [
        "Macro sensitivity may affect demand and valuation multiples.",
        "Earnings variability can arise from input costs, pricing pressure, or FX movement.",
        "Regulatory and compliance developments may impact operations and disclosures.",
    ]

    if subject.debt_to_equity and subject.debt_to_equity > 150:
        risks.append("Leverage appears elevated on Debt/Equity basis and warrants balance-sheet monitoring.")

    return "### 4) Key Risks\n" + "\n".join(f"- {r}" for r in risks)


def recommendation_logic(subject: CompanySnapshot) -> str:
    score = 0
    rationale = []

    if subject.revenue_growth is not None:
        if subject.revenue_growth > 0.10:
            score += 1
            rationale.append("Revenue growth is above 10%.")
        else:
            rationale.append("Revenue growth is moderate/low.")

    if subject.return_on_equity is not None:
        if subject.return_on_equity > 0.15:
            score += 1
            rationale.append("ROE is above 15%.")
        else:
            rationale.append("ROE is not above 15%.")

    if subject.debt_to_equity is not None:
        if subject.debt_to_equity < 100:
            score += 1
            rationale.append("Leverage appears manageable.")
        else:
            rationale.append("Leverage appears elevated.")

    label = "Watchlist / Neutral"
    if score >= 3:
        label = "Constructive"
    elif score <= 1:
        label = "Cautious"

    text = (
        "### 5) Recommendation Logic\n"
        f"Rule-based outcome: **{label}** (score={score}/3).\n"
        "This model is heuristic and should be supplemented with analyst judgment.\n"
        "Rationale:\n"
        + "\n".join(f"- {r}" for r in rationale)
    )
    return neutral_language_wrap(text)


def build_report(
    subject: CompanySnapshot,
    financial_trend: pd.DataFrame,
    peers_table: pd.DataFrame,
    compliance_note: str,
) -> str:
    sections = [
        f"# Automated Equity Research Report: {subject.company_name} ({subject.ticker})",
        business_overview(subject),
        financial_performance(subject, financial_trend),
        peer_comparison(subject, peers_table),
        key_risks(subject),
        recommendation_logic(subject),
        "---",
        compliance_note,
    ]
    return "\n\n".join(sections) + "\n"
