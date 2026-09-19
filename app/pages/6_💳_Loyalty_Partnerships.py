import sys
from pathlib import Path

# Automatically add project root to Python path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import streamlit as st
import pandas as pd

from app.utils.styling import (
    apply_apple_style,
    render_kpi_card,
    render_portal_nav_link,
    render_html,
    fmt_integer,
)
from app.utils.auth import require_auth
from app.data.ref_logos_svg import get_vector_logo_data_uri
from app.data.ref_ffp_partnerships import (
    PROGRAMS,
    CARRIER_TO_PROGRAM,
    BILATERAL_PARTNERSHIPS,
    CURATED_CASE_STUDIES,
    get_all_programs,
    get_program_by_id,
    get_program_by_carrier,
    get_tiers_for_program,
    get_partnerships_for_year,
    get_partnerships_for_carrier,
    get_curated_case_studies,
)

st.set_page_config(
    page_title="Loyalty & Bilateral Partnerships | AvDB",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_apple_style()
render_portal_nav_link()
require_auth()

# -------------------------------------------------------------
# 1. Header & Title Section
# -------------------------------------------------------------
st.title("💳 Frequent Flyer Programs & Bilateral Partnerships (1980–2026)")
st.markdown(
    "<p style='color: #94A3B8; font-size: 1.05rem; margin-top: -10px; margin-bottom: 24px; font-family: \"Inter\", sans-serif;'>"
    "Explore 46 years of US airline loyalty architecture: elite tier hierarchies, qualification criteria, upgrade windows, "
    "reciprocal club access, and the intricate, shifting web of bilateral alliance partnerships across deregulation history."
    "</p>",
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# 2. Interactive Control Bar: Carrier / Program & Timeline Year
# -------------------------------------------------------------
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2.5, 2.5, 1.2])

# Carrier options formatted with status indicators
carrier_options = [
    ("AS", "Alaska Airlines (AS) — Mileage Plan [Active]"),
    ("AA", "American Airlines (AA) — AAdvantage [Active]"),
    ("DL", "Delta Air Lines (DL) — SkyMiles [Active]"),
    ("UA", "United Airlines (UA) — MileagePlus [Active]"),
    ("NW", "Northwest Airlines (NW) — WorldPerks [Historical 1986–2009]"),
    ("CO", "Continental Airlines (CO) — OnePass [Historical 1987–2012]"),
    ("US", "US Airways (US) — Dividend Miles [Historical 1988–2015]"),
    ("HP", "America West (HP) — FlightFund [Historical 1987–2006]"),
    ("TW", "TWA (TW) — Aviators / FFB [Historical 1979–2001]"),
    ("EA", "Eastern Air Lines (EA) — Ionosphere Club / OnePass [Historical 1981–1991]"),
    ("PA", "Pan Am (PA) — WorldPass [Historical 1982–1991]"),
]
carrier_map = {opt[1]: opt[0] for opt in carrier_options}

with ctrl_col1:
    selected_label = st.selectbox(
        "Select Airline & Loyalty Program",
        options=[opt[1] for opt in carrier_options],
        index=0,
        help="Choose a major US carrier to inspect its loyalty program, tier benefits, and partner network.",
    )
    selected_carrier = carrier_map[selected_label]
    program_data = get_program_by_carrier(selected_carrier)

with ctrl_col2:
    selected_year = st.slider(
        "Historical Analysis Year",
        min_value=1985,
        max_value=2026,
        value=2024 if program_data and program_data["is_active"] else (program_data["dissolved_year"] or 2000),
        step=1,
        help="Slide along the 1985–2026 timeline to observe active bilateral partnerships and program status for that specific year.",
    )

with ctrl_col3:
    network_scope = st.radio(
        "Partner Filter",
        options=["Selected Airline", "All US Carriers"],
        index=0,
        horizontal=False,
        help="View bilateral partnerships for the selected airline or view the entire industry web active in this year.",
    )

# -------------------------------------------------------------
# 3. Selected Program Profile Hero Card
# -------------------------------------------------------------
if program_data:
    p_name = program_data["program_name"]
    c_code = program_data["carrier_code"]
    c_name = program_data["carrier_name"]
    f_year = program_data["founded_year"]
    d_year = program_data["dissolved_year"]
    is_active = program_data["is_active"]
    curr_name = program_data["currency_name"]
    curr_type = program_data["currency_type"]
    lineage = program_data["lineage_summary"]
    successor = program_data.get("successor_program")

    # Status in selected year
    if selected_year < f_year:
        year_status = f"⏳ Not Yet Founded in {selected_year} (Founded {f_year})"
        status_color = "#94A3B8"
        status_bg = "rgba(148, 163, 184, 0.15)"
    elif d_year and selected_year > d_year:
        year_status = f"Consolidated into {successor} (Ended {d_year})"
        status_color = "#F59E0B"
        status_bg = "rgba(245, 158, 11, 0.15)"
    elif is_active:
        year_status = f"🟢 Active Operating Program in {selected_year}"
        status_color = "#30D158"
        status_bg = "rgba(48, 209, 88, 0.15)"
    else:
        year_status = f"🟢 Actively Operating in {selected_year} (Dissolved {d_year})"
        status_color = "#38BDF8"
        status_bg = "rgba(56, 189, 248, 0.15)"

    logo_uri = get_vector_logo_data_uri(c_code)

    hero_html = f"""
    <div style="background: rgba(17, 29, 51, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 22px 24px; margin-top: 12px; margin-bottom: 24px; backdrop-filter: blur(14px);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 18px;">
                <img src="{logo_uri}" style="height: 52px; width: 120px; object-fit: contain; border-radius: 8px;" alt="{c_name}"/>
                <div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.5rem; font-weight: 800; color: #FFFFFF;">
                            {c_name} <span style="color: #38BDF8;">{p_name}</span>
                        </span>
                        <span style="background: {status_bg}; color: {status_color}; border: 1px solid {status_color}; font-size: 0.75rem; font-weight: 700; padding: 3px 9px; border-radius: 20px; font-family: 'JetBrains Mono', monospace;">
                            {year_status}
                        </span>
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #94A3B8; margin-top: 4px;">
                        IATA: <span style="color: #FFFFFF; font-weight: 600;">{c_code}</span> · Currency: <span style="color: #F59E0B; font-weight: 600;">{curr_name}</span> · Operational Lifespan: <span style="color: #FFFFFF;">{f_year} – {'Present' if is_active else d_year}</span>
                    </div>
                </div>
            </div>
            <div style="text-align: right; background: rgba(11, 25, 44, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 10px; padding: 10px 16px;">
                <div style="font-size: 0.72rem; color: #94A3B8; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: 0.8px;">Loyalty Model</div>
                <div style="font-size: 0.88rem; font-weight: 700; color: #CBD5E1; font-family: 'Plus Jakarta Sans', sans-serif; margin-top: 2px;">
                    {curr_type}
                </div>
            </div>
        </div>
        <div style="margin-top: 16px; padding-top: 14px; border-top: 1px solid rgba(255, 255, 255, 0.06); font-family: 'Inter', sans-serif; font-size: 0.92rem; line-height: 1.6; color: #CBD5E1;">
            {lineage}
        </div>
    </div>
    """
    render_html(hero_html)

# -------------------------------------------------------------
# 4. KPI Metrics Strip for Selected Year
# -------------------------------------------------------------
carrier_filter = None if network_scope == "All US Carriers" else selected_carrier
partners_in_year = get_partnerships_for_year(selected_year, carrier_code=carrier_filter)
tiers = get_tiers_for_program(program_data["program_id"]) if program_data else []

# Metrics computation
num_partners = len(partners_in_year)
num_tiers = len(tiers)
reciprocal_elites = sum(1 for p in partners_in_year if p["elite_reciprocity"])
reciprocal_lounges = sum(1 for p in partners_in_year if p["lounge_reciprocity"])

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    render_kpi_card("Active Bilateral Partners", str(num_partners), subtitle=f"Calendar year {selected_year}")
with k2:
    render_kpi_card("Program Status", "Active" if (program_data and (program_data["founded_year"] <= selected_year and (program_data["dissolved_year"] is None or selected_year <= program_data["dissolved_year"]))) else "Inactive", subtitle=f"Year {selected_year} standing")
with k3:
    render_kpi_card("Status Tiers", str(num_tiers), subtitle=f"{program_data['program_name'] if program_data else ''} levels")
with k4:
    render_kpi_card("Elite Reciprocity Ties", str(reciprocal_elites), subtitle=f"Upgrades & priority in {selected_year}")
with k5:
    render_kpi_card("Reciprocal Lounge Ties", str(reciprocal_lounges), subtitle=f"Club access agreements in {selected_year}")

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 5. Status Tier Hierarchy & Qualification Requirements
# -------------------------------------------------------------
if tiers:
    st.markdown(f"### 🏆 {c_name} {p_name} Status Tier Hierarchy & Perks")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.9rem; margin-top: -8px; margin-bottom: 16px;'>"
        "Detailed qualification thresholds, domestic upgrade clearance prioritization windows, "
        "bonus mile multipliers, and premium reciprocal privileges."
        "</p>",
        unsafe_allow_html=True,
    )

    tier_cards_html = []
    level_colors = {
        1: ("#94A3B8", "rgba(148, 163, 184, 0.12)", "Silver / Base Elite"),
        2: ("#F59E0B", "rgba(245, 158, 11, 0.12)", "Gold / Mid Elite"),
        3: ("#38BDF8", "rgba(56, 189, 248, 0.12)", "Platinum / High Elite"),
        4: ("#A855F7", "rgba(168, 85, 247, 0.12)", "Executive / Top Elite"),
        5: ("#10B981", "rgba(16, 185, 129, 0.12)", "VIP / Invitation Only"),
    }

    cols = st.columns(len(tiers))
    for idx, tier in enumerate(tiers):
        t_name = tier["tier_name"]
        t_level = tier["tier_level"]
        color, bg_color, level_desc = level_colors.get(t_level, ("#0A84FF", "rgba(10, 132, 255, 0.12)", "Elite Tier"))
        eqm = f"{tier['eqm_required']:,} EQM" if tier["eqm_required"] else "Invitation Only"
        eqs = f"{tier['eqs_required']} EQS" if tier["eqs_required"] else "N/A"
        spend = tier.get("spend_required") or "None (Distance-based qualification)"
        window = tier["upgrade_window"]
        bonus = f"+{tier['bonus_miles_pct']}%"
        bags = tier["baggage_allowance"]
        lounge = tier["lounge_access"]
        perks = tier["priority_services"]

        with cols[idx]:
            card_html = f"""
            <div style="background: rgba(17, 29, 51, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-top: 4px solid {color}; border-radius: 14px; padding: 18px; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.15rem; font-weight: 800; color: #FFFFFF; line-height: 1.2;">
                            {t_name}
                        </span>
                        <span style="background: {bg_color}; color: {color}; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; font-weight: 700; padding: 2px 7px; border-radius: 6px; border: 1px solid {color};">
                            L{t_level}
                        </span>
                    </div>
                    <div style="font-size: 0.75rem; color: {color}; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; margin-bottom: 12px;">
                        {level_desc}
                    </div>

                    <div style="background: rgba(11, 25, 44, 0.7); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 10px; margin-bottom: 12px; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;">
                        <div style="color: #94A3B8; font-size: 0.7rem;">QUALIFICATION:</div>
                        <div style="color: #FFFFFF; font-weight: 700; margin-top: 2px;">{eqm} <span style="color: #94A3B8; font-weight: 400;">or</span> {eqs}</div>
                        <div style="color: #38BDF8; font-size: 0.72rem; margin-top: 4px; border-top: 1px dashed rgba(255,255,255,0.08); padding-top: 4px;">{spend}</div>
                    </div>

                    <div style="font-size: 0.8rem; line-height: 1.5; color: #CBD5E1; margin-bottom: 10px;">
                        <div style="margin-bottom: 6px;">
                            <span style="color: #F59E0B; font-weight: 700;">⚡ Upgrade Window:</span><br/>
                            <span style="color: #FFFFFF; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;">{window}</span>
                        </div>
                        <div style="margin-bottom: 6px;">
                            <span style="color: #38BDF8; font-weight: 700;">🎁 Bonus Miles:</span>
                            <span style="color: #30D158; font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.85rem;">{bonus}</span>
                        </div>
                        <div style="margin-bottom: 6px;">
                            <span style="color: #CBD5E1; font-weight: 700;">🧳 Baggage:</span> {bags}
                        </div>
                        <div style="margin-bottom: 6px;">
                            <span style="color: #CBD5E1; font-weight: 700;">🍸 Lounge Access:</span> {lounge}
                        </div>
                    </div>
                </div>
                <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.06); font-size: 0.75rem; color: #94A3B8;">
                    <span style="color: #FFFFFF; font-weight: 600;">Priority Services:</span> {perks}
                </div>
            </div>
            """
            render_html(card_html)

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. Active Bilateral Partnerships Grid in Selected Year
# -------------------------------------------------------------
scope_title = (
    f"Active Bilateral Partnerships for {c_name} in {selected_year}"
    if network_scope == "Selected Airline"
    else f"All Active US Airline Bilateral Loyalty Partnerships in {selected_year}"
)
st.markdown(f"### 🤝 {scope_title}")

if not partners_in_year:
    st.info(
        f"No bilateral partnerships recorded for {c_name if network_scope == 'Selected Airline' else 'any airline'} "
        f"in calendar year {selected_year}. Slide the timeline or switch to 'All US Carriers' to explore other eras."
    )
else:
    st.markdown(
        f"<p style='color: #94A3B8; font-size: 0.9rem; margin-top: -8px; margin-bottom: 18px;'>"
        f"Displaying <b>{len(partners_in_year)} active bilateral agreements</b> in <b>{selected_year}</b>. "
        f"Notice how airlines maintained complex multi-partner ties prior to rigid multilateral global alliances."
        f"</p>",
        unsafe_allow_html=True,
    )

    p_cols = st.columns(2)
    for p_idx, p in enumerate(partners_in_year):
        col = p_cols[p_idx % 2]
        c1 = p["carrier_1"]
        c2 = p["carrier_2"]
        n1 = p["carrier_1_name"]
        n2 = p["carrier_2_name"]
        prog1 = p["program_1"]
        prog2 = p["program_2"]
        ptype = p["partnership_type"]
        s_yr = p["start_year"]
        e_yr = p["end_year"] or "Present"
        e_recip = p["elite_reciprocity"]
        l_recip = p["lounge_reciprocity"]
        details = p["reciprocity_details"]
        context = p["historical_context"]
        signif = p["significance"]
        tags = p.get("tags", [])

        # Logos
        logo1 = get_vector_logo_data_uri(c1)
        logo2 = get_vector_logo_data_uri(c2)

        # Depth color styling
        depth_color_map = {
            "Full Alliance / Joint Venture": ("#30D158", "rgba(48, 209, 88, 0.12)"),
            "Codeshare & Reciprocal Earn/Burn": ("#38BDF8", "rgba(56, 189, 248, 0.12)"),
            "Bilateral Reciprocal Earn/Burn": ("#F59E0B", "rgba(245, 158, 11, 0.12)"),
            "Redemption Only": ("#A855F7", "rgba(168, 85, 247, 0.12)"),
        }
        depth_color, depth_bg = depth_color_map.get(ptype, ("#0A84FF", "rgba(10, 132, 255, 0.12)"))

        elite_badge = (
            "<span style='background: rgba(48, 209, 88, 0.15); color: #30D158; border: 1px solid #30D158; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-family: \"JetBrains Mono\", monospace;'>✓ Reciprocal Elite Upgrades</span>"
            if e_recip
            else "<span style='background: rgba(148, 163, 184, 0.15); color: #94A3B8; border: 1px solid #64748B; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-family: \"JetBrains Mono\", monospace;'>✗ No Elite Reciprocity</span>"
        )

        lounge_badge = (
            "<span style='background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid #38BDF8; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-family: \"JetBrains Mono\", monospace;'>✓ Reciprocal Lounge Access</span>"
            if l_recip
            else "<span style='background: rgba(148, 163, 184, 0.15); color: #94A3B8; border: 1px solid #64748B; padding: 2px 8px; border-radius: 6px; font-size: 0.72rem; font-family: \"JetBrains Mono\", monospace;'>✗ No Lounge Reciprocity</span>"
        )

        tag_pills = "".join(
            f"<span style='background: rgba(255, 255, 255, 0.05); color: #CBD5E1; border: 1px solid rgba(255, 255, 255, 0.1); padding: 1px 7px; border-radius: 4px; font-size: 0.68rem; font-family: \"JetBrains Mono\", monospace; margin-right: 5px;'>#{tag}</span>"
            for tag in tags
        )

        with col:
            partner_card = f"""
            <div style="background: rgba(17, 29, 51, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 20px; margin-bottom: 20px; backdrop-filter: blur(12px);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.06); padding-bottom: 12px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <img src="{logo1}" style="height: 32px; width: 68px; object-fit: contain; border-radius: 4px;" alt="{c1}"/>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 700; color: #F59E0B;">⟷</span>
                        <img src="{logo2}" style="height: 32px; width: 68px; object-fit: contain; border-radius: 4px;" alt="{c2}"/>
                        <div>
                            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.05rem; font-weight: 800; color: #FFFFFF;">
                                {n1} & {n2}
                            </div>
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94A3B8;">
                                {prog1} · {prog2}
                            </div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: {depth_bg}; color: {depth_color}; border: 1px solid {depth_color}; padding: 3px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700; font-family: 'JetBrains Mono', monospace;">
                            {ptype}
                        </span>
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">
                            Active: <span style="color: #FFFFFF; font-weight: 600;">{s_yr} – {e_yr}</span>
                        </div>
                    </div>
                </div>

                <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
                    {elite_badge}
                    {lounge_badge}
                </div>

                <div style="background: rgba(11, 25, 44, 0.6); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 10px 12px; margin-bottom: 12px; font-size: 0.82rem; line-height: 1.5; color: #E2E8F0;">
                    <b style="color: #38BDF8;">Reciprocity Terms:</b> {details}
                </div>

                <div style="font-size: 0.84rem; line-height: 1.55; color: #94A3B8; margin-bottom: 12px;">
                    {context}
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255, 255, 255, 0.06); padding-top: 10px;">
                    <div style="font-size: 0.75rem; color: #CBD5E1; font-family: 'Inter', sans-serif;">
                        <b style="color: #F59E0B;">Significance:</b> {signif}
                    </div>
                </div>
                <div style="margin-top: 8px;">
                    {tag_pills}
                </div>
            </div>
            """
            render_html(partner_card)

# -------------------------------------------------------------
# 7. Curated Deep-Dives: Historical Alliances & Rivalries
# -------------------------------------------------------------
st.markdown("---")
st.markdown("### 🏛️ Historical Loyalty Alliances & Rivalries: Curated Deep Dives")
st.markdown(
    "<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -8px; margin-bottom: 20px;'>"
    "Behind the scenes of deregulation: how airline executives forged and severed loyalty treaties, "
    "traded equity stakes, and used frequent flyer points as strategic weapons."
    "</p>",
    unsafe_allow_html=True,
)

case_studies = get_curated_case_studies()
for cs in case_studies:
    cs_id = cs["case_id"]
    cs_title = cs["title"]
    cs_sub = cs["subtitle"]
    cs_icon = cs["icon"]
    cs_carrier = cs["primary_carrier"]
    cs_narrative = cs["narrative"]
    cs_takeaways = cs["key_takeaways"]

    with st.expander(f"{cs_icon} {cs_title}", expanded=False):
        st.markdown(
            f"<p style='color: #38BDF8; font-size: 0.92rem; font-weight: 600; margin-bottom: 14px; font-family: \"Plus Jakarta Sans\", sans-serif;'>"
            f"{cs_sub}"
            f"</p>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<div style='font-size: 0.92rem; line-height: 1.65; color: #CBD5E1; margin-bottom: 18px; font-family: \"Inter\", sans-serif;'>"
            f"{cs_narrative.replace(chr(10) + chr(10), '<br/><br/>')}"
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='background: rgba(11, 25, 44, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 14px 18px;'>"
            "<div style='font-size: 0.78rem; font-weight: 700; color: #F59E0B; font-family: \"JetBrains Mono\", monospace; text-transform: uppercase; margin-bottom: 8px;'>Strategic Takeaways</div>"
            + "".join(
                f"<div style='font-size: 0.85rem; color: #E2E8F0; margin-bottom: 6px; line-height: 1.5;'>• {takeaway}</div>"
                for takeaway in cs_takeaways
            )
            + "</div>",
            unsafe_allow_html=True,
        )
