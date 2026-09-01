import sys
from pathlib import Path

# Automatically add project root to Python path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import os
import streamlit as st
import pandas as pd
from app.config import settings
from app.utils.styling import apply_apple_style, render_kpi_card
from app.utils.queries import (
    get_available_airports,
    get_airport_catchment_info,
    get_airport_kpis,
    get_airport_routes_dataset,
    get_airport_carrier_breakdown,
)
from app.utils.visualizers import (
    build_route_map_deck,
    build_top_routes_bar_chart,
    build_carrier_market_share_donut,
)

st.set_page_config(
    page_title="Airports Explorer | AvDB",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply Apple-esque CSS styling
apply_apple_style()

# -------------------------------------------------------------
# 1. Header & Top Control Filter Bar
# -------------------------------------------------------------
st.title("✈️ Airport Network & Route Explorer")
st.markdown("<p style='color: #8E8E93; margin-top: -12px; margin-bottom: 20px;'>Analyze origin route connectivity, direct carrier capacity, O&D yields, and great-circle flight paths.</p>", unsafe_allow_html=True)

# Fetch active airports
df_airports = get_available_airports()
airport_list = df_airports["airport_code"].tolist() if not df_airports.empty else ["ORD", "ATL", "DFW", "DEN", "LAX", "JFK", "SFO"]

# Default selection helper
default_index = airport_list.index("ORD") if "ORD" in airport_list else 0

filter_col1, filter_col2, filter_col3 = st.columns([2.5, 1.5, 2])

with filter_col1:
    selected_airport = st.selectbox(
        "Origin Airport / Catchment",
        options=airport_list,
        index=default_index,
        format_func=lambda code: f"{code} — {df_airports.loc[df_airports['airport_code'] == code, 'airport_name'].iloc[0]}" if not df_airports.empty and code in df_airports['airport_code'].values else code,
        label_visibility="collapsed"
    )

with filter_col2:
    selected_year = st.selectbox(
        "Analysis Year",
        options=[2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018],
        index=0,
        label_visibility="collapsed"
    )

# Check for Metropolitan Catchment mapping (e.g. WAS, NYC, CHI)
catchment_info = get_airport_catchment_info(selected_airport)
if catchment_info:
    members_str = ", ".join(catchment_info["member_airports"])
    st.markdown(f"""
        <div class="catchment-badge">
            🏛️ <b>Metropolitan Catchment Market</b>: {catchment_info['market_name']} (Includes: {members_str})
        </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. Top-Level Apple-Style KPI Cards
# -------------------------------------------------------------
kpi_data = get_airport_kpis(selected_airport, selected_year)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    pax_val = f"{kpi_data['total_passengers'] / 1e6:.2f}M" if kpi_data['total_passengers'] >= 1e6 else f"{kpi_data['total_passengers']:,}"
    render_kpi_card("Total Passengers", pax_val)

with kpi2:
    render_kpi_card("Direct Destinations", f"{kpi_data['direct_destinations']}")

with kpi3:
    lf_val = f"{kpi_data['load_factor_pct']:.1f}%" if kpi_data['load_factor_pct'] else "—"
    render_kpi_card("Avg Load Factor", lf_val)

with kpi4:
    fare_val = f"${kpi_data['avg_od_fare']:.0f}" if kpi_data.get('avg_od_fare') else "—"
    render_kpi_card("Inferred Avg Fare", fare_val)

with kpi5:
    render_kpi_card("Leading Carrier", f"{kpi_data.get('leading_carrier', '—')}")

# -------------------------------------------------------------
# 3. Top 1/3: Analytical Charts (Bar Chart & Donut)
# -------------------------------------------------------------
df_routes = get_airport_routes_dataset(selected_airport, selected_year)
df_carriers = get_airport_carrier_breakdown(selected_airport, selected_year)

chart_col1, chart_col2 = st.columns([1.2, 1])

with chart_col1:
    fig_routes = build_top_routes_bar_chart(df_routes, top_n=8)
    st.plotly_chart(fig_routes, use_container_width=True, config={"displayModeBar": False})

with chart_col2:
    fig_carriers = build_carrier_market_share_donut(df_carriers)
    st.plotly_chart(fig_carriers, use_container_width=True, config={"displayModeBar": False})

# -------------------------------------------------------------
# 4. Bottom 2/3 (Hero Section): Interactive Great-Circle Map
# -------------------------------------------------------------
st.markdown("### 🌐 Route Network & Great-Circle Paths")

if not df_routes.empty:
    origin_meta = {
        "airport_code": selected_airport,
        "airport_name": df_airports.loc[df_airports['airport_code'] == selected_airport, 'airport_name'].iloc[0] if not df_airports.empty and selected_airport in df_airports['airport_code'].values else selected_airport,
        "latitude": df_routes["origin_lat"].iloc[0],
        "longitude": df_routes["origin_lon"].iloc[0],
    }
    
    # Mapbox style and API key from environment / secrets
    mapbox_token = os.getenv("MAPBOX_API_KEY", "")
    mapbox_style = os.getenv("MAPBOX_STYLE", "mapbox://styles/mapbox/dark-v11" if mapbox_token else "dark")

    deck_map = build_route_map_deck(
        df_routes,
        origin_meta=origin_meta,
        mapbox_api_key=mapbox_token or None,
        mapbox_style=mapbox_style
    )

    st.pydeck_chart(deck_map, use_container_width=True)
else:
    st.info(f"No direct flight route operations recorded for {selected_airport} in {selected_year}.")

# -------------------------------------------------------------
# 5. Expandable Route Data Table
# -------------------------------------------------------------
with st.expander("📋 View Detailed Route Data Table"):
    if not df_routes.empty:
        display_df = df_routes[[
            "dest", "dest_name", "dest_city", "dest_state", "dest_country",
            "departures_performed", "total_seats", "operational_passengers",
            "load_factor_pct", "avg_gauge_seats", "distance_miles", "avg_od_fare", "operating_carriers"
        ]].rename(columns={
            "dest": "Destination",
            "dest_name": "Airport Name",
            "dest_city": "City",
            "dest_state": "State",
            "dest_country": "Country",
            "departures_performed": "Departures",
            "total_seats": "Seats",
            "operational_passengers": "Passengers",
            "load_factor_pct": "Load Factor %",
            "avg_gauge_seats": "Seats/Dep",
            "distance_miles": "Distance (mi)",
            "avg_od_fare": "Avg Fare ($)",
            "operating_carriers": "Carriers"
        })
        st.dataframe(display_df, use_container_width=True, hide_index=True)
