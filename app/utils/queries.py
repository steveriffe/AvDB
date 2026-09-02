"""
BigQuery Query Layer for AvDB Streamlit Dashboard
Cached with @st.cache_data for instant interactive responses.
"""
import streamlit as st
import pandas as pd
from typing import Optional, List, Dict, Any
from app.utils.bq_client import run_query
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
    return run_query(query)


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
    """Calculates top-level KPI metrics for an airport, filtering noise/charters by min_departures."""
    query = f"""
        WITH route_grouped AS (
            SELECT 
                dest,
                unique_carrier,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS operational_passengers,
                AVG(avg_od_fare) AS avg_od_fare
            FROM `db1b-1.reporting.mart_airport_network_summary`
            WHERE origin = @airport_code AND year = @year
            {'AND operational_passengers > 0 AND total_seats > 0' if passenger_only else ''}
            GROUP BY dest, unique_carrier
        ),
        filtered AS (
            SELECT * FROM route_grouped
            WHERE departures_performed >= @min_departures
        ),
        carrier_totals AS (
            SELECT unique_carrier, SUM(total_seats) AS carrier_seats
            FROM filtered
            GROUP BY 1
            ORDER BY carrier_seats DESC
            LIMIT 1
        )
        SELECT 
            COUNT(DISTINCT dest) AS direct_destinations,
            SUM(departures_performed) AS total_departures,
            SUM(total_seats) AS total_seats,
            SUM(operational_passengers) AS total_passengers,
            ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct,
            ROUND(AVG(avg_od_fare), 2) AS avg_od_fare,
            (SELECT unique_carrier FROM carrier_totals) AS leading_carrier
        FROM filtered
    """
    df = run_query(query, params={"airport_code": airport_code, "year": year, "min_departures": min_departures})
    if not df.empty:
        return df.iloc[0].to_dict()
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
    """Fetches full route network details with GPS coordinates, applying min_departures frequency filter."""
    query = f"""
        WITH route_agg AS (
            SELECT 
                origin,
                origin_name,
                origin_city,
                origin_lat,
                origin_lon,
                dest,
                dest_name,
                dest_city,
                dest_state,
                dest_country,
                dest_lat,
                dest_lon,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS operational_passengers,
                ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct,
                ROUND(SAFE_DIVIDE(SUM(total_seats), NULLIF(SUM(departures_performed), 0)), 1) AS avg_gauge_seats,
                AVG(distance_miles) AS distance_miles,
                ROUND(AVG(avg_od_fare), 2) AS avg_od_fare,
                STRING_AGG(DISTINCT unique_carrier, ', ' ORDER BY unique_carrier) AS operating_carriers
            FROM `db1b-1.reporting.mart_airport_network_summary`
            WHERE origin = @airport_code 
              AND year = @year
              {'AND operational_passengers > 0 AND total_seats > 0' if passenger_only else ''}
              AND origin_lat IS NOT NULL 
              AND dest_lat IS NOT NULL
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
    """Fetches carrier market share breakdown by seats and passenger volume."""
    query = f"""
        WITH carrier_agg AS (
            SELECT 
                unique_carrier,
                carrier_name,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS operational_passengers,
                ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct,
                ROUND(AVG(avg_od_fare), 2) AS avg_fare
            FROM `db1b-1.reporting.mart_airport_network_summary`
            WHERE origin = @airport_code AND year = @year
            {'AND operational_passengers > 0 AND total_seats > 0' if passenger_only else ''}
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
    query = """
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
        od_demand AS (
            SELECT 
                origin,
                destination AS dest,
                -- Scale DB1B 10% sample volume by 10x for true 100% annual passenger count
                SUM(estimated_passengers * 10) AS annual_od_passengers,
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
            ROUND(ST_DISTANCE(ST_GEOGPOINT(o_apt.longitude, o_apt.latitude), ST_GEOGPOINT(d_apt.longitude, d_apt.latitude)) / 1609.34, 0) AS distance_miles
        FROM od_demand d
        LEFT JOIN nonstop_serviced n ON d.dest = n.dest
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
    query = """
        SELECT 
            unique_carrier,
            carrier_name,
            SUM(departures_performed) AS departures_performed,
            SUM(total_seats) AS total_seats,
            SUM(operational_passengers) AS operational_passengers,
            ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct,
            ROUND(AVG(distance_miles), 0) AS distance_miles,
            ROUND(AVG(avg_od_fare), 2) AS avg_fare
        FROM `db1b-1.reporting.mart_airport_network_summary`
        WHERE origin = @origin AND dest = @dest AND year = @year
          AND departures_performed >= 5
        GROUP BY 1, 2
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
def get_airline_kpis(carrier_code: str, year: int) -> Dict[str, Any]:
    """Calculates top-level performance KPIs for an airline."""
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
    if not df.empty:
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
def get_airline_hubs(carrier_code: str, year: int) -> pd.DataFrame:
    """Fetches top hub operations for an airline by seats and departures."""
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
def get_airline_yield_curve(carrier_code: str, year: int) -> pd.DataFrame:
    """Fetches route-level stage length vs fare yields for an airline."""
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
          AND avg_od_fare > 20 AND avg_stage_length_miles > 50
        ORDER BY operational_passengers DESC
        LIMIT 200
    """
    return run_query(query, params={"carrier_code": carrier_code, "year": year})


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
