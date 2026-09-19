"""
Steve Riffe Unified Portfolio Design System: Authentic Product Preview & Landing Page for AvDB
Provides a representative, interactive snapshot of the AvDB platform before sign-in:
- Interactive lens previews (Airports, Airlines, Fleet & Routes, Alliances, Personal Traveler)
- Authentic monochromatic route cartography & Plotly analytical charts
- Tightly scoped pre-computed data to guarantee ZERO BigQuery cost explosion from bots
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

from app.config import settings
from app.utils.auth import get_google_auth_url, get_redirect_uri, logout
from app.utils.styling import render_html, render_kpi_card
from app.utils.queries import get_platform_live_kpis
from app.data.ref_demo_peeks import DEMO_PEEKS
from app.utils.flighty import build_flighty_travel_deck, generate_sample_flighty_data
from app.utils.visualizers import (
    MAP_THEMES,
    ROUTE_COLORWAYS,
    build_flighty_yoy_trends,
    build_flighty_alliance_donut,
    build_flighty_seat_preference_donut,
    PALETTE
)


def _build_anc_demo_deck() -> Any:
    """Builds a representative monochromatic route map for Anchorage (ANC) 2025 routes."""
    import pydeck as pdk

    routes = [
        {"origin": "ANC", "dest": "SEA", "origin_lat": 61.1743, "origin_lon": -149.996, "dest_lat": 47.4502, "dest_lon": -122.3088, "pax": "894k pax", "weight": 5.0},
        {"origin": "ANC", "dest": "IAH", "origin_lat": 61.1743, "origin_lon": -149.996, "dest_lat": 29.9902, "dest_lon": -95.3368, "pax": "142k pax", "weight": 3.0},
        {"origin": "ANC", "dest": "ORD", "origin_lat": 61.1743, "origin_lon": -149.996, "dest_lat": 41.9742, "dest_lon": -87.9073, "pax": "128k pax", "weight": 2.8},
        {"origin": "ANC", "dest": "MSP", "origin_lat": 61.1743, "origin_lon": -149.996, "dest_lat": 44.8848, "dest_lon": -93.2223, "pax": "119k pax", "weight": 2.6},
        {"origin": "ANC", "dest": "PDX", "origin_lat": 61.1743, "origin_lon": -149.996, "dest_lat": 45.5898, "dest_lon": -122.5951, "pax": "98k pax", "weight": 2.4},
        {"origin": "ANC", "dest": "DEN", "origin_lat": 61.1743, "origin_lon": -149.996, "dest_lat": 39.8561, "dest_lon": -104.6737, "pax": "92k pax", "weight": 2.2},
        {"origin": "ANC", "dest": "SLC", "origin_lat": 61.1743, "origin_lon": -149.996, "dest_lat": 40.7899, "dest_lon": -111.9791, "pax": "74k pax", "weight": 2.0},
        {"origin": "ANC", "dest": "LAX", "origin_lat": 61.1743, "origin_lon": -149.996, "dest_lat": 33.9416, "dest_lon": -118.4085, "pax": "68k pax", "weight": 1.9},
        {"origin": "ANC", "dest": "SFO", "origin_lat": 61.1743, "origin_lon": -149.996, "dest_lat": 37.6213, "dest_lon": -122.3790, "pax": "62k pax", "weight": 1.8},
        {"origin": "ANC", "dest": "FAI", "origin_lat": 61.1743, "origin_lon": -149.996, "dest_lat": 64.8151, "dest_lon": -147.8560, "pax": "210k pax", "weight": 3.8},
        {"origin": "ANC", "dest": "JNU", "origin_lat": 61.1743, "origin_lon": -149.996, "dest_lat": 58.3549, "dest_lon": -134.5760, "pax": "154k pax", "weight": 3.2},
    ]
    df_routes = pd.DataFrame(routes)

    nodes = [
        {"code": "ANC", "name": "Anchorage Int'l", "lat": 61.1743, "lon": -149.996, "is_hub": True},
        {"code": "SEA", "name": "Seattle-Tacoma", "lat": 47.4502, "lon": -122.3088, "is_hub": False},
        {"code": "IAH", "name": "Houston Bush", "lat": 29.9902, "lon": -95.3368, "is_hub": False},
        {"code": "ORD", "name": "Chicago O'Hare", "lat": 41.9742, "lon": -87.9073, "is_hub": False},
        {"code": "MSP", "name": "Minneapolis", "lat": 44.8848, "lon": -93.2223, "is_hub": False},
        {"code": "PDX", "name": "Portland", "lat": 45.5898, "lon": -122.5951, "is_hub": False},
        {"code": "DEN", "name": "Denver", "lat": 39.8561, "lon": -104.6737, "is_hub": False},
        {"code": "SLC", "name": "Salt Lake City", "lat": 40.7899, "lon": -111.9791, "is_hub": False},
        {"code": "LAX", "name": "Los Angeles", "lat": 33.9416, "lon": -118.4085, "is_hub": False},
        {"code": "SFO", "name": "San Francisco", "lat": 37.6213, "lon": -122.3790, "is_hub": False},
        {"code": "FAI", "name": "Fairbanks", "lat": 64.8151, "lon": -147.8560, "is_hub": False},
        {"code": "JNU", "name": "Juneau", "lat": 58.3549, "lon": -134.5760, "is_hub": False},
    ]
    df_nodes = pd.DataFrame(nodes)

    route_layer = pdk.Layer(
        "GreatCircleLayer",
        data=df_routes,
        id="demo-routes",
        get_source_position=["origin_lon", "origin_lat"],
        get_target_position=["dest_lon", "dest_lat"],
        get_source_color=[56, 189, 248, 220],
        get_target_color=[56, 189, 248, 220],
        get_width="weight",
        width_min_pixels=1.5,
        width_max_pixels=6,
        pickable=True,
        auto_highlight=True,
    )

    node_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_nodes,
        id="demo-nodes",
        get_position=["lon", "lat"],
        get_radius=30000,
        get_fill_color=[255, 107, 0, 240],
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=50.0,
        longitude=-125.0,
        zoom=2.6,
        min_zoom=1,
        max_zoom=8,
        pitch=0,
        bearing=0,
    )

    token = settings.mapbox_token
    style_url = MAP_THEMES.get("retro", MAP_THEMES["midnight"])

    return pdk.Deck(
        layers=[route_layer, node_layer],
        initial_view_state=view_state,
        map_style=style_url,
        tooltip={"text": "{origin} ➔ {dest}\nVolume: {pax}"},
        api_keys={"mapbox": token} if token else None
    )


def _build_fleet_gauge_preview() -> go.Figure:
    """Generates a representative 36-year aircraft gauge trend for preview."""
    years = list(range(1990, 2026))
    
    # Representative gauge curves
    b737 = [128 + (y - 1990) * 1.35 for y in years]
    a320 = [150 + (y - 1990) * 0.95 for y in years]
    rjs = [50 if y < 2005 else 50 + (y - 2005) * 1.5 for y in years]
    widebodies = [260 + (y - 1990) * 1.1 for y in years]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=widebodies, name="Widebody (B777/A330/B787)", line={"color": "#BF5AF2", "width": 2.5}))
    fig.add_trace(go.Scatter(x=years, y=b737, name="Boeing 737 Family (737-300 to MAX 9)", line={"color": "#0A84FF", "width": 2.5}))
    fig.add_trace(go.Scatter(x=years, y=a320, name="Airbus A320 Family (A319 to A321neo)", line={"color": "#30D158", "width": 2.5}))
    fig.add_trace(go.Scatter(x=years, y=rjs, name="Regional Jets (CRJ-200 to E175)", line={"color": "#FF9F0A", "width": 2.5, "dash": "dot"}))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": PALETTE["text"], "family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto"},
        xaxis={"title": "Year", "showgrid": True, "gridcolor": PALETTE["grid"]},
        yaxis={"title": "Average Seats per Departure", "showgrid": True, "gridcolor": PALETTE["grid"]},
        margin={"t": 10, "b": 20, "l": 40, "r": 20},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1}
    )
    return fig


def _build_alliance_market_share_preview() -> go.Figure:
    """Generates a representative 36-year global alliance consolidation area chart."""
    years = list(range(1990, 2026))
    
    star_shares = [0 if y < 1997 else min(38.0, (y - 1996) * 2.1) for y in years]
    skyteam_shares = [0 if y < 2000 else min(26.0, (y - 1999) * 1.8) for y in years]
    oneworld_shares = [0 if y < 1999 else min(22.0, (y - 1998) * 1.4) for y in years]
    wings_shares = [max(0, 14.0 - (y - 1990) * 0.4) if 1990 <= y <= 2004 else 0 for y in years]
    unaligned = [max(12.0, 100.0 - star_shares[i] - skyteam_shares[i] - oneworld_shares[i] - wings_shares[i]) for i in range(len(years))]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=star_shares, mode='lines', stackgroup='one', name='Star Alliance', line={"color": "#D4AF37", "width": 0.5}))
    fig.add_trace(go.Scatter(x=years, y=skyteam_shares, mode='lines', stackgroup='one', name='SkyTeam', line={"color": "#002F6C", "width": 0.5}))
    fig.add_trace(go.Scatter(x=years, y=oneworld_shares, mode='lines', stackgroup='one', name='oneworld', line={"color": "#7D0022", "width": 0.5}))
    fig.add_trace(go.Scatter(x=years, y=wings_shares, mode='lines', stackgroup='one', name='NW/KL Wings (1989-2004)', line={"color": "#00A3E0", "width": 0.5}))
    fig.add_trace(go.Scatter(x=years, y=unaligned, mode='lines', stackgroup='one', name='Unaligned / Independent', line={"color": "#475569", "width": 0.5}))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": PALETTE["text"], "family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto"},
        xaxis={"title": "Year", "showgrid": True, "gridcolor": PALETTE["grid"]},
        yaxis={"title": "US Gateway Share %", "showgrid": True, "gridcolor": PALETTE["grid"], "range": [0, 100]},
        margin={"t": 10, "b": 20, "l": 40, "r": 20},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1}
    )
    return fig


def render_landing_page():
    """
    Renders the public landing homepage with:
    1. Hero title & Live BigQuery Scale Strip
    2. Interactive Scoped Product Sandbox (Zero BigQuery Scans)
    3. Analytical Lenses Overview & Google Sign-In
    """
    redirect_uri = get_redirect_uri()
    auth_url = get_google_auth_url(redirect_uri)
    kpis = get_platform_live_kpis()

    render_html("""
        <style>
        .landing-portal-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 18px;
            margin-bottom: 20px;
            background: rgba(17, 29, 51, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            backdrop-filter: blur(14px);
        }
        .portal-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
        }
        .portal-avatar {
            width: 34px;
            height: 34px;
            border-radius: 8px;
            background: linear-gradient(135deg, #2563EB, #0F172A);
            border: 1px solid rgba(56, 189, 248, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 800;
            color: #FFFFFF;
            font-size: 13px;
        }
        .portal-text-name {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            color: #FFFFFF;
            font-size: 14px;
            line-height: 1.2;
        }
        .portal-text-sub {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #94A3B8;
        }
        .hero-banner-card {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(6, 9, 17, 0.98) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 18px;
            padding: 32px;
            margin-bottom: 24px;
            text-align: center;
            box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(16px);
        }
        .cta-button-orange {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #FF6B00;
            color: #FFFFFF !important;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            font-size: 1.02rem;
            padding: 12px 28px;
            border-radius: 10px;
            text-decoration: none !important;
            box-shadow: 0 4px 14px rgba(255, 107, 0, 0.35);
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .cta-button-orange:hover {
            background: #EA580C;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(255, 107, 0, 0.5);
        }
        .preview-container {
            background: rgba(17, 29, 51, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-top: 16px;
            margin-bottom: 28px;
        }
        .metric-badge-box {
            text-align: center;
            background: rgba(17, 29, 51, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 16px 12px;
            backdrop-filter: blur(12px);
        }
        .metric-val {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.7rem;
            font-weight: 800;
            color: #FFFFFF;
        }
        .metric-lbl {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.74rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #94A3B8;
            margin-top: 4px;
        }
        </style>
    """)

    # Top Portal Bar
    render_html(f"""
        <div class="landing-portal-bar">
            <div class="portal-brand">
                <div class="portal-avatar">✈️</div>
                <div>
                    <div class="portal-text-name">AvDB Aviation Intelligence</div>
                    <div class="portal-text-sub">US BTS T-100 & DB1B/OD40 Cloud Analytics · Monochromatic Cartography</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #10B981; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 4px 10px; border-radius: 6px;">● Zero-Scan Sandbox</span>
                <a href="{auth_url}" target="_self" class="cta-button-orange" style="padding: 8px 18px; font-size: 0.88rem;">
                    <span>🔐</span> Sign In
                </a>
            </div>
        </div>
    """)

    # Hero Banner
    render_html(f"""
        <div class="hero-banner-card">
            <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(56, 189, 248, 0.12); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; font-weight: 700; padding: 5px 14px; border-radius: 20px; margin-bottom: 16px; letter-spacing: 0.5px; text-transform: uppercase;">
                BigQuery Aviation Warehouse · {kpis['total_records_formatted']} Records
            </div>
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.6rem; font-weight: 800; color: #FFFFFF; margin-bottom: 14px; letter-spacing: -0.03em; line-height: 1.15;">
                AvDB Aviation Intelligence Platform <span style="color: #FF6B00;">.</span>
            </div>
            <div style="font-size: 1.1rem; color: #CBD5E1; max-width: 720px; margin: 0 auto 26px auto; line-height: 1.6;">
                Analyze 36 continuous years of commercial airline operations, multi-airport catchment dynamics, fleet gauge transitions,
                and empirical regional carrier attribution across the entire United States.
            </div>
            <a href="{auth_url}" target="_self" class="cta-button-orange">
                <span style="margin-right: 8px;">🔐</span> Sign In with Google to Unlock Full Platform
            </a>
            <div style="margin-top: 14px; color: #94A3B8; font-size: 0.82rem; font-family: 'JetBrains Mono', monospace;">
                Protected access • Google OAuth 2.0 • Google Cloud Run
            </div>
        </div>
    """)

    # Live Warehouse Scale Strip
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_html(f"""
            <div class="metric-badge-box">
                <div class="metric-val" style="color: #FB923C;">{kpis['t100_rows_formatted']}</div>
                <div class="metric-lbl">T-100 Operations Mart</div>
            </div>
        """)
    with col2:
        render_html(f"""
            <div class="metric-badge-box">
                <div class="metric-val" style="color: #38BDF8;">{kpis['od40_rows_formatted']}</div>
                <div class="metric-lbl">DB1B OD40 Survey Mart</div>
            </div>
        """)
    with col3:
        render_html(f"""
            <div class="metric-badge-box">
                <div class="metric-val" style="color: #FFFFFF;">{kpis['ref_airports_formatted']}</div>
                <div class="metric-lbl">Global Airport Coordinates</div>
            </div>
        """)
    with col4:
        render_html(f"""
            <div class="metric-badge-box">
                <div class="metric-val" style="color: #10B981;">{kpis['fleet_rows_formatted']}</div>
                <div class="metric-lbl">Fleet Dynamics Mart</div>
            </div>
        """)

    st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)

    # =========================================================================
    # Representative Product Snapshot & Interactive Scoped Sandbox
    # =========================================================================
    st.markdown("### 🖥️ Representative Product Preview")

    tab_airports, tab_airlines, tab_fleet, tab_alliances, tab_traveler = st.tabs([
        "✈️ Airport Explorer Preview",
        "🏢 Airline Network Preview",
        "💺 Fleet Dynamics Preview",
        "🌐 Alliances Preview",
        "📱 Personal Traveler Preview"
    ])

    # --- TAB 1: Airport Explorer Preview ---
    with tab_airports:
        anc_peek = DEMO_PEEKS["anc_2025"]
        st.markdown(f"#### {anc_peek['title']}")
        st.caption(f"{anc_peek['subtitle']} · Monochromatic In-Flight Route Cartography")

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_kpi_card("Total Passengers", anc_peek['kpis']['passengers'], subtitle=f"{anc_peek['kpis']['pax_yoy']} YoY")
        with k2:
            render_kpi_card("Commercial Departures", anc_peek['kpis']['departures'], subtitle=f"{anc_peek['kpis']['dep_yoy']} YoY")
        with k3:
            render_kpi_card("Available Capacity", anc_peek['kpis']['seats'], subtitle=f"{anc_peek['kpis']['load_factor']} Load Factor")
        with k4:
            render_kpi_card("Market Leader", "Alaska Airlines", subtitle="58.4% share (Attributed)")

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

        # Monochromatic Route Map
        deck_anc = _build_anc_demo_deck()
        st.pydeck_chart(deck_anc, height=440, width="stretch")

        st.markdown("##### 🛫 Direct Route Volume Breakdown (2025 Snapshot)")
        df_routes = pd.DataFrame(anc_peek['top_routes'])
        st.dataframe(
            df_routes.rename(columns={
                "route": "Corridor",
                "pax": "Annual Passengers",
                "carriers": "Attributed Operators",
                "distance": "Distance",
                "gauge": "Average Gauge"
            }),
            hide_index=True,
            width="stretch"
        )

    # --- TAB 2: Airline Network Preview ---
    with tab_airlines:
        as_peek = DEMO_PEEKS["as_2025"]
        st.markdown(f"#### {as_peek['title']}")
        st.caption(f"{as_peek['subtitle']} · Capturing Mainline AS + Contract Flying (Horizon & SkyWest)")

        ak1, ak2, ak3, ak4 = st.columns(4)
        with ak1:
            render_kpi_card("System Volume", as_peek['kpis']['system_pax'], subtitle=f"{as_peek['kpis']['pax_yoy']} YoY")
        with ak2:
            render_kpi_card("Departures", as_peek['kpis']['system_departures'], subtitle="Full Contract Network")
        with ak3:
            render_kpi_card("System Load Factor", as_peek['kpis']['load_factor'], subtitle=as_peek['kpis']['routes_served'])
        with ak4:
            render_kpi_card("Average Fleet Gauge", as_peek['kpis']['avg_gauge'], subtitle=as_peek['kpis']['gauge_trend'])

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        col_hubs, col_fleet = st.columns(2)
        with col_hubs:
            st.markdown("##### 🗺️ Top Hub Concentration by Departure Share")
            df_hubs = pd.DataFrame(as_peek['hubs'])
            st.dataframe(
                df_hubs.rename(columns={
                    "hub": "Hub Airport",
                    "dep_share": "Share %",
                    "annual_deps": "Annual Flights",
                    "destinations": "Direct Routes"
                }),
                hide_index=True,
                width="stretch"
            )
        with col_fleet:
            st.markdown("##### ✈️ Operational Fleet Deployment")
            df_fleet = pd.DataFrame(as_peek['fleet_mix'])
            st.dataframe(
                df_fleet.rename(columns={
                    "model": "Aircraft Model",
                    "count": "Hull Count",
                    "seats": "Seats/Ship",
                    "role": "Mission Profile"
                }),
                hide_index=True,
                width="stretch"
            )

    # --- TAB 3: Fleet Dynamics Preview ---
    with tab_fleet:
        st.markdown("#### 💺 Three-Decade Aircraft Gauge Evolution (1990–2026)")
        st.caption("Tracking the transition from 1990s narrowbodies through the 50-seat regional jet boom into modern up-gauging (MAX 9 & A321neo).")

        fig_gauge = _build_fleet_gauge_preview()
        st.plotly_chart(fig_gauge, width="stretch")

        st.markdown("""
            > **Analytical Key Insight**: U.S. carriers aggressively down-gauged secondary routes to 50-seat regional jets (CRJ-200 / ERJ-145) in the early 2000s, 
            > before fuel spikes and pilot shortages forced rapid consolidation into 76-seat dual-class E-Jets and high-capacity mainline narrowbodies.
        """)

    # --- TAB 4: Alliances Preview ---
    with tab_alliances:
        st.markdown("#### 🌐 Global Airline Alliances Market Share (1990–2026)")
        st.caption("36 years of international consolidation touching U.S. gateways: from the pioneering 1989 Northwest/KLM partnership to multilateral joint ventures.")

        fig_alliances = _build_alliance_market_share_preview()
        st.plotly_chart(fig_alliances, width="stretch")

        st.markdown("""
            > **Historical Note**: AvDB uniquely tracks the **Northwest / KLM Wings Alliance** from 1989, predating the multilateral Star Alliance (1997) 
            > and oneworld (1999) by nearly a decade.
        """)

    # --- TAB 5: Personal Traveler Preview ---
    with tab_traveler:
        st.markdown("#### 📱 Flighty Personal Traveler & BigQuery Cloud Vault")
        st.markdown(
            "AvDB allows users to upload their personal **Flighty CSV exports** to view their entire travel history mapped onto vintage "
            "monochromatic in-flight route cartography, with subfleet variant detection and private cloud vault persistence."
        )

        tk1, tk2, tk3 = st.columns(3)
        with tk1:
            render_kpi_card("Subfleet Detection", "32 Variants", subtitle="Distinguishes 737-900ER vs MAX 9")
        with tk2:
            render_kpi_card("Cloud Persistence", "Google BigQuery", subtitle="Capped at 1,000 flights/user")
        with tk3:
            render_kpi_card("Zero Data Risk", "Typed DELETE Purge", subtitle="Self-service instant deletion")

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        # Interactive Sample Route Cartography Preview
        df_sample = generate_sample_flighty_data()
        deck_sample = build_flighty_travel_deck(df_sample, home_airport="SEA", map_theme="retro", colorway="cobalt")
        st.pydeck_chart(deck_sample, height=380, width="stretch")

    # Privacy & Data Governance Footer Strip
    render_html("""
        <div style="margin-top: 48px; padding-top: 24px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 16px; font-size: 0.85rem; color: #94A3B8;">
                <span>🔒 <b>Privacy Assured</b>: Authenticated Google identity used strictly for access control</span>
                <span>•</span>
                <span>Travel logs committed to private BigQuery vault (capped at 1,000 flights)</span>
                <span>•</span>
                <span>Self-service fail-safe purge anytime</span>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #64748B;">
                BTS Data Attribution: US DOT TranStats (T-100 & DB1B/OD40)
            </div>
        </div>
    """)


def render_unauthorized_page(user_info: dict):
    """
    Renders an access denied message if the authenticated user is not in the allowlist.
    """
    email = user_info.get("email", "Unknown")
    name = user_info.get("name", "Traveler")

    render_html(f"""
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 16px; padding: 36px; text-align: center; max-width: 600px; margin: 60px auto;">
            <div style="font-size: 3rem; margin-bottom: 12px;">🚫</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #F5F5F7; margin-bottom: 8px;">Access Restricted</div>
            <div style="color: #CBD5E1; font-size: 1rem; line-height: 1.5; margin-bottom: 24px;">
                Hello <b>{name}</b> ({email}), your Google account is authenticated, but not on the authorized allowlist for this environment.
            </div>
        </div>
    """)
    if st.button("Sign Out / Switch Account", type="primary"):
        logout()
