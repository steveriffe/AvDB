import sys
from pathlib import Path

# Automatically add project root to Python path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import streamlit as st
import pandas as pd
from app.config import settings
from app.utils.styling import apply_apple_style, render_kpi_card
from app.utils.auth import require_auth

st.set_page_config(
    page_title="Flighty Personal Traveler | AvDB",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_apple_style()
require_auth()

import plotly.express as px
import plotly.graph_objects as go
from app.utils.alliances import get_carrier_logo_url
from app.utils.visualizers import (
    MAP_THEMES, 
    ROUTE_COLORWAYS, 
    build_flighty_alliance_donut, 
    build_flighty_yoy_trends, 
    build_flighty_seat_preference_donut
)
from app.utils.flighty import (
    parse_flighty_csv,
    generate_sample_flighty_data,
    build_flighty_travel_deck,
    AIRPORT_COORDINATES
)

st.title("📱 Flighty Personal Traveler")
st.markdown(
    "<p style='color: #8E8E93; font-size: 1.05rem; margin-top: -12px; margin-bottom: 24px;'>"
    "Upload your personal <b>Flighty CSV export</b> to explore your travel history on AvDB's vintage "
    "1990s in-flight route cartography, with granular <b>aircraft subfleet grouping</b> and fleet breakdowns."
    "</p>",
    unsafe_allow_html=True
)

# ----------------------------------------------------------------------
# Data Ingestion & State Management
# ----------------------------------------------------------------------
if "flighty_df" not in st.session_state:
    st.session_state["flighty_df"] = None
if "flighty_source_name" not in st.session_state:
    st.session_state["flighty_source_name"] = None

with st.sidebar:
    st.markdown("### 🗂️ Travel Data Source")
    uploaded_file = st.file_uploader("Upload Flighty CSV", type=["csv"], help="Export your flights from the Flighty app as CSV and drop here.")

    if uploaded_file is not None:
        try:
            st.session_state["flighty_df"] = parse_flighty_csv(uploaded_file.getvalue())
            st.session_state["flighty_source_name"] = uploaded_file.name
            st.success(f"Loaded {len(st.session_state['flighty_df'])} flights from `{uploaded_file.name}`")
        except Exception as e:
            st.error(f"Error parsing CSV: {e}")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("Load Sample Log", help="Load realistic 30-flight sample log featuring 737-900ER, MAX 9, 787-9, A321neo"):
            st.session_state["flighty_df"] = generate_sample_flighty_data()
            st.session_state["flighty_source_name"] = "Sample Travel Log (Frequent Traveler)"
            st.rerun()
    with col_s2:
        if st.session_state["flighty_df"] is not None:
            if st.button("Clear Log"):
                st.session_state["flighty_df"] = None
                st.session_state["flighty_source_name"] = None
                st.rerun()

    st.markdown("---")
    st.markdown("### 🗺️ Map Appearance")
    theme_options = list(MAP_THEMES.keys())
    selected_theme = st.selectbox("Cartography Theme", options=theme_options, index=0)
    colorway_options = list(ROUTE_COLORWAYS.keys())
    selected_colorway = st.selectbox("Route Colorway", options=colorway_options, index=0)

# If no data is loaded yet, show welcoming hero banner
if st.session_state["flighty_df"] is None:
    st.info("👋 No flight log loaded yet. Click **'Load Sample Log'** in the sidebar to test with a realistic 30-flight travel log, or upload your own Flighty CSV export above!")
    st.stop()

df_flights: pd.DataFrame = st.session_state["flighty_df"]

st.caption(f"Showing **{len(df_flights)} flights** from *{st.session_state.get('flighty_source_name', 'Loaded Data')}*")

# ----------------------------------------------------------------------
# Top Travel KPIs
# ----------------------------------------------------------------------
total_flights = len(df_flights)
total_miles = int(df_flights["distance_miles"].sum())
unique_airports = len(set(df_flights["origin"]).union(set(df_flights["dest"])))
favorite_subfleet = df_flights["aircraft_subfleet"].value_counts().index[0] if not df_flights.empty else "N/A"
top_route = df_flights["route"].value_counts().index[0] if not df_flights.empty else "N/A"
top_carrier = df_flights["carrier"].value_counts().index[0] if not df_flights.empty else "N/A"
top_carrier_code = df_flights["carrier_code"].value_counts().index[0] if "carrier_code" in df_flights.columns and not df_flights.empty else "AS"
top_carrier_logo = get_carrier_logo_url(top_carrier_code)

total_co2_kg = df_flights["co2_kg"].sum() if "co2_kg" in df_flights.columns else 0.0
total_co2_tonnes = total_co2_kg / 1000.0
trees_offset = int(total_co2_tonnes * 45)

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
with kpi1:
    render_kpi_card("Total Flights", f"{total_flights:,}", subtitle="Flight segments")
with kpi2:
    render_kpi_card("Total Distance", f"{total_miles:,} mi", subtitle="Air miles flown")
with kpi3:
    render_kpi_card("Airports Visited", f"{unique_airports}", subtitle="Unique IATA hubs")
with kpi4:
    render_kpi_card("Top Subfleet", favorite_subfleet, subtitle="Most flown model")
with kpi5:
    render_kpi_card("Top Carrier", top_carrier, subtitle=f"Top Route: {top_route}", logo_url=top_carrier_logo)
with kpi6:
    render_kpi_card("CO₂ Footprint", f"{total_co2_tonnes:.1f} t", subtitle=f"~{trees_offset:,} trees offset")

st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Personal 1990s In-Flight Route Map
# ----------------------------------------------------------------------
st.subheader("🌐 Personal In-Flight Route Map")
st.markdown("<p style='color: #8E8E93; font-size: 0.9rem;'>Rendered in AvDB's clean 1990s airline in-flight cartography. Line thickness reflects flight frequency.</p>", unsafe_allow_html=True)

# Determine primary home hub
home_hub = df_flights["origin"].value_counts().index[0] if not df_flights.empty else "SEA"
deck = build_flighty_travel_deck(
    df_flights=df_flights,
    home_airport=home_hub,
    map_theme=selected_theme,
    colorway=selected_colorway
)
st.pydeck_chart(deck, height=520, width="stretch")

st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Granular Subfleet Breakdown & Grouping Hierarchy
# ----------------------------------------------------------------------
st.subheader("✈️ Aircraft Subfleet & Equipment Analytics")
st.markdown(
    "<p style='color: #8E8E93; font-size: 0.92rem; margin-top: -6px; margin-bottom: 18px;'>"
    "Toggle between granular subfleet variants (e.g. distinguishing <b>Boeing 737-900ER</b> from <b>737-800</b> and <b>MAX 9</b>), "
    "broader aircraft generations (NextGen vs MAX), or high-level airframe families."
    "</p>",
    unsafe_allow_html=True
)

grouping_mode = st.radio(
    "Subfleet Hierarchy Level",
    options=["Exact Subfleet Variant (e.g. 737-900ER vs MAX 9)", "Aircraft Generation (e.g. 737 NextGen vs 737 MAX)", "Airframe Family (e.g. Boeing 737 vs Airbus A320)"],
    index=0,
    horizontal=True
)

col_target = "aircraft_subfleet"
if "Generation" in grouping_mode:
    col_target = "aircraft_generation"
elif "Family" in grouping_mode:
    col_target = "aircraft_family"

fleet_summary = df_flights.groupby(col_target).agg(
    flights=("flight_date", "count"),
    total_miles=("distance_miles", "sum"),
    unique_routes=("route", "nunique")
).reset_index().sort_values(by="flights", ascending=False)

fleet_summary["miles_pct"] = (fleet_summary["total_miles"] / total_miles * 100).round(1)
fleet_summary["flights_pct"] = (fleet_summary["flights"] / total_flights * 100).round(1)

fcol1, fcol2 = st.columns([3, 2])

with fcol1:
    fig_bar = px.bar(
        fleet_summary,
        x="flights",
        y=col_target,
        orientation="h",
        color="flights",
        color_continuous_scale="Blues",
        labels={"flights": "Flights Flown", col_target: ""},
        text="flights"
    )
    fig_bar.update_layout(
        title=dict(text=f"Flight Volume by {grouping_mode.split('(')[0].strip()}", font=dict(size=14, color="#F5F5F7")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=10, r=20, t=35, b=10),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8E8E93")),
        yaxis=dict(showgrid=False, tickfont=dict(color="#F5F5F7"), autorange="reversed"),
        coloraxis_showscale=False
    )
    fig_bar.update_traces(textposition="outside", textfont=dict(color="#F5F5F7"))
    st.plotly_chart(fig_bar, width="stretch")

with fcol2:
    fig_donut = px.pie(
        fleet_summary.head(7),
        names=col_target,
        values="total_miles",
        hole=0.6,
        color_discrete_sequence=["#0A84FF", "#30D158", "#FF9F0A", "#BF5AF2", "#FF375F", "#64D2FF", "#FFD60A"]
    )
    fig_donut.update_layout(
        title=dict(text="Distance Flown Share (Miles)", font=dict(size=14, color="#F5F5F7")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=10, r=10, t=35, b=10),
        legend=dict(orientation="v", font=dict(color="#F5F5F7", size=11))
    )
    st.plotly_chart(fig_donut, width="stretch")

# ----------------------------------------------------------------------
# Year-over-Year Travel Dynamics & Alliance Loyalty
# ----------------------------------------------------------------------
st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
st.subheader("📈 Annual Travel Trends & Global Alliance Loyalty")
st.markdown(
    "<p style='color: #8E8E93; font-size: 0.92rem; margin-top: -6px; margin-bottom: 18px;'>"
    "Track year-over-year flight volume and cumulative air miles alongside historical global alliance loyalty shares "
    "(Star Alliance, oneworld, SkyTeam, and Independent carriers)."
    "</p>",
    unsafe_allow_html=True
)

ycol1, ycol2 = st.columns([3, 2])
with ycol1:
    fig_yoy = build_flighty_yoy_trends(df_flights)
    st.plotly_chart(fig_yoy, width="stretch")
with ycol2:
    fig_alliance = build_flighty_alliance_donut(df_flights)
    st.plotly_chart(fig_alliance, width="stretch")

# ----------------------------------------------------------------------
# In-Flight Experience: Seating Preference & Cabin Class
# ----------------------------------------------------------------------
st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
st.subheader("💺 In-Flight Experience & Cabin Seating Preferences")
st.markdown(
    "<p style='color: #8E8E93; font-size: 0.92rem; margin-top: -6px; margin-bottom: 18px;'>"
    "Analyze your seating behavior across aircraft cabins: Window vs. Aisle vs. Middle seat selection, "
    "and premium cabin allocation."
    "</p>",
    unsafe_allow_html=True
)

scol1, scol2 = st.columns(2)
with scol1:
    fig_seat = build_flighty_seat_preference_donut(df_flights)
    st.plotly_chart(fig_seat, width="stretch")
with scol2:
    cabin_counts = df_flights["cabin_class"].value_counts().reset_index()
    cabin_counts.columns = ["cabin_class", "count"]
    fig_cabin = px.pie(
        cabin_counts,
        names="cabin_class",
        values="count",
        hole=0.55,
        color_discrete_sequence=["#30D158", "#0A84FF", "#BF5AF2", "#FF9F0A"]
    )
    fig_cabin.update_layout(
        title=dict(text="Cabin Class Distribution", font=dict(size=14, color="#F5F5F7")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=280,
        margin=dict(l=10, r=10, t=35, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(color="#F5F5F7", size=10)),
        showlegend=True
    )
    st.plotly_chart(fig_cabin, width="stretch")

# ----------------------------------------------------------------------
# Flown Routes & Carbon Footprint Analysis
# ----------------------------------------------------------------------
st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
st.subheader("🛫 Frequent Routes & Environmental Footprint")

rcol1, rcol2 = st.columns([3, 2])
with rcol1:
    st.markdown("##### 📍 Top Flown Route Corridors")
    top_routes_df = df_flights.groupby(["route", "origin", "dest"]).agg(
        flights=("flight_date", "count"),
        total_miles=("distance_miles", "sum"),
        carriers=("carrier", lambda x: ", ".join(sorted(x.unique()))),
        equipment=("aircraft_subfleet", lambda x: ", ".join(sorted(x.unique()))),
        total_co2=("co2_kg", "sum") if "co2_kg" in df_flights.columns else ("flight_date", "count")
    ).reset_index().sort_values(by="flights", ascending=False).head(10)
    top_routes_df["co2_tonnes"] = (top_routes_df["total_co2"] / 1000.0).round(2) if "co2_kg" in df_flights.columns else 0.0

    st.dataframe(
        top_routes_df[[
            "route", "flights", "total_miles", "carriers", "equipment", "co2_tonnes"
        ]].rename(columns={
            "route": "Route",
            "flights": "Flights",
            "total_miles": "Total Miles",
            "carriers": "Airlines Flown",
            "equipment": "Subfleet Variants",
            "co2_tonnes": "Est. CO₂ (t)"
        }),
        width="stretch",
        hide_index=True
    )

with rcol2:
    st.markdown("##### 🌿 Carbon Emissions & Offsets")
    st.markdown(
        f"""
        <div style="background: rgba(48, 209, 88, 0.08); border: 1px solid rgba(48, 209, 88, 0.25); border-radius: 10px; padding: 18px; margin-top: 4px;">
            <div style="color: #30D158; font-size: 15px; font-weight: 700; margin-bottom: 8px;">🌱 Aviation Sustainability Metrics</div>
            <div style="color: #F5F5F7; font-size: 13px; line-height: 1.6;">
                • <b>Total Flight CO₂</b>: <span style="color: #30D158; font-weight: 700;">{total_co2_tonnes:.2f} metric tons</span><br/>
                • <b>Average per Flight</b>: <b>{total_co2_kg / max(total_flights, 1):.0f} kg CO₂</b><br/>
                • <b>Forest Offset Equivalent</b>: <b>~{trees_offset:,} mature urban trees</b> growing for one full year to sequester this output.<br/>
                • <b>Efficiency Profile</b>: Stage lengths & modern high-bypass fleet matching significantly reduce per-passenger emissions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------------------------------------------------
# Searchable Complete Flight Log
# ----------------------------------------------------------------------
with st.expander("📋 View Complete Personal Flight Log", expanded=False):
    log_cols = [
        "flight_date", "carrier", "carrier_code", "alliance", "flight_number", 
        "origin", "dest", "aircraft_subfleet", "aircraft_generation", 
        "cabin_class", "seat", "seat_position", "distance_miles", "co2_kg"
    ]
    available_cols = [c for c in log_cols if c in df_flights.columns]
    
    st.dataframe(
        df_flights[available_cols].rename(columns={
            "flight_date": "Date",
            "carrier": "Airline",
            "carrier_code": "IATA",
            "alliance": "Alliance",
            "flight_number": "Flight #",
            "origin": "Origin",
            "dest": "Dest",
            "aircraft_subfleet": "Aircraft Subfleet",
            "aircraft_generation": "Generation",
            "cabin_class": "Cabin",
            "seat": "Seat",
            "seat_position": "Seat Position",
            "distance_miles": "Distance (mi)",
            "co2_kg": "CO₂ (kg)"
        }),
        width="stretch",
        hide_index=True
    )


