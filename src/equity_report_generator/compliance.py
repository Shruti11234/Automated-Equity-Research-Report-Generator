from __future__ import annotations


def compliance_footer() -> str:
    return (
        "**Compliance Note:** This report is automatically generated from publicly available data and "
        "is intended for educational and analytical purposes only. It should not be construed as "
        "personalized investment advice, a solicitation, or a recommendation to buy/sell securities."
    )


def neutral_language_wrap(text: str) -> str:
    replacements = {
        "will definitely": "may",
        "guaranteed": "not assured",
        "best stock": "relatively favorable setup",
        "must buy": "requires independent due diligence",
    }

    normalized = text
    for source, target in replacements.items():
        normalized = normalized.replace(source, target)
    return normalized
