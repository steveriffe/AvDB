"""
Automated Filter & Query Matrix Unit Tests across AvDB Dashboards.
Tests current and historical carriers, airports, and fleet types.
"""
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import pandas as pd
from app.utils.queries import (
    get_airline_kpis,
    get_airline_hubs,
    get_airline_yield_curve,
    get_airline_routes_dataset,
    get_available_airports,
    get_airport_kpis,
    get_airport_routes_dataset,
    get_airport_carrier_breakdown,
    get_airport_fleet_mix,
    get_fleet_kpis,
    get_fleet_aircraft_breakdown,
    get_fleet_operators_breakdown
)

def test_airline_dashboard_filters():
    print("\n--- Testing Airline Dashboard Filters (Current & Historical) ---")
    carriers_to_test = [
        ("AS", 2024, "Alaska Airlines Current"),
        ("AS", 2010, "Alaska Airlines Historical (2010)"),
        ("CO", 2005, "Continental Airlines Historical (2005)"),
        ("NW", 2005, "Northwest Airlines Historical (2005)"),
        ("US", 2010, "US Airways Historical (2010)"),
        ("HP", 2000, "America West Airlines Historical (2000)"),
        ("TW", 2000, "Trans World Airlines Historical (2000)"),
        ("FL", 2008, "AirTran Airways Historical (2008)"),
        ("DL", 2023, "Delta Air Lines Current"),
        ("UA", 2023, "United Airlines Current"),
        ("AA", 2023, "American Airlines Current"),
    ]

    for code, year, desc in carriers_to_test:
        print(f"\nTesting: {desc} ({code}, {year})")
        kpis = get_airline_kpis(code, year)
        print(f"  KPIs: active_routes={kpis.get('active_routes')}, total_deps={kpis.get('total_departures')}, total_pax={kpis.get('total_passengers')}")
        assert kpis.get("total_departures", 0) > 0, f"Expected departures for {code} in {year}, got 0"
        assert kpis.get("total_passengers", 0) > 0, f"Expected passengers for {code} in {year}, got 0"

        hubs = get_airline_hubs(code, year)
        print(f"  Hubs count: {len(hubs)}")
        assert len(hubs) > 0, f"Expected hubs for {code} in {year}, got 0"

        routes = get_airline_routes_dataset(code, year, min_departures=10)
        print(f"  Routes dataset count: {len(routes)}")
        assert len(routes) > 0, f"Expected routes for {code} in {year}, got 0"

        yields = get_airline_yield_curve(code, year)
        print(f"  Yield curve stage points: {len(yields)}")
        assert isinstance(yields, pd.DataFrame), f"Yield curve should return DataFrame for {code} in {year}"

    print("✅ All Airline Dashboard filter tests passed!")


def test_airport_dashboard_filters():
    print("\n--- Testing Airport Dashboard Filters (Current & Historical) ---")
    test_cases = [
        ("SEA", 2024, True, 10),
        ("SEA", 2010, True, 10),
        ("ORD", 2023, True, 10),
        ("ORD", 2005, True, 10),
        ("ATL", 2024, False, 10),
        ("ATL", 2000, True, 10),
        ("DFW", 2020, True, 365),
    ]

    for apt, yr, pax_only, min_deps in test_cases:
        print(f"\nTesting Airport: {apt}, Year: {yr}, PaxOnly: {pax_only}, MinDeps: {min_deps}")
        kpis = get_airport_kpis(apt, yr, passenger_only=pax_only, min_departures=min_deps)
        print(f"  KPIs: pax={kpis.get('total_passengers')}, deps={kpis.get('total_departures')}")
        assert kpis.get("total_departures", 0) > 0, f"Expected departures for {apt} in {yr}"
        assert kpis.get("total_passengers", 0) > 0, f"Expected passengers for {apt} in {yr}"

        routes = get_airport_routes_dataset(apt, yr, passenger_only=pax_only, min_departures=min_deps)
        print(f"  Direct routes: {len(routes)}")
        assert len(routes) > 0, f"Expected routes for {apt} in {yr}"

        carriers = get_airport_carrier_breakdown(apt, yr, passenger_only=pax_only, min_departures=min_deps)
        print(f"  Operating carriers: {len(carriers)}")
        assert len(carriers) > 0, f"Expected carriers for {apt} in {yr}"

        fleet = get_airport_fleet_mix(apt, yr, passenger_only=pax_only, min_departures=min_deps)
        print(f"  Fleet types: {len(fleet)}")
        assert len(fleet) > 0, f"Expected fleet mix for {apt} in {yr}"

    print("✅ All Airport Dashboard filter tests passed!")


def test_fleet_dashboard_filters():
    print("\n--- Testing Fleet Dashboard Filters (Current & Historical) ---")
    test_cases = [
        ("Boeing 737 Family (737-700/800/900/MAX)", 2024),
        ("Boeing 737 Family (737-700/800/900/MAX)", 2005),
        ("Boeing Widebody (777/787/767)", 2024),
        ("Boeing Widebody (777/787/767)", 2000),
        ("Airbus A320 Family (A319/A320/A321)", 2024),
        ("Airbus A320 Family (A319/A320/A321)", 2010),
    ]
    for fam, yr in test_cases:
        print(f"\nTesting Fleet Family: {fam} ({yr})")
        kpis = get_fleet_kpis(fam, yr)
        print(f"  KPIs: models={kpis.get('unique_models')}, carriers={kpis.get('operating_carriers')}, deps={kpis.get('total_departures')}")
        assert kpis.get("total_departures", 0) > 0, f"Expected departures for {fam} in {yr}"

        models = get_fleet_aircraft_breakdown(fam, yr)
        print(f"  Submodels: {len(models)}")
        assert len(models) > 0, f"Expected models for {fam} in {yr}"

        operators = get_fleet_operators_breakdown(fam, yr)
        print(f"  Operators: {len(operators)}")
        assert len(operators) > 0, f"Expected operators for {fam} in {yr}"

    print("✅ All Fleet Dashboard filter tests passed!")


if __name__ == "__main__":
    test_airline_dashboard_filters()
    test_airport_dashboard_filters()
    test_fleet_dashboard_filters()
    print("\n=======================================================")
    print("🏆 ALL DASHBOARD FILTER & QUERY TESTS PASSED SUCCESSFULLY!")
    print("=======================================================")
