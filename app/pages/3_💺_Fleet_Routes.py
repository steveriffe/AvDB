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
from app.utils.styling import apply_apple_style, render_kpi_card, render_portal_nav_link
from app.utils.auth import require_auth

st.set_page_config(
    page_title="Fleet & Routes | AvDB",
    page_icon="💺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply Apple-esque CSS styling & Steve Riffe Portfolio link
apply_apple_style()
render_portal_nav_link()
require_auth()

import plotly.express as px
import plotly.graph_objects as go
from app.utils.queries import (
    get_fleet_kpis,
    get_fleet_aircraft_breakdown,
    get_fleet_operators_breakdown,
    get_fleet_time_series,
)
from app.utils.visualizers import FAMILY_COLORS, build_fleet_gauge_trend_chart
from app.utils.alliances import get_carrier_logo_url, get_carrier_name
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

# Multi-Year Gauge & Up-Gauging Trajectory Expander
df_fleet_ts = get_fleet_time_series()
if not df_fleet_ts.empty:
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    with st.expander("📈 Three-Decade Gauge Evolution & Category Shifts (1990–2025)", expanded=False):
        fig_gauge_trend = build_fleet_gauge_trend_chart(df_fleet_ts)
        st.plotly_chart(fig_gauge_trend, width="stretch")
        
        # Historical context summary
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            st.metric("1990 Baseline Narrowbody Gauge", "130 seats/dep", "MD-80s, 737 Classics, 727s")
        with fc2:
            st.metric("2000s Regional Jet Surge", "25–50 seats/dep", "CRJ-100/200 & ERJ-145 explosion")
        with fc3:
            st.metric("2020s Up-Gauging Renaissance", "175–230 seats/dep", "A321neo, 737 MAX 9, E175 transitions")

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
            yaxis=dict(showgrid=False, autorange="reversed", tickfont=dict(color="#F5F5F7", size=10.5))
        )
        st.plotly_chart(fig_fleet, width="stretch", config={"displayModeBar": False})
    else:
        st.info("No fleet deployment data found for this selection.")

with c2:
    st.markdown("### 📊 Stage Length vs Passenger Yield ($/mi)")
    if not df_fleet.empty:
        scatter_data = df_fleet.dropna(subset=["avg_stage_length", "yield_per_mile", "total_seats"])
        scatter_data = scatter_data[(scatter_data["avg_stage_length"] > 0) & (scatter_data["yield_per_mile"] > 0) & (scatter_data["total_seats"] > 0)]
        if not scatter_data.empty:
            fig_scatter = px.scatter(
                scatter_data,
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
        else:
            st.info("Stage length and passenger yield data not available for this selection.")
    else:
        st.info("No fleet deployment data available.")

# -------------------------------------------------------------
# 4. Aircraft Technical Specifications & Operator Branding
# -------------------------------------------------------------
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
st.subheader("🛠️ Aircraft Technical Specifications & Operator Deployment")

model_options = df_fleet["aircraft_description"].tolist() if not df_fleet.empty else ["Boeing 737-900ER"]
selected_model = st.selectbox("Inspect Aircraft Model Specifications", options=model_options, index=0)
spec = get_aircraft_spec(selected_model)

if spec:
    spec_col1, spec_col2 = st.columns([1.1, 1.2])
    with spec_col1:
        photo_url = spec.get("photo_url", "")
        photo_credit = spec.get("photo_credit", "Aviation Photography")
        photo_license = spec.get("photo_license", "Editorial / Public Domain")
        photo_source = spec.get("photo_source_url", "#")
        photo_caption = spec.get("photo_caption", "")
        
        st.markdown(
            f"""
            <div style="background: rgba(17, 29, 51, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px; overflow: hidden; box-shadow: 0 12px 30px rgba(0,0,0,0.4);">
                <div style="position: relative; overflow: hidden; max-height: 250px;">
                    <img src="{photo_url}" style="width: 100%; height: 250px; object-fit: cover; filter: brightness(1.02);" alt="{selected_model}"/>
                    <div style="position: absolute; bottom: 8px; left: 10px; background: rgba(11, 25, 44, 0.85); backdrop-filter: blur(8px); padding: 4px 10px; border-radius: 6px; font-size: 11px; font-family: 'JetBrains Mono', monospace; color: #CBD5E1; border: 1px solid rgba(255,255,255,0.1);">
                        {photo_caption}
                    </div>
                </div>
                <div style="padding: 10px 14px; background: rgba(6, 9, 17, 0.7); display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-family: 'JetBrains Mono', monospace; border-top: 1px solid rgba(255,255,255,0.06);">
                    <span style="color: #94A3B8;">📷 <b>Photo:</b> {photo_credit} ({photo_license})</span>
                    <a href="{photo_source}" target="_blank" rel="noopener noreferrer" style="color: #38BDF8; text-decoration: none; font-weight: 600;">License & Source ↗</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with spec_col2:
        status_color = "#10B981" if "Active" in spec.get("status", "") else "#FF9F0A"
        mtow_str = f"{spec.get('mtow_lbs', 0):,} lbs" if spec.get('mtow_lbs') else "N/A"
        height_str = f" / {spec.get('height_ft')} ft" if spec.get('height_ft') else ""
        
        st.markdown(
            f"""
            <div style="background: rgba(17, 29, 51, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px; padding: 18px 20px; backdrop-filter: blur(14px);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <div>
                        <div style="color: #FFFFFF; font-size: 18px; font-weight: 800; font-family: 'Plus Jakarta Sans', sans-serif;">{selected_model}</div>
                        <div style="color: #94A3B8; font-size: 12px; font-family: 'JetBrains Mono', monospace; margin-top: 2px;">{spec['family']} · First Flight: {spec.get('first_flight', 'N/A')}</div>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); color: #38BDF8; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; font-family: 'JetBrains Mono', monospace;">{spec['category']}</span><br/>
                        <span style="display: inline-block; margin-top: 4px; color: {status_color}; font-size: 10.5px; font-weight: 600;">● {spec.get('status', 'Active')}</span>
                    </div>
                </div>
                <p style="color: #CBD5E1; font-size: 12.5px; line-height: 1.5; margin-bottom: 14px;">{spec['summary']}</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 12px; font-family: 'JetBrains Mono', monospace;">
                    <div><span style="color: #94A3B8;">Gauge:</span> <b style="color: #FFFFFF;">{spec['seats_typical']}</b></div>
                    <div><span style="color: #94A3B8;">Max Range:</span> <b style="color: #10B981;">{spec['range_miles']:,} sm</b></div>
                    <div><span style="color: #94A3B8;">Span / Length:</span> <b style="color: #FFFFFF;">{spec['wingspan_ft']} ft / {spec['length_ft']} ft{height_str}</b></div>
                    <div><span style="color: #94A3B8;">MTOW:</span> <b style="color: #FB923C;">{mtow_str}</b></div>
                    <div><span style="color: #94A3B8;">Cruise Speed:</span> <b style="color: #FFFFFF;">{spec['cruise_speed']}</b></div>
                    <div><span style="color: #94A3B8;">Powerplant:</span> <b style="color: #38BDF8;">{spec['engines']}</b></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Operators Strip
        ops = spec.get("key_operators", [])
        if ops:
            logo_htmls = []
            for op in ops:
                l_url = get_carrier_logo_url(op) or ""
                op_name = get_carrier_name(op)
                logo_tag = f"<img src='{l_url}' style='height: 20px; width: 20px; object-fit: contain; border-radius: 4px; flex-shrink: 0;' alt='{op}' />" if l_url else ""
                logo_htmls.append(
                    f"""
                    <div style="display: inline-flex; align-items: center; gap: 7px; background: rgba(11, 25, 44, 0.75); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 5px 11px; margin: 3px 6px 3px 0;" title="{op_name} ({op})">
                        {logo_tag}
                        <span style="color: #FFFFFF; font-weight: 700; font-size: 11px; font-family: 'JetBrains Mono', monospace;">{op}</span>
                        <span style="color: #94A3B8; font-size: 11px; font-family: 'Plus Jakarta Sans', sans-serif;">{op_name}</span>
                    </div>
                    """
                )
            st.markdown(
                f"<div style='margin-top: 12px;'><span style='font-size: 11px; font-weight: 700; color: #94A3B8; font-family: \"JetBrains Mono\", monospace;'>PRIMARY OPERATORS:</span><br/><div style='display: flex; flex-wrap: wrap; margin-top: 4px;'>{''.join(logo_htmls)}</div></div>",
                unsafe_allow_html=True
            )
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
            carrier_raw = row.get("carrier_name")
            carrier_str = str(carrier_raw) if pd.notna(carrier_raw) and carrier_raw else c_code
            carrier_disp = carrier_str.split(" ")[0]
            lf_str = f"LF: {row['load_factor_pct']:.1f}%" if pd.notna(row.get("load_factor_pct")) else "LF: N/A"
            fare_str = f"Fare: ${row['avg_segment_fare']:.0f}" if pd.notna(row.get("avg_segment_fare")) else "Fare: N/A"
            render_kpi_card(
                label=f"{c_code} — {carrier_disp}",
                value=f"{seats_k} seats",
                subtitle=f"{lf_str} | {fare_str}",
                logo_url=c_logo
            )
            
    # Leading Airline Operators Horizontal Bar Chart (Sorted Descending)
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    fig_ops = go.Figure()
    op_labels = df_ops["unique_carrier"] + " — " + df_ops["carrier_name"].fillna(df_ops["unique_carrier"])
    fig_ops.add_trace(go.Bar(
        y=op_labels,
        x=df_ops["total_seats"],
        orientation="h",
        marker=dict(color="#FF6B00", opacity=0.85),
        customdata=df_ops[["departures_performed", "load_factor_pct", "avg_segment_fare"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Total Seats: <b>%{x:,.0f}</b><br>"
            "Departures: <b>%{customdata[0]:,.0f}</b><br>"
            "Load Factor: <b>%{customdata[1]}%</b><br>"
            "Avg Fare: <b>$%{customdata[2]}</b>"
            "<extra></extra>"
        )
    ))
    fig_ops.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8E8E93")),
        yaxis=dict(showgrid=False, autorange="reversed", tickfont=dict(color="#F5F5F7", size=11))
    )
    st.plotly_chart(fig_ops, width="stretch", config={"displayModeBar": False})

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

