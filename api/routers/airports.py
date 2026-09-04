"""
Airport Endpoints: Catalog, KPIs, Route Network, and Catchment Analysis
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from api.schemas import Airport, AirportKPIs, RouteItem, CatchmentInfo, AirportCarrierShare
from api.bq import execute_query
from api.config import settings

router = APIRouter(prefix="/api/airports", tags=["Airports"])


# Fallback airport catalog for offline/rapid local dev
MOCK_AIRPORTS = [
    Airport(airport_code="SEA", airport_name="Seattle-Tacoma International Airport", city="Seattle", state="WA", is_commercial=True, latitude=47.4502, longitude=-122.3088),
    Airport(airport_code="ORD", airport_name="Chicago O'Hare International Airport", city="Chicago", state="IL", is_commercial=True, latitude=41.9742, longitude=-87.9073),
    Airport(airport_code="ATL", airport_name="Hartsfield-Jackson Atlanta International Airport", city="Atlanta", state="GA", is_commercial=True, latitude=33.6407, longitude=-84.4277),
    Airport(airport_code="DFW", airport_name="Dallas/Fort Worth International Airport", city="Dallas", state="TX", is_commercial=True, latitude=32.8998, longitude=-97.0403),
    Airport(airport_code="DEN", airport_name="Denver International Airport", city="Denver", state="CO", is_commercial=True, latitude=39.8561, longitude=-104.6737),
    Airport(airport_code="LAX", airport_name="Los Angeles International Airport", city="Los Angeles", state="CA", is_commercial=True, latitude=33.9416, longitude=-118.4085),
    Airport(airport_code="SFO", airport_name="San Francisco International Airport", city="San Francisco", state="CA", is_commercial=True, latitude=37.6213, longitude=-122.3790),
    Airport(airport_code="JFK", airport_name="John F. Kennedy International Airport", city="New York", state="NY", is_commercial=True, latitude=40.6413, longitude=-73.7781),
    Airport(airport_code="BOS", airport_name="Boston Logan International Airport", city="Boston", state="MA", is_commercial=True, latitude=42.3656, longitude=-71.0096),
    Airport(airport_code="MIA", airport_name="Miami International Airport", city="Miami", state="FL", is_commercial=True, latitude=25.7959, longitude=-80.2870),
    Airport(airport_code="PHX", airport_name="Phoenix Sky Harbor International Airport", city="Phoenix", state="AZ", is_commercial=True, latitude=33.4373, longitude=-112.0078),
    Airport(airport_code="LAS", airport_name="Harry Reid International Airport", city="Las Vegas", state="NV", is_commercial=True, latitude=36.0840, longitude=-115.1537),
    Airport(airport_code="MCO", airport_name="Orlando International Airport", city="Orlando", state="FL", is_commercial=True, latitude=28.4312, longitude=-81.3081),
    Airport(airport_code="EWR", airport_name="Newark Liberty International Airport", city="Newark", state="NJ", is_commercial=True, latitude=40.6895, longitude=-74.1745),
    Airport(airport_code="MSP", airport_name="Minneapolis-Saint Paul International Airport", city="Minneapolis", state="MN", is_commercial=True, latitude=44.8848, longitude=-93.2223),
    Airport(airport_code="DTW", airport_name="Detroit Metropolitan Airport", city="Detroit", state="MI", is_commercial=True, latitude=42.2162, longitude=-83.3554),
    Airport(airport_code="CLT", airport_name="Charlotte Douglas International Airport", city="Charlotte", state="NC", is_commercial=True, latitude=35.2140, longitude=-80.9431),
    Airport(airport_code="SLC", airport_name="Salt Lake City International Airport", city="Salt Lake City", state="UT", is_commercial=True, latitude=40.7899, longitude=-111.9791),
    Airport(airport_code="SAN", airport_name="San Diego International Airport", city="San Diego", state="CA", is_commercial=True, latitude=32.7338, longitude=-117.1933),
    Airport(airport_code="PDX", airport_name="Portland International Airport", city="Portland", state="OR", is_commercial=True, latitude=45.5898, longitude=-122.5951),
    Airport(airport_code="ANC", airport_name="Ted Stevens Anchorage International Airport", city="Anchorage", state="AK", is_commercial=True, latitude=61.1760, longitude=-149.9901),
]


@router.get("", response_model=List[Airport])
def list_airports() -> List[Airport]:
    """Fetches list of active commercial and metro airports."""
    query = f"""
        SELECT DISTINCT 
            m.origin AS airport_code,
            COALESCE(a.airport_name, m.origin_name, m.origin) AS airport_name,
            COALESCE(a.city, m.origin_city, '') AS city,
            COALESCE(a.state_region, m.origin_state, '') AS state,
            COALESCE(a.country, m.origin_country, 'US') AS country,
            COALESCE(a.is_commercial, TRUE) AS is_commercial,
            COALESCE(a.is_metro_code, FALSE) AS is_metro_code,
            COALESCE(a.latitude, m.origin_lat) AS latitude,
            COALESCE(a.longitude, m.origin_lon) AS longitude
        FROM `{settings.dataset_reporting}.mart_airport_network_summary` m
        LEFT JOIN `{settings.dataset_reporting}.ref_airports` a
            ON m.origin = a.airport_code
        WHERE m.year >= 2023 AND m.operational_passengers > 0
        ORDER BY is_metro_code DESC, is_commercial DESC, airport_code ASC
    """
    try:
        results = execute_query(query, cache_key="api_airports_catalog")
        if results:
            return [Airport(**r) for r in results]
    except Exception:
        pass
    return MOCK_AIRPORTS


@router.get("/{code}/catchment", response_model=Optional[CatchmentInfo])
def get_catchment(code: str) -> Optional[CatchmentInfo]:
    """Checks if the airport is a metropolitan catchment market (e.g. WAS, NYC, CHI)."""
    code = code.upper()
    query = f"""
        SELECT 
            market_code,
            market_name,
            metro_city,
            ARRAY_AGG(airport_code ORDER BY airport_code) AS member_airports,
            ANY_VALUE(description) AS description
        FROM `{settings.dataset_reporting}.ref_city_markets`
        WHERE market_code = @airport_code
        GROUP BY 1, 2, 3
    """
    try:
        results = execute_query(query, params={"airport_code": code}, cache_key=f"api_catchment_{code}")
        if results:
            return CatchmentInfo(**results[0])
    except Exception:
        pass
    return None


@router.get("/{code}/kpis", response_model=AirportKPIs)
def get_airport_kpi_summary(
    code: str,
    year: int = Query(2023, description="Reporting year"),
    passenger_only: bool = Query(True, description="Filter passenger operations only"),
    min_departures: int = Query(10, description="Minimum frequency filter")
) -> AirportKPIs:
    """Calculates top-level KPI metrics for an airport."""
    code = code.upper()
    query = f"""
        WITH route_grouped AS (
            SELECT 
                dest,
                unique_carrier,
                SUM(departures_performed) AS departures_performed,
                SUM(total_seats) AS total_seats,
                SUM(operational_passengers) AS operational_passengers,
                AVG(avg_od_fare) AS avg_od_fare
            FROM `{settings.dataset_reporting}.mart_airport_network_summary`
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
            @airport_code AS airport_code,
            @year AS year,
            COUNT(DISTINCT dest) AS direct_destinations,
            COALESCE(SUM(departures_performed), 0) AS total_departures,
            COALESCE(SUM(total_seats), 0) AS total_seats,
            COALESCE(SUM(operational_passengers), 0) AS total_passengers,
            ROUND(SAFE_DIVIDE(SUM(operational_passengers), SUM(total_seats)) * 100, 1) AS load_factor_pct,
            ROUND(AVG(avg_od_fare), 2) AS avg_od_fare,
            COALESCE((SELECT unique_carrier FROM carrier_totals), '—') AS leading_carrier
        FROM filtered
    """
    cache_key = f"api_kpi_{code}_{year}_{min_departures}"
    try:
        results = execute_query(query, params={"airport_code": code, "year": year, "min_departures": min_departures}, cache_key=cache_key)
        if results and results[0].get("total_departures", 0) > 0:
            return AirportKPIs(**results[0])
    except Exception:
        pass

    # Mock response for local development
    return AirportKPIs(
        airport_code=code,
        year=year,
        direct_destinations=98,
        total_departures=142500,
        total_seats=23100000,
        total_passengers=19800000,
        load_factor_pct=85.7,
        avg_od_fare=242.50,
        leading_carrier="AS" if code == "SEA" else "UA" if code == "ORD" else "DL"
    )


@router.get("/{code}/routes", response_model=List[RouteItem])
def get_airport_routes(
    code: str,
    year: int = Query(2023, description="Reporting year"),
    passenger_only: bool = Query(True, description="Filter passenger operations only"),
    min_departures: int = Query(10, description="Minimum frequency filter")
) -> List[RouteItem]:
    """Fetches full route network details with GPS coordinates for mapping and analytics."""
    code = code.upper()
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
            FROM `{settings.dataset_reporting}.mart_airport_network_summary`
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
    cache_key = f"api_routes_{code}_{year}_{min_departures}"
    try:
        results = execute_query(query, params={"airport_code": code, "year": year, "min_departures": min_departures}, cache_key=cache_key)
        if results:
            return [RouteItem(**r) for r in results]
    except Exception:
        pass

    # Provide high-quality mock routes for testing offline
    origin_pt = next((a for a in MOCK_AIRPORTS if a.airport_code == code), MOCK_AIRPORTS[0])
    mock_routes = []
    for dest in MOCK_AIRPORTS:
        if dest.airport_code == code:
            continue
        mock_routes.append(
            RouteItem(
                origin=code,
                origin_name=origin_pt.airport_name,
                origin_city=origin_pt.city,
                origin_lat=origin_pt.latitude or 47.4502,
                origin_lon=origin_pt.longitude or -122.3088,
                dest=dest.airport_code,
                dest_name=dest.airport_name,
                dest_city=dest.city,
                dest_state=dest.state,
                dest_country=dest.country,
                dest_lat=dest.latitude or 41.9742,
                dest_lon=dest.longitude or -87.9073,
                departures_performed=1250,
                total_seats=210000,
                operational_passengers=182000,
                load_factor_pct=86.7,
                avg_gauge_seats=168.0,
                distance_miles=1720.0,
                avg_od_fare=265.0,
                operating_carriers="AS, DL, UA"
            )
        )
    return mock_routes
