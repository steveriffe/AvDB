"""
AvDB Executive Formatting Helpers
Ensures rigorous numeric discipline, discrete integer counts, and clean financial notation
across all dashboard lenses and analytical marts.
"""
from typing import Any, Union
import pandas as pd


def fmt_integer(val: Any) -> str:
    """
    Formats discrete counts (routes, aircraft, airlines, models, direct destinations).
    Strictly avoids fractional decimals (e.g. renders 5,704 instead of 5,704.0).
    """
    if val is None or pd.isna(val):
        return "0"
    try:
        num = float(val)
        return f"{int(round(num)):,}"
    except (ValueError, TypeError):
        return str(val)


def fmt_volume(val: Any) -> str:
    """
    Formats large passenger, seat, and departure volumes cleanly.
    e.g. 1.78M instead of 1784.8K, 450K instead of 450.0K, 850 for smaller counts.
    """
    if val is None or pd.isna(val):
        return "0"
    try:
        num = float(val)
        abs_n = abs(num)
        if abs_n >= 1_000_000_000:
            return f"{num / 1e9:.2f}B"
        elif abs_n >= 1_000_000:
            return f"{num / 1e6:.2f}M"
        elif abs_n >= 100_000:
            return f"{num / 1e3:.0f}K"
        elif abs_n >= 10_000:
            return f"{num / 1e3:.1f}K"
        else:
            return f"{int(round(num)):,}"
    except (ValueError, TypeError):
        return str(val)


def fmt_currency(val: Any, decimals: int = 0, compact: bool = False) -> str:
    """
    Formats currency values cleanly ($411, $0.1845).
    If compact=True or val >= 100M, renders standard financial notation ($29.68B, $45.2M).
    """
    if val is None or pd.isna(val) or val == 0:
        return "—"
    try:
        n = float(val)
        abs_n = abs(n)
        if compact or abs_n >= 100_000_000:
            if abs_n >= 1_000_000_000:
                return f"${n / 1e9:.2f}B"
            elif abs_n >= 1_000_000:
                return f"${n / 1e6:.2f}M"
            elif abs_n >= 100_000:
                return f"${n / 1e3:.0f}K"
        if decimals == 0:
            return f"${int(round(n)):,}"
        return f"${n:,.{decimals}f}"
    except (ValueError, TypeError):
        return str(val)


def fmt_percent(val: Any, decimals: int = 1) -> str:
    """Formats percentage values cleanly (83.7%)."""
    if val is None or pd.isna(val):
        return "—"
    try:
        return f"{float(val):.{decimals}f}%"
    except (ValueError, TypeError):
        return str(val)
