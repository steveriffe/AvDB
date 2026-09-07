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
    page_title="Airlines Explorer | AvDB",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply Apple-esque CSS styling
apply_apple_style()
require_auth()

import plotly.express as px
import plotly.graph_objects as go
from app.utils.queries import (
    get_airline_kpis,
    get_airline_hubs,
    get_airline_yield_curve,
    CARRIER_STRATEGY,
    get_airline_hub_expansion_proposals,
    get_unserved_connecting_markets,
    get_airline_routes_dataset,
)
from app.utils.visualizers import (
    build_airline_network_deck,
)
from app.utils.alliances import (
    get_carrier_alliance,
    get_carrier_logo_url,
    get_carrier_alliance_timeline,
)
from app.utils.mergers import (
    get_merger_as_predecessor,
    get_mergers_as_successor,
    get_all_ancestor_codes,
    get_ultimate_successor,
    format_merger_lineage_html,
    get_all_airline_mergers,
)


# -------------------------------------------------------------
# 1. Header & Top Control Bar
# -------------------------------------------------------------
st.title("🏢 Airline Network & Yield Explorer")
st.markdown("<p style='color: #8E8E93; margin-top: -12px; margin-bottom: 20px;'>Inspect route network density, hub concentration, fare yield curves, competitor price premiums, historical corporate mergers, and target expansion cities by hub.</p>", unsafe_allow_html=True)

carriers_dict = {
    "AS": "Alaska Airlines (AS)",
    "UA": "United Airlines (UA)",
    "DL": "Delta Air Lines (DL)",
    "AA": "American Airlines (AA)",
    "WN": "Southwest Airlines (WN)",
    "B6": "JetBlue Airways (B6)",
    "NK": "Spirit Airlines (NK)",
    "F9": "Frontier Airlines (F9)",
    "G4": "Allegiant Air (G4)",
    "HA": "Hawaiian Airlines (HA - Acquired by AS 2024)",
    "CO": "Continental Airlines (CO - Merged with UA 2010)",
    "NW": "Northwest Airlines (NW - Merged with DL 2008)",
    "US": "US Airways (US - Merged with AA 2013)",
    "HP": "America West Airlines (HP - Merged with US 2005 / AA 2013)",
    "QQ": "Reno Air (QQ - Acquired by AA 1999)",
    "TW": "Trans World Airlines (TW - Acquired by AA 2001)",
    "FL": "AirTran Airways (FL - Acquired by WN 2011)",
    "VX": "Virgin America (VX - Acquired by AS 2016)",
    "YX": "Midwest Airlines (YX - Acquired by F9 2009)",
    "PA": "Pan American World Airways (PA - Acquired by DL 1991)",
}

col_f1, col_f2, col_f3 = st.columns([2.2, 1.2, 2.6])

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
        options=[2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2015, 2010, 2005, 2000],
        index=0,
        label_visibility="collapsed"
    )

# Alliance & Branding Lookup
carrier_logo = get_carrier_logo_url(selected_code)
alliance_info = get_carrier_alliance(selected_code, selected_year)

with col_f3:
    carrier_strat = CARRIER_STRATEGY.get(selected_code, {})
    hubs_str = ", ".join(carrier_strat.get("hubs", []))
    
    alliance_badge = ""
    if alliance_info:
        a_name = alliance_info["alliance_name"]
        a_logo = alliance_info.get("alliance_logo_url", "")
        alliance_badge = f"<span style='background: rgba(10, 132, 255, 0.18); border: 1px solid #0A84FF; color: #64D2FF; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 11px; margin-left: 8px;'>🌐 {a_name}</span>"
    else:
        alliance_badge = "<span style='background: rgba(255, 255, 255, 0.08); color: #8E8E93; padding: 2px 8px; border-radius: 6px; font-size: 11px; margin-left: 8px;'>Independent / Unaligned</span>"
    
    logo_html = f"<img src='{carrier_logo}' style='height: 22px; max-width: 80px; object-fit: contain; vertical-align: middle; margin-right: 8px; filter: brightness(1.1);'/>" if carrier_logo else ""
    
    st.markdown(
        f"<div style='display: flex; align-items: center; margin-top: 4px;'>"
        f"{logo_html}"
        f"<span style='font-size: 13px; font-weight: 600; color: #F5F5F7;'>{carriers_dict.get(selected_code, selected_code)}</span>"
        f"{alliance_badge}"
        f"</div>"
        f"<div style='color: #8E8E93; font-size: 11px; margin-top: 4px;'><b>Primary Hubs:</b> {hubs_str if hubs_str else 'N/A'}</div>",
        unsafe_allow_html=True
    )

# Corporate Merger Lineage Banner
lineage_banner = format_merger_lineage_html(selected_code)
if lineage_banner:
    st.markdown(lineage_banner, unsafe_allow_html=True)

# Historical Alliance & Corporate Transition Timeline expander
timeline = get_carrier_alliance_timeline(selected_code)
pred_merger = get_merger_as_predecessor(selected_code)
absorbed_mergers = get_mergers_as_successor(selected_code)

if timeline or pred_merger or absorbed_mergers:
    with st.expander(f"📜 {carriers_dict.get(selected_code, selected_code)}: Corporate Lineage, Mergers & Alliances", expanded=False):
        # Section 1: Mergers & Acquisitions
        if pred_merger:
            st.markdown(f"#### 🤝 Corporate Acquisition & Integration")
            st.markdown(
                f"- **Acquiring Carrier**: **{pred_merger['successor_name']} ({pred_merger['successor_code']})**\n"
                f"- **Announcement Date**: `{pred_merger['announced_date']}` | **Closing Date**: `{pred_merger['closing_date']}`\n"
                f"- **Single Operating Certificate (SOC)**: `{pred_merger['soc_date']}` | **Final Flight**: `{pred_merger['final_flight_date']}`\n"
                f"- **Hubs Absorbed**: `{', '.join(pred_merger['hubs_absorbed'])}`\n"
                f"- **Fleet Inherited**: {', '.join(pred_merger['fleet_types_inherited'])}\n"
                f"- **Transaction Summary**: {pred_merger['summary']}\n"
                f"- [Official Regulatory & Press Citation ↗]({pred_merger['source_url']})"
            )
            st.markdown("---")
        elif absorbed_mergers:
            st.markdown(f"#### 🏛️ Historical Predecessor Airlines Absorbed")
            for am in absorbed_mergers:
                st.markdown(
                    f"##### <img src='{am['predecessor_logo']}' style='height: 18px; vertical-align: middle; margin-right: 6px;'/> {am['predecessor_name']} ({am['predecessor_code']}) — Merged in {am.get('cutover_year', '')}\n"
                    f"- **Closing / Single Certificate**: `{am['closing_date']}` (SOC: `{am['soc_date']}`, Final Flight: `{am['final_flight_date']}`)\n"
                    f"- **Hubs Added**: `{', '.join(am['hubs_absorbed'])}`\n"
                    f"- **Fleet Added**: {', '.join(am['fleet_types_inherited'])}\n"
                    f"- **Summary**: {am['summary']} [Source Citation ↗]({am['source_url']})",
                    unsafe_allow_html=True
                )
            st.markdown("---")

        # Section 2: Global Alliance Membership History
        if timeline:
            st.markdown("#### 🌐 Global Alliance Timeline")
            for t in timeline:
                join = t.get("join_date", "Unknown")
                exit_d = t.get("exit_date") or "Present"
                status_emoji = "🟢" if exit_d == "Present" else "⚪"
                st.markdown(
                    f"- **{status_emoji} {t['alliance_name']}** ({join} ➔ {exit_d}): "
                    f"{t.get('transition_notes', '')} "
                    f"[Source Citation ↗]({t.get('source_url', '#')})"
                )

# -------------------------------------------------------------
# 2. Top KPI Cards
# -------------------------------------------------------------
kpis = get_airline_kpis(selected_code, selected_year)

k1, k2, k3, k4, k5 = st.columns(5)

tot_deps = kpis.get('total_departures') or 0
with k1:
    render_kpi_card("Active Routes", f"{kpis.get('active_routes', 0):,}")

with k2:
    deps_val = f"{tot_deps/1e3:.1f}K" if tot_deps >= 1000 else f"{tot_deps:,}"
    render_kpi_card("Total Departures", deps_val)

with k3:
    lf_str = f"{kpis['system_load_factor']:.1f}%" if kpis.get('system_load_factor') and not pd.isna(kpis['system_load_factor']) else "—"
    render_kpi_card("System Load Factor", lf_str)

with k4:
    yield_str = f"${kpis['avg_yield_per_mile']:.4f}" if kpis.get('avg_yield_per_mile') and not pd.isna(kpis['avg_yield_per_mile']) else "—"
    render_kpi_card("Yield / Passenger-Mile", yield_str)

with k5:
    fare_str = f"${kpis['avg_network_fare']:.0f}" if kpis.get('avg_network_fare') and not pd.isna(kpis['avg_network_fare']) else "—"
    render_kpi_card("Avg Network Fare", fare_str)

# -------------------------------------------------------------
# 3. Hero Section: Nationwide Route Network Atlas (1990s In-Flight Cartography)
# -------------------------------------------------------------
df_carrier_routes = get_airline_routes_dataset(selected_code, selected_year, min_departures=10)

if not df_carrier_routes.empty:
    st.markdown("### 🌐 Nationwide Route Network Atlas (1990s In-Flight Cartography)")
    
    col_am1, col_am2, col_am3 = st.columns([1.3, 1.2, 1.1])
    with col_am1:
        air_theme_label = st.selectbox(
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
            key="air_map_theme",
            label_visibility="collapsed"
        )
        if "Personal" in air_theme_label:
            air_theme = "personal"
        elif "Love" in air_theme_label:
            air_theme = "love"
        elif "Mono" in air_theme_label:
            air_theme = "mono"
        elif "Midnight" in air_theme_label:
            air_theme = "midnight"
        elif "Paper" in air_theme_label:
            air_theme = "paper"
        else:
            air_theme = "slate"
        
    with col_am2:
        air_color_label = st.selectbox(
            "Linework Color",
            options=["✈️ Carrier Signature Color", "🔷 Classic Cobalt", "🔴 Vintage Crimson", "🔶 Amber Gold", "🟢 Emerald Green"],
            index=0,
            key="air_map_color",
            label_visibility="collapsed"
        )
        if "Carrier" in air_color_label:
            air_color = "auto"
        elif "Cobalt" in air_color_label:
            air_color = "cobalt"
        elif "Crimson" in air_color_label:
            air_color = "crimson"
        elif "Gold" in air_color_label:
            air_color = "gold"
        else:
            air_color = "emerald"

    with col_am3:
        air_label_opt = st.selectbox(
            "Airport Labels",
            options=["🏛️ Hubs Only", "🌐 Hubs + Top Spokes", "⚪ Dots Only"],
            index=0,
            key="air_map_labels",
            label_visibility="collapsed"
        )
        air_label_density = "hubs_only" if "Hubs Only" in air_label_opt else ("all" if "Top Spokes" in air_label_opt else "none")

    deck_air = build_airline_network_deck(
        df_carrier_routes,
        hub_codes=carrier_strat.get("hubs", []),
        carrier_code=selected_code,
        carrier_name=carriers_dict[selected_code],
        theme=air_theme,
        colorway=air_color,
        label_density=air_label_density
    )
    st.pydeck_chart(deck_air, width="stretch")

# -------------------------------------------------------------
# 4. Hub Operations & Yield Curve Charts
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
        st.plotly_chart(fig_hubs, width="stretch", config={"displayModeBar": False})
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
        st.plotly_chart(fig_yield, width="stretch", config={"displayModeBar": False})
    else:
        st.info("No yield curve data available.")

# -------------------------------------------------------------
# 5. Target Network Expansion Proposals: Top 5 Next Routes by Hub
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
                st.dataframe(display_h, width="stretch", hide_index=True)
            else:
                st.info(f"No major unserved route opportunities found matching criteria for hub {hub}.")
else:
    st.info("No hub expansion proposals available for this carrier selection.")

# -------------------------------------------------------------
# 6. Master Reference Catalog: US Commercial Airline Mergers (1990 - Present)
# -------------------------------------------------------------
with st.expander("📚 Master Catalog: US Commercial Airline Mergers & Acquisitions (1990 – Present)", expanded=False):
    all_mergers = get_all_airline_mergers()
    mergers_table_data = []
    for m in all_mergers:
        mergers_table_data.append({
            "Predecessor": f"{m['predecessor_name']} ({m['predecessor_code']})",
            "Successor": f"{m['successor_name']} ({m['successor_code']})",
            "Announced": m["announced_date"],
            "Closing / Cutover": f"{m['closing_date']} (Cutover: {m['cutover_year']})",
            "Hubs Absorbed": ", ".join(m["hubs_absorbed"]),
            "Fleets Inherited": ", ".join(m["fleet_types_inherited"][:2]) + ("..." if len(m["fleet_types_inherited"]) > 2 else ""),
            "Key Rationale / Summary": m["summary"]
        })
    df_all_mergers = pd.DataFrame(mergers_table_data)
    st.dataframe(df_all_mergers, width="stretch", hide_index=True)

