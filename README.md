# Automated Equity Research Report Generator

A Python-based system that generates a structured equity research report from a single company name/ticker.

## What it does

The generator creates the following sections automatically:

1. **Business Overview**
2. **Financial Performance**
3. **Peer Comparison**
4. **Key Risks**
5. **Recommendation Logic**

The writing style is intentionally compliance-oriented and avoids promotional language.

## Why this project is strong

- Demonstrates **Research Analyst + AI** alignment.
- Bridges raw market data, financial interpretation, and structured report writing.
- Suitable for NISM-style report structuring and interview case discussions.

## Project structure

```text
src/equity_report_generator/
  data_pipeline.py       # pulls and normalizes company + peer data
  report_sections.py     # section generation + recommendation logic
  compliance.py          # compliance-style helper rules
  cli.py                 # command line entry point
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Generate a report using a ticker symbol (recommended):

```bash
python -m equity_report_generator.cli --company "Apple Inc" --ticker AAPL --peers MSFT GOOGL AMZN --output reports/aapl_report.md
```

Generate a report without manually passing peers (auto peer fallback from sector ETF proxies):

```bash
python -m equity_report_generator.cli --company "Infosys" --ticker INFY --output reports/infy_report.md
```

## Notes

- Data source: `yfinance`.
- If some values are unavailable, the report explicitly discloses missing data.
- This project is educational and not investment advice.

## Resume title

**Automated Equity Research Report Generator**

