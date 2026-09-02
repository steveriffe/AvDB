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
    get_fleet_kpis,
    get_fleet_aircraft_breakdown,
)
from app.utils.visualizers import FAMILY_COLORS

st.set_page_config(
    page_title="Fleet & Routes | AvDB",
    page_icon="💺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply Apple-esque CSS styling
apply_apple_style()

# -------------------------------------------------------------
# 1. Header & Control Bar
# -------------------------------------------------------------
st.title("💺 Fleet Deployment & Aircraft Routing")
st.markdown("<p style='color: #8E8E93; margin-top: -12px; margin-bottom: 20px;'>Analyze aircraft family allocation, gauge deployment (seats per departure), stage-length matching, and regional vs mainline fleet dynamics.</p>", unsafe_allow_html=True)

col_f1, col_f2 = st.columns([2.5, 1.2])

with col_f1:
    selected_family = st.selectbox(
        "Aircraft Category / Family",
        options=[
            "All Mainline & Regional",
            "Airbus A320 Family (A319/A320/A321)",
            "Boeing 737 Family (737-700/800/900/MAX)",
            "Boeing Widebody (777/787/767)",
            "Embraer E-Jets (E170/E175/E190)",
            "Bombardier CRJ Series (CRJ2/7/9)"
        ],
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

# -------------------------------------------------------------
# 2. Top KPI Cards
# -------------------------------------------------------------
kpis = get_fleet_kpis(selected_family, selected_year)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    render_kpi_card("Unique Airframe Models", f"{kpis['unique_models']}")

with k2:
    render_kpi_card("Operating Carriers", f"{kpis['operating_carriers']}")

with k3:
    deps_val = f"{kpis['total_departures']/1e3:.1f}K" if kpis['total_departures'] >= 1000 else f"{kpis['total_departures']:,}"
    render_kpi_card("Total Departures", deps_val)

with k4:
    gauge_val = f"{kpis['avg_gauge_seats']:.0f} seats" if kpis['avg_gauge_seats'] else "—"
    render_kpi_card("Avg Gauge (Seats/Dep)", gauge_val)

with k5:
    stage_val = f"{kpis['avg_stage_length']:,} mi" if kpis['avg_stage_length'] else "—"
    render_kpi_card("Avg Stage Length", stage_val)

# -------------------------------------------------------------
# 3. Aircraft Model Deployment Mix
# -------------------------------------------------------------
df_fleet = get_fleet_aircraft_breakdown(selected_family, selected_year)

c1, c2 = st.columns([1.2, 1.0])

with c1:
    st.markdown("### ✈️ Top Aircraft Models by Seat Capacity")
    if not df_fleet.empty:
        colors = [FAMILY_COLORS.get(fam, "#0A84FF") for fam in df_fleet["aircraft_family"]]
        fig_fleet = go.Figure()
        fig_fleet.add_trace(go.Bar(
            y=df_fleet["aircraft_description"],
            x=df_fleet["total_seats"],
            orientation="h",
            marker=dict(color=colors, opacity=0.9),
            customdata=df_fleet[["avg_gauge_seats", "load_factor_pct", "avg_stage_length"]],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Total Seats: <b>%{x:,.0f}</b><br>"
                "Avg Gauge: <b>%{customdata[0]} seats/dep</b><br>"
                "Load Factor: <b>%{customdata[1]:.1f}%</b><br>"
                "Avg Stage: <b>%{customdata[2]:,} miles</b>"
                "<extra></extra>"
            )
        ))
        fig_fleet.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8E8E93")),
            yaxis=dict(showgrid=False, tickfont=dict(color="#F5F5F7", size=10.5))
        )
        st.plotly_chart(fig_fleet, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No fleet deployment data found for this selection.")

with c2:
    st.markdown("### 📊 Gauge vs Stage Length Economics")
    if not df_fleet.empty:
        fig_scatter = px.scatter(
            df_fleet,
            x="avg_stage_length",
            y="avg_gauge_seats",
            size="total_seats",
            color="aircraft_family",
            hover_name="aircraft_description",
            labels={"avg_stage_length": "Avg Stage Length (Miles)", "avg_gauge_seats": "Avg Gauge (Seats/Dep)"}
        )
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8E8E93")),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8E8E93")),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#F5F5F7", size=9.5))
        )
        st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

# -------------------------------------------------------------
# 4. Detailed Data Table
# -------------------------------------------------------------
with st.expander("📋 Detailed Fleet Deployment Data Table", expanded=True):
    if not df_fleet.empty:
        display_fleet = df_fleet[[
            "aircraft_description", "aircraft_family", "departures_performed",
            "total_seats", "operational_passengers", "avg_gauge_seats",
            "load_factor_pct", "avg_stage_length"
        ]].rename(columns={
            "aircraft_description": "Aircraft Model",
            "aircraft_family": "Category",
            "departures_performed": "Departures",
            "total_seats": "Seats",
            "operational_passengers": "Passengers",
            "avg_gauge_seats": "Seats/Dep",
            "load_factor_pct": "Load Factor %",
            "avg_stage_length": "Avg Stage (mi)"
        })
        st.dataframe(display_fleet, use_container_width=True, hide_index=True)
