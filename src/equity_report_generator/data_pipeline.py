from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd
import yfinance as yf


@dataclass
class CompanySnapshot:
    ticker: str
    company_name: str
    sector: str | None
    industry: str | None
    market_cap: float | None
    trailing_pe: float | None
    price_to_book: float | None
    revenue_growth: float | None
    return_on_equity: float | None
    debt_to_equity: float | None
    current_price: float | None
    target_mean_price: float | None


def _safe_info_value(info: dict, key: str):
    value = info.get(key)
    if value in (None, ""):
        return None
    return value


def fetch_company_snapshot(ticker: str, company_name: str | None = None) -> CompanySnapshot:
    stock = yf.Ticker(ticker)
    info = stock.info or {}

    return CompanySnapshot(
        ticker=ticker.upper(),
        company_name=company_name or _safe_info_value(info, "longName") or ticker.upper(),
        sector=_safe_info_value(info, "sector"),
        industry=_safe_info_value(info, "industry"),
        market_cap=_safe_info_value(info, "marketCap"),
        trailing_pe=_safe_info_value(info, "trailingPE"),
        price_to_book=_safe_info_value(info, "priceToBook"),
        revenue_growth=_safe_info_value(info, "revenueGrowth"),
        return_on_equity=_safe_info_value(info, "returnOnEquity"),
        debt_to_equity=_safe_info_value(info, "debtToEquity"),
        current_price=_safe_info_value(info, "currentPrice"),
        target_mean_price=_safe_info_value(info, "targetMeanPrice"),
    )


def fetch_financial_trend(ticker: str) -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    income = stock.financials
    if income is None or income.empty:
        return pd.DataFrame()

    income = income.T.sort_index()
    needed_cols = [c for c in ["Total Revenue", "Operating Income", "Net Income"] if c in income.columns]
    if not needed_cols:
        return pd.DataFrame()

    result = income[needed_cols].copy()
    result.index = pd.to_datetime(result.index).year
    return result


def to_metric_table(snapshots: Iterable[CompanySnapshot]) -> pd.DataFrame:
    rows = []
    for s in snapshots:
        rows.append(
            {
                "Ticker": s.ticker,
                "Company": s.company_name,
                "Market Cap": s.market_cap,
                "P/E": s.trailing_pe,
                "P/B": s.price_to_book,
                "Revenue Growth": s.revenue_growth,
                "ROE": s.return_on_equity,
                "Debt/Equity": s.debt_to_equity,
            }
        )
    return pd.DataFrame(rows)
