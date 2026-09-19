"""
AvDB Unified Test Suite Runner & Regression Verification
Executes all unit tests and checks for packaging, styling, auth, and query safety.
"""
import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

def test_kpi_styling_alias():
    """Verify render_kpi_card accepts both label and title without error."""
    import streamlit as st
    from app.utils.styling import render_kpi_card
    
    # Should not raise TypeError:
    render_kpi_card(label="Test Label", value="100")
    render_kpi_card(title="Test Title", value="200")
    render_kpi_card(label="Test Label 2", title="Ignored Title", value="300")
    print("✅ Styling render_kpi_card alias tests passed!")


def test_landing_page_rendering():
    """Verify render_landing_page and render_html run without TypeError."""
    from app.components.landing import render_landing_page, render_unauthorized_page
    from app.utils.styling import render_html

    render_html("<div>test</div>", unsafe_allow_html=True)
    render_landing_page()
    render_unauthorized_page({"email": "test@test.com", "name": "Tester", "picture": ""})
    print("✅ Landing page and render_html tests passed!")


def test_auth_open_registration():
    """Verify open registration allows any Google-authenticated user when ALLOWED_EMAILS is '*'."""
    import streamlit as st
    from app.config import settings
    from app.utils.auth import is_authenticated

    # Mock session state
    st.session_state["user"] = {"email": "random_user@gmail.com", "name": "Google User"}
    assert is_authenticated() is True, "Expected open registration for random_user@gmail.com"

    st.session_state["user"] = {"email": "pilot@delta.com", "name": "Delta Pilot"}
    assert is_authenticated() is True, "Expected open registration for pilot@delta.com"

    st.session_state["user"] = None
    assert is_authenticated() is False, "Expected False for unauthenticated user"
    print("✅ Open Google authentication tests passed!")


def test_ignore_rules():
    """Verify git check-ignore respects /data/ vs app/data/."""
    cmd = ["git", "check-ignore", "data/", "app/data/", "app/data/ref_mergers.py"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    ignored = res.stdout.strip().splitlines()
    assert "data/" in ignored, "Expected root data/ to be ignored"
    assert "app/data/" not in ignored, "Expected app/data/ NOT to be ignored"
    assert "app/data/ref_mergers.py" not in ignored, "Expected app/data/ref_mergers.py NOT to be ignored"

    # Verify .dockerignore and .gcloudignore have /data/, !app/data/, and .env
    dockerignore = (REPO_ROOT / ".dockerignore").read_text()
    assert "/data/" in dockerignore and "!app/data/" in dockerignore, "Missing anchored data rules in .dockerignore"
    assert ".env" in dockerignore, "Missing .env in .dockerignore"

    gcloudignore = (REPO_ROOT / ".gcloudignore").read_text()
    assert "/data/" in gcloudignore and "!app/data/" in gcloudignore, "Missing anchored data rules in .gcloudignore"
    assert ".env" in gcloudignore, "Missing .env in .gcloudignore"
    print("✅ Ignore rules and packaging protection tests passed!")


def test_carrier_breakdown_query():
    """Verify get_airport_carrier_breakdown includes carrier_name in carrier_attributed CTE."""
    from app.utils.queries import CARRIER_NAME_LOOKUP_SQL
    import inspect
    from app.utils import queries
    
    assert "COALESCE(carrier_name, carrier_code)" in CARRIER_NAME_LOOKUP_SQL, "CARRIER_NAME_LOOKUP_SQL missing safe COALESCE fallback"

    source = inspect.getsource(queries.get_airport_carrier_breakdown)
    assert "carrier_name," in source, "carrier_attributed CTE missing carrier_name column"
    print("✅ Carrier breakdown query and name lookup SQL verified!")


def run_existing_tests():
    """Run all existing unit test files."""
    test_files = [
        "tests/test_aircraft_specs.py",
        "tests/test_alliances.py",
        "tests/test_mergers.py",
        "tests/test_flighty.py",
        "tests/test_api.py",
    ]
    for tf in test_files:
        print(f"\n--- Running {tf} ---")
        cmd = [sys.executable, str(REPO_ROOT / tf)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ Failed: {tf}\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")
            sys.exit(res.returncode)
        else:
            print(res.stdout.strip())


def test_all_module_imports():
    """Verify that all core modules import cleanly and page scripts compile without syntax/import errors."""
    import importlib
    import py_compile

    modules = [
        "app.config",
        "app.utils.auth",
        "app.utils.styling",
        "app.utils.queries",
        "app.utils.visualizers",
        "app.utils.flighty",
        "app.utils.alliances",
        "app.utils.mergers",
        "app.data.ref_aircraft_specs",
        "app.data.ref_alliances",
        "app.data.ref_mergers",
        "app.data.ref_demo_peeks",
        "app.components.landing",
        "api.config",
        "api.schemas",
        "api.bq",
        "api.cache",
        "api.main",
        "api.routers.airports",
        "api.routers.airlines",
        "api.routers.fleet",
    ]
    for mod in modules:
        importlib.import_module(mod)

    # Compile Streamlit page scripts to verify syntax and structure
    page_files = [
        "app/main.py",
        "app/pages/1_✈️_Airports.py",
        "app/pages/2_🏢_Airlines.py",
        "app/pages/3_💺_Fleet_Routes.py",
        "app/pages/4_📱_Flighty_Traveler.py",
        "app/pages/5_🌐_Alliances.py",
        "app/pages/6_🔒_Privacy_Policy.py",
    ]
    for pf in page_files:
        py_compile.compile(str(REPO_ROOT / pf), doraise=True)

    print("✅ All core modules imported and all Streamlit pages compiled cleanly!")


def test_time_series_queries():
    """Verify time series queries execute against BigQuery without syntax or partitioning errors, and KPIs match."""
    import pandas as pd
    from app.utils.queries import (
        get_airport_time_series,
        get_airport_kpis,
        get_airline_time_series,
        get_fleet_time_series,
        get_alliances_time_series
    )
    from app.utils.visualizers import build_airline_network_deck
    
    df_apt = get_airport_time_series("SEA", passenger_only=True)
    assert not df_apt.empty, "Expected non-empty time series for SEA"
    assert "year" in df_apt.columns and "top_carrier" in df_apt.columns
    assert df_apt["year"].max() == 2025, "Time series should cap at completed year 2025"

    # Verify COS KPI harmony and peak network accuracy (Western Pacific 1996 hub peak)
    cos_kpi_2025 = get_airport_kpis("COS", 2025, min_departures=10)
    cos_ts = get_airport_time_series("COS", passenger_only=True, min_departures=10)
    cos_ts_2025 = cos_ts[cos_ts["year"] == 2025].iloc[0]
    assert cos_kpi_2025["total_passengers"] == cos_ts_2025["total_passengers"], "Airport KPI total pax must match time series"
    cos_peak_dest = cos_ts.loc[cos_ts["direct_destinations"].idxmax()]
    assert int(cos_peak_dest["year"]) == 1996, f"Expected 1996 peak destinations for COS, got {cos_peak_dest['year']}"
    assert cos_peak_dest["direct_destinations"] == 36, f"Expected 36 peak destinations for COS in 1996, got {cos_peak_dest['direct_destinations']}"

    df_air = get_airline_time_series("UA")
    assert not df_air.empty, "Expected non-empty time series for UA"
    assert "total_asm" in df_air.columns and "total_rpm" in df_air.columns
    assert df_air["year"].max() == 2025

    df_fleet = get_fleet_time_series()
    assert not df_fleet.empty, "Expected non-empty fleet time series"
    assert "avg_gauge" in df_fleet.columns
    assert df_fleet["year"].max() == 2025

    df_alliances = get_alliances_time_series()
    assert not df_alliances.empty, "Expected non-empty alliances time series"
    assert "pax_share_pct" in df_alliances.columns
    assert df_alliances["year"].max() == 2025

    # Verify build_airline_network_deck layer toggling (Dots Only vs Arcs)
    mock_routes = pd.DataFrame([{
        'origin': 'SEA', 'origin_name': 'Seattle', 'origin_city': 'Seattle', 'origin_lat': 47.4, 'origin_lon': -122.3,
        'dest': 'ANC', 'dest_name': 'Anchorage', 'dest_city': 'Anchorage', 'dest_state': 'AK', 'dest_country': 'US',
        'dest_lat': 61.1, 'dest_lon': -149.9, 'departures_performed': 100, 'total_seats': 15000,
        'operational_passengers': 12000, 'load_factor_pct': 80.0, 'avg_gauge_seats': 150, 'distance_miles': 1400, 'avg_od_fare': 300
    }])
    deck_arcs = build_airline_network_deck(mock_routes, ['SEA'], label_density='hubs_only', show_routes=True)
    deck_dots = build_airline_network_deck(mock_routes, ['SEA'], label_density='dots_only', show_routes=False)
    deck_clean = build_airline_network_deck(mock_routes, ['SEA'], label_density='none', show_routes=True)
    assert any(l.type == 'GreatCircleLayer' for l in deck_arcs.layers)
    assert not any(l.type == 'GreatCircleLayer' for l in deck_dots.layers)
    assert not any(l.type == 'TextLayer' for l in deck_dots.layers)
    assert not any(l.type == 'TextLayer' for l in deck_clean.layers)

    print("✅ All four time series queries verified (1990-2025 completed years) and KPI/map layers verified!")


def test_regional_carrier_attribution():
    """Verify regional carrier attribution properly maps contract & subsidiary flying to mainlines."""
    from app.utils.queries import (
        get_airport_kpis,
        get_airport_carrier_breakdown,
        get_airport_time_series,
        get_route_carrier_competition,
        get_airline_kpis
    )
    
    # Test 1: Eugene (EUG) in 2019 - Alaska should be leading carrier
    eug_2019_kpi = get_airport_kpis("EUG", 2019)
    assert eug_2019_kpi["leading_carrier"] == "AS", f"Expected AS to be leading carrier at EUG in 2019, got {eug_2019_kpi['leading_carrier']}"

    # Test 2: EUG Carrier Breakdown in 2019
    df_eug_2019 = get_airport_carrier_breakdown("EUG", 2019)
    assert not df_eug_2019.empty
    assert df_eug_2019.iloc[0]["unique_carrier"] == "AS", f"Expected #1 carrier to be AS, got {df_eug_2019.iloc[0]['unique_carrier']}"
    assert df_eug_2019.iloc[0]["operational_passengers"] > 200000

    # Test 3: EUG Time Series - no raw regional codes in top_carrier
    df_eug_ts = get_airport_time_series("EUG")
    assert not df_eug_ts.empty
    recent_tops = set(df_eug_ts[df_eug_ts["year"] >= 2010]["top_carrier"].dropna())
    assert "OO" not in recent_tops, "SkyWest (OO) should not appear as top_carrier"
    assert "QX" not in recent_tops, "Horizon (QX) should not appear as top_carrier"

    # Test 4: EUG-SEA Route Competition attributes to AS and DL
    df_comp = get_route_carrier_competition("EUG", "SEA", 2024)
    assert not df_comp.empty
    comp_carriers = set(df_comp["unique_carrier"].values)
    assert "AS" in comp_carriers, "Expected AS in EUG-SEA competition"
    assert "DL" in comp_carriers, "Expected DL in EUG-SEA competition"
    assert "OO" not in comp_carriers, "Expected OO to be attributed on EUG-SEA"

    # Test 5: Alaska Airlines full network includes regional capacity
    as_full_kpi = get_airline_kpis("AS", 2024, include_regionals=True)
    assert as_full_kpi["total_passengers"] > 40_000_000, f"Expected full AS network > 40M pax, got {as_full_kpi['total_passengers']}"

    print("✅ Regional carrier attribution tests passed (EUG properly attributed to AS/DL)!")


def test_demo_peeks_and_sample_deck():
    """Verify curated peeks, sample flighty travel deck, and monochromatic basemap."""
    from app.data.ref_demo_peeks import DEMO_PEEKS
    from app.utils.flighty import generate_sample_flighty_data, build_flighty_travel_deck
    from app.components.landing import _build_anc_demo_deck

    df = generate_sample_flighty_data()
    assert len(df) > 0, "Expected sample flighty travel data"

    # Monochromatic PyDeck route decks generate correctly
    deck = build_flighty_travel_deck(df, home_airport="SEA", map_theme="retro", colorway="cobalt")
    assert len(deck.layers) >= 2, "Expected PyDeck deck with Great-Circle layers"

    deck_anc = _build_anc_demo_deck()
    assert len(deck_anc.layers) >= 2, "Expected ANC demo deck with monochromatic route layers"

    # Curated peeks exist
    assert "anc_2025" in DEMO_PEEKS, "Expected anc_2025 peek"
    assert "as_2025" in DEMO_PEEKS, "Expected as_2025 peek"

    print("✅ Curated peeks and sample flighty travel decks verified!")


if __name__ == "__main__":
    print("==========================================")
    print("🚀 Running AvDB Complete Verification Suite")
    print("==========================================")
    test_kpi_styling_alias()
    test_landing_page_rendering()
    test_auth_open_registration()
    test_ignore_rules()
    test_carrier_breakdown_query()
    test_all_module_imports()
    test_time_series_queries()
    test_regional_carrier_attribution()
    test_demo_peeks_and_sample_deck()
    run_existing_tests()
    print("\n==========================================")
    print("🎉 ALL AVDB TEST SUITES & REGRESSIONS PASSED!")
    print("==========================================")

