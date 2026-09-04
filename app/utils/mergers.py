"""
AvDB Airline Merger & Corporate Lineage Utilities
Provides lookup functions, predecessor/successor lineage resolutions,
and HTML badge helpers for UI display.
"""
from typing import List, Dict, Any, Optional
from app.data.ref_mergers import AIRLINE_MERGERS, get_all_airline_mergers


def get_merger_as_predecessor(carrier_code: str) -> Optional[Dict[str, Any]]:
    """Returns the merger record where carrier_code was acquired / merged."""
    code = carrier_code.strip().upper()
    for m in AIRLINE_MERGERS:
        if m["predecessor_code"] == code:
            return m
    return None


def get_mergers_as_successor(carrier_code: str) -> List[Dict[str, Any]]:
    """Returns all mergers where carrier_code was the acquiring / surviving airline."""
    code = carrier_code.strip().upper()
    return [m for m in AIRLINE_MERGERS if m["successor_code"] == code]


def get_all_ancestor_codes(carrier_code: str) -> List[str]:
    """
    Recursively discovers all historic airline codes absorbed into carrier_code.
    e.g. AA -> [US, HP, QQ, TW]
    """
    code = carrier_code.strip().upper()
    ancestors = []
    direct = [m["predecessor_code"] for m in AIRLINE_MERGERS if m["successor_code"] == code]
    for a in direct:
        ancestors.append(a)
        # Recurse for multi-tier mergers (e.g. HP -> US -> AA)
        ancestors.extend(get_all_ancestor_codes(a))
    return list(dict.fromkeys(ancestors))  # Preserves order and uniqueness


def get_ultimate_successor(carrier_code: str) -> Optional[Dict[str, Any]]:
    """
    Returns the ultimate surviving carrier for a historic predecessor code.
    e.g. HP -> AA (via US)
    """
    code = carrier_code.strip().upper()
    curr_m = get_merger_as_predecessor(code)
    if not curr_m:
        return None
    
    # Follow chain if successor was also acquired
    visited = {code}
    while True:
        succ_code = curr_m["successor_code"]
        if succ_code in visited:
            break
        visited.add(succ_code)
        next_m = get_merger_as_predecessor(succ_code)
        if not next_m:
            return curr_m
        curr_m = next_m
    return curr_m


def is_historical_carrier(carrier_code: str) -> bool:
    """Checks if the carrier has been absorbed into another carrier."""
    return get_merger_as_predecessor(carrier_code) is not None


def format_merger_lineage_html(carrier_code: str) -> str:
    """
    Generates rich, clean HTML summary of airline corporate lineage for Streamlit.
    """
    code = carrier_code.strip().upper()
    
    # Check if this carrier was acquired
    pred_merger = get_merger_as_predecessor(code)
    if pred_merger:
        succ_name = pred_merger["successor_name"]
        succ_code = pred_merger["successor_code"]
        cutover = pred_merger.get("cutover_year", "")
        return (
            f"<div style='background: rgba(255, 159, 10, 0.12); border: 1px solid rgba(255, 159, 10, 0.4); "
            f"border-radius: 8px; padding: 10px 14px; margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between;'>"
            f"<div>"
            f"<span style='color: #FF9F0A; font-weight: 700; font-size: 13px;'>📜 Historical Airline Lineage</span><br/>"
            f"<span style='color: #EBEBF5; font-size: 12px;'><b>{pred_merger['predecessor_name']} ({code})</b> was merged into "
            f"<b>{succ_name} ({succ_code})</b> in {cutover}.</span>"
            f"</div>"
            f"</div>"
        )
    
    # Check if this carrier absorbed other airlines
    absorbed = get_mergers_as_successor(code)
    if absorbed:
        predecessor_badges = []
        for m in absorbed:
            p_code = m["predecessor_code"]
            p_name = m["predecessor_name"]
            predecessor_badges.append(f"<span style='background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; font-weight: 600;'>{p_code} ({p_name})</span>")
        
        badges_str = " ".join(predecessor_badges)
        return (
            f"<div style='background: rgba(10, 132, 255, 0.08); border: 1px solid rgba(10, 132, 255, 0.25); "
            f"border-radius: 8px; padding: 8px 12px; margin-bottom: 14px; font-size: 12px; color: #EBEBF5;'>"
            f"<b>Corporate Lineage</b>: Absorbed historical networks of {badges_str}."
            f"</div>"
        )
    
    return ""


def enrich_historical_route_service(
    origin: str, 
    dest: str, 
    last_year: Optional[Any], 
    carriers: Optional[str]
) -> str:
    """
    Synthesizes historical route service with merger lineage.
    E.g. ANC -> DTW previously flown by DL is tagged as '🔄 Flown until 2024 (NW/DL)'.
    """
    import pandas as pd
    if last_year is None or pd.isna(last_year):
        return "✨ Never Flown Nonstop"
    
    try:
        yr = int(last_year)
    except (ValueError, TypeError):
        return "✨ Never Flown Nonstop"
        
    carrier_tokens = [c.strip().upper() for c in str(carriers).split('/') if c.strip()]
    enriched_tokens = []
    
    hub_overrides = {
        ("DL", "DTW"): "NW/DL",
        ("DL", "MSP"): "NW/DL",
        ("DL", "MEM"): "NW/DL",
        ("UA", "IAH"): "CO/UA",
        ("UA", "EWR"): "CO/UA",
        ("UA", "CLE"): "CO/UA",
        ("UA", "GUM"): "CO/UA",
        ("AA", "CLT"): "US/AA",
        ("AA", "PHL"): "US/AA",
        ("AA", "PHX"): "HP/US/AA",
        ("AA", "LAS"): "HP/US/AA",
        ("AA", "RNO"): "QQ/AA",
        ("AA", "SJC"): "QQ/AA",
        ("AA", "STL"): "TW/AA",
        ("AS", "HNL"): "HA/AS",
        ("AS", "OGG"): "HA/AS",
        ("AS", "KOA"): "HA/AS",
        ("AS", "SFO"): "VX/AS",
        ("WN", "ATL"): "FL/WN",
        ("F9", "MKE"): "YX/F9",
    }
    
    for c in carrier_tokens:
        matched = False
        for (carrier, hub), tag in hub_overrides.items():
            if c == carrier and (origin == hub or dest == hub):
                enriched_tokens.append(tag)
                matched = True
                break
        if not matched:
            # Check dynamic hub absorption in mergers catalog
            for m in get_mergers_as_successor(c):
                hubs = m.get("hubs_absorbed", [])
                if origin in hubs or dest in hubs:
                    enriched_tokens.append(f"{m['predecessor_code']}/{c}")
                    matched = True
                    break
        if not matched:
            enriched_tokens.append(c)
            
    # Deduplicate while preserving order
    unique_tokens = list(dict.fromkeys(enriched_tokens))
    carrier_str = "/".join(unique_tokens) if unique_tokens else "Unknown"
    return f"🔄 Flown until {yr} ({carrier_str})"

