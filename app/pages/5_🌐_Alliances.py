import sys
from pathlib import Path

# Automatically add project root to Python path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app.config import settings
from app.utils.styling import apply_apple_style, render_kpi_card, render_portal_nav_link
from app.utils.auth import require_auth
from app.utils.queries import (
    get_alliance_performance_metrics,
    get_alliance_fleet_deployment,
    get_alliances_time_series,
)
from app.utils.visualizers import build_alliance_market_share_trend_chart
from app.utils.alliances import (
    ALLIANCE_COLORS,
    get_vector_logo_data_uri,
    get_carrier_logo_url,
    get_carrier_name,
    get_alliance_carriers,
)

st.set_page_config(
    page_title="Airline Alliances | AvDB",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_apple_style()
render_portal_nav_link()
require_auth()

# -------------------------------------------------------------
# 1. Header & Data Scope Caveats
# -------------------------------------------------------------
st.title("🌐 Global Airline Alliances & Joint Ventures")
st.markdown(
    "<p style='color: #8E8E93; font-size: 1.05rem; margin-top: -12px; margin-bottom: 20px;'>"
    "Comparative intelligence across global multilateral alliances (<b>Star Alliance</b>, <b>SkyTeam</b>, <b>oneworld</b>) "
    "and pioneering transatlantic joint ventures (<b>Northwest / KLM Wings Alliance</b>, <b>Qualiflyer</b>)."
    "</p>",
    unsafe_allow_html=True,
)

# Prominent US Data Boundary Alert
st.html(
    "<div style='background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px; padding: 14px 18px; margin-bottom: 24px;'>"
    "<div style='display: flex; align-items: center; gap: 8px; font-weight: 700; color: #38BDF8; font-size: 0.92rem; margin-bottom: 4px;'>"
    "<span>ℹ️</span> US-Origin & Gateway Data Boundary Notice"
    "</div>"
    "<div style='color: #CBD5E1; font-size: 0.85rem; line-height: 1.5;'>"
    "All metrics are computed from U.S. Department of Transportation BTS T-100 operations and DB1B/OD40 ticket surveys. "
    "Data reflects <b>100% of US domestic sectors</b> and <b>all international flights touching US gateways</b> (e.g. British Airways LHR➔JFK, Lufthansa FRA➔ORD, ANA HND➔LAX). "
    "Foreign-to-foreign intra-continental sectors (e.g. Lufthansa domestic Germany, Air France intra-Europe) are not reported to the US DOT and therefore not included."
    "</div>"
    "</div>"
)

# -------------------------------------------------------------
# 2. Control Bar: Year Selection
# -------------------------------------------------------------
col_ctrl1, col_ctrl2 = st.columns([1.5, 3.5])
with col_ctrl1:
    selected_year = st.selectbox(
        "Analysis Year",
        options=list(range(2025, 1989, -1)),
        index=0,
        help="Select calendar year for temporal alliance membership attribution."
    )

# Fetch Aggregated Data
with st.spinner(f"Aggregating alliance intelligence for {selected_year}..."):
    df_perf = get_alliance_performance_metrics(selected_year)
    df_fleet = get_alliance_fleet_deployment(selected_year)

if df_perf.empty:
    st.warning(f"No operational data available for year {selected_year}.")
    st.stop()

# -------------------------------------------------------------
# 3. Top-Level Platform KPIs
# -------------------------------------------------------------
total_pax = df_perf["passengers"].sum()
total_deps = df_perf["departures"].sum()
weighted_load_factor = (df_perf["passengers"].sum() / max(df_perf["total_seats"].sum(), 1)) * 100
total_est_revenue = df_perf["estimated_revenue"].sum()

# Leading alliance
lead_alliance = df_perf.iloc[0]["alliance_name"]
lead_pax_share = df_perf.iloc[0]["passenger_share_pct"]

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    render_kpi_card("Total US Passengers", f"{total_pax/1e6:.1f}M", subtitle="Reported T-100 traffic")
with k2:
    render_kpi_card("Total Departures", f"{total_deps:,}", subtitle="Commercial departures")
with k3:
    render_kpi_card("Avg System Load Factor", f"{weighted_load_factor:.1f}%", subtitle="Pax / Seats")
with k4:
    rev_str = f"${total_est_revenue/1e9:.2f}B" if total_est_revenue > 0 else "N/A"
    render_kpi_card("Est. O&D Revenue", rev_str, subtitle="US-originating sample")
with k5:
    render_kpi_card("Market Leader", lead_alliance, subtitle=f"{lead_pax_share}% passenger share")

st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. Comparative Market Share & Efficiency Visualizers
# -------------------------------------------------------------
vcol1, vcol2 = st.columns([2.5, 3.5])

COLOR_MAP = {
    "Star Alliance": "#C5A059",
    "SkyTeam": "#0090DA",
    "oneworld": "#1A2C80",
    "Wings Alliance (NW / KL)": "#D62828",
    "Qualiflyer": "#D0021B",
    "Independent / Unaligned": "#64748B",
}

with vcol1:
    st.markdown("### 🍩 Passenger Volume by Alliance")
    fig_donut = px.pie(
        df_perf,
        values="passengers",
        names="alliance_name",
        color="alliance_name",
        color_discrete_map=COLOR_MAP,
        hole=0.55,
    )
    fig_donut.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Passengers: %{value:,.0f}<br>Share: %{percent:.1%}<extra></extra>",
    )
    fig_donut.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", family="Plus Jakarta Sans"),
        height=330,
    )
    st.plotly_chart(fig_donut, width="stretch")

with vcol2:
    st.markdown("### 📊 Load Factor & Capacity (ASM) Comparison")
    
    # Dual-metric comparison
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=df_perf["alliance_name"],
        y=df_perf["load_factor_pct"],
        name="Load Factor %",
        marker_color="#38BDF8",
        yaxis="y",
        hovertemplate="<b>%{x}</b><br>Load Factor: %{y:.1f}%<extra></extra>"
    ))
    fig_bar.add_trace(go.Scatter(
        x=df_perf["alliance_name"],
        y=df_perf["asm"] / 1e9,
        name="Available Seat Miles (Billion ASM)",
        marker=dict(color="#FF6B00", size=10),
        mode="lines+markers",
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Capacity: %{y:.2f}B ASM<extra></extra>"
    ))
    fig_bar.update_layout(
        yaxis=dict(title="Load Factor %", range=[50, 100], color="#94A3B8"),
        yaxis2=dict(title="Billion ASM", overlaying="y", side="right", color="#FF6B00"),
        legend=dict(orientation="h", y=1.12, x=0.2),
        margin=dict(t=30, b=30, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", family="Plus Jakarta Sans"),
        height=330,
    )
    st.plotly_chart(fig_bar, width="stretch")

# -------------------------------------------------------------
# 5. Multi-Year Historical Trend: 1990–2025 Alliance Evolution
# -------------------------------------------------------------
with st.expander("📈 Alliance Market Share Evolution (1990–2025)", expanded=False):
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.9rem; margin-bottom: 12px;'>"
        "Tracking 36 years of global consolidation and joint-venture formation touching US international gateways: "
        "from the 1989 Northwest/KLM transatlantic joint venture (Wings), through the founding of Star Alliance (1997), "
        "oneworld (1999), and SkyTeam (2000), up to current multilateral immunity partnerships."
        "</p>",
        unsafe_allow_html=True,
    )
    with st.spinner("Generating 36-year alliance market trajectory..."):
        df_alliance_ts = get_alliances_time_series()
    if not df_alliance_ts.empty:
        fig_ts = build_alliance_market_share_trend_chart(df_alliance_ts)
        st.plotly_chart(fig_ts, width="stretch")
    else:
        st.info("Time-series alliance intelligence currently calculating.")

# -------------------------------------------------------------
# 6. Alliance Deep-Dive Profiles
# -------------------------------------------------------------
st.markdown("---")
st.markdown("### 🏛️ Alliance Profiles & Member Carriers")

for _, a_row in df_perf.iterrows():
    a_name = a_row["alliance_name"]
    clean_name = a_name.split(" (")[0]
    a_logo = get_vector_logo_data_uri(clean_name) if clean_name in ("Star Alliance", "SkyTeam", "oneworld", "Wings Alliance") else None
    logo_img = f"<img src='{a_logo}' style='height: 32px; max-width: 90px; object-fit: contain; margin-right: 14px;' alt='{a_name}'/>" if a_logo else ""

    # Build member carrier pills ranked by volume
    carrier_details = a_row.get("carrier_details", [])
    pills_html = []
    
    if carrier_details:
        top_carriers = carrier_details[:12]
        for item in top_carriers:
            c_code = item["code"]
            pax = item["passengers"]
            pax_str = f"{pax/1e6:.1f}M" if pax >= 1e6 else f"{pax/1e3:.0f}K"
            c_name = get_carrier_name(c_code)
            c_logo = get_carrier_logo_url(c_code) or ""
            logo_tag = f"<img src='{c_logo}' style='height: 22px; width: 22px; object-fit: contain; border-radius: 4px; flex-shrink: 0;' alt='{c_code}'/>" if c_logo else ""
            pills_html.append(
                f"<div style='display: inline-flex; align-items: center; gap: 8px; background: rgba(11, 25, 44, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 6px 12px; margin: 3px 6px 3px 0;' title='{c_name} ({c_code}): {pax_str} US BTS Passengers'>"
                f"{logo_tag}"
                f"<div>"
                f"<div style='font-family: \"Plus Jakarta Sans\", sans-serif; font-size: 11px; font-weight: 700; color: #FFFFFF; line-height: 1.2;'>{c_name}</div>"
                f"<div style='font-family: \"JetBrains Mono\", monospace; font-size: 10px; color: #94A3B8;'>{c_code} · <span style='color: #38BDF8; font-weight: 600;'>{pax_str} Pax</span></div>"
                f"</div>"
                f"</div>"
            )
    else:
        for c_code in a_row["carriers"][:12]:
            c_name = get_carrier_name(c_code)
            c_logo = get_carrier_logo_url(c_code) or ""
            logo_tag = f"<img src='{c_logo}' style='height: 22px; width: 22px; object-fit: contain; border-radius: 4px; flex-shrink: 0;' alt='{c_code}'/>" if c_logo else ""
            pills_html.append(
                f"<div style='display: inline-flex; align-items: center; gap: 8px; background: rgba(11, 25, 44, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 6px 12px; margin: 3px 6px 3px 0;' title='{c_name} ({c_code})'>"
                f"{logo_tag}"
                f"<div>"
                f"<div style='font-family: \"Plus Jakarta Sans\", sans-serif; font-size: 11px; font-weight: 700; color: #FFFFFF; line-height: 1.2;'>{c_name}</div>"
                f"<div style='font-family: \"JetBrains Mono\", monospace; font-size: 10px; color: #94A3B8;'>{c_code}</div>"
                f"</div>"
                f"</div>"
            )

    members_block = f"<div style='margin-top: 14px; border-top: 1px solid rgba(255, 255, 255, 0.06); padding-top: 12px;'><div style='font-size: 11px; font-weight: 700; color: #94A3B8; font-family: \"JetBrains Mono\", monospace; margin-bottom: 8px;'>TOP MEMBER AIRLINES (BY ANNUAL US PASSENGER VOLUME):</div><div style='display: flex; flex-wrap: wrap;'>{''.join(pills_html)}</div></div>" if pills_html else ""

    profile_html = (
        f"<div style='background: rgba(17, 29, 51, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; margin-bottom: 20px; backdrop-filter: blur(12px);'>"
        f"<div style='display: flex; justify-content: space-between; align-items: center;'>"
        f"<div style='display: flex; align-items: center;'>"
        f"{logo_img}"
        f"<div>"
        f"<div style='font-family: \"Plus Jakarta Sans\", sans-serif; font-size: 1.35rem; font-weight: 800; color: #FFFFFF;'>"
        f"{a_name}"
        f"</div>"
        f"<div style='color: #94A3B8; font-size: 0.88rem; font-family: \"JetBrains Mono\", monospace; margin-top: 2px;'>"
        f"US Network Share: <span style='color: #FF6B00; font-weight: 700;'>{a_row['passenger_share_pct']}%</span> Pax · {a_row['seat_share_pct']}% Seats · {a_row['load_factor_pct']}% Avg LF"
        f"</div>"
        f"</div>"
        f"</div>"
        f"<div style='text-align: right;'>"
        f"<div style='font-family: \"JetBrains Mono\", monospace; font-size: 1.45rem; font-weight: 800; color: #38BDF8;'>"
        f"{a_row['passengers']/1e6:.1f}M Pax"
        f"</div>"
        f"<div style='font-size: 0.78rem; color: #94A3B8; font-family: \"JetBrains Mono\", monospace;'>{a_row['departures']:,} Departures</div>"
        f"</div>"
        f"</div>"
        f"{members_block}"
        f"</div>"
    )
    st.html(profile_html)

# -------------------------------------------------------------
# 7. Fleet Deployment Mix: Widebody vs Narrowbody by Alliance
# -------------------------------------------------------------
if not df_fleet.empty:
    st.markdown("---")
    st.markdown("### ✈️ Fleet Equipment Mix Deployment by Alliance")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.9rem; margin-top: -10px; margin-bottom: 16px;'>"
        "Distribution of widebody long-haul equipment vs narrowbody mainline and regional jets across alliance networks touching US gateways."
        "</p>",
        unsafe_allow_html=True
    )
    
    fig_fleet = px.bar(
        df_fleet,
        x="alliance_name",
        y="departures",
        color="aircraft_family",
        barmode="stack",
        color_discrete_sequence=["#2563EB", "#38BDF8", "#FF6B00", "#10B981", "#8B5CF6", "#64748B"],
    )
    fig_fleet.update_layout(
        xaxis=dict(title=""),
        yaxis=dict(title="Departures Performed", color="#94A3B8"),
        margin=dict(t=20, b=30, l=40, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", family="Plus Jakarta Sans"),
        height=360,
        legend=dict(orientation="h", y=1.15, x=0.1)
    )
    st.plotly_chart(fig_fleet, width="stretch")

