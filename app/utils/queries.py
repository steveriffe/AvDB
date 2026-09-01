"""
BigQuery Query Layer for AvDB Streamlit Dashboard
Cached with @st.cache_data for instant interactive responses.
"""
import streamlit as st
import pandas as pd
from typing import Optional, List, Dict, Any
from app.utils.bq_client import run_query
from app.config import settings

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
def get_airport_kpis(airport_code: str, year: int, passenger_only: bool = True) -> Dict[str, Any]:
    """Calculates top-level KPI metrics for an airport in a given year."""
    query = f"""
        WITH filtered AS (
            SELECT 
                dest,
                unique_carrier,
                departures_performed,
                total_seats,
                operational_passengers,
                avg_od_fare
            FROM `db1b-1.reporting.mart_airport_network_summary`
            WHERE origin = @airport_code AND year = @year
            {'AND operational_passengers > 0 AND total_seats > 0' if passenger_only else ''}
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
    df = run_query(query, params={"airport_code": airport_code, "year": year})
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
def get_airport_routes_dataset(airport_code: str, year: int, passenger_only: bool = True) -> pd.DataFrame:
    """Fetches full route network details with GPS coordinates and fares for mapping."""
    query = f"""
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
        ORDER BY operational_passengers DESC
    """
    return run_query(query, params={"airport_code": airport_code, "year": year})


@st.cache_data(ttl=3600, show_spinner=False)
def get_airport_carrier_breakdown(airport_code: str, year: int, passenger_only: bool = True) -> pd.DataFrame:
    """Fetches carrier market share breakdown by seats and passenger volume."""
    query = f"""
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
        ORDER BY total_seats DESC
    """
    return run_query(query, params={"airport_code": airport_code, "year": year})


@st.cache_data(ttl=3600, show_spinner=False)
def get_airport_fleet_mix(airport_code: str, year: int, passenger_only: bool = True) -> pd.DataFrame:
    """Fetches airport fleet deployment mix by aircraft family and specific model."""
    query = f"""
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
        ORDER BY operational_passengers DESC
    """
    return run_query(query, params={"airport_code": airport_code, "year": year})
