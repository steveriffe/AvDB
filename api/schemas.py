"""
Pydantic Schemas for AvDB API & iOS Client Serialization
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# -------------------------------------------------------------
# AIRPORT MODELS
# -------------------------------------------------------------

class Airport(BaseModel):
    airport_code: str
    airport_name: str
    city: str
    state: str = ""
    country: str = "US"
    is_commercial: bool = True
    is_metro_code: bool = False
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CatchmentInfo(BaseModel):
    market_code: str
    market_name: str
    metro_city: str
    member_airports: List[str]
    description: Optional[str] = None


class AirportKPIs(BaseModel):
    airport_code: str
    year: int
    direct_destinations: int
    total_departures: int
    total_seats: int
    total_passengers: int
    load_factor_pct: float
    avg_od_fare: Optional[float] = None
    leading_carrier: str = "—"


class RouteItem(BaseModel):
    origin: str
    origin_name: Optional[str] = None
    origin_city: Optional[str] = None
    origin_lat: float
    origin_lon: float
    dest: str
    dest_name: Optional[str] = None
    dest_city: Optional[str] = None
    dest_state: Optional[str] = None
    dest_country: Optional[str] = None
    dest_lat: float
    dest_lon: float
    departures_performed: int
    total_seats: int
    operational_passengers: int
    load_factor_pct: float
    avg_gauge_seats: float
    distance_miles: float
    avg_od_fare: Optional[float] = None
    operating_carriers: Optional[str] = None


class AirportCarrierShare(BaseModel):
    unique_carrier: str
    carrier_name: Optional[str] = None
    departures_performed: int
    total_seats: int
    operational_passengers: int
    load_factor_pct: float
    avg_fare: Optional[float] = None


# -------------------------------------------------------------
# AIRLINE MODELS
# -------------------------------------------------------------

class AirlineKPIs(BaseModel):
    carrier_code: str
    year: int
    active_routes: int
    total_departures: int
    total_seats: int
    total_passengers: int
    total_asm: int
    total_rpm: int
    system_load_factor: float
    avg_network_fare: float
    avg_yield_per_mile: float


class AirlineHub(BaseModel):
    airport_code: str
    origin_name: Optional[str] = None
    origin_city: Optional[str] = None
    departures_performed: int
    total_seats: int
    total_passengers: int
    direct_destinations: int


class YieldCurvePoint(BaseModel):
    origin: str
    dest: str
    route_label: str
    stage_length_miles: float
    avg_od_fare: float
    yield_per_mile: float
    operational_passengers: int
    load_factor_pct: float


class AirlineNetworkResponse(BaseModel):
    carrier_code: str
    carrier_name: str
    year: int
    hubs: List[AirlineHub]
    routes: List[RouteItem]


# -------------------------------------------------------------
# FLEET MODELS
# -------------------------------------------------------------

class FleetKPIs(BaseModel):
    family_filter: str
    year: int
    unique_models: int
    operating_carriers: int
    total_departures: int
    total_seats: int
    total_passengers: int
    avg_gauge_seats: float
    fleet_load_factor: float
    avg_stage_length: int
    avg_segment_fare: float
    yield_per_mile: float


class SubfleetItem(BaseModel):
    aircraft_family: str
    aircraft_description: str
    departures_performed: int
    total_seats: int
    operational_passengers: int
    avg_gauge_seats: float
    load_factor_pct: float
    avg_stage_length: int
    avg_segment_fare: float
    yield_per_mile: float


class FleetSummaryResponse(BaseModel):
    family_filter: str
    year: int
    kpis: FleetKPIs
    subfleets: List[SubfleetItem]


# -------------------------------------------------------------
# CONFIGURATION & SETTINGS MODELS
# -------------------------------------------------------------

class SettingsResponse(BaseModel):
    mapbox_token: str
    mapbox_style_personal: str
    mapbox_style_love: str
    mapbox_style_mono: str
    supported_years: List[int] = [2024, 2023, 2022, 2021]
    api_version: str = "1.0.0"
