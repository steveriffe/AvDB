"""
Steve Riffe Unified Portfolio Design System: Image-Rich Landing Homepage & Road Warrior Demo for AvDB
Provides a comprehensive pre-sign-in demo featuring Dave Pierce's 25-year Oil & Gas travel chronicle (2000–2025),
curated platform peeks (ANC 2025, Alaska Airlines 2025), and zero-BigQuery wallet protection.
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
from app.data.ref_demo_images import DEMO_HUBS_IMAGES, DEMO_AIRCRAFT_IMAGES
from app.data.ref_demo_peeks import DEMO_PEEKS
from app.data.dave_roadwarrior_dataset import get_dave_pierce_flighty_df
from app.utils.flighty import build_flighty_travel_deck
from app.utils.visualizers import (
    MAP_THEMES,
    ROUTE_COLORWAYS,
    build_flighty_yoy_trends,
    build_flighty_alliance_donut,
    build_flighty_seat_preference_donut,
    PALETTE
)


def render_landing_page():
    """
    Renders the public landing homepage with:
    1. Dave Pierce Oil & Gas Road Warrior Demo (2000–2025)
    2. Curated Platform Peeks (Anchorage 2025, Alaska Airlines 2025)
    3. Platform Overview & Google Sign-In (Zero-BigQuery Wallet Protection)
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
            padding: 28px 32px;
            margin-bottom: 24px;
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
            font-size: 0.95rem;
            padding: 10px 24px;
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
        .image-card {
            background: rgba(17, 29, 51, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            overflow: hidden;
            margin-bottom: 20px;
            transition: all 0.25s ease;
        }
        .image-card:hover {
            border-color: rgba(56, 189, 248, 0.4);
            transform: translateY(-3px);
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.4);
        }
        .image-card img {
            width: 100%;
            height: 180px;
            object-fit: cover;
            display: block;
        }
        .image-card-body {
            padding: 16px;
        }
        .image-card-tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            padding: 3px 8px;
            border-radius: 6px;
            display: inline-block;
            margin-bottom: 8px;
        }
        .image-card-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 4px;
        }
        .image-card-desc {
            font-size: 0.84rem;
            color: #CBD5E1;
            line-height: 1.45;
            margin-bottom: 10px;
        }
        .image-card-credit {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            color: #64748B;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding-top: 8px;
        }
        .image-card-credit a {
            color: #38BDF8;
            text-decoration: none;
        }
        .feature-card {
            background: rgba(17, 29, 51, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            height: 100%;
            transition: all 0.25s ease;
        }
        .feature-card:hover {
            border-color: rgba(56, 189, 248, 0.35);
            transform: translateY(-3px);
            box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.5);
        }
        .feature-icon {
            font-size: 2.2rem;
            margin-bottom: 12px;
        }
        .feature-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 8px;
        }
        .feature-desc {
            font-size: 0.92rem;
            color: #CBD5E1;
            line-height: 1.5;
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

    # Top AvDB Platform Bar
    render_html(f"""
        <div class="landing-portal-bar">
            <div class="portal-brand">
                <div class="portal-avatar">✈️</div>
                <div>
                    <div class="portal-text-name">AvDB Aviation Intelligence</div>
                    <div class="portal-text-sub">US BTS T-100 & DB1B/OD40 Cloud Analytics · Pre-Sign-In Interactive Demo</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #10B981; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 4px 10px; border-radius: 6px;">● Zero-BigQuery Demo Active</span>
                <a href="{auth_url}" target="_self" class="cta-button-orange">
                    <span>🔐</span> Sign In with Google
                </a>
            </div>
        </div>
    """)

    # 3-Tab Pre-Sign-In Navigation
    tab_demo, tab_peeks, tab_overview = st.tabs([
        "🌍 Road Warrior Demo (Dave Pierce 2000–2025)",
        "🔍 Curated Platform Peeks (ANC & Alaska 2025)",
        "⚡ Platform Overview & Full Catalog"
    ])

    # =========================================================================
    # TAB 1: Dave Pierce Oil & Gas Road Warrior Demo
    # =========================================================================
    with tab_demo:
        df_dave = get_dave_pierce_flighty_df()

        render_html("""
            <div class="hero-banner-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 700; color: #FF9F0A; background: rgba(255, 159, 10, 0.15); border: 1px solid rgba(255, 159, 10, 0.35); padding: 4px 10px; border-radius: 20px; text-transform: uppercase;">
                        Road Warrior Case Study
                    </span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #94A3B8;">2000 – 2025 Travel Chronicle</span>
                </div>
                <h1 style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.2rem; font-weight: 800; color: #FFFFFF; margin: 0 0 10px 0; line-height: 1.2;">
                    Dave Pierce <span style="color: #38BDF8;">·</span> Senior Petroleum Reservoir Engineer
                </h1>
                <p style="font-size: 1.05rem; color: #CBD5E1; line-height: 1.6; margin-bottom: 18px;">
                    Over a quarter-century of upstream energy exploration, Dave globe-trotted between North American deepwater and Arctic frontiers
                    and Asian marine fabrication yards. Centered on <b>Anchorage (ANC)</b>, <b>Houston (IAH)</b>, <b>Hong Kong (HKG)</b>, and <b>Halifax (YHZ)</b>,
                    his 275-flight log realistically reflects <b>Continental/United (44%)</b>, <b>Air Canada (26%)</b>, and <b>Alaska Airlines (21%)</b> —
                    along with the odd reluctant holiday to <b>Honolulu (HNL)</b> and <b>Bali (DPS)</b> where Dave famously shunned the beach to analyze well logs in air-conditioned comfort.
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #38BDF8; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); padding: 3px 8px; border-radius: 6px;">ANC: North Slope Arctic</span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #FB923C; background: rgba(251, 146, 60, 0.1); border: 1px solid rgba(251, 146, 60, 0.3); padding: 3px 8px; border-radius: 6px;">IAH: Energy Corridor HQ</span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #F43F5E; background: rgba(244, 63, 94, 0.1); border: 1px solid rgba(244, 63, 94, 0.3); padding: 3px 8px; border-radius: 6px;">HKG: Asia-Pacific Shipyards</span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #34D399; background: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.3); padding: 3px 8px; border-radius: 6px;">YHZ: Sable Offshore Energy</span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #A78BFA; background: rgba(167, 139, 250, 0.1); border: 1px solid rgba(167, 139, 250, 0.3); padding: 3px 8px; border-radius: 6px;">HNL & DPS: Reluctant R&R</span>
                </div>
            </div>
        """)

        # Top Metric Cards
        total_flights = len(df_dave)
        total_miles = int(df_dave["distance_miles"].sum())
        total_co2_t = df_dave["co2_kg"].sum() / 1000.0 if "co2_kg" in df_dave.columns else 142.1
        trees_offset = int(total_co2_t * 45)
        circ_earth = total_miles / 24901.0

        col_k1, col_k2, col_k3, col_k4, col_k5, col_k6 = st.columns(6)
        with col_k1:
            render_kpi_card("Total Flights", f"{total_flights}", subtitle="2000–2025 Segments")
        with col_k2:
            render_kpi_card("Total Air Miles", f"{total_miles:,} mi", subtitle=f"~{circ_earth:.1f}x Earth laps")
        with col_k3:
            render_kpi_card("Top Carrier", "United / Continental", subtitle="122 flights (44.4%)")
        with col_k4:
            render_kpi_card("Frequent Hub", "Houston (IAH)", subtitle="96 flight segments")
        with col_k5:
            render_kpi_card("Premium Cabin", "74.2% First/Polaris", subtitle="Lie-flat long haul")
        with col_k6:
            render_kpi_card("CO₂ Footprint", f"{total_co2_t:.1f} t", subtitle=f"~{trees_offset:,} trees offset")

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # Interactive 3D Great-Circle Route Map (PyDeck)
        # ---------------------------------------------------------------------
        st.subheader("🌐 Dave's Global Route Network (In-Flight Cartography)")
        st.markdown(
            "<p style='color: #8E8E93; font-size: 0.9rem; margin-top: -8px; margin-bottom: 14px;'>"
            "Visualized with geodesic Great-Circle arcs on AvDB's dark luxury mapbox basemap. Arc thickness reflects flight frequency."
            "</p>",
            unsafe_allow_html=True
        )

        deck = build_flighty_travel_deck(
            df_flights=df_dave,
            home_airport="IAH",
            map_theme="personal",
            colorway="ember"
        )
        st.pydeck_chart(deck, height=520, width="stretch")

        st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # Image Gallery: Core Hubs & Reluctant R&R
        # ---------------------------------------------------------------------
        st.subheader("📸 Core Energy Nodes & Leisure Escapes")
        st.markdown(
            "<p style='color: #8E8E93; font-size: 0.9rem; margin-top: -8px; margin-bottom: 20px;'>"
            "The operational centers defining Dave Pierce's career, plus high-res photography with verified credits and open licensing."
            "</p>",
            unsafe_allow_html=True
        )

        gcol1, gcol2, gcol3 = st.columns(3)
        hubs_list = list(DEMO_HUBS_IMAGES.items())

        for idx, (code, hub_info) in enumerate(hubs_list):
            target_col = gcol1 if idx % 3 == 0 else (gcol2 if idx % 3 == 1 else gcol3)
            badge_color = "#38BDF8" if code in ["ANC", "YHZ"] else ("#FB923C" if code == "IAH" else ("#F43F5E" if code == "HKG" else "#A78BFA"))
            bg_color = "rgba(56, 189, 248, 0.15)" if code in ["ANC", "YHZ"] else ("rgba(251, 146, 60, 0.15)" if code == "IAH" else ("rgba(244, 63, 94, 0.15)" if code == "HKG" else "rgba(167, 139, 250, 0.15)"))
            
            with target_col:
                render_html(f"""
                    <div class="image-card">
                        <img src="{hub_info['image_url']}" alt="{hub_info['name']}" loading="lazy" />
                        <div class="image-card-body">
                            <span class="image-card-tag" style="color: {badge_color}; background: {bg_color};">{hub_info['tag']} · {code}</span>
                            <div class="image-card-title">{hub_info['city']}</div>
                            <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 8px; font-family: 'JetBrains Mono', monospace;">{hub_info['name']}</div>
                            <div class="image-card-desc">{hub_info['description']}</div>
                            <div class="image-card-credit">
                                📷 Photo: <a href="{hub_info['source_url']}" target="_blank">{hub_info['credit']}</a> ({hub_info['license']})
                            </div>
                        </div>
                    </div>
                """)

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # Visual Analytics: Carrier Mix & YoY Trends
        # ---------------------------------------------------------------------
        st.subheader("📊 25-Year Travel Analytics & Fleet Breakdown")
        st.markdown(
            "<p style='color: #8E8E93; font-size: 0.9rem; margin-top: -8px; margin-bottom: 18px;'>"
            "Longitudinal trends reflecting carrier consolidation, alliance transitions, and equipment evolution."
            "</p>",
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### 📈 Annual Flight Frequency & Air Miles")
            fig_yoy = build_flighty_yoy_trends(df_dave)
            st.plotly_chart(fig_yoy, width="stretch")
        with c2:
            st.markdown("##### 🌐 Alliance Loyalty Transition (Star vs Mileage Plan)")
            fig_alliance = build_flighty_alliance_donut(df_dave)
            st.plotly_chart(fig_alliance, width="stretch")

        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

        c3, c4 = st.columns(2)
        with c3:
            st.markdown("##### 💺 In-Flight Seating Position Preference")
            fig_seat = build_flighty_seat_preference_donut(df_dave)
            st.plotly_chart(fig_seat, width="stretch")
        with c4:
            st.markdown("##### 🏢 Carrier Share Breakdown")
            carrier_counts = df_dave["carrier"].value_counts().reset_index()
            carrier_counts.columns = ["Carrier", "Flights"]
            carrier_colors = {
                "CONTINENTAL AIRLINES": "#002244",
                "UNITED AIRLINES": "#005DAA",
                "AIR CANADA": "#E31837",
                "ALASKA AIRLINES": "#01426A",
                "SINGAPORE AIRLINES": "#F5A800",
                "GARUDA INDONESIA": "#007A87"
            }
            fig_carrier = px.pie(
                carrier_counts,
                values="Flights",
                names="Carrier",
                hole=0.55,
                color="Carrier",
                color_discrete_map=carrier_colors
            )
            fig_carrier.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": PALETTE["text"], "family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto"},
                margin={"t": 10, "b": 10, "l": 10, "r": 10},
                showlegend=True
            )
            st.plotly_chart(fig_carrier, width="stretch")

        st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # Aircraft Workhorses Gallery
        # ---------------------------------------------------------------------
        st.subheader("✈️ Iconic Aircraft Fleet Workhorses")
        st.markdown(
            "<p style='color: #8E8E93; font-size: 0.9rem; margin-top: -8px; margin-bottom: 20px;'>"
            "The workhorses that carried Dave across polar latitudes, transpacific routes, and Canadian maritimes."
            "</p>",
            unsafe_allow_html=True
        )

        acol1, acol2, acol3, acol4 = st.columns(4)
        for idx, ac in enumerate(DEMO_AIRCRAFT_IMAGES):
            target_acol = acol1 if idx == 0 else (acol2 if idx == 1 else (acol3 if idx == 2 else acol4))
            with target_acol:
                render_html(f"""
                    <div class="image-card">
                        <img src="{ac['image_url']}" alt="{ac['model']}" loading="lazy" />
                        <div class="image-card-body">
                            <div class="image-card-title" style="font-size: 0.95rem;">{ac['model']}</div>
                            <div style="font-size: 0.78rem; color: #38BDF8; margin-bottom: 6px; font-family: 'JetBrains Mono', monospace;">{ac['operator']}</div>
                            <div class="image-card-desc" style="font-size: 0.8rem;">{ac['description']}</div>
                            <div class="image-card-credit">
                                📷 {ac['credit']} ({ac['license']})
                            </div>
                        </div>
                    </div>
                """)

        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # Filterable Flight Log Table
        # ---------------------------------------------------------------------
        st.subheader("📋 Searchable 275-Flight Travel Log (2000–2025)")
        st.markdown(
            "<p style='color: #8E8E93; font-size: 0.9rem; margin-top: -8px; margin-bottom: 16px;'>"
            "Search by project note, airport code, or airline to inspect individual flight segments."
            "</p>",
            unsafe_allow_html=True
        )

        fcol1, fcol2, fcol3 = st.columns([2, 1, 1])
        with fcol1:
            search_query = st.text_input("🔍 Search Flights", placeholder="e.g. Prudhoe Bay, Deep Panuke, Shekou, Waikiki, Bali, 777-200ER...")
        with fcol2:
            airline_filter = st.selectbox("Filter Airline", options=["All Airlines"] + sorted(df_dave["carrier"].unique().tolist()))
        with fcol3:
            year_range = st.slider("Year Range", min_value=2000, max_value=2025, value=(2000, 2025))

        df_filtered = df_dave.copy()
        if search_query:
            q = search_query.lower()
            df_filtered = df_filtered[
                df_filtered["route"].str.lower().str.contains(q, na=False) |
                df_filtered["carrier"].str.lower().str.contains(q, na=False) |
                df_filtered["aircraft_subfleet"].str.lower().str.contains(q, na=False) |
                df_filtered["Reason"].astype(str).str.lower().str.contains(q, na=False) |
                df_filtered["seat"].str.lower().str.contains(q, na=False)
            ]
        if airline_filter != "All Airlines":
            df_filtered = df_filtered[df_filtered["carrier"] == airline_filter]
        
        df_filtered = df_filtered[
            (df_filtered["year"] >= year_range[0]) & 
            (df_filtered["year"] <= year_range[1])
        ]

        display_cols = ["date", "flight_number", "route", "carrier", "aircraft_subfleet", "seat", "cabin_class", "distance_miles", "Reason"]
        renamed_cols = {
            "date": "Date",
            "flight_number": "Flight",
            "route": "Route",
            "carrier": "Airline",
            "aircraft_subfleet": "Aircraft Model",
            "seat": "Seat",
            "cabin_class": "Class",
            "distance_miles": "Miles",
            "Reason": "Project / Mission Purpose"
        }
        df_table = df_filtered[display_cols].rename(columns=renamed_cols)

        st.dataframe(
            df_table,
            height=380,
            width="stretch",
            hide_index=True,
            column_config={
                "Miles": st.column_config.NumberColumn(format="%d mi"),
                "Project / Mission Purpose": st.column_config.TextColumn(width="large")
            }
        )

        csv_data = df_table.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Dave Pierce Flight Dataset (CSV)",
            data=csv_data,
            file_name="dave_pierce_oil_and_gas_flights_2000_2025.csv",
            mime="text/csv",
            help="Download Dave's full 275-record flight log formatted for Flighty or spreadsheet analysis"
        )

    # =========================================================================
    # TAB 2: Curated Platform Peeks (Zero-BigQuery)
    # =========================================================================
    with tab_peeks:
        st.markdown("### 🔍 Curated Platform Peeks (Zero-BigQuery Scan Guarantee)")
        st.markdown(
            "<p style='color: #8E8E93; font-size: 0.95rem; margin-top: -8px; margin-bottom: 24px;'>"
            "Get an authentic taste of AvDB's analytical depth without executing live BigQuery queries. "
            "These pre-computed snapshots illustrate what AvDB generates across our 50,000+ airports and 100+ airlines."
            "</p>",
            unsafe_allow_html=True
        )

        anc_peek = DEMO_PEEKS["anc_2025"]
        as_peek = DEMO_PEEKS["as_2025"]

        # Anchorage Peek Section
        st.markdown(f"#### ✈️ {anc_peek['title']}")
        st.caption(anc_peek['subtitle'])

        pcol1, pcol2 = st.columns([1, 2])
        with pcol1:
            render_html(f"""
                <div class="image-card" style="margin-bottom: 0;">
                    <img src="{DEMO_HUBS_IMAGES['ANC']['image_url']}" alt="Anchorage Airport" style="height: 220px;" />
                    <div class="image-card-body">
                        <div class="image-card-title">Ted Stevens Anchorage (ANC)</div>
                        <div class="image-card-desc">Leading cargo crossroad and Arctic passenger hub nestled against the Chugach Mountains.</div>
                        <div class="image-card-credit">📷 Paxson Woelber / Unsplash</div>
                    </div>
                </div>
            """)
        with pcol2:
            ak1, ak2, ak3, ak4 = st.columns(4)
            with ak1:
                render_kpi_card("Total Passengers", anc_peek['kpis']['passengers'], subtitle=f"{anc_peek['kpis']['pax_yoy']} YoY")
            with ak2:
                render_kpi_card("Departures", anc_peek['kpis']['departures'], subtitle=f"{anc_peek['kpis']['dep_yoy']} YoY")
            with ak3:
                render_kpi_card("Avg Load Factor", anc_peek['kpis']['load_factor'], subtitle=f"{anc_peek['kpis']['seats']} seats")
            with ak4:
                render_kpi_card("Market Leader", "Alaska Airlines", subtitle="58.4% commercial share")

            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            st.markdown("##### 🛫 Top 5 Direct Anchorage Routes (2025)")
            df_anc_routes = pd.DataFrame(anc_peek['top_routes'])
            st.dataframe(
                df_anc_routes.rename(columns={
                    "route": "Corridor",
                    "pax": "Annual Passengers",
                    "carriers": "Operating Carriers",
                    "distance": "Distance",
                    "gauge": "Avg Gauge"
                }),
                hide_index=True,
                width="stretch"
            )

        st.markdown("---")

        # Alaska Airlines Peek Section
        st.markdown(f"#### 🏢 {as_peek['title']}")
        st.caption(as_peek['subtitle'])

        ask1, ask2, ask3, ask4 = st.columns(4)
        with ask1:
            render_kpi_card("System Passengers", as_peek['kpis']['system_pax'], subtitle=f"{as_peek['kpis']['pax_yoy']} YoY")
        with ask2:
            render_kpi_card("System Departures", as_peek['kpis']['system_departures'], subtitle="382k movements")
        with ask3:
            render_kpi_card("System Load Factor", as_peek['kpis']['load_factor'], subtitle=as_peek['kpis']['routes_served'])
        with ask4:
            render_kpi_card("Average Fleet Gauge", as_peek['kpis']['avg_gauge'], subtitle=as_peek['kpis']['gauge_trend'])

        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

        hcol1, hcol2 = st.columns(2)
        with hcol1:
            st.markdown("##### 🗺️ Top Alaska Airlines Hubs by Departure Share")
            df_hubs = pd.DataFrame(as_peek['hubs'])
            st.dataframe(
                df_hubs.rename(columns={
                    "hub": "Hub Airport",
                    "dep_share": "Share %",
                    "annual_deps": "Departures",
                    "destinations": "Direct Routes"
                }),
                hide_index=True,
                width="stretch"
            )
        with hcol2:
            st.markdown("##### 💺 Fleet Mix & Modernization Status")
            df_fleet = pd.DataFrame(as_peek['fleet_mix'])
            st.dataframe(
                df_fleet.rename(columns={
                    "model": "Aircraft Model",
                    "count": "Active Fleet",
                    "seats": "Seats/Ship",
                    "role": "Mission Profile"
                }),
                hide_index=True,
                width="stretch"
            )

        render_html(f"""
            <div style="margin-top: 32px; background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 14px; padding: 20px 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
                <div>
                    <div style="font-weight: 700; color: #FFFFFF; font-size: 1.05rem;">🔒 Unlock Live BigQuery Analytics for 50,000+ Airports & All Airlines</div>
                    <div style="color: #94A3B8; font-size: 0.88rem; margin-top: 4px;">Sign in with Google to explore 36 years of historical trends (1990–2026), Great-Circle cartography, and your own Flighty travel vault.</div>
                </div>
                <a href="{auth_url}" target="_self" class="cta-button-orange">
                    <span>🔐</span> Sign In with Google
                </a>
            </div>
        """)

    # =========================================================================
    # TAB 3: Platform Overview & Login
    # =========================================================================
    with tab_overview:
        render_html(f"""
            <div style="background: linear-gradient(135deg, rgba(17, 29, 51, 0.95) 0%, rgba(6, 9, 17, 0.98) 100%); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 40px 32px; text-align: center; margin-bottom: 24px; box-shadow: 0 20px 48px -12px rgba(0, 0, 0, 0.6); backdrop-filter: blur(16px);">
                <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(56, 189, 248, 0.12); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; font-weight: 700; padding: 5px 14px; border-radius: 20px; margin-bottom: 16px; letter-spacing: 0.5px; text-transform: uppercase;">
                    BigQuery Aviation Intelligence · {kpis['total_records_formatted']} System Records
                </div>
                <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.6rem; font-weight: 800; color: #FFFFFF; margin-bottom: 14px; letter-spacing: -0.03em; line-height: 1.15;">
                    AvDB Aviation Platform <span style="color: #FF6B00;">.</span>
                </div>
                <div style="font-size: 1.1rem; color: #CBD5E1; max-width: 680px; margin: 0 auto 28px auto; line-height: 1.6;">
                    Interactive U.S. BTS T-100 operations and DB1B ticket yield analytics modeled in Google BigQuery, featuring geodesic great-circle cartography, multi-airport catchment systems, and complete fleet dynamics.
                </div>
                <a href="{auth_url}" target="_self" class="cta-button-orange" style="font-size: 1.05rem; padding: 12px 32px;">
                    <span style="margin-right: 8px;">🔐</span> Sign in with Google
                </a>
                <div style="margin-top: 14px; color: #94A3B8; font-size: 0.82rem; font-family: 'JetBrains Mono', monospace;">
                    Protected access • Google OAuth 2.0 • Google Cloud Run
                </div>
            </div>
        """)

        # Dynamic BigQuery Warehouse Scale Strip
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

        render_html("<div style='margin-top: 32px;'></div>")

        # Feature Grid
        st.markdown("### 🧭 Analytical Lenses & Capabilities")
        fcol1, fcol2, fcol3 = st.columns(3)

        with fcol1:
            render_html("""
                <div class="feature-card">
                    <div class="feature-icon">✈️</div>
                    <div class="feature-title">Airports Lens</div>
                    <div class="feature-desc">
                        Comprehensive passenger traffic trends, catchment metro area analysis, route churn, and interactive Great-Circle destination mapping.
                    </div>
                </div>
            """)

        with fcol2:
            render_html("""
                <div class="feature-card">
                    <div class="feature-icon">🏢</div>
                    <div class="feature-title">Airlines Lens</div>
                    <div class="feature-desc">
                        Carrier route networks, hub concentration metrics, average fares, Stage Length vs. Yield per RPM curves, and corporate merger timelines.
                    </div>
                </div>
            """)

        with fcol3:
            render_html("""
                <div class="feature-card">
                    <div class="feature-icon">💺</div>
                    <div class="feature-title">Fleet & Routes</div>
                    <div class="feature-desc">
                        Aircraft gauge transitions, equipment utilization by route, regional vs. mainline shifts, and verified engineering specifications & photography.
                    </div>
                </div>
            """)

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
