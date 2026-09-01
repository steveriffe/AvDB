import streamlit as st
from app.config import settings

st.set_page_config(page_title="Airports Explorer | AvDB", page_icon="✈️", layout="wide")

st.title("✈️ Airport Network & Route Explorer")
st.markdown("Analyze route connectivity, carrier seat share, O&D passenger volume, and route additions/terminations.")

# Sidebar Filters
with st.sidebar:
    st.header("Filters")
    selected_airport = st.selectbox("Select Airport (IATA)", ["ORD", "ATL", "DFW", "DEN", "LAX", "JFK", "SFO", "SEA", "BOS", "MCO"])
    selected_year = st.slider("Analysis Year", min_value=2018, max_value=2024, value=2023)

st.info(f"Viewing analytics for **{selected_airport}** in **{selected_year}** (Connected to BigQuery dataset `{settings.dataset_analytics}`).")

# Placeholder Metric Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Direct Destinations", "—")
col2.metric("Total Annual Passengers", "—")
col3.metric("Avg O&D One-Way Fare", "—")
col4.metric("Leading Carrier Share", "—")

