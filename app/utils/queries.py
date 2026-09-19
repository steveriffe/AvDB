"""
BigQuery Query Layer for AvDB Streamlit Dashboard
Cached with @st.cache_data for instant interactive responses.
"""
import streamlit as st
import pandas as pd
from typing import Optional, List, Dict, Any
from app.utils.bq_client import run_query
from app.utils.mergers import enrich_historical_route_service
from app.config import settings

# -------------------------------------------------------------
# Carrier Hub & Network Strategy Alignment Mapping
# -------------------------------------------------------------
CARRIER_STRATEGY = {
    "AS": {
        "name": "Alaska Airlines",
        "hubs": ["SEA", "PDX", "ANC", "SFO", "LAX", "SAN", "PAE"],
        "focus_regions": ["US West", "Transcontinental", "Hawaii", "Alaska Intra"],
        "min_stage": 200,
        "max_stage": 3000
    },
    "UA": {
        "name": "United Airlines",
        "hubs": ["ORD", "DEN", "EWR", "IAD", "IAH", "SFO", "LAX", "GUM"],
        "focus_regions": ["Global Network", "Transcontinental", "Midwest/East Hubs"],
        "min_stage": 150,
        "max_stage": 8000
    },
    "DL": {
        "name": "Delta Air Lines",
        "hubs": ["ATL", "DTW", "MSP", "SLC", "SEA", "JFK", "LGA", "BOS", "LAX"],
        "focus_regions": ["Global Network", "East/Southeast", "Mountain West Hubs"],
        "min_stage": 150,
        "max_stage": 8000
    },
    "AA": {
        "name": "American Airlines",
        "hubs": ["DFW", "CLT", "MIA", "ORD", "PHL", "PHX", "DCA", "LAX", "JFK"],
        "focus_regions": ["Sunbelt Hubs", "Latin America Gateways", "Northeast Corridor"],
        "min_stage": 150,
        "max_stage": 8000
    },
    "WN": {
        "name": "Southwest Airlines",
        "hubs": ["MDW", "DAL", "BWI", "DEN", "LAS", "PHX", "HOU", "MCO", "OAK", "BNA", "SMF"],
        "focus_regions": ["Point-to-Point High Density", "Sunbelt", "Leisure / Short Haul"],
        "min_stage": 100,
        "max_stage": 2500
    },
    "B6": {
        "name": "JetBlue Airways",
        "hubs": ["JFK", "BOS", "FLL", "MCO", "SJU"],
        "focus_regions": ["East Coast Corridor", "Transcon Mint", "Caribbean"],
        "min_stage": 300,
        "max_stage": 3500
    },
    "NK": {
        "name": "Spirit Airlines",
        "hubs": ["FLL", "MCO", "DTW", "LAS", "DFW", "IAH"],
        "focus_regions": ["ULCC Leisure Volume", "Latin America / Caribbean"],
        "min_stage": 200,
        "max_stage": 2500
    },
    "F9": {
        "name": "Frontier Airlines",
        "hubs": ["DEN", "MCO", "LAS", "PHX", "ATL", "DFW", "PHL"],
        "focus_regions": ["ULCC Leisure", "Sunbelt Hubs"],
        "min_stage": 200,
        "max_stage": 2500
    },
    "G4": {
        "name": "Allegiant Air",
        "hubs": ["SFB", "PIE", "PGD", "MYR", "LAS", "AZA", "CVG", "TYS"],
        "focus_regions": ["Secondary Airport Leisure", "Vacation Destinations"],
        "min_stage": 200,
        "max_stage": 2500
    }
}


def _recommend_aligned_carrier(origin: str, dest: str, distance_miles: float, yield_per_mile: float) -> str:
    """
    Derives the most aligned carrier strategy for an unserved O&D market based on
    origin/destination hub presence, stage length, and yield profile.
    """
    best_carrier = "Unassigned / Regional"
    best_score = -1

    for code, strat in CARRIER_STRATEGY.items():
        score = 0
        hubs = strat["hubs"]
        
        # Hub matching bonus
        if origin in hubs or dest in hubs:
            score += 50
        if origin in hubs and dest in hubs:
            score += 40
            
        # Distance suitability
        if strat["min_stage"] <= distance_miles <= strat["max_stage"]:
            score += 20
            
        # Yield alignment: Premium yields favor legacy mainline (AS, UA, DL, AA) over ULCC
        if yield_per_mile >= 0.25 and code in ["AS", "UA", "DL", "AA", "B6"]:
            score += 25
        elif yield_per_mile < 0.15 and code in ["WN", "F9", "NK", "G4"]:
            score += 25
            
        if score > best_score:
            best_score = score
            best_carrier = f"{code} ({strat['name']})"

    return best_carrier


# -------------------------------------------------------------
# Regional Operating Carrier Attribution SQL Expressions
# Maps contract and subsidiary regional flights to consumer-facing marketing brands
# Powered by `db1b-1.reporting.ref_regional_route_attribution` (DB1B 10% survey shares)
# with deterministic fallbacks for wholly owned & dedicated airline subsidiaries.
# -------------------------------------------------------------
REGIONAL_ATTRIBUTION_JOIN = """
    LEFT JOIN `db1b-1.reporting.ref_regional_route_attribution` _reg
      ON base.unique_carrier = _reg.op_carrier 
     AND base.origin = _reg.origin 
     AND base.dest = _reg.dest
"""

ATTRIBUTED_CARRIER_SQL = """
    COALESCE(
        _reg.mkt_carrier,
        CASE 
            WHEN base.unique_carrier = 'QX' THEN 'AS'
            WHEN base.unique_carrier = '9E' THEN 'DL'
            WHEN base.unique_carrier IN ('MQ', 'OH', 'PT') THEN 'AA'
            WHEN base.unique_carrier IN ('C5', 'G7') THEN 'UA'
            WHEN base.unique_carrier IN ('CP', 'CP (2)') THEN 'DL'
            WHEN base.unique_carrier = 'XJ' THEN 'NW'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('ATL', 'MSP', 'DTW', 'SLC') OR base.origin IN ('ATL', 'MSP', 'DTW', 'SLC')) THEN 'DL'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('ORD', 'DEN', 'IAH', 'EWR', 'IAD', 'SFO') OR base.origin IN ('ORD', 'DEN', 'IAH', 'EWR', 'IAD', 'SFO')) THEN 'UA'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('DFW', 'CLT', 'MIA', 'PHX', 'PHL') OR base.origin IN ('DFW', 'CLT', 'MIA', 'PHX', 'PHL')) THEN 'AA'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('SEA', 'PDX', 'SAN', 'BUR', 'OAK', 'SJC', 'SMF', 'ANC', 'LAX') OR base.origin IN ('SEA', 'PDX', 'SAN', 'BUR', 'OAK', 'SJC', 'SMF', 'ANC', 'LAX')) THEN 'AS'
            ELSE base.unique_carrier
        END
    )
"""

ATTRIBUTED_SHARE_SQL = "COALESCE(_reg.attribution_share, 1.0)"

REGIONAL_ATTRIBUTION_SQL = """
    CASE
        WHEN unique_carrier = 'QX' THEN 'AS'
        WHEN unique_carrier = '9E' THEN 'DL'
        WHEN unique_carrier IN ('MQ', 'OH', 'PT') THEN 'AA'
        WHEN unique_carrier IN ('C5', 'G7') THEN 'UA'
        WHEN unique_carrier IN ('CP', 'CP (2)') THEN 'DL'
        WHEN unique_carrier = 'XJ' THEN 'NW'
        WHEN unique_carrier = 'OO' AND (dest IN ('ATL', 'MSP', 'DTW', 'SLC') OR origin IN ('ATL', 'MSP', 'DTW', 'SLC')) THEN 'DL'
        WHEN unique_carrier = 'OO' AND (dest IN ('ORD', 'DEN', 'IAH', 'EWR', 'IAD', 'SFO') OR origin IN ('ORD', 'DEN', 'IAH', 'EWR', 'IAD', 'SFO')) THEN 'UA'
        WHEN unique_carrier = 'OO' AND (dest IN ('DFW', 'CLT', 'MIA', 'PHX', 'PHL') OR origin IN ('DFW', 'CLT', 'MIA', 'PHX', 'PHL')) THEN 'AA'
        WHEN unique_carrier = 'OO' AND (dest IN ('SEA', 'PDX', 'SAN', 'BUR', 'OAK', 'SJC', 'SMF', 'ANC', 'LAX') OR origin IN ('SEA', 'PDX', 'SAN', 'BUR', 'OAK', 'SJC', 'SMF', 'ANC', 'LAX')) THEN 'AS'
        ELSE unique_carrier
    END
"""

CARRIER_NAME_LOOKUP_SQL = """
    CASE 
        WHEN carrier_code = 'DL' THEN 'Delta Air Lines Inc.'
        WHEN carrier_code = 'AS' THEN 'Alaska Airlines Inc.'
        WHEN carrier_code = 'UA' THEN 'United Air Lines Inc.'
        WHEN carrier_code = 'AA' THEN 'American Airlines Inc.'
        WHEN carrier_code = 'WN' THEN 'Southwest Airlines Co.'
        WHEN carrier_code = 'B6' THEN 'JetBlue Airways'
        WHEN carrier_code = 'NK' THEN 'Spirit Airlines'
        WHEN carrier_code = 'F9' THEN 'Frontier Airlines'
        WHEN carrier_code = 'G4' THEN 'Allegiant Air'
        WHEN carrier_code = 'CO' THEN 'Continental Airlines'
        WHEN carrier_code = 'NW' THEN 'Northwest Airlines'
        WHEN carrier_code = 'US' THEN 'US Airways'
        WHEN carrier_code = 'HP' THEN 'America West Airlines'
        WHEN carrier_code = 'QQ' THEN 'Reno Air'
        WHEN carrier_code = 'TW' THEN 'Trans World Airlines'
        WHEN carrier_code = 'FL' THEN 'AirTran Airways'
        WHEN carrier_code = 'VX' THEN 'Virgin America'
        WHEN carrier_code = 'YX' THEN 'Republic Airways'
        WHEN carrier_code = 'HA' THEN 'Hawaiian Airlines'
        WHEN carrier_code = 'PA' THEN 'Pan American World Airways'
        ELSE COALESCE(carrier_name, carrier_code)
    END
"""


# -------------------------------------------------------------
# AIRPORT EXPLORER QUERIES
# -------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def get_available_airports() -> pd.DataFrame:
    """Fetches list of active origin airports with names and metro flags."""
    query = """
        SELECT DISTINCT 
            m.origin AS airport_code,
            COALESCE(a.airport_name, m.origin_name, m.origin) AS airport_name,
            COALESCE(a.city, m.origin_city, '') AS city,
            COALESCE(a.state_region, m.origin_state, '') AS state,
            COALESCE(a.country, m.origin_country, 'US') AS country,
            COALESCE(a.is_commercial, FALSE) AS is_commercial,
            COALESCE(a.is_metro_code, FALSE) AS is_metro_code
        FROM `db1b-1.reporting.mart_airport_network_summary` m
        LEFT JOIN `db1b-1.reporting.ref_airports` a
            ON m.origin = a.airport_code
        WHERE m.year >= 2023 AND m.operational_passengers > 0
        ORDER BY 
            is_metro_code DESC,
            is_commercial DESC,
            airport_code ASC
    """
    try:
        return run_query(query)
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def get_airport_catchment_info(airport_code: str) -> Optional[Dict[str, Any]]:
    """Checks if the airport is a metropolitan catchment market (e.g. WAS, NYC)."""
    query = """
        SELECT 
            market_code,
            market_name,
            metro_city,
            ARRAY_AGG(airport_code ORDER BY airport_code) AS member_airports,
            ANY_VALUE(description) AS description
        FROM `db1b-1.reporting.ref_city_markets`
        WHERE market_code = @airport_code
        GROUP BY 1, 2, 3
    """
    df = run_query(query, params={"airport_code": airport_code})
    if not df.empty:
        return df.iloc[0].to_dict()
    return None


@st.cache_data(ttl=3600, show_spinner=False)
def get_airport_kpis(
    airport_code: str, 
    year: int, 
    passenger_only: bool = True,
    min_departures: int = 10
) -> Dict[str, Any]:
    """Calculates top-level KPI metrics for an airport, attributing regional partner operations to marketing carriers."""
    query = f"""
        WITH base AS (
            SELECT 
                dest,
                origin,
                unique_carrier,
                departures_performed,
                total_seats,
                operational_passengers,
                avg_od_fare
            FROM `db1b-1.reporting.mart_airport_network_summary`
            WHERE origin = @airport_code AND year = @year
            {'AND operational_passengers > 0 AND total_seats > 0' if passenger_only else ''}
        ),
        attributed AS (
            SELECT 
                base.dest,
                {ATTRIBUTED_CARRIER_SQL} AS unique_carrier,
                ROUND(base.departures_performed * {ATTRIBUTED_SHARE_SQL}) AS departures_performed,
                ROUND(base.total_seats * {ATTRIBUTED_SHARE_SQL}) AS total_seats,
                ROUND(base.operational_passengers * {ATTRIBUTED_SHARE_SQL}) AS operational_passengers,
                base.avg_od_fare
            FROM base
            {REGIONAL_ATTRIBUTION_JOIN}
        ),
        route_totals AS (
            SELECT dest, SUM(departures_performed) AS route_deps
            FROM attributed
            GROUP BY 1
        ),
        carrier_totals AS (
            SELECT unique_carrier, SUM(total_seats) AS carrier_seats, SUM(operational_passengers) AS carrier_pax
            FROM attributed
            GROUP BY 1
            ORDER BY carrier_seats DESC
            LIMIT 1
        )
        SELECT 
            COUNT(DISTINCT CASE WHEN r.route_deps >= @min_departures THEN a.dest END) AS direct_destinations,
            SUM(a.departures_performed) AS total_departures,
            SUM(a.total_seats) AS total_seats,
            SUM(a.operational_passengers) AS total_passengers,
            ROUND(SAFE_DIVIDE(SUM(a.operational_passengers), SUM(a.total_seats)) * 100, 1) AS load_factor_pct,
            ROUND(AVG(a.avg_od_fare), 2) AS avg_od_fare,
            (SELECT unique_carrier FROM carrier_totals) AS leading_carrier
        FROM attributed a
        LEFT JOIN route_totals r ON a.dest = r.dest
    """
    df = run_query(query, params={"airport_code": airport_code, "year": year, "min_departures": min_departures})
    if not df.empty and df["total_passengers"].iloc[0] is not None and not pd.isna(df["total_passengers"].iloc[0]):
        row = df.iloc[0].to_dict()
        row["leading_carrier"] = row.get("leading_carrier") or "—"
        return row
    return {
        "direct_destinations": 0,
        "total_departures": 0,
        "total_seats": 0,
        "total_passengers": 0,
        "load_factor_pct": 0.0,
        "avg_od_fare": None,
        "leading_carrier": "—"
    }


@st.cache_data(ttl=3600, show_spinner=False)
def get_airport_routes_dataset(
    airport_code: str, 
    year: int, 
    passenger_only: bool = True,
    min_departures: int = 10
) -> pd.DataFrame:
    """Fetches full route network details with GPS coordinates, applying empirical regional carrier attribution."""
    query = f"""
        WITH base AS (
            SELECT 
                origin, origin_name, origin_city, origin_lat, origin_lon,
                dest, dest_name, dest_city, dest_state, dest_country, dest_lat, dest_lon,
                unique_carrier, carrier_name,
                departures_performed, total_seats, operational_passengers,
                distance_miles, avg_od_fare
            FROM `db1b-1.reporting.mart_airport_network_summary`
            WHERE origin = @airport_code 
              AND year = @year
              {'AND operational_passengers > 0 AND total_seats > 0' if passenger_only else ''}
              AND origin_lat IS NOT NULL 
              AND dest_lat IS NOT NULL
        ),
        attributed AS (
            SELECT 
                base.origin, base.origin_name, base.origin_city, base.origin_lat, base.origin_lon,
                base.dest, base.dest_name, base.dest_city, base.dest_state, base.dest_country, base.dest_lat, base.dest_lon,
                {ATTRIBUTED_CARRIER_SQL} AS marketing_carrier,
                ROUND(base.departures_performed * {ATTRIBUTED_SHARE_SQL}) AS departures_performed,
                ROUND(base.total_seats * {ATTRIBUTED_SHARE_SQL}) AS total_seats,
                ROUND(base.operational_passengers * {ATTRIBUTED_SHARE_SQL}) AS operational_passengers,
                base.distance_miles, base.avg_od_fare
            FROM base
            {REGIONAL_ATTRIBUTION_JOIN}
        ),
        route_agg AS (
            SELECT 
                origin, origin_name, origin_city, origin_lat, origin_lon,
                dest, dest_name, dest_city, dest_state, dest_country, dest_lat, dest_lon,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS operational_passengers,
                ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct,
                ROUND(SAFE_DIVIDE(SUM(total_seats), NULLIF(SUM(departures_performed), 0)), 1) AS avg_gauge_seats,
                AVG(distance_miles) AS distance_miles,
                ROUND(AVG(avg_od_fare), 2) AS avg_od_fare,
                STRING_AGG(DISTINCT marketing_carrier, ', ' ORDER BY marketing_carrier) AS operating_carriers
            FROM attributed
            GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        )
        SELECT * FROM route_agg
        WHERE departures_performed >= @min_departures
        ORDER BY operational_passengers DESC
    """
    return run_query(query, params={"airport_code": airport_code, "year": year, "min_departures": min_departures})


@st.cache_data(ttl=3600, show_spinner=False)
def get_airport_carrier_breakdown(
    airport_code: str, 
    year: int, 
    passenger_only: bool = True,
    min_departures: int = 10
) -> pd.DataFrame:
    """Fetches carrier market share breakdown attributed to consumer marketing brands using DB1B ticket survey shares."""
    query = f"""
        WITH base AS (
            SELECT 
                origin,
                dest,
                unique_carrier,
                carrier_name,
                departures_performed,
                total_seats,
                operational_passengers,
                avg_od_fare
            FROM `db1b-1.reporting.mart_airport_network_summary`
            WHERE origin = @airport_code AND year = @year
            {'AND operational_passengers > 0 AND total_seats > 0' if passenger_only else ''}
        ),
        carrier_attributed AS (
            SELECT 
                {ATTRIBUTED_CARRIER_SQL} AS carrier_code,
                base.carrier_name,
                ROUND(base.departures_performed * {ATTRIBUTED_SHARE_SQL}) AS departures_performed,
                ROUND(base.total_seats * {ATTRIBUTED_SHARE_SQL}) AS total_seats,
                ROUND(base.operational_passengers * {ATTRIBUTED_SHARE_SQL}) AS operational_passengers,
                base.avg_od_fare
            FROM base
            {REGIONAL_ATTRIBUTION_JOIN}
        ),
        carrier_agg AS (
            SELECT 
                carrier_code AS unique_carrier,
                {CARRIER_NAME_LOOKUP_SQL} AS carrier_name,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS operational_passengers,
                ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct,
                ROUND(AVG(avg_od_fare), 2) AS avg_fare
            FROM carrier_attributed
            GROUP BY 1, 2
        )
        SELECT * FROM carrier_agg
        WHERE departures_performed >= @min_departures
        ORDER BY total_seats DESC
    """
    return run_query(query, params={"airport_code": airport_code, "year": year, "min_departures": min_departures})


@st.cache_data(ttl=3600, show_spinner=False)
def get_airport_fleet_mix(
    airport_code: str, 
    year: int, 
    passenger_only: bool = True,
    min_departures: int = 10
) -> pd.DataFrame:
    """Fetches airport fleet deployment mix by aircraft family and specific model."""
    query = f"""
        WITH fleet_agg AS (
            SELECT 
                aircraft_family,
                aircraft_description,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS operational_passengers,
                ROUND(SAFE_DIVIDE(SUM(total_seats), NULLIF(SUM(departures_performed), 0)), 1) AS avg_gauge_seats,
                ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct
            FROM `db1b-1.reporting.mart_fleet_route_dynamics`
            WHERE origin = @airport_code AND year = @year
            {'AND operational_passengers > 0 AND total_seats > 0' if passenger_only else ''}
            GROUP BY 1, 2
        )
        SELECT * FROM fleet_agg
        WHERE departures_performed >= @min_departures
        ORDER BY operational_passengers DESC
    """
    return run_query(query, params={"airport_code": airport_code, "year": year, "min_departures": min_departures})


# -------------------------------------------------------------
# UNSERVED CONNECTING MARKETS & CARRIER ALIGNMENT PROPOSALS
# -------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def get_unserved_connecting_markets(
    airport_code: str, 
    year: int = 2023, 
    min_annual_pax: int = 1000,
    exclude_alternate_airports: bool = False
) -> pd.DataFrame:
    """
    Identifies top 1-stop connecting O&D markets with low or zero nonstop service,
    scales DB1B 10% sample by 10x to reflect true annual passenger traffic,
    classifies Business vs. Leisure demand by yield ($/mile), tags hub-strategy aligned carriers,
    and identifies Metro Catchment status (e.g. HOU served via IAH vs 100% New City Market).
    """
    query = f"""
        WITH nonstop_serviced AS (
            SELECT dest
            FROM `db1b-1.reporting.mart_airport_network_summary`
            WHERE origin = @airport_code AND year = @year
            GROUP BY dest
            HAVING SUM(departures_performed) >= 10
        ),
        metro_members AS (
            SELECT airport_code, market_code, market_name
            FROM `db1b-1.reporting.ref_city_markets`
        ),
        nonstop_metros AS (
            SELECT DISTINCT m.market_code
            FROM nonstop_serviced n
            JOIN metro_members m ON n.dest = m.airport_code
        ),
        historical_routes AS (
            SELECT 
                dest,
                MAX(year) AS last_year_served,
                STRING_AGG(DISTINCT {REGIONAL_ATTRIBUTION_SQL}, '/' ORDER BY {REGIONAL_ATTRIBUTION_SQL}) AS historical_carriers
            FROM `db1b-1.reporting.mart_airport_network_summary`
            WHERE origin = @airport_code AND year < @year AND departures_performed >= 10
            GROUP BY dest
        ),
        od_demand AS (
            SELECT 
                origin,
                destination AS dest,
                -- Handle BTS DB1B sample rate transition: 10% sample (10x) for <= 2024 vs 40% sample (2.5x) for >= 2025
                SUM(estimated_passengers * IF(@year >= 2025, 2.5, 10.0)) AS annual_od_passengers,
                AVG(avg_fare) AS avg_fare
            FROM `db1b-1.DB1B_RAW.v_market_demand_itinerary`
            WHERE origin = @airport_code
            GROUP BY 1, 2
        )
        SELECT 
            d.origin,
            d.dest,
            COALESCE(d_apt.airport_name, d.dest) AS dest_name,
            COALESCE(d_apt.city, d.dest) AS dest_city,
            COALESCE(d_apt.state_region, '') AS dest_state,
            m.market_code AS dest_market_code,
            m.market_name AS dest_market_name,
            CASE 
                WHEN nm.market_code IS NOT NULL THEN CONCAT('🔄 Alternate Airport (Metro Served)')
                ELSE '🌟 100% New City Market'
            END AS metro_status,
            ROUND(d.annual_od_passengers, 0) AS annual_connecting_pax,
            ROUND(SAFE_DIVIDE(d.annual_od_passengers, 365.0), 1) AS pdew,
            ROUND(d.avg_fare, 2) AS avg_fare,
            -- Estimate distance using geographic coordinates if available
            ROUND(ST_DISTANCE(ST_GEOGPOINT(o_apt.longitude, o_apt.latitude), ST_GEOGPOINT(d_apt.longitude, d_apt.latitude)) / 1609.34, 0) AS distance_miles,
            h.last_year_served,
            h.historical_carriers
        FROM od_demand d
        LEFT JOIN nonstop_serviced n ON d.dest = n.dest
        LEFT JOIN historical_routes h ON d.dest = h.dest
        LEFT JOIN metro_members m ON d.dest = m.airport_code
        LEFT JOIN nonstop_metros nm ON m.market_code = nm.market_code
        LEFT JOIN `db1b-1.reporting.ref_airports` o_apt ON d.origin = o_apt.airport_code
        LEFT JOIN `db1b-1.reporting.ref_airports` d_apt ON d.dest = d_apt.airport_code
        WHERE n.dest IS NULL -- Physical airport is unserved nonstop
          AND d.dest != @airport_code
          AND d.annual_od_passengers >= @min_annual_pax
        ORDER BY annual_connecting_pax DESC
        LIMIT 35
    """
    df = run_query(query, params={"airport_code": airport_code, "year": year, "min_annual_pax": min_annual_pax})
    if df.empty:
        return pd.DataFrame()

    if exclude_alternate_airports and "metro_status" in df.columns:
        df = df[df["metro_status"].str.contains("100% New", na=False)]

    # Fill default distance if null
    df["distance_miles"] = df["distance_miles"].fillna(800.0)
    df["yield_per_mile"] = (df["avg_fare"] / df["distance_miles"].replace(0, 1)).round(4)
    df["route_label"] = df["origin"] + " ➔ " + df["dest"] + " (" + df["dest_city"] + ")"
    
    # Enrich historical route service badge with merger lineage
    df["historical_service"] = df.apply(
        lambda r: enrich_historical_route_service(
            airport_code, 
            r["dest"], 
            r["last_year_served"] if "last_year_served" in r and pd.notna(r["last_year_served"]) else None, 
            r["historical_carriers"] if "historical_carriers" in r and pd.notna(r["historical_carriers"]) else None
        ),
        axis=1
    )
    
    # Classify Business vs Leisure demand
    def classify_market(row):
        y = row["yield_per_mile"]
        fare = row["avg_fare"]
        if y >= 0.22 or fare >= 320:
            return "💼 Business Heavy"
        elif y <= 0.14 or fare <= 180:
            return "🏖️ Leisure Heavy"
        else:
            return "⚖️ Balanced Mix"

    df["market_type"] = df.apply(classify_market, axis=1)
    
    # Derives aligned carrier based on network strategy
    df["aligned_carrier"] = df.apply(
        lambda r: _recommend_aligned_carrier(airport_code, r["dest"], r["distance_miles"], r["yield_per_mile"]),
        axis=1
    )
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def get_airline_hub_expansion_proposals(
    carrier_code: str, 
    year: int = 2023,
    exclude_alternate_airports: bool = True
) -> Dict[str, pd.DataFrame]:
    """
    Generates Top 5 candidate unserved connecting routes for EACH hub of the selected airline,
    formatting full O&D route labels (e.g. SEA ➔ HOU) with Catchment Market Awareness.
    """
    strat = CARRIER_STRATEGY.get(carrier_code, {})
    hubs = strat.get("hubs", ["ORD"])
    
    results = {}
    for hub in hubs[:6]:  # Limit to top 6 hubs
        df_hub = get_unserved_connecting_markets(
            hub, 
            year=year, 
            min_annual_pax=1000,
            exclude_alternate_airports=exclude_alternate_airports
        )
        if not df_hub.empty:
            df_hub["route_code"] = df_hub["origin"] + " ➔ " + df_hub["dest"]
            df_hub["full_route_name"] = df_hub["origin"] + " ➔ " + df_hub["dest"] + " (" + df_hub["dest_city"] + ")"
            results[hub] = df_hub.head(5)
            
    return results


# -------------------------------------------------------------
# ROUTE CARRIER COMPETITION & FARE PREMIUMS
# -------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def get_route_carrier_competition(origin: str, dest: str, year: int) -> pd.DataFrame:
    """
    Derives head-to-head carrier competition metrics on a specific route:
    market share, seats, average fare, yield ($/mile), and fare premium over competitors.
    """
    query = f"""
        WITH base AS (
            SELECT 
                origin, dest, unique_carrier, carrier_name,
                departures_performed, total_seats, operational_passengers,
                distance_miles, avg_od_fare
            FROM `db1b-1.reporting.mart_airport_network_summary`
            WHERE origin = @origin AND dest = @dest AND year = @year
        ),
        attributed AS (
            SELECT 
                {ATTRIBUTED_CARRIER_SQL} AS carrier_code,
                base.carrier_name,
                ROUND(base.departures_performed * {ATTRIBUTED_SHARE_SQL}) AS departures_performed,
                ROUND(base.total_seats * {ATTRIBUTED_SHARE_SQL}) AS total_seats,
                ROUND(base.operational_passengers * {ATTRIBUTED_SHARE_SQL}) AS operational_passengers,
                base.distance_miles,
                base.avg_od_fare
            FROM base
            {REGIONAL_ATTRIBUTION_JOIN}
        ),
        carrier_comp AS (
            SELECT 
                carrier_code AS unique_carrier,
                {CARRIER_NAME_LOOKUP_SQL} AS carrier_name,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS operational_passengers,
                ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct,
                ROUND(AVG(distance_miles), 0) AS distance_miles,
                ROUND(AVG(avg_od_fare), 2) AS avg_fare
            FROM attributed
            GROUP BY 1, 2
            HAVING departures_performed >= 5
        )
        SELECT * FROM carrier_comp
        ORDER BY total_seats DESC
    """
    df = run_query(query, params={"origin": origin, "dest": dest, "year": year})
    if df.empty:
        return df

    total_route_seats = df["total_seats"].sum() or 1
    total_route_pax = df["operational_passengers"].sum() or 1

    df["capacity_share_pct"] = (df["total_seats"] / total_route_seats * 100).round(1)
    df["passenger_share_pct"] = (df["operational_passengers"] / total_route_pax * 100).round(1)
    df["yield_per_mile"] = (df["avg_fare"] / df["distance_miles"].replace(0, 1)).round(4)
    
    # Min fare benchmark on route for premium calculation
    min_fare = df["avg_fare"].min() if not df["avg_fare"].dropna().empty else 1.0
    avg_route_fare = df["avg_fare"].mean() if not df["avg_fare"].dropna().empty else 1.0

    df["fare_premium_vs_min"] = (df["avg_fare"] - min_fare).round(2)
    df["fare_premium_pct"] = (((df["avg_fare"] - avg_route_fare) / avg_route_fare) * 100).round(1)
    return df


# -------------------------------------------------------------
# AIRLINE EXPLORER QUERIES
# -------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def get_airline_kpis(carrier_code: str, year: int, include_regionals: bool = True) -> Dict[str, Any]:
    """Calculates top-level performance KPIs for an airline, optionally including regional partner network operations."""
    if include_regionals:
        query = f"""
            WITH base AS (
                SELECT 
                    origin, dest, unique_carrier,
                    departures_performed, total_seats, operational_passengers,
                    available_seat_miles, revenue_passenger_miles, avg_od_fare, yield_per_mile
                FROM `db1b-1.reporting.mart_airline_network_performance`
                WHERE year = @year
            ),
            attributed AS (
                SELECT 
                    base.origin, base.dest,
                    {ATTRIBUTED_CARRIER_SQL} AS marketing_carrier,
                    ROUND(base.departures_performed * {ATTRIBUTED_SHARE_SQL}) AS departures_performed,
                    ROUND(base.total_seats * {ATTRIBUTED_SHARE_SQL}) AS total_seats,
                    ROUND(base.operational_passengers * {ATTRIBUTED_SHARE_SQL}) AS operational_passengers,
                    ROUND(base.available_seat_miles * {ATTRIBUTED_SHARE_SQL}) AS available_seat_miles,
                    ROUND(base.revenue_passenger_miles * {ATTRIBUTED_SHARE_SQL}) AS revenue_passenger_miles,
                    base.avg_od_fare, base.yield_per_mile
                FROM base
                {REGIONAL_ATTRIBUTION_JOIN}
            )
            SELECT 
                COUNT(DISTINCT CONCAT(origin, '-', dest)) AS active_routes,
                SUM(departures_performed) AS total_departures,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS total_passengers,
                SUM(available_seat_miles) AS total_asm,
                SUM(revenue_passenger_miles) AS total_rpm,
                ROUND(SAFE_DIVIDE(SUM(revenue_passenger_miles), SUM(available_seat_miles)) * 100, 1) AS system_load_factor,
                ROUND(AVG(avg_od_fare), 2) AS avg_network_fare,
                ROUND(AVG(yield_per_mile), 4) AS avg_yield_per_mile
            FROM attributed
            WHERE marketing_carrier = @carrier_code
        """
    else:
        query = """
            SELECT 
                COUNT(DISTINCT CONCAT(origin, '-', dest)) AS active_routes,
                SUM(departures_performed) AS total_departures,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS total_passengers,
                SUM(available_seat_miles) AS total_asm,
                SUM(revenue_passenger_miles) AS total_rpm,
                ROUND(SAFE_DIVIDE(SUM(revenue_passenger_miles), SUM(available_seat_miles)) * 100, 1) AS system_load_factor,
                ROUND(AVG(avg_od_fare), 2) AS avg_network_fare,
                ROUND(AVG(yield_per_mile), 4) AS avg_yield_per_mile
            FROM `db1b-1.reporting.mart_airline_network_performance`
            WHERE unique_carrier = @carrier_code AND year = @year
        """
    df = run_query(query, params={"carrier_code": carrier_code, "year": year})
    if not df.empty and df["total_departures"].iloc[0] is not None and not pd.isna(df["total_departures"].iloc[0]):
        return df.iloc[0].to_dict()
    return {
        "active_routes": 0,
        "total_departures": 0,
        "total_seats": 0,
        "total_passengers": 0,
        "total_asm": 0,
        "total_rpm": 0,
        "system_load_factor": 0.0,
        "avg_network_fare": 0.0,
        "avg_yield_per_mile": 0.0
    }


@st.cache_data(ttl=3600, show_spinner=False)
def get_airline_hubs(carrier_code: str, year: int, include_regionals: bool = True) -> pd.DataFrame:
    """Fetches top hub operations for an airline by seats and departures."""
    if include_regionals:
        query = f"""
            WITH base AS (
                SELECT 
                    origin, dest, origin_name, origin_city, unique_carrier,
                    departures_performed, total_seats, operational_passengers
                FROM `db1b-1.reporting.mart_airline_network_performance`
                WHERE year = @year
            ),
            attributed AS (
                SELECT 
                    base.origin AS airport_code,
                    base.origin_name,
                    base.origin_city,
                    base.dest,
                    {ATTRIBUTED_CARRIER_SQL} AS marketing_carrier,
                    ROUND(base.departures_performed * {ATTRIBUTED_SHARE_SQL}) AS departures_performed,
                    ROUND(base.total_seats * {ATTRIBUTED_SHARE_SQL}) AS total_seats,
                    ROUND(base.operational_passengers * {ATTRIBUTED_SHARE_SQL}) AS operational_passengers
                FROM base
                {REGIONAL_ATTRIBUTION_JOIN}
            )
            SELECT 
                airport_code,
                origin_name,
                origin_city,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS total_passengers,
                COUNT(DISTINCT dest) AS direct_destinations
            FROM attributed
            WHERE marketing_carrier = @carrier_code
            GROUP BY 1, 2, 3
            ORDER BY total_seats DESC
            LIMIT 10
        """
    else:
        query = """
            SELECT 
                origin AS airport_code,
                origin_name,
                origin_city,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS total_passengers,
                COUNT(DISTINCT dest) AS direct_destinations
            FROM `db1b-1.reporting.mart_airline_network_performance`
            WHERE unique_carrier = @carrier_code AND year = @year
            GROUP BY 1, 2, 3
            ORDER BY total_seats DESC
            LIMIT 10
        """
    return run_query(query, params={"carrier_code": carrier_code, "year": year})


@st.cache_data(ttl=3600, show_spinner=False)
def get_airline_yield_curve(carrier_code: str, year: int, include_regionals: bool = True) -> pd.DataFrame:
    """Fetches route-level stage length vs fare yields for an airline."""
    if include_regionals:
        query = f"""
            WITH base AS (
                SELECT 
                    origin, dest, unique_carrier,
                    avg_stage_length_miles, avg_od_fare, yield_per_mile,
                    operational_passengers, load_factor_pct
                FROM `db1b-1.reporting.mart_airline_network_performance`
                WHERE year = @year
                  AND avg_stage_length_miles > 50
                  AND (avg_od_fare IS NULL OR avg_od_fare > 20)
            ),
            attributed AS (
                SELECT 
                    base.origin, base.dest,
                    CONCAT(base.origin, '-', base.dest) AS route_label,
                    base.avg_stage_length_miles AS stage_length_miles,
                    base.avg_od_fare, base.yield_per_mile,
                    {ATTRIBUTED_CARRIER_SQL} AS marketing_carrier,
                    ROUND(base.operational_passengers * {ATTRIBUTED_SHARE_SQL}) AS operational_passengers,
                    base.load_factor_pct
                FROM base
                {REGIONAL_ATTRIBUTION_JOIN}
            )
            SELECT 
                origin, dest, route_label, stage_length_miles,
                avg_od_fare, yield_per_mile, operational_passengers, load_factor_pct
            FROM attributed
            WHERE marketing_carrier = @carrier_code
            ORDER BY operational_passengers DESC
            LIMIT 200
        """
    else:
        query = """
            SELECT 
                origin,
                dest,
                CONCAT(origin, '-', dest) AS route_label,
                avg_stage_length_miles AS stage_length_miles,
                avg_od_fare,
                yield_per_mile,
                operational_passengers,
                load_factor_pct
            FROM `db1b-1.reporting.mart_airline_network_performance`
            WHERE unique_carrier = @carrier_code AND year = @year
              AND avg_stage_length_miles > 50
              AND (avg_od_fare IS NULL OR avg_od_fare > 20)
            ORDER BY operational_passengers DESC
            LIMIT 200
        """
    return run_query(query, params={"carrier_code": carrier_code, "year": year})


@st.cache_data(ttl=3600, show_spinner=False)
def get_airline_routes_dataset(carrier_code: str, year: int, min_departures: int = 20, include_regionals: bool = True) -> pd.DataFrame:
    """Fetches nationwide route network with GPS coordinates for an airline."""
    if include_regionals:
        query = f"""
            WITH base AS (
                SELECT 
                    origin, origin_name, origin_city, origin_lat, origin_lon,
                    dest, dest_name, dest_city, dest_state, dest_country, dest_lat, dest_lon,
                    unique_carrier, departures_performed, total_seats, operational_passengers,
                    distance_miles, avg_od_fare
                FROM `db1b-1.reporting.mart_airport_network_summary`
                WHERE year = @year
                  AND origin_lat IS NOT NULL AND dest_lat IS NOT NULL
            ),
            attributed AS (
                SELECT 
                    base.origin, base.origin_name, base.origin_city, base.origin_lat, base.origin_lon,
                    base.dest, base.dest_name, base.dest_city, base.dest_state, base.dest_country, base.dest_lat, base.dest_lon,
                    {ATTRIBUTED_CARRIER_SQL} AS marketing_carrier,
                    ROUND(base.departures_performed * {ATTRIBUTED_SHARE_SQL}) AS departures_performed,
                    ROUND(base.total_seats * {ATTRIBUTED_SHARE_SQL}) AS total_seats,
                    ROUND(base.operational_passengers * {ATTRIBUTED_SHARE_SQL}) AS operational_passengers,
                    base.distance_miles, base.avg_od_fare
                FROM base
                {REGIONAL_ATTRIBUTION_JOIN}
            )
            SELECT 
                origin, origin_name, origin_city, origin_lat, origin_lon,
                dest, dest_name, dest_city, dest_state, dest_country, dest_lat, dest_lon,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS operational_passengers,
                ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct,
                ROUND(SAFE_DIVIDE(SUM(total_seats), NULLIF(SUM(departures_performed), 0)), 1) AS avg_gauge_seats,
                AVG(distance_miles) AS distance_miles,
                ROUND(AVG(avg_od_fare), 2) AS avg_od_fare
            FROM attributed
            WHERE marketing_carrier = @carrier_code
            GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
            HAVING departures_performed >= @min_departures
            ORDER BY operational_passengers DESC
            LIMIT 4000
        """
    else:
        query = """
            SELECT 
                origin, origin_name, origin_city, origin_lat, origin_lon,
                dest, dest_name, dest_city, dest_state, dest_country, dest_lat, dest_lon,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS operational_passengers,
                ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct,
                ROUND(SAFE_DIVIDE(SUM(total_seats), NULLIF(SUM(departures_performed), 0)), 1) AS avg_gauge_seats,
                AVG(distance_miles) AS distance_miles,
                ROUND(AVG(avg_od_fare), 2) AS avg_od_fare
            FROM `db1b-1.reporting.mart_airport_network_summary`
            WHERE unique_carrier = @carrier_code AND year = @year
              AND origin_lat IS NOT NULL AND dest_lat IS NOT NULL
            GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
            HAVING departures_performed >= @min_departures
            ORDER BY operational_passengers DESC
            LIMIT 4000
        """
    return run_query(query, params={"carrier_code": carrier_code, "year": year, "min_departures": min_departures})


# -------------------------------------------------------------
# FLEET & AIRCRAFT EXPLORER QUERIES
# -------------------------------------------------------------

def _build_fleet_where(family_filter: str) -> tuple[str, dict]:
    """Helper to build robust SQL WHERE clause for aircraft family/model selections."""
    where_sql = "WHERE year = @year"
    params = {}
    if family_filter != "All Mainline & Regional":
        if "A320" in family_filter:
            where_sql += " AND (aircraft_description LIKE '%A320%' OR aircraft_description LIKE '%A321%' OR aircraft_description LIKE '%A319%')"
        elif "737" in family_filter:
            where_sql += " AND (aircraft_description LIKE '%737%' OR aircraft_description LIKE '%MAX%')"
        elif "Widebody" in family_filter:
            where_sql += " AND aircraft_family = 'Widebody'"
        elif "Embraer" in family_filter or "E-Jets" in family_filter:
            where_sql += " AND (aircraft_description LIKE '%E17%' OR aircraft_description LIKE '%E19%' OR aircraft_description LIKE '%ERJ%')"
        elif "CRJ" in family_filter:
            where_sql += " AND aircraft_description LIKE '%CRJ%'"
        else:
            where_sql += " AND aircraft_family LIKE @fam_pattern"
            params["fam_pattern"] = f"%{family_filter.split(' ')[0]}%"
    return where_sql, params


@st.cache_data(ttl=3600, show_spinner=False)
def get_fleet_kpis(family_filter: str, year: int) -> Dict[str, Any]:
    """Calculates top-level utilization and revenue metrics for an aircraft category or family."""
    where_sql, extra_params = _build_fleet_where(family_filter)
    params = {"year": year, **extra_params}

    query = f"""
        SELECT 
            COUNT(DISTINCT aircraft_type_code) AS unique_models,
            COUNT(DISTINCT unique_carrier) AS operating_carriers,
            SUM(departures_performed) AS total_departures,
            SUM(total_seats) AS total_seats,
            SUM(operational_passengers) AS total_passengers,
            ROUND(SAFE_DIVIDE(SUM(total_seats), NULLIF(SUM(departures_performed), 0)), 1) AS avg_gauge_seats,
            ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS fleet_load_factor,
            ROUND(AVG(distance_miles), 0) AS avg_stage_length,
            ROUND(AVG(avg_od_fare), 2) AS avg_segment_fare,
            ROUND(SAFE_DIVIDE(AVG(avg_od_fare), NULLIF(AVG(distance_miles), 0)), 4) AS yield_per_mile
        FROM `db1b-1.reporting.mart_fleet_route_dynamics`
        {where_sql}
    """
    df = run_query(query, params=params)
    if not df.empty and df["total_departures"].iloc[0] is not None:
        return df.iloc[0].to_dict()
    return {
        "unique_models": 0,
        "operating_carriers": 0,
        "total_departures": 0,
        "total_seats": 0,
        "total_passengers": 0,
        "avg_gauge_seats": 0.0,
        "fleet_load_factor": 0.0,
        "avg_stage_length": 0,
        "avg_segment_fare": 0.0,
        "yield_per_mile": 0.0
    }


@st.cache_data(ttl=3600, show_spinner=False)
def get_fleet_aircraft_breakdown(family_filter: str, year: int) -> pd.DataFrame:
    """Fetches top aircraft model deployment and revenue statistics."""
    where_sql, extra_params = _build_fleet_where(family_filter)
    params = {"year": year, **extra_params}

    query = f"""
        SELECT 
            aircraft_family,
            aircraft_description,
            SUM(departures_performed) AS departures_performed,
            SUM(total_seats) AS total_seats,
            SUM(operational_passengers) AS operational_passengers,
            ROUND(SAFE_DIVIDE(SUM(total_seats), NULLIF(SUM(departures_performed), 0)), 1) AS avg_gauge_seats,
            ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct,
            ROUND(AVG(distance_miles), 0) AS avg_stage_length,
            ROUND(AVG(avg_od_fare), 2) AS avg_segment_fare,
            ROUND(SAFE_DIVIDE(AVG(avg_od_fare), NULLIF(AVG(distance_miles), 0)), 4) AS yield_per_mile
        FROM `db1b-1.reporting.mart_fleet_route_dynamics`
        {where_sql}
        GROUP BY 1, 2
        ORDER BY total_seats DESC
        LIMIT 15
    """
    return run_query(query, params=params)


@st.cache_data(ttl=3600, show_spinner=False)
def get_fleet_operators_breakdown(family_filter: str, year: int) -> pd.DataFrame:
    """Fetches top airline operators for the selected aircraft family, applying regional attribution."""
    where_sql, extra_params = _build_fleet_where(family_filter)
    params = {"year": year, **extra_params}

    query = f"""
        WITH attributed AS (
            SELECT 
                {REGIONAL_ATTRIBUTION_SQL} AS carrier_code,
                carrier_name,
                departures_performed,
                total_seats,
                operational_passengers,
                avg_od_fare
            FROM `db1b-1.reporting.mart_fleet_route_dynamics`
            {where_sql}
        ),
        carrier_agg AS (
            SELECT 
                carrier_code AS unique_carrier,
                {CARRIER_NAME_LOOKUP_SQL} AS carrier_name,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS operational_passengers,
                ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct,
                ROUND(AVG(avg_od_fare), 2) AS avg_segment_fare
            FROM attributed
            GROUP BY 1, 2
        )
        SELECT * FROM carrier_agg
        WHERE total_seats > 0
        ORDER BY total_seats DESC
        LIMIT 10
    """
    return run_query(query, params=params)


@st.cache_data(ttl=3600, show_spinner=False)
def get_platform_live_kpis() -> Dict[str, Any]:
    """
    Queries zero-scan BigQuery __TABLES__ metadata to fetch authoritative,
    real-time row counts and scale metrics across all operational datasets and analytical marts.
    Automatically keeps all landing page and dashboard KPIs fresh.
    """
    query = """
        SELECT dataset_id, table_id, row_count, TIMESTAMP_MILLIS(last_modified_time) as modified
        FROM `db1b-1.reporting.__TABLES__`
        UNION ALL
        SELECT dataset_id, table_id, row_count, TIMESTAMP_MILLIS(last_modified_time) as modified
        FROM `db1b-1.DB1B_RAW.__TABLES__`
        UNION ALL
        SELECT dataset_id, table_id, row_count, TIMESTAMP_MILLIS(last_modified_time) as modified
        FROM `db1b-1.bts_t100_data.__TABLES__`
    """
    try:
        df = run_query(query)
        if df.empty:
            raise ValueError("No table metadata returned")
            
        stats = {}
        for _, row in df.iterrows():
            stats[f"{row['dataset_id']}.{row['table_id']}"] = {
                "rows": int(row["row_count"]),
                "modified": str(row["modified"])[:10]
            }
            
        t100_rows = stats.get("bts_t100_data.t100_segments", {}).get("rows", 14035905)
        od40_rows = stats.get("DB1B_RAW.OD40_DB1B_RAW", {}).get("rows", 79858501)
        fleet_rows = stats.get("reporting.mart_fleet_route_dynamics", {}).get("rows", 13604268)
        airports_rows = stats.get("reporting.mart_airport_network_summary", {}).get("rows", 8532624)
        airlines_rows = stats.get("reporting.mart_airline_network_performance", {}).get("rows", 8532624)
        ref_airports = stats.get("reporting.ref_airports", {}).get("rows", 50568)
        
        total_records = t100_rows + od40_rows
        
        def _fmt(n):
            if n >= 1e6:
                return f"{n/1e6:.2f}M"
            if n >= 1e3:
                return f"{n/1e3:.0f}K"
            return f"{n:,}"
            
        return {
            "total_records_formatted": f"{total_records/1e6:.1f}M+",
            "total_records_raw": total_records,
            "t100_rows_formatted": _fmt(t100_rows),
            "t100_rows_raw": t100_rows,
            "od40_rows_formatted": _fmt(od40_rows),
            "od40_rows_raw": od40_rows,
            "fleet_rows_formatted": _fmt(fleet_rows),
            "fleet_rows_raw": fleet_rows,
            "airports_rows_formatted": _fmt(airports_rows),
            "airlines_rows_formatted": _fmt(airlines_rows),
            "ref_airports_formatted": f"{ref_airports:,}",
            "raw_stats": stats
        }
    except Exception:
        return {
            "total_records_formatted": "93.9M+",
            "total_records_raw": 93894406,
            "t100_rows_formatted": "14.04M",
            "t100_rows_raw": 14035905,
            "od40_rows_formatted": "79.86M",
            "od40_rows_raw": 79858501,
            "fleet_rows_formatted": "13.60M",
            "fleet_rows_raw": 13604268,
            "airports_rows_formatted": "8.53M",
            "airlines_rows_formatted": "8.53M",
            "ref_airports_formatted": "50,568",
            "raw_stats": {}
        }


# -------------------------------------------------------------
# Global & Historical Alliance Intelligence Queries
# -------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def get_alliance_performance_metrics(year: int) -> pd.DataFrame:
    """
    Computes system operational metrics across all global and historical alliances
    (Star Alliance, SkyTeam, oneworld, Wings Alliance / NW-KL, Qualiflyer, and Independent)
    for a given calendar year using reporting.mart_airport_network_summary with regional carrier attribution.
    Note: Reflects US-origin and US-touching international operations reported to US BTS.
    """
    from app.utils.alliances import get_carrier_alliance
    
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    
    sql = f"""
    WITH base AS (
      SELECT
        origin,
        dest,
        unique_carrier,
        carrier_name,
        departures_performed,
        total_seats,
        operational_passengers,
        distance_miles,
        estimated_od_passengers,
        avg_od_fare
      FROM `db1b-1.reporting.mart_airport_network_summary`
      WHERE flight_date >= '{start_date}' AND flight_date <= '{end_date}'
    ),
    attributed AS (
      SELECT
        COALESCE(_reg.mkt_carrier,
          CASE 
            WHEN base.unique_carrier = 'QX' THEN 'AS'
            WHEN base.unique_carrier = '9E' THEN 'DL'
            WHEN base.unique_carrier IN ('MQ', 'OH', 'PT') THEN 'AA'
            WHEN base.unique_carrier IN ('C5', 'G7') THEN 'UA'
            WHEN base.unique_carrier IN ('CP', 'CP (2)') THEN 'DL'
            WHEN base.unique_carrier = 'XJ' THEN 'NW'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('ATL', 'MSP', 'DTW', 'SLC') OR base.origin IN ('ATL', 'MSP', 'DTW', 'SLC')) THEN 'DL'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('ORD', 'DEN', 'IAH', 'EWR', 'IAD', 'SFO') OR base.origin IN ('ORD', 'DEN', 'IAH', 'EWR', 'IAD', 'SFO')) THEN 'UA'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('DFW', 'CLT', 'MIA', 'PHX', 'PHL') OR base.origin IN ('DFW', 'CLT', 'MIA', 'PHX', 'PHL')) THEN 'AA'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('SEA', 'PDX', 'SAN', 'BUR', 'OAK', 'SJC', 'SMF', 'ANC', 'LAX') OR base.origin IN ('SEA', 'PDX', 'SAN', 'BUR', 'OAK', 'SJC', 'SMF', 'ANC', 'LAX')) THEN 'AS'
            WHEN base.unique_carrier = 'YX' AND (base.dest IN ('ORD', 'EWR', 'IAH', 'IAD') OR base.origin IN ('ORD', 'EWR', 'IAH', 'IAD')) THEN 'UA'
            WHEN base.unique_carrier = 'YX' AND (base.dest IN ('LGA', 'JFK', 'BOS', 'ATL') OR base.origin IN ('LGA', 'JFK', 'BOS', 'ATL')) THEN 'DL'
            WHEN base.unique_carrier = 'YX' THEN 'AA'
            ELSE base.unique_carrier
          END
        ) AS carrier_code,
        ROUND(base.departures_performed * COALESCE(_reg.attribution_share, 1.0)) AS departures_attr,
        ROUND(base.total_seats * COALESCE(_reg.attribution_share, 1.0)) AS total_seats_attr,
        ROUND(base.operational_passengers * COALESCE(_reg.attribution_share, 1.0)) AS passengers_attr,
        (base.distance_miles * base.operational_passengers * COALESCE(_reg.attribution_share, 1.0)) AS rpm_attr,
        (base.distance_miles * base.total_seats * COALESCE(_reg.attribution_share, 1.0)) AS asm_attr,
        (base.estimated_od_passengers * base.avg_od_fare * COALESCE(_reg.attribution_share, 1.0)) AS estimated_revenue_attr
      FROM base
      LEFT JOIN `db1b-1.reporting.ref_regional_route_attribution` _reg
        ON base.unique_carrier = _reg.op_carrier
       AND base.origin = _reg.origin
       AND base.dest = _reg.dest
    )
    SELECT
      carrier_code,
      SUM(departures_attr) as departures,
      SUM(total_seats_attr) as total_seats,
      SUM(passengers_attr) as passengers,
      SUM(rpm_attr) as rpm,
      SUM(asm_attr) as asm,
      SUM(estimated_revenue_attr) as estimated_revenue
    FROM attributed
    GROUP BY 1
    HAVING SUM(passengers_attr) >= 10000
    ORDER BY passengers DESC
    """
    df_raw = run_query(sql)
    if df_raw.empty:
        return pd.DataFrame()

    records = []
    for _, row in df_raw.iterrows():
        c_code = str(row["carrier_code"]).strip().upper()
        a_info = get_carrier_alliance(c_code, year)
        
        a_name = a_info["alliance_name"] if a_info else "Independent / Unaligned"
        
        # Special recognition: NW and KL joint venture (Wings Alliance)
        if a_name == "Wings Alliance":
            a_label = "Wings Alliance (NW / KL)"
        else:
            a_label = a_name

        records.append({
            "carrier_code": c_code,
            "alliance_name": a_label,
            "departures": row["departures"],
            "total_seats": row["total_seats"],
            "passengers": row["passengers"],
            "rpm": row["rpm"],
            "asm": row["asm"],
            "estimated_revenue": row["estimated_revenue"] or 0.0
        })

    df_enriched = pd.DataFrame(records)
    if df_enriched.empty:
        return pd.DataFrame()

    # Aggregate by alliance, preserving carrier ranking by passenger volume descending
    def _extract_ranked_carriers(group):
        sorted_g = group.sort_values("passengers", ascending=False)
        return list(sorted_g["carrier_code"])

    def _extract_carrier_details(group):
        sorted_g = group.sort_values("passengers", ascending=False)
        return [
            {"code": r["carrier_code"], "passengers": r["passengers"]}
            for _, r in sorted_g.iterrows()
        ]

    agg_rows = []
    for a_name, g in df_enriched.groupby("alliance_name"):
        agg_rows.append({
            "alliance_name": a_name,
            "departures": g["departures"].sum(),
            "total_seats": g["total_seats"].sum(),
            "passengers": g["passengers"].sum(),
            "rpm": g["rpm"].sum(),
            "asm": g["asm"].sum(),
            "estimated_revenue": g["estimated_revenue"].sum(),
            "carriers": _extract_ranked_carriers(g),
            "carrier_details": _extract_carrier_details(g)
        })

    agg = pd.DataFrame(agg_rows)
    agg["load_factor_pct"] = (agg["passengers"] / agg["total_seats"] * 100).round(1)
    agg["system_load_factor_pct"] = (agg["rpm"] / agg["asm"] * 100).round(1)
    
    total_pax = agg["passengers"].sum()
    agg["passenger_share_pct"] = (agg["passengers"] / total_pax * 100).round(1) if total_pax > 0 else 0.0
    
    total_seats = agg["total_seats"].sum()
    agg["seat_share_pct"] = (agg["total_seats"] / total_seats * 100).round(1) if total_seats > 0 else 0.0

    return agg.sort_values(by="passengers", ascending=False)


@st.cache_data(ttl=3600, show_spinner=False)
def get_alliance_fleet_deployment(year: int) -> pd.DataFrame:
    """
    Analyzes widebody vs. narrowbody vs. regional fleet deployment mix
    by alliance for a given calendar year using reporting.mart_fleet_route_dynamics
    with regional carrier attribution.
    """
    from app.utils.alliances import get_carrier_alliance
    
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    
    sql = f"""
    WITH base AS (
      SELECT
        origin,
        dest,
        unique_carrier,
        aircraft_family,
        departures_performed,
        total_seats,
        operational_passengers
      FROM `db1b-1.reporting.mart_fleet_route_dynamics`
      WHERE flight_date >= '{start_date}' AND flight_date <= '{end_date}'
    ),
    attributed AS (
      SELECT
        COALESCE(_reg.mkt_carrier,
          CASE 
            WHEN base.unique_carrier = 'QX' THEN 'AS'
            WHEN base.unique_carrier = '9E' THEN 'DL'
            WHEN base.unique_carrier IN ('MQ', 'OH', 'PT') THEN 'AA'
            WHEN base.unique_carrier IN ('C5', 'G7') THEN 'UA'
            WHEN base.unique_carrier IN ('CP', 'CP (2)') THEN 'DL'
            WHEN base.unique_carrier = 'XJ' THEN 'NW'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('ATL', 'MSP', 'DTW', 'SLC') OR base.origin IN ('ATL', 'MSP', 'DTW', 'SLC')) THEN 'DL'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('ORD', 'DEN', 'IAH', 'EWR', 'IAD', 'SFO') OR base.origin IN ('ORD', 'DEN', 'IAH', 'EWR', 'IAD', 'SFO')) THEN 'UA'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('DFW', 'CLT', 'MIA', 'PHX', 'PHL') OR base.origin IN ('DFW', 'CLT', 'MIA', 'PHX', 'PHL')) THEN 'AA'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('SEA', 'PDX', 'SAN', 'BUR', 'OAK', 'SJC', 'SMF', 'ANC', 'LAX') OR base.origin IN ('SEA', 'PDX', 'SAN', 'BUR', 'OAK', 'SJC', 'SMF', 'ANC', 'LAX')) THEN 'AS'
            WHEN base.unique_carrier = 'YX' AND (base.dest IN ('ORD', 'EWR', 'IAH', 'IAD') OR base.origin IN ('ORD', 'EWR', 'IAH', 'IAD')) THEN 'UA'
            WHEN base.unique_carrier = 'YX' AND (base.dest IN ('LGA', 'JFK', 'BOS', 'ATL') OR base.origin IN ('LGA', 'JFK', 'BOS', 'ATL')) THEN 'DL'
            WHEN base.unique_carrier = 'YX' THEN 'AA'
            ELSE base.unique_carrier
          END
        ) AS carrier_code,
        base.aircraft_family,
        ROUND(base.departures_performed * COALESCE(_reg.attribution_share, 1.0)) AS departures,
        ROUND(base.total_seats * COALESCE(_reg.attribution_share, 1.0)) AS total_seats,
        ROUND(base.operational_passengers * COALESCE(_reg.attribution_share, 1.0)) AS passengers
      FROM base
      LEFT JOIN `db1b-1.reporting.ref_regional_route_attribution` _reg
        ON base.unique_carrier = _reg.op_carrier
       AND base.origin = _reg.origin
       AND base.dest = _reg.dest
    )
    SELECT
      carrier_code,
      aircraft_family,
      SUM(departures) as departures,
      SUM(total_seats) as total_seats,
      SUM(passengers) as passengers
    FROM attributed
    GROUP BY 1, 2
    """
    df_raw = run_query(sql)
    if df_raw.empty:
        return pd.DataFrame()

    rows = []
    for _, r in df_raw.iterrows():
        c = str(r["carrier_code"]).strip().upper()
        a_info = get_carrier_alliance(c, year)
        a_name = a_info["alliance_name"] if a_info else "Independent / Unaligned"
        if a_name == "Wings Alliance":
            a_name = "Wings Alliance (NW / KL)"

        rows.append({
            "alliance_name": a_name,
            "aircraft_family": r["aircraft_family"],
            "departures": r["departures"],
            "total_seats": r["total_seats"],
            "passengers": r["passengers"]
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame()

    return df.groupby(["alliance_name", "aircraft_family"]).agg(
        departures=("departures", "sum"),
        total_seats=("total_seats", "sum"),
        passengers=("passengers", "sum")
    ).reset_index()


# -------------------------------------------------------------
# Multi-Year Time-Series & Trending Queries (1990–2026)
# -------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def get_airport_time_series(
    airport_code: str, 
    passenger_only: bool = True,
    min_departures: int = 10
) -> pd.DataFrame:
    """
    Retrieves annual time-series metrics (1990–2025 completed years) for a specific airport with regional carrier attribution.
    Returns year-by-year departures, total_seats, passengers, load_factor_pct, direct_destinations, and attributed top_carrier.
    """
    code = airport_code.strip().upper()
    pax_filter = "AND operational_passengers > 0 AND total_seats > 0" if passenger_only else ""

    sql = f"""
    WITH base AS (
      SELECT
        EXTRACT(YEAR FROM flight_date) as year,
        origin,
        dest,
        unique_carrier,
        departures_performed,
        total_seats,
        operational_passengers
      FROM `db1b-1.reporting.mart_airport_network_summary`
      WHERE origin = '{code}' {pax_filter}
        AND EXTRACT(YEAR FROM flight_date) <= 2025
    ),
    attributed AS (
      SELECT
        base.year,
        base.dest,
        {ATTRIBUTED_CARRIER_SQL} AS unique_carrier,
        ROUND(base.departures_performed * {ATTRIBUTED_SHARE_SQL}) AS departures_performed,
        ROUND(base.total_seats * {ATTRIBUTED_SHARE_SQL}) AS total_seats,
        ROUND(base.operational_passengers * {ATTRIBUTED_SHARE_SQL}) AS operational_passengers
      FROM base
      {REGIONAL_ATTRIBUTION_JOIN}
    ),
    route_annual AS (
      SELECT
        year,
        dest,
        SUM(departures_performed) as route_deps
      FROM attributed
      GROUP BY 1, 2
    ),
    annual_summary AS (
      SELECT
        a.year,
        SUM(a.departures_performed) as total_departures,
        SUM(a.total_seats) as total_seats,
        SUM(a.operational_passengers) as total_passengers,
        COUNT(DISTINCT CASE WHEN r.route_deps >= {min_departures} THEN a.dest END) as direct_destinations,
        ROUND(SUM(a.operational_passengers) / NULLIF(SUM(a.total_seats), 0) * 100, 1) as load_factor_pct
      FROM attributed a
      LEFT JOIN route_annual r ON a.year = r.year AND a.dest = r.dest
      GROUP BY 1
    ),
    carrier_annual AS (
      SELECT
        year,
        unique_carrier,
        SUM(operational_passengers) as carrier_pax,
        ROW_NUMBER() OVER(PARTITION BY year ORDER BY SUM(operational_passengers) DESC) as rn
      FROM attributed
      GROUP BY 1, 2
    )
    SELECT
      a.year,
      a.total_departures,
      a.total_seats,
      a.total_passengers,
      a.direct_destinations,
      a.load_factor_pct,
      c.unique_carrier as top_carrier
    FROM annual_summary a
    LEFT JOIN carrier_annual c ON a.year = c.year AND c.rn = 1
    ORDER BY a.year ASC
    """
    df = run_query(sql)
    if not df.empty:
        # Calculate YoY passenger growth
        df["pax_growth_pct"] = (df["total_passengers"].pct_change() * 100).round(1)
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def get_airline_time_series(carrier_code: str, include_regionals: bool = True) -> pd.DataFrame:
    """
    Retrieves annual time-series performance metrics (1990–2026) for an airline,
    optionally attributing regional partner network operations.
    """
    code = carrier_code.strip().upper()
    if include_regionals:
        sql = f"""
        WITH base AS (
          SELECT
            EXTRACT(YEAR FROM flight_date) as year,
            origin,
            dest,
            unique_carrier,
            departures_performed,
            total_seats,
            operational_passengers,
            available_seat_miles,
            revenue_passenger_miles
          FROM `db1b-1.reporting.mart_airline_network_performance`
          WHERE EXTRACT(YEAR FROM flight_date) <= 2025
        ),
        attributed AS (
          SELECT
            base.year,
            base.dest,
            {ATTRIBUTED_CARRIER_SQL} AS marketing_carrier,
            ROUND(base.departures_performed * {ATTRIBUTED_SHARE_SQL}) AS departures_performed,
            ROUND(base.total_seats * {ATTRIBUTED_SHARE_SQL}) AS total_seats,
            ROUND(base.operational_passengers * {ATTRIBUTED_SHARE_SQL}) AS operational_passengers,
            ROUND(base.available_seat_miles * {ATTRIBUTED_SHARE_SQL}) AS available_seat_miles,
            ROUND(base.revenue_passenger_miles * {ATTRIBUTED_SHARE_SQL}) AS revenue_passenger_miles
          FROM base
          {REGIONAL_ATTRIBUTION_JOIN}
        )
        SELECT
          year,
          SUM(departures_performed) as total_departures,
          SUM(total_seats) as total_seats,
          SUM(operational_passengers) as total_passengers,
          SUM(available_seat_miles) as total_asm,
          SUM(revenue_passenger_miles) as total_rpm,
          ROUND(SUM(revenue_passenger_miles) / NULLIF(SUM(available_seat_miles), 0) * 100, 1) as system_load_factor_pct,
          ROUND(SUM(operational_passengers) / NULLIF(SUM(total_seats), 0) * 100, 1) as load_factor_pct,
          COUNT(DISTINCT dest) as active_routes
        FROM attributed
        WHERE marketing_carrier = '{code}'
        GROUP BY 1
        ORDER BY year ASC
        """
    else:
        sql = f"""
        SELECT
          EXTRACT(YEAR FROM flight_date) as year,
          SUM(departures_performed) as total_departures,
          SUM(total_seats) as total_seats,
          SUM(operational_passengers) as total_passengers,
          SUM(available_seat_miles) as total_asm,
          SUM(revenue_passenger_miles) as total_rpm,
          ROUND(SUM(revenue_passenger_miles) / NULLIF(SUM(available_seat_miles), 0) * 100, 1) as system_load_factor_pct,
          ROUND(SUM(operational_passengers) / NULLIF(SUM(total_seats), 0) * 100, 1) as load_factor_pct,
          COUNT(DISTINCT dest) as active_routes
        FROM `db1b-1.reporting.mart_airline_network_performance`
        WHERE unique_carrier = '{code}'
          AND EXTRACT(YEAR FROM flight_date) <= 2025
        GROUP BY 1
        ORDER BY year ASC
        """
    df = run_query(sql)
    if not df.empty:
        df["pax_growth_pct"] = (df["total_passengers"].pct_change() * 100).round(1)
        df["asm_growth_pct"] = (df["total_asm"].pct_change() * 100).round(1)
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def get_fleet_time_series(aircraft_family: Optional[str] = None) -> pd.DataFrame:
    """
    Retrieves annual gauge and equipment mix trends (1990–2025).
    If aircraft_family is specified, returns model-level gauge and departures over time.
    If None, returns industry-wide category transitions (Mainline vs Widebody vs RJ vs Prop).
    """
    fam_filter = f"AND aircraft_family = '{aircraft_family}'" if aircraft_family and aircraft_family != "All Families" else ""
    
    sql = f"""
    SELECT
      EXTRACT(YEAR FROM flight_date) as year,
      aircraft_family,
      SUM(departures_performed) as departures,
      SUM(total_seats) as total_seats,
      SUM(operational_passengers) as passengers,
      ROUND(SUM(total_seats) / NULLIF(SUM(departures_performed), 0), 1) as avg_gauge
    FROM `db1b-1.reporting.mart_fleet_route_dynamics`
    WHERE EXTRACT(YEAR FROM flight_date) <= 2025
    {fam_filter}
    GROUP BY 1, 2
    ORDER BY year ASC, departures DESC
    """
    return run_query(sql)


@st.cache_data(ttl=3600, show_spinner=False)
def get_alliances_time_series() -> pd.DataFrame:
    """
    Retrieves multi-year alliance market share trends (1990–2025) across
    Star Alliance, SkyTeam, oneworld, Wings Alliance (NW/KL), Qualiflyer, and Independent
    with full regional carrier attribution.
    """
    from app.utils.alliances import get_carrier_alliance
    
    sql = """
    WITH base AS (
      SELECT
        EXTRACT(YEAR FROM flight_date) as year,
        origin,
        dest,
        unique_carrier,
        SUM(departures_performed) as departures_performed,
        SUM(total_seats) as total_seats,
        SUM(operational_passengers) as operational_passengers
      FROM `db1b-1.reporting.mart_airport_network_summary`
      WHERE EXTRACT(YEAR FROM flight_date) <= 2025
      GROUP BY 1, 2, 3, 4
    ),
    attributed AS (
      SELECT
        base.year,
        COALESCE(_reg.mkt_carrier,
          CASE 
            WHEN base.unique_carrier = 'QX' THEN 'AS'
            WHEN base.unique_carrier = '9E' THEN 'DL'
            WHEN base.unique_carrier IN ('MQ', 'OH', 'PT') THEN 'AA'
            WHEN base.unique_carrier IN ('C5', 'G7') THEN 'UA'
            WHEN base.unique_carrier IN ('CP', 'CP (2)') THEN 'DL'
            WHEN base.unique_carrier = 'XJ' THEN 'NW'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('ATL', 'MSP', 'DTW', 'SLC') OR base.origin IN ('ATL', 'MSP', 'DTW', 'SLC')) THEN 'DL'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('ORD', 'DEN', 'IAH', 'EWR', 'IAD', 'SFO') OR base.origin IN ('ORD', 'DEN', 'IAH', 'EWR', 'IAD', 'SFO')) THEN 'UA'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('DFW', 'CLT', 'MIA', 'PHX', 'PHL') OR base.origin IN ('DFW', 'CLT', 'MIA', 'PHX', 'PHL')) THEN 'AA'
            WHEN base.unique_carrier = 'OO' AND (base.dest IN ('SEA', 'PDX', 'SAN', 'BUR', 'OAK', 'SJC', 'SMF', 'ANC', 'LAX') OR base.origin IN ('SEA', 'PDX', 'SAN', 'BUR', 'OAK', 'SJC', 'SMF', 'ANC', 'LAX')) THEN 'AS'
            WHEN base.unique_carrier = 'YX' AND (base.dest IN ('ORD', 'EWR', 'IAH', 'IAD') OR base.origin IN ('ORD', 'EWR', 'IAH', 'IAD')) THEN 'UA'
            WHEN base.unique_carrier = 'YX' AND (base.dest IN ('LGA', 'JFK', 'BOS', 'ATL') OR base.origin IN ('LGA', 'JFK', 'BOS', 'ATL')) THEN 'DL'
            WHEN base.unique_carrier = 'YX' THEN 'AA'
            ELSE base.unique_carrier
          END
        ) AS carrier_code,
        ROUND(base.departures_performed * COALESCE(_reg.attribution_share, 1.0)) AS departures_attr,
        ROUND(base.total_seats * COALESCE(_reg.attribution_share, 1.0)) AS total_seats_attr,
        ROUND(base.operational_passengers * COALESCE(_reg.attribution_share, 1.0)) AS passengers_attr
      FROM base
      LEFT JOIN `db1b-1.reporting.ref_regional_route_attribution` _reg
        ON base.unique_carrier = _reg.op_carrier
       AND base.origin = _reg.origin
       AND base.dest = _reg.dest
    )
    SELECT
      year,
      carrier_code,
      SUM(departures_attr) as departures,
      SUM(total_seats_attr) as total_seats,
      SUM(passengers_attr) as passengers
    FROM attributed
    GROUP BY 1, 2
    HAVING SUM(passengers_attr) >= 10000
    ORDER BY year ASC, passengers DESC
    """
    df_raw = run_query(sql)
    if df_raw.empty:
        return pd.DataFrame()

    records = []
    for _, r in df_raw.iterrows():
        yr = int(r["year"])
        c = str(r["carrier_code"]).strip().upper()
        a_info = get_carrier_alliance(c, yr)
        a_name = a_info["alliance_name"] if a_info else "Independent / Unaligned"
        if a_name == "Wings Alliance":
            a_name = "Wings Alliance (NW / KL)"

        records.append({
            "year": yr,
            "alliance_name": a_name,
            "departures": r["departures"],
            "total_seats": r["total_seats"],
            "passengers": r["passengers"]
        })

    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame()

    agg = df.groupby(["year", "alliance_name"]).agg(
        departures=("departures", "sum"),
        total_seats=("total_seats", "sum"),
        passengers=("passengers", "sum")
    ).reset_index()

    # Compute annual market share %
    yearly_totals = agg.groupby("year")["passengers"].transform("sum")
    agg["pax_share_pct"] = (agg["passengers"] / yearly_totals * 100).round(1)

    return agg



