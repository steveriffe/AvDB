import streamlit as st
from app.config import settings
from app.utils.styling import apply_apple_style, render_kpi_card
from app.utils.queries import run_query

st.set_page_config(
    page_title=settings.app_title,
    page_icon=settings.page_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_apple_style()

def main():
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
    lcol1, lcol2, lcol3 = st.columns(3)

    with lcol1:
        st.markdown("""
            <div class="metric-container" style="min-height: 180px;">
                <div style="font-size: 1.3rem; font-weight: 600; color: #F5F5F7; margin-bottom: 8px;">✈️ Airport Explorer</div>
                <div style="color: #8E8E93; font-size: 0.9rem; line-height: 1.5; margin-bottom: 14px;">
                    Explore direct destinations, carrier seat share, O&D fare yields, and interactive great-circle route maps.
                </div>
                <a href="/Airports" target="_self" style="color: #0A84FF; font-weight: 500; text-decoration: none; font-size: 0.92rem;">Open Airport Explorer →</a>
            </div>
        """, unsafe_allow_html=True)

    with lcol2:
        st.markdown("""
            <div class="metric-container" style="min-height: 180px;">
                <div style="font-size: 1.3rem; font-weight: 600; color: #F5F5F7; margin-bottom: 8px;">🏢 Airline Explorer</div>
                <div style="color: #8E8E93; font-size: 0.9rem; line-height: 1.5; margin-bottom: 14px;">
                    Inspect route networks, hub concentration, passenger market share, and revenue passenger mile (RPM) yields.
                </div>
                <a href="/Airlines" target="_self" style="color: #0A84FF; font-weight: 500; text-decoration: none; font-size: 0.92rem;">Open Airline Explorer →</a>
            </div>
        """, unsafe_allow_html=True)

    with lcol3:
        st.markdown("""
            <div class="metric-container" style="min-height: 180px;">
                <div style="font-size: 1.3rem; font-weight: 600; color: #F5F5F7; margin-bottom: 8px;">💺 Fleet & Routes</div>
                <div style="color: #8E8E93; font-size: 0.9rem; line-height: 1.5; margin-bottom: 14px;">
                    Analyze aircraft type allocation, up-gauging / down-gauging trends, and stage-length economics.
                </div>
                <a href="/Fleet_Routes" target="_self" style="color: #0A84FF; font-weight: 500; text-decoration: none; font-size: 0.92rem;">Open Fleet Analytics →</a>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
