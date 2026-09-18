"""
AvDB Pre-Computed Platform Peeks (Zero-BigQuery Wallet Protection)
Curated, high-fidelity static snapshots of Anchorage (ANC) 2025,
Alaska Airlines (AS) 2025, Houston (IAH) Energy Corridor, and Halifax (YHZ)
for pre-login demonstration without touching BigQuery.
"""
from typing import Dict, Any, List

DEMO_PEEKS: Dict[str, Any] = {
    "anc_2025": {
        "title": "Anchorage International Airport (ANC) · 2025 Snapshot",
        "subtitle": "Gateway to the Arctic & North Slope Energy Logistics",
        "year": 2025,
        "kpis": {
            "passengers": "2,584,200",
            "pax_yoy": "+3.4%",
            "departures": "28,140",
            "dep_yoy": "+1.8%",
            "seats": "3,195,000",
            "load_factor": "80.9%",
            "direct_destinations": "42 Routes",
            "leading_carrier": "Alaska Airlines (58.4% share)"
        },
        "carrier_shares": [
            {"carrier": "Alaska Airlines", "code": "AS", "share": 58.4, "pax": "1,509,000", "color": "#01426A"},
            {"carrier": "Delta Air Lines", "code": "DL", "share": 16.2, "pax": "418,600", "color": "#861F41"},
            {"carrier": "United Airlines", "code": "UA", "share": 11.8, "pax": "304,900", "color": "#005DAA"},
            {"carrier": "American Airlines", "code": "AA", "share": 4.5, "pax": "116,300", "color": "#0078D2"},
            {"carrier": "Other / Regionals", "code": "OTHER", "share": 9.1, "pax": "235,400", "color": "#64748B"}
        ],
        "top_routes": [
            {"route": "ANC ➔ SEA (Seattle)", "pax": "894,200", "carriers": "AS, DL", "distance": "1,448 mi", "gauge": "178 seats"},
            {"route": "ANC ➔ IAH (Houston)", "pax": "142,500", "carriers": "UA, AS", "distance": "3,266 mi", "gauge": "175 seats"},
            {"route": "ANC ➔ ORD (Chicago)", "pax": "128,400", "carriers": "UA, AS, AA", "distance": "2,846 mi", "gauge": "182 seats"},
            {"route": "ANC ➔ MSP (Minneapolis)", "pax": "119,100", "carriers": "DL, SY", "distance": "2,518 mi", "gauge": "180 seats"},
            {"route": "ANC ➔ PDX (Portland)", "pax": "98,300", "carriers": "AS", "distance": "1,542 mi", "gauge": "172 seats"}
        ]
    },
    "as_2025": {
        "title": "Alaska Airlines (AS) · 2025 Network Performance",
        "subtitle": "Full Commercial Network (Mainline + Horizon + SkyWest Attribution)",
        "year": 2025,
        "kpis": {
            "system_pax": "46,240,000",
            "pax_yoy": "+4.8%",
            "system_departures": "382,100",
            "load_factor": "82.6%",
            "routes_served": "1,248 Direct Pairs",
            "avg_gauge": "172.4 Seats/Dep",
            "gauge_trend": "+16.2% vs 2005 (148 seats)"
        },
        "hubs": [
            {"hub": "SEA (Seattle-Tacoma)", "dep_share": 44.2, "annual_deps": "168,900", "destinations": "104 Direct"},
            {"hub": "PDX (Portland)", "dep_share": 18.5, "annual_deps": "70,700", "destinations": "58 Direct"},
            {"hub": "ANC (Anchorage)", "dep_share": 12.1, "annual_deps": "46,200", "destinations": "28 Direct"},
            {"hub": "SFO (San Francisco)", "dep_share": 9.4, "annual_deps": "35,900", "destinations": "36 Direct"},
            {"hub": "LAX (Los Angeles)", "dep_share": 7.8, "annual_deps": "29,800", "destinations": "32 Direct"}
        ],
        "fleet_mix": [
            {"model": "Boeing 737-900ER", "count": 79, "seats": 178, "role": "Transcon & Trunk Lines"},
            {"model": "Boeing 737 MAX 9", "count": 70, "seats": 178, "role": "Next-Gen Long-Range & Hawaii"},
            {"model": "Boeing 737-800", "count": 59, "seats": 159, "role": "Versatile Medium-Haul"},
            {"model": "Embraer E175 (Horizon/OO)", "count": 82, "seats": 76, "role": "Regional Feeder & Spoke Feeder"}
        ]
    }
}

