import sys
from pathlib import Path

# Automatically add project root to Python path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.config import settings
from app.utils.styling import apply_apple_style, render_kpi_card
from app.utils.queries import (
    get_airline_kpis,
    get_airline_hubs,
    get_airline_yield_curve,
    CARRIER_STRATEGY,
    get_airline_hub_expansion_proposals,
    get_unserved_connecting_markets,
)

from app.utils.auth import require_auth

st.set_page_config(
    page_title="Airlines Explorer | AvDB",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply Apple-esque CSS styling
apply_apple_style()
require_auth()


# -------------------------------------------------------------
# 1. Header & Top Control Bar
# -------------------------------------------------------------
st.title("🏢 Airline Network & Yield Explorer")
st.markdown("<p style='color: #8E8E93; margin-top: -12px; margin-bottom: 20px;'>Inspect route network density, hub concentration, fare yield curves, competitor price premiums, and target expansion cities by hub.</p>", unsafe_allow_html=True)

carriers_dict = {
    "AS": "Alaska Airlines (AS)",
    "UA": "United Airlines (UA)",
    "DL": "Delta Air Lines (DL)",
    "AA": "American Airlines (AA)",
    "WN": "Southwest Airlines (WN)",
    "B6": "JetBlue Airways (B6)",
    "NK": "Spirit Airlines (NK)",
    "F9": "Frontier Airlines (F9)",
    "G4": "Allegiant Air (G4)"
}

col_f1, col_f2, col_f3 = st.columns([2.5, 1.2, 1.8])

with col_f1:
    selected_code = st.selectbox(
        "Select Carrier",
        options=list(carriers_dict.keys()),
        format_func=lambda k: carriers_dict[k],
        index=0,
        label_visibility="collapsed"
    )

with col_f2:
    selected_year = st.selectbox(
        "Analysis Year",
        options=[2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018],
        index=0,
        label_visibility="collapsed"
    )

with col_f3:
    carrier_strat = CARRIER_STRATEGY.get(selected_code, {})
    hubs_str = ", ".join(carrier_strat.get("hubs", []))
    st.markdown(f"<div style='color: #64D2FF; font-size: 12px; margin-top: 6px;'><b>Primary Hubs:</b> {hubs_str}</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. Top KPI Cards
# -------------------------------------------------------------
kpis = get_airline_kpis(selected_code, selected_year)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    render_kpi_card("Active Routes", f"{kpis['active_routes']:,}")

with k2:
    deps_val = f"{kpis['total_departures']/1e3:.1f}K" if kpis['total_departures'] >= 1000 else f"{kpis['total_departures']:,}"
    render_kpi_card("Total Departures", deps_val)

with k3:
    lf_str = f"{kpis['system_load_factor']:.1f}%" if kpis['system_load_factor'] else "—"
    render_kpi_card("System Load Factor", lf_str)

with k4:
    yield_str = f"${kpis['avg_yield_per_mile']:.4f}" if kpis['avg_yield_per_mile'] else "—"
    render_kpi_card("Yield / Passenger-Mile", yield_str)

with k5:
    fare_str = f"${kpis['avg_network_fare']:.0f}" if kpis['avg_network_fare'] else "—"
    render_kpi_card("Avg Network Fare", fare_str)

# -------------------------------------------------------------
# 3. Hub Operations & Yield Curve Charts
# -------------------------------------------------------------
df_hubs = get_airline_hubs(selected_code, selected_year)
df_yields = get_airline_yield_curve(selected_code, selected_year)

c1, c2 = st.columns([1.1, 1.3])

with c1:
    st.markdown("### 🏛️ Top Hub & Focus City Concentration")
    if not df_hubs.empty:
        fig_hubs = go.Figure()
        fig_hubs.add_trace(go.Bar(
            y=df_hubs["airport_code"] + " — " + df_hubs["origin_city"],
            x=df_hubs["total_seats"],
            orientation="h",
            marker=dict(color="#0A84FF", opacity=0.92),
            hovertemplate="<b>%{y}</b><br>Seats: %{x:,.0f}<br>Departures: %{customdata[0]:,}<extra></extra>",
            customdata=df_hubs[["departures_performed"]]
        ))
        fig_hubs.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8E8E93")),
            yaxis=dict(showgrid=False, tickfont=dict(color="#F5F5F7", size=10.5))
        )
        st.plotly_chart(fig_hubs, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No hub data available for selected parameters.")

with c2:
    st.markdown("### 📈 Network Yield Curve (Stage Length vs Yield)")
    if not df_yields.empty:
        fig_yield = px.scatter(
            df_yields,
            x="stage_length_miles",
            y="yield_per_mile",
            size="operational_passengers",
            hover_name="route_label",
            hover_data={"avg_od_fare": ":$.0f", "load_factor_pct": ":.1f%"},
            labels={"stage_length_miles": "Stage Length (Miles)", "yield_per_mile": "Yield ($/Mile)"}
        )
        fig_yield.update_traces(marker=dict(color="#64D2FF", opacity=0.75))
        fig_yield.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8E8E93")),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8E8E93"))
        )
        st.plotly_chart(fig_yield, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No yield curve data available.")

# -------------------------------------------------------------
# 4. Target Network Expansion Proposals: Top 5 Next Routes by Hub
# -------------------------------------------------------------
st.markdown("### 🎯 Strategic Route Expansion: Top 5 Next Route Candidates by Hub")

scope_col1, scope_col2 = st.columns([2.5, 1.5])
with scope_col1:
    st.markdown(f"Top 5 unserved nonstop route opportunities originating from **{carriers_dict[selected_code]}**'s primary hubs:")
with scope_col2:
    market_filter = st.selectbox(
        "Market Scope Filter",
        options=["🌟 100% New City Markets Only", "🔄 Include Alternate Secondary Airports"],
        index=0,
        label_visibility="collapsed"
    )
    only_new_cities = "100% New" in market_filter

proposals = get_airline_hub_expansion_proposals(selected_code, year=2023, exclude_alternate_airports=only_new_cities)

if proposals:
    hub_keys = list(proposals.keys())
    tabs = st.tabs([f"🏛️ Hub: {h}" for h in hub_keys])
    
    for idx, hub in enumerate(hub_keys):
        with tabs[idx]:
            df_h = proposals[hub]
            if not df_h.empty:
                display_h = df_h[[
                    "full_route_name", "metro_status", "annual_connecting_pax", "pdew",
                    "avg_fare", "yield_per_mile", "market_type"
                ]].rename(columns={
                    "full_route_name": "Proposed Route (Origin ➔ Destination)",
                    "metro_status": "Catchment Market Status",
                    "annual_connecting_pax": "Annual Pax (1-Stop)",
                    "pdew": "PDEW",
                    "avg_fare": "Avg Fare ($)",
                    "yield_per_mile": "Yield ($/mi)",
                    "market_type": "Demand Segment"
                })
                st.dataframe(display_h, use_container_width=True, hide_index=True)
            else:
                st.info(f"No major unserved route opportunities found matching criteria for hub {hub}.")
else:
    st.info("No hub expansion proposals available for this carrier selection.")
