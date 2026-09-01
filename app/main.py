import streamlit as st
from app.config import settings

st.set_page_config(
    page_title=settings.app_title,
    page_icon=settings.page_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    st.title(f"{settings.page_icon} {settings.app_title}")
    st.markdown("""
    Welcome to **AvDB**, an interactive aviation intelligence platform powered by **Google BigQuery**, **BTS T-100**, and **DB1B (10% Ticket Survey)**.

    ---

    ### 🧭 Analytical Lenses
    Explore the industry from three distinct dimensions:
    * ✈️ **[Airports](Airports)**: Route network expansion/drops, carrier market shares, O&D fare yields, and passenger volume trends.
    * 🏢 **[Airlines](Airlines)**: Route density, hub vs. point-to-point networks, yield per RPM/ASM, and load factors.
    * 💺 **[Fleet & Routes](Fleet_Routes)**: Aircraft type utilization, gauge trends (seats per departure), and stage-length economics.

    ---
    
    ### ⚙️ Environment & Data Health
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("GCP Project", settings.gcp_project_id or "Not Configured (Check .env)")
    with col2:
        st.metric("Raw Dataset", settings.dataset_raw)
    with col3:
        st.metric("Analytics Marts", settings.dataset_analytics)

if __name__ == "__main__":
    main()

