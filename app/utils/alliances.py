"""
AvDB Airline Alliance & Branding Utility Layer
Enables temporal alliance lookups, carrier alliance timelines, and logo resolutions.
"""
from typing import Optional, List, Dict, Any
from app.data.ref_alliances import ALLIANCES_METADATA, CARRIER_LOGOS, ALLIANCE_MEMBERSHIPS


def get_carrier_alliance(carrier_code: str, year: int) -> Optional[Dict[str, Any]]:
    """
    Returns the alliance for a carrier during a specific calendar year,
    taking into account join and exit dates.
    """
    c = carrier_code.strip().upper()
    target_date = f"{year}-07-01"  # Mid-year reference

    for m in ALLIANCE_MEMBERSHIPS:
        if m["carrier_code"] == c:
            join = m["join_date"] or "1900-01-01"
            exit_d = m["exit_date"] or "2099-12-31"
            if join <= target_date <= exit_d:
                return m
    return None


def get_alliance_carriers(alliance_name: str, year: int) -> List[str]:
    """
    Returns list of member carrier codes (IATA) belonging to an alliance in a specific year.
    """
    target_date = f"{year}-07-01"
    carriers = set()
    norm = alliance_name.strip().lower()

    for m in ALLIANCE_MEMBERSHIPS:
        if m["alliance_name"].strip().lower() == norm:
            join = m["join_date"] or "1900-01-01"
            exit_d = m["exit_date"] or "2099-12-31"
            if join <= target_date <= exit_d:
                carriers.add(m["carrier_code"])
    return sorted(list(carriers))


def get_all_alliances_for_year(year: int) -> List[Dict[str, Any]]:
    """
    Returns all active alliances and their member count for a given year.
    """
    target_date = f"{year}-07-01"
    res = []
    for a_name, a_info in ALLIANCES_METADATA.items():
        found = a_info["founded_date"] or "1900-01-01"
        diss = a_info["dissolved_date"] or "2099-12-31"
        if found <= target_date <= diss:
            members = get_alliance_carriers(a_name, year)
            res.append({
                "alliance_name": a_name,
                "alliance_id": a_info["alliance_id"],
                "logo_url": a_info["logo_url"],
                "member_count": len(members),
                "members": members,
                "website": a_info["website"]
            })
    return res


def get_carrier_logo_url(carrier_code: str) -> Optional[str]:
    """
    Returns verified SVG/PNG brand logo URL for a carrier code.
    """
    c = carrier_code.strip().upper()
    return CARRIER_LOGOS.get(c, None)


def get_carrier_alliance_timeline(carrier_code: str) -> List[Dict[str, Any]]:
    """
    Returns full chronological history of alliance memberships and transitions for an airline.
    """
    c = carrier_code.strip().upper()
    timeline = [m for m in ALLIANCE_MEMBERSHIPS if m["carrier_code"] == c]
    return sorted(timeline, key=lambda x: x["join_date"])
