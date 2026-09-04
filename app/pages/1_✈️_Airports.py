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
    get_airport_fleet_mix,
    get_unserved_connecting_markets,
    get_route_carrier_competition,
)
from app.utils.visualizers import (
    build_route_map_deck,
    build_top_routes_bar_chart,
    build_carrier_market_share_donut,
    build_airport_alliance_share_donut,
    build_airport_fleet_bar_chart,
    build_unserved_markets_scatter_chart,
    build_carrier_premium_bar_chart,
)
from app.utils.alliances import (
    get_carrier_alliance,
    get_carrier_logo_url,
    get_airport_alliance_breakdown,
)

from app.utils.auth import require_auth

st.set_page_config(
    page_title="Airports Explorer | AvDB",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply Apple-esque CSS styling
apply_apple_style()
require_auth()


# -------------------------------------------------------------
# 1. Header & Top Control Filter Bar
# -------------------------------------------------------------
st.title("✈️ Airport Network & Route Explorer")
st.markdown("<p style='color: #8E8E93; margin-top: -12px; margin-bottom: 20px;'>Analyze origin route connectivity, direct carrier capacity, O&D yields, fleet equipment mix, and great-circle flight paths.</p>", unsafe_allow_html=True)

# Fetch active airports
df_airports = get_available_airports()
airport_list = df_airports["airport_code"].tolist() if not df_airports.empty else ["ORD", "ATL", "DFW", "DEN", "LAX", "JFK", "SFO", "ANC"]

default_index = airport_list.index("ORD") if "ORD" in airport_list else 0

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([2.2, 1.1, 1.4, 1.4])

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

with filter_col3:
    flight_type = st.selectbox(
        "Service Filter",
        options=["✈️ Passenger Flights Only", "📦 Include Cargo & Charters"],
        index=0,
        label_visibility="collapsed"
    )
    is_pax_only = "Passenger Flights Only" in flight_type

with filter_col4:
    freq_label = st.selectbox(
        "Min Route Frequency",
        options=["≥ 10 flights/yr (Default)", "≥ 50 flights/yr (Weekly+)", "≥ 365 flights/yr (Daily)", "All (Include 1-off charters)"],
        index=0,
        label_visibility="collapsed"
    )
    if "≥ 10" in freq_label:
        min_deps = 10
    elif "≥ 50" in freq_label:
        min_deps = 50
    elif "≥ 365" in freq_label:
        min_deps = 365
    else:
        min_deps = 1

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
kpi_data = get_airport_kpis(selected_airport, selected_year, passenger_only=is_pax_only, min_departures=min_deps)

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
    leading_c = kpi_data.get('leading_carrier', '—')
    # Resolve leading carrier code for logo and alliance lookup
    leading_code = leading_c.split('—')[0].strip() if '—' in leading_c else leading_c.strip()
    if "(" in leading_c and ")" in leading_c:
        leading_code = leading_c.split("(")[-1].split(")")[0].strip()
    leading_logo = get_carrier_logo_url(leading_code)
    leading_alliance = get_carrier_alliance(leading_code, selected_year)
    leading_sub = f"🌐 {leading_alliance['alliance_name']}" if leading_alliance else "Independent / Unaligned"
    render_kpi_card("Leading Carrier", leading_c, subtitle=leading_sub, logo_url=leading_logo)

# -------------------------------------------------------------
# 3. Analytical Charts (Top Routes, Carrier/Alliance Donut, Fleet Mix)
# -------------------------------------------------------------
df_routes = get_airport_routes_dataset(selected_airport, selected_year, passenger_only=is_pax_only, min_departures=min_deps)
df_carriers = get_airport_carrier_breakdown(selected_airport, selected_year, passenger_only=is_pax_only, min_departures=min_deps)
df_fleet = get_airport_fleet_mix(selected_airport, selected_year, passenger_only=is_pax_only, min_departures=min_deps)

chart_col1, chart_col2, chart_col3 = st.columns([1.15, 1.05, 1.1])

with chart_col1:
    fig_routes = build_top_routes_bar_chart(df_routes, top_n=7)
    st.plotly_chart(fig_routes, width="stretch", config={"displayModeBar": False})

with chart_col2:
    tab_c, tab_a = st.tabs(["🏢 Carriers", "🌐 Alliances"])
    with tab_c:
        fig_carriers = build_carrier_market_share_donut(df_carriers)
        st.plotly_chart(fig_carriers, width="stretch", config={"displayModeBar": False})
    with tab_a:
        df_alliance = get_airport_alliance_breakdown(df_carriers, selected_year)
        fig_alliance = build_airport_alliance_share_donut(df_alliance)
        st.plotly_chart(fig_alliance, width="stretch", config={"displayModeBar": False})

with chart_col3:
    fig_fleet = build_airport_fleet_bar_chart(df_fleet, top_n=7)
    st.plotly_chart(fig_fleet, width="stretch", config={"displayModeBar": False})

if not df_carriers.empty:
    df_alliance_summary = get_airport_alliance_breakdown(df_carriers, selected_year)
    if not df_alliance_summary.empty:
        pills = []
        for _, a_row in df_alliance_summary.iterrows():
            a_name = a_row["alliance_name"]
            share = a_row["seat_share_pct"]
            pills.append(f"<b>{a_name}</b>: {share:.1f}%")
        pills_str = " &nbsp;|&nbsp; ".join(pills)
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 7px 14px; margin-top: 4px; margin-bottom: 18px; font-size: 0.85rem; color: #EBEBF5;">
                🌐 <b>Airport Global Alliance Capacity Share ({selected_year})</b>: &nbsp;{pills_str}
            </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. Hero Section: 1990s Airline Route Atlas & Geodesic Network
# -------------------------------------------------------------
st.markdown("### 🌐 Route Network Atlas (1990s In-Flight Cartography)")

if not df_routes.empty:
    origin_meta = {
        "airport_code": selected_airport,
        "airport_name": df_airports.loc[df_airports['airport_code'] == selected_airport, 'airport_name'].iloc[0] if not df_airports.empty and selected_airport in df_airports['airport_code'].values else selected_airport,
        "latitude": df_routes["origin_lat"].iloc[0],
        "longitude": df_routes["origin_lon"].iloc[0],
        "city": df_routes["origin_city"].iloc[0] if "origin_city" in df_routes.columns else "",
        "state": df_routes["origin_state"].iloc[0] if "origin_state" in df_routes.columns else "",
        "country": df_routes["origin_country"].iloc[0] if "origin_country" in df_routes.columns else "US",
    }
    
    # Vintage in-flight map controls
    map_ctrl1, map_ctrl2, map_ctrl3 = st.columns([1.3, 1.2, 1.1])
    with map_ctrl1:
        map_theme_label = st.selectbox(
            "Cartography Theme",
            options=[
                "🎨 Mapbox: Personal (Custom)",
                "💖 Mapbox: Love (Custom)",
                "🏁 Mapbox: Mono (Custom)",
                "🌌 Midnight Navy (Dark)",
                "📜 Classic In-Flight Paper (Light)",
                "🌑 Minimal Slate (Dark)"
            ],
            index=0,
            key="airport_map_theme",
            label_visibility="collapsed"
        )
        if "Personal" in map_theme_label:
            theme_key = "personal"
        elif "Love" in map_theme_label:
            theme_key = "love"
        elif "Mono" in map_theme_label:
            theme_key = "mono"
        elif "Midnight" in map_theme_label:
            theme_key = "midnight"
        elif "Paper" in map_theme_label:
            theme_key = "paper"
        else:
            theme_key = "slate"
        
    with map_ctrl2:
        colorway_label = st.selectbox(
            "Linework Color",
            options=["🔷 Classic Cobalt", "🔴 Vintage Crimson", "🔶 Amber Gold", "🟢 Emerald Green"],
            index=0,
            key="airport_map_color",
            label_visibility="collapsed"
        )
        color_key = "cobalt" if "Cobalt" in colorway_label else ("crimson" if "Crimson" in colorway_label else ("gold" if "Gold" in colorway_label else "emerald"))

    with map_ctrl3:
        label_opt = st.selectbox(
            "IATA Labels",
            options=["🏷️ Top 30 Destinations", "🌐 All Destinations", "⚪ Hub & Dots Only"],
            index=0,
            key="airport_map_labels",
            label_visibility="collapsed"
        )
        label_density = "top30" if "Top 30" in label_opt else ("all" if "All" in label_opt else "none")

    mapbox_token = os.getenv("MAPBOX_API_KEY", "")
    mapbox_style = os.getenv("MAPBOX_STYLE", None)

    deck_map = build_route_map_deck(
        df_routes,
        origin_meta=origin_meta,
        theme=theme_key,
        colorway=color_key,
        label_density=label_density,
        mapbox_api_key=mapbox_token or None,
        mapbox_style=mapbox_style
    )

    st.pydeck_chart(deck_map, width="stretch")
else:
    st.info(f"No direct flight route operations matching filter criteria for {selected_airport} in {selected_year}.")

# -------------------------------------------------------------
# 5. Destination Development & Unserved Connecting Markets
# -------------------------------------------------------------
with st.expander("🎯 Target Destination Proposals (Unserved Connecting Markets)", expanded=False):
    st.markdown("""
        **Unserved Nonstop Opportunities**: Analysis of true 1-stop connecting Origin-Destination (O&D) passenger volume.
        Markets are classified into **Business Heavy** (high yield) vs. **Leisure Heavy**, with recommended carrier alignment based on hub network strategy.
    """)
    df_unserved = get_unserved_connecting_markets(selected_airport, year=2023, min_annual_pax=365)
    
    if not df_unserved.empty:
        fig_unserved = build_unserved_markets_scatter_chart(df_unserved)
        st.plotly_chart(fig_unserved, width="stretch", config={"displayModeBar": False})
        
        display_unserved = df_unserved.head(10)[[
            "route_label", "metro_status", "annual_connecting_pax", "pdew",
            "avg_fare", "yield_per_mile", "market_type", "aligned_carrier"
        ]].rename(columns={
            "route_label": "Proposed Route (Origin ➔ Dest)",
            "metro_status": "Catchment Market Status",
            "annual_connecting_pax": "Annual Pax (1-Stop)",
            "pdew": "PDEW",
            "avg_fare": "Avg Fare ($)",
            "yield_per_mile": "Yield ($/mi)",
            "market_type": "Market Profile",
            "aligned_carrier": "Strategy-Aligned Carrier"
        })
        st.dataframe(display_unserved, width="stretch", hide_index=True)
    else:
        st.info("No major unserved connecting markets exceeding threshold found for this origin.")

# -------------------------------------------------------------
# 6. Route Carrier Competition & Fare Premiums
# -------------------------------------------------------------
with st.expander("⚔️ Multi-Carrier Route Competition & Fare Premium Matrix", expanded=False):
    if not df_routes.empty:
        # Multi-carrier selection
        multi_routes = df_routes[df_routes["operating_carriers"].str.contains(",", na=False)]
        selected_dest = st.selectbox(
            "Select Route for Operator Breakdown",
            options=df_routes["dest"].tolist(),
            format_func=lambda d: f"{selected_airport} ➔ {d} ({df_routes.loc[df_routes['dest'] == d, 'dest_city'].iloc[0]}) — Carriers: {df_routes.loc[df_routes['dest'] == d, 'operating_carriers'].iloc[0]}"
        )
        
        df_comp = get_route_carrier_competition(selected_airport, selected_dest, selected_year)
        if not df_comp.empty and len(df_comp) > 1:
            col_c1, col_c2 = st.columns([1.2, 1.0])
            with col_c1:
                fig_comp = build_carrier_premium_bar_chart(df_comp)
                st.plotly_chart(fig_comp, width="stretch", config={"displayModeBar": False})
            with col_c2:
                st.markdown(f"**Carrier Yield & Premium Summary ({selected_airport} ➔ {selected_dest})**")
                display_comp = df_comp[[
                    "unique_carrier", "carrier_name", "total_seats", "capacity_share_pct",
                    "passenger_share_pct", "avg_fare", "yield_per_mile", "fare_premium_vs_min"
                ]].rename(columns={
                    "unique_carrier": "Code",
                    "carrier_name": "Carrier",
                    "total_seats": "Seats",
                    "capacity_share_pct": "Capacity %",
                    "passenger_share_pct": "Pax Share %",
                    "avg_fare": "Avg Fare ($)",
                    "yield_per_mile": "Yield ($/mi)",
                    "fare_premium_vs_min": "Premium vs Low ($)"
                })
                st.dataframe(display_comp, width="stretch", hide_index=True)
        else:
            st.info(f"Route {selected_airport} ➔ {selected_dest} is operated by a single carrier or has limited competitor sample data.")

# -------------------------------------------------------------
# 7. Expandable Route Data Table
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
        st.dataframe(display_df, width="stretch", hide_index=True)
