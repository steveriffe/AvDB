import sys
from pathlib import Path

# Automatically add project root to Python path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import streamlit as st
from app.config import settings
from app.utils.styling import apply_apple_style, render_kpi_card
from app.utils.auth import init_auth, is_authenticated, render_user_sidebar
from app.components.landing import render_landing_page, render_unauthorized_page

st.set_page_config(
    page_title=settings.app_title,
    page_icon=settings.page_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_apple_style()


def main():
    # 🔐 Authentication Guard
    if settings.google_client_id:
        user_info = init_auth()
        if not user_info:
            st.markdown("<style>[data-testid='stSidebarNav'], [data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)
            render_landing_page()
            return
        elif not is_authenticated():
            st.markdown("<style>[data-testid='stSidebarNav'], [data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)
            render_unauthorized_page(user_info)
            return
        else:
            render_user_sidebar()
    else:
        with st.sidebar:
            st.caption("ℹ️ Local Dev Mode (No GOOGLE_CLIENT_ID configured)")

    # -------------------------------------------------------------
    # Authenticated Main Dashboard View
    # -------------------------------------------------------------
    st.title(f"{settings.page_icon} {settings.app_title}")
    st.markdown("<p style='color: #8E8E93; font-size: 1.15rem; margin-top: -10px; margin-bottom: 24px;'>Enterprise aviation intelligence platform powered by Google BigQuery, BTS T-100 operations, and DB1B ticket yields.</p>", unsafe_allow_html=True)

    # Top Data Summary Cards
    st.markdown("### 📊 Platform Metrics & BigQuery Marts")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("T-100 Operations Mart", "2.52M Rows", "1990 – Present")
    with col2:
        render_kpi_card("DB1B OD40 Survey", "40.3M Rows", "2025 Standard")
    with col3:
        render_kpi_card("Global Airport DB", "50,409 Points", "Coordinates & Catchments")
    with col4:
        render_kpi_card("Fleet Analytics Mart", "4.04M Rows", "Widebody / Narrow / RJ")

    st.markdown("---")

    st.markdown("### 🧭 Analytical Lenses")
    lcol1, lcol2, lcol3, lcol4 = st.columns(4)

    with lcol1:
        st.markdown("""
            <div class="metric-container" style="min-height: 190px;">
                <div style="font-size: 1.25rem; font-weight: 600; color: #F5F5F7; margin-bottom: 8px;">✈️ Airport Explorer</div>
                <div style="color: #8E8E93; font-size: 0.88rem; line-height: 1.5; margin-bottom: 14px;">
                    Explore direct destinations, carrier seat share, O&D fare yields, and interactive great-circle route maps.
                </div>
                <a href="/Airports" target="_self" style="color: #0A84FF; font-weight: 500; text-decoration: none; font-size: 0.92rem;">Open Airport Explorer →</a>
            </div>
        """, unsafe_allow_html=True)

    with lcol2:
        st.markdown("""
            <div class="metric-container" style="min-height: 190px;">
                <div style="font-size: 1.25rem; font-weight: 600; color: #F5F5F7; margin-bottom: 8px;">🏢 Airline Explorer</div>
                <div style="color: #8E8E93; font-size: 0.88rem; line-height: 1.5; margin-bottom: 14px;">
                    Inspect route networks, hub concentration, passenger market share, and revenue passenger mile (RPM) yields.
                </div>
                <a href="/Airlines" target="_self" style="color: #0A84FF; font-weight: 500; text-decoration: none; font-size: 0.92rem;">Open Airline Explorer →</a>
            </div>
        """, unsafe_allow_html=True)

    with lcol3:
        st.markdown("""
            <div class="metric-container" style="min-height: 190px;">
                <div style="font-size: 1.25rem; font-weight: 600; color: #F5F5F7; margin-bottom: 8px;">💺 Fleet & Routes</div>
                <div style="color: #8E8E93; font-size: 0.88rem; line-height: 1.5; margin-bottom: 14px;">
                    Analyze aircraft type allocation, up-gauging / down-gauging trends, and stage-length economics.
                </div>
                <a href="/Fleet_Routes" target="_self" style="color: #0A84FF; font-weight: 500; text-decoration: none; font-size: 0.92rem;">Open Fleet Analytics →</a>
            </div>
        """, unsafe_allow_html=True)

    with lcol4:
        st.markdown("""
            <div class="metric-container" style="min-height: 190px;">
                <div style="font-size: 1.25rem; font-weight: 600; color: #F5F5F7; margin-bottom: 8px;">📱 Personal Traveler</div>
                <div style="color: #8E8E93; font-size: 0.88rem; line-height: 1.5; margin-bottom: 14px;">
                    Upload Flighty travel logs, analyze granular subfleet variants (737-900ER vs MAX), and plot personal route maps.
                </div>
                <a href="/Flighty_Traveler" target="_self" style="color: #0A84FF; font-weight: 500; text-decoration: none; font-size: 0.92rem;">Open Personal Traveler →</a>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
