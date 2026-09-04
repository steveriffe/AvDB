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


ALLIANCE_COLORS = {
    "Star Alliance": "#C5A059",
    "oneworld": "#1A2C80",
    "SkyTeam": "#0090DA",
    "Wings Alliance": "#4A90E2",
    "Qualiflyer": "#D0021B",
    "Independent / Unaligned": "#8E8E93"
}


def get_airport_alliance_breakdown(df_carriers, year: int):
    """
    Aggregates airport carrier breakdown by global alliance for a given year.
    Returns DataFrame with alliance_name, total_seats, operational_passengers, seat_share_pct.
    """
    import pandas as pd
    if df_carriers is None or df_carriers.empty:
        return pd.DataFrame()
    
    rows = []
    for _, r in df_carriers.iterrows():
        c_code = str(r.get("unique_carrier", "")).strip().upper()
        a_info = get_carrier_alliance(c_code, year)
        a_name = a_info["alliance_name"] if a_info else "Independent / Unaligned"
        
        rows.append({
            "carrier_code": c_code,
            "carrier_name": r.get("carrier_name", c_code),
            "alliance_name": a_name,
            "total_seats": r.get("total_seats", 0),
            "operational_passengers": r.get("operational_passengers", 0),
            "departures_performed": r.get("departures_performed", 0)
        })
    
    df_raw = pd.DataFrame(rows)
    if df_raw.empty:
        return pd.DataFrame()
        
    agg = df_raw.groupby("alliance_name").agg(
        total_seats=("total_seats", "sum"),
        operational_passengers=("operational_passengers", "sum"),
        departures_performed=("departures_performed", "sum"),
        carriers=("carrier_code", lambda x: ", ".join(sorted(x.unique())))
    ).reset_index()
    
    tot_seats = agg["total_seats"].sum()
    agg["seat_share_pct"] = (agg["total_seats"] / tot_seats * 100).round(1) if tot_seats > 0 else 0
    tot_pax = agg["operational_passengers"].sum()
    agg["pax_share_pct"] = (agg["operational_passengers"] / tot_pax * 100).round(1) if tot_pax > 0 else 0
    
    return agg.sort_values(by="total_seats", ascending=False)

