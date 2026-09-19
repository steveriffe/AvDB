import sys
from pathlib import Path

# Automatically add project root to Python path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import streamlit as st
import pandas as pd
from app.config import settings
from app.utils.styling import apply_apple_style, render_kpi_card, render_portal_nav_link
from app.utils.auth import require_auth

st.set_page_config(
    page_title="Flighty Personal Traveler | AvDB",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_apple_style()
render_portal_nav_link()
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
    save_user_flights_to_bigquery,
    load_user_flights_from_bigquery,
    delete_user_flights_from_bigquery,
    get_user_travel_telemetry,
    USER_FLIGHT_LIMIT,
    AIRPORT_COORDINATES
)

st.title("📱 Flighty Personal Traveler")

# ----------------------------------------------------------------------
# Data Ingestion & State Management (BigQuery Vault Integration)
# ----------------------------------------------------------------------
user_profile = st.session_state.get("user") or {}
current_user_email = user_profile.get("email", "")

if "flighty_df" not in st.session_state:
    st.session_state["flighty_df"] = None
if "flighty_source_name" not in st.session_state:
    st.session_state["flighty_source_name"] = None
if "vault_loaded" not in st.session_state:
    st.session_state["vault_loaded"] = False

# Automatically load persisted flight log from BigQuery on first load
if not st.session_state["vault_loaded"] and current_user_email:
    persisted_df = load_user_flights_from_bigquery(current_user_email)
    if persisted_df is not None and not persisted_df.empty:
        st.session_state["flighty_df"] = persisted_df
        st.session_state["flighty_source_name"] = f"BigQuery Vault ({current_user_email})"
    st.session_state["vault_loaded"] = True

with st.sidebar:
    st.markdown("### 🗂️ Travel Data Source")
    uploaded_file = st.file_uploader(
        "Upload Flighty CSV", 
        type=["csv"], 
        help=f"Export your flights from the Flighty app as CSV. Max limit: {USER_FLIGHT_LIMIT:,} flight segments."
    )

    if uploaded_file is not None:
        try:
            parsed_df = parse_flighty_csv(uploaded_file.getvalue())
            if len(parsed_df) > USER_FLIGHT_LIMIT:
                st.error(f"⚠️ Log contains {len(parsed_df):,} flights, which exceeds the {USER_FLIGHT_LIMIT:,} safety limit. Only the first {USER_FLIGHT_LIMIT:,} will be loaded.")
                parsed_df = parsed_df.iloc[:USER_FLIGHT_LIMIT]
            st.session_state["flighty_df"] = parsed_df
            st.session_state["flighty_source_name"] = uploaded_file.name
            st.success(f"Loaded {len(parsed_df)} flights from `{uploaded_file.name}`")
        except Exception as e:
            st.error(f"Error parsing CSV: {e}")

    # Persistence Action: Commit to BigQuery Vault
    if st.session_state["flighty_df"] is not None and current_user_email:
        if st.button("💾 Save to Cloud Vault (BigQuery)", use_container_width=True, help="Persists your flight log securely in BigQuery under your authenticated account"):
            with st.spinner("Committing flight log to Google BigQuery..."):
                ok, msg = save_user_flights_to_bigquery(current_user_email, st.session_state["flighty_df"])
                if ok:
                    st.success(msg)
                    st.session_state["flighty_source_name"] = f"BigQuery Vault ({current_user_email})"
                else:
                    st.error(msg)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("Load Sample", help="Load 30-flight modern sample log"):
            st.session_state["flighty_df"] = generate_sample_flighty_data()
            st.session_state["flighty_source_name"] = "Sample Travel Log (Frequent Traveler)"
            st.rerun()
    with col_s2:
        if st.session_state["flighty_df"] is not None:
            if st.button("Clear View"):
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
    st.info("👋 No flight log loaded yet. Click **'Load Sample'** in the sidebar to test with a realistic 30-flight travel log, or upload your own Flighty CSV export above!")
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

# Determine primary home hub
home_hub = df_flights["origin"].value_counts().index[0] if not df_flights.empty else "SEA"
try:
    deck = build_flighty_travel_deck(
        df_flights=df_flights,
        home_airport=home_hub,
        map_theme=selected_theme,
        colorway=selected_colorway
    )
    st.pydeck_chart(deck, height=520, width="stretch")
except (KeyError, Exception) as _map_err:
    st.markdown(
        """
        <div style="background: radial-gradient(circle at 50% 35%, rgba(56, 189, 248, 0.06) 0%, rgba(11, 25, 44, 0.65) 75%); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 48px 24px; text-align: center; backdrop-filter: blur(12px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 60px; height: 60px; border-radius: 50%; background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.25); margin-bottom: 16px;">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="2" y1="12" x2="22" y2="12"></line>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                </svg>
            </div>
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 6px;">
                Geodesic Route Cartography Offline
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #94A3B8; max-width: 440px; margin: 0 auto; line-height: 1.5;">
                Airport waypoint coordinates could not be resolved for this segment log. Re-import your flight log CSV to reconstruct 3D great-circle arcs.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Granular Subfleet Breakdown & Grouping Hierarchy
# ----------------------------------------------------------------------
st.subheader("✈️ Aircraft Subfleet & Equipment Analytics")

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
    # Monochromatic sequential cobalt/indigo gradient for distance flown
    dist_sorted = fleet_summary.sort_values("total_miles", ascending=True).head(8)
    n_items = len(dist_sorted)
    mono_ramp = [
        "#1E3A8A", "#1E40AF", "#1D4ED8", "#2563EB",
        "#3B82F6", "#60A5FA", "#38BDF8", "#7DD3FC"
    ]
    colors = mono_ramp[max(0, len(mono_ramp) - n_items):]
    fig_dist_bar = go.Figure(go.Bar(
        x=dist_sorted["total_miles"],
        y=dist_sorted[col_target],
        orientation="h",
        marker=dict(
            color=colors,
            opacity=0.85,
            line=dict(color="rgba(255, 255, 255, 0.12)", width=1)
        ),
        text=[f"{v:,.0f} mi" for v in dist_sorted["total_miles"]],
        textposition="outside",
        textfont=dict(color="#CBD5E1", size=10, family="JetBrains Mono"),
        hovertemplate="<b>%{y}</b><br>Miles: %{x:,.0f}<extra></extra>",
    ))
    fig_dist_bar.update_layout(
        title=dict(text="Distance Flown (Miles)", font=dict(size=14, color="#F5F5F7")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=10, r=70, t=35, b=10),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8E8E93"), showticklabels=False),
        yaxis=dict(showgrid=False, tickfont=dict(color="#F5F5F7", size=11)),
        showlegend=False,
    )
    st.plotly_chart(fig_dist_bar, width="stretch")

# ----------------------------------------------------------------------
# Year-over-Year Travel Dynamics & Alliance Loyalty
# ----------------------------------------------------------------------
st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
st.subheader("📈 Annual Travel Trends & Global Alliance Loyalty")

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

scol1, scol2 = st.columns(2)
with scol1:
    fig_seat = build_flighty_seat_preference_donut(df_flights)
    st.plotly_chart(fig_seat, width="stretch")
with scol2:
    from app.utils.flighty import standardize_cabin_class
    df_flights["cabin_class"] = df_flights["cabin_class"].apply(standardize_cabin_class)
    cabin_counts = df_flights["cabin_class"].value_counts().reset_index()
    cabin_counts.columns = ["cabin_class", "count"]
    fig_cabin = px.pie(
        cabin_counts,
        names="cabin_class",
        values="count",
        hole=0.55,
        color="cabin_class",
        color_discrete_map={
            "First": "#BF5AF2",
            "Business": "#0A84FF",
            "Premium Economy": "#30D158",
            "Economy": "#FF9F0A"
        }
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

# ----------------------------------------------------------------------
# Account Privacy & Fail-Safe Data Deletion Section
# ----------------------------------------------------------------------
st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)
with st.expander("🔒 Account Data Governance & Fail-Safe Deletion", expanded=False):
    st.markdown("### 🗄️ Cloud Vault Telemetry & Deletion Controls")
    
    # Telemetry
    telemetry = get_user_travel_telemetry()
    tcol1, tcol2, tcol3 = st.columns(3)
    with tcol1:
        st.metric("Total User Flights in Vault", f"{telemetry['total_user_flights']:,}")
    with tcol2:
        st.metric("Total Registered Travelers", f"{telemetry['total_traveler_users']:,}")
    with tcol3:
        user_flight_count = len(df_flights) if "BigQuery Vault" in st.session_state.get("flighty_source_name", "") else 0
        st.metric("Your Stored Records", f"{user_flight_count:,} / {USER_FLIGHT_LIMIT:,}")

    st.markdown("---")
    st.markdown("#### ⚠️ Danger Zone: Permanent Data Deletion")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.9rem;'>"
        "To prevent accidental loss, deleting your stored personal travel records from BigQuery requires explicit confirmation. "
        "Type <b>DELETE</b> in the verification box below to enable the permanent purge button."
        "</p>",
        unsafe_allow_html=True
    )

    del_col1, del_col2 = st.columns([2, 1])
    with del_col1:
        delete_confirmation = st.text_input(
            "Confirmation Input",
            placeholder="Type DELETE to confirm",
            label_visibility="collapsed"
        )
    with del_col2:
        can_delete = delete_confirmation.strip() == "DELETE" and bool(current_user_email)
        if st.button("🚨 Purge All My Flight Records", type="primary", disabled=not can_delete, use_container_width=True):
            with st.spinner("Purging flight records from BigQuery..."):
                ok, msg = delete_user_flights_from_bigquery(current_user_email)
                if ok:
                    st.success(msg)
                    st.session_state["flighty_df"] = None
                    st.session_state["flighty_source_name"] = None
                    st.rerun()
                else:
                    st.error(msg)



