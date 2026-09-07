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
from app.utils.auth import require_auth

st.set_page_config(
    page_title="Fleet & Routes | AvDB",
    page_icon="💺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply Apple-esque CSS styling
apply_apple_style()
require_auth()

import plotly.express as px
import plotly.graph_objects as go
from app.utils.queries import (
    get_fleet_kpis,
    get_fleet_aircraft_breakdown,
    get_fleet_operators_breakdown,
)
from app.utils.visualizers import FAMILY_COLORS
from app.utils.alliances import get_carrier_logo_url
from app.data.ref_aircraft_specs import get_aircraft_spec


# -------------------------------------------------------------
# 1. Header & Control Bar
# -------------------------------------------------------------
st.title("💺 Fleet Deployment & Aircraft Routing Economics")
st.markdown("<p style='color: #8E8E93; margin-top: -12px; margin-bottom: 20px;'>Analyze aircraft family allocation, gauge deployment (seats per departure), stage-length matching, and revenue/yield potential per equipment type.</p>", unsafe_allow_html=True)

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
        options=[2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2015, 2010, 2005, 2000, 1995, 1990],
        index=0,
        label_visibility="collapsed"
    )

# -------------------------------------------------------------
# 2. Top KPI Cards
# -------------------------------------------------------------
kpis = get_fleet_kpis(selected_family, selected_year)

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    render_kpi_card("Airframe Models", f"{kpis['unique_models']}")

with k2:
    render_kpi_card("Carriers", f"{kpis['operating_carriers']}")

with k3:
    deps_val = f"{kpis['total_departures']/1e3:.1f}K" if kpis.get('total_departures') and kpis['total_departures'] >= 1000 else f"{kpis.get('total_departures', 0):,}"
    render_kpi_card("Total Departures", deps_val)

with k4:
    gauge_val = f"{kpis['avg_gauge_seats']:.0f} seats" if kpis.get('avg_gauge_seats') else "—"
    render_kpi_card("Avg Gauge", gauge_val)

with k5:
    fare_val = f"${kpis['avg_segment_fare']:.0f}" if kpis.get('avg_segment_fare') else "—"
    render_kpi_card("Avg Segment Fare", fare_val)

with k6:
    yield_val = f"${kpis['yield_per_mile']:.4f}" if kpis.get('yield_per_mile') else "—"
    render_kpi_card("Yield / Passenger-Mile", yield_val)

# -------------------------------------------------------------
# 3. Aircraft Model Deployment & Yield Economics
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
            customdata=df_fleet[["avg_gauge_seats", "load_factor_pct", "avg_stage_length", "avg_segment_fare", "yield_per_mile"]],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Total Seats: <b>%{x:,.0f}</b><br>"
                "Avg Gauge: <b>%{customdata[0]} seats/dep</b><br>"
                "Load Factor: <b>%{customdata[1]:.1f}%</b><br>"
                "Avg Stage: <b>%{customdata[2]:,} miles</b><br>"
                "Avg Fare: <b>$%{customdata[3]:.0f}</b><br>"
                "Yield: <b>$%{customdata[4]:.4f}/mi</b>"
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
        st.plotly_chart(fig_fleet, width="stretch", config={"displayModeBar": False})
    else:
        st.info("No fleet deployment data found for this selection.")

with c2:
    st.markdown("### 📊 Stage Length vs Passenger Yield ($/mi)")
    if not df_fleet.empty:
        fig_scatter = px.scatter(
            df_fleet,
            x="avg_stage_length",
            y="yield_per_mile",
            size="total_seats",
            color="aircraft_family",
            hover_name="aircraft_description",
            hover_data={"avg_segment_fare": ":$.0f", "avg_gauge_seats": ":.0f"},
            labels={"avg_stage_length": "Avg Stage Length (Miles)", "yield_per_mile": "Yield ($/Mile)"}
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
        st.plotly_chart(fig_scatter, width="stretch", config={"displayModeBar": False})

# -------------------------------------------------------------
# 4. Aircraft Technical Specifications & Operator Branding
# -------------------------------------------------------------
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
st.subheader("🛠️ Aircraft Technical Specifications & Operator Deployment")

model_options = df_fleet["aircraft_description"].tolist() if not df_fleet.empty else ["Boeing 737-900ER"]
selected_model = st.selectbox("Inspect Aircraft Model Specifications", options=model_options, index=0)
spec = get_aircraft_spec(selected_model)

if spec:
    spec_col1, spec_col2 = st.columns([1.1, 1.0])
    with spec_col1:
        st.markdown(
            f"""
            <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 18px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="color: #F5F5F7; font-size: 18px; font-weight: 700;">{selected_model}</span>
                    <span style="background: rgba(10, 132, 255, 0.2); color: #0A84FF; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: 600;">{spec['category']}</span>
                </div>
                <p style="color: #8E8E93; font-size: 13px; margin-bottom: 14px;">{spec['summary']}</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 13px;">
                    <div><span style="color: #8E8E93;">Typical Gauge:</span> <b style="color: #F5F5F7;">{spec['seats_typical']}</b></div>
                    <div><span style="color: #8E8E93;">Max Range:</span> <b style="color: #30D158;">{spec['range_miles']:,} statute miles</b></div>
                    <div><span style="color: #8E8E93;">Wingspan / Length:</span> <b style="color: #F5F5F7;">{spec['wingspan_ft']} ft / {spec['length_ft']} ft</b></div>
                    <div><span style="color: #8E8E93;">Cruise Speed:</span> <b style="color: #F5F5F7;">{spec['cruise_speed']}</b></div>
                    <div style="grid-column: span 2;"><span style="color: #8E8E93;">Powerplant:</span> <b style="color: #FF9F0A;">{spec['engines']}</b></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with spec_col2:
        st.markdown(f"**Primary US Operators ({selected_model})**")
        ops = spec.get("key_operators", [])
        logo_htmls = []
        for op in ops:
            l_url = get_carrier_logo_url(op)
            logo_htmls.append(
                f"""
                <div style="display: inline-flex; align-items: center; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 8px 12px; margin: 4px;">
                    <img src="{l_url}" style="height: 22px; width: 42px; object-fit: contain; margin-right: 8px;" />
                    <span style="color: #F5F5F7; font-weight: 600; font-size: 13px;">{op}</span>
                </div>
                """
            )
        st.markdown("".join(logo_htmls), unsafe_allow_html=True)
else:
    st.info(f"Engineering specification card not yet configured for {selected_model}.")

# -------------------------------------------------------------
# 5. Top Operating Carriers for Category
# -------------------------------------------------------------
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
st.markdown(f"### 🏢 Leading Airline Operators for {selected_family}")
df_ops = get_fleet_operators_breakdown(selected_family, selected_year)

if not df_ops.empty:
    cols = st.columns(min(len(df_ops), 5))
    for i, (_, row) in enumerate(df_ops.head(5).iterrows()):
        with cols[i]:
            c_code = row["unique_carrier"]
            c_logo = get_carrier_logo_url(c_code)
            seats_k = f"{row['total_seats']/1e6:.1f}M" if row['total_seats'] >= 1e6 else f"{row['total_seats']/1e3:.0f}K"
            render_kpi_card(
                label=f"{c_code} — {row['carrier_name'].split(' ')[0]}",
                value=f"{seats_k} seats",
                subtitle=f"LF: {row['load_factor_pct']:.1f}% | Fare: ${row['avg_segment_fare']:.0f}",
                logo_url=c_logo
            )

# -------------------------------------------------------------
# 6. Detailed Data Table
# -------------------------------------------------------------
with st.expander("📋 Detailed Fleet Deployment & Revenue Data Table", expanded=True):
    if not df_fleet.empty:
        display_fleet = df_fleet[[
            "aircraft_description", "aircraft_family", "departures_performed",
            "total_seats", "operational_passengers", "avg_gauge_seats",
            "load_factor_pct", "avg_stage_length", "avg_segment_fare", "yield_per_mile"
        ]].rename(columns={
            "aircraft_description": "Aircraft Model",
            "aircraft_family": "Category",
            "departures_performed": "Departures",
            "total_seats": "Seats",
            "operational_passengers": "Passengers",
            "avg_gauge_seats": "Seats/Dep",
            "load_factor_pct": "Load Factor %",
            "avg_stage_length": "Avg Stage (mi)",
            "avg_segment_fare": "Avg Segment Fare ($)",
            "yield_per_mile": "Yield ($/mi)"
        })
        st.dataframe(display_fleet, width="stretch", hide_index=True)

