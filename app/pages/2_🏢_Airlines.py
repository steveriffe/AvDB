import sys
from pathlib import Path

# Automatically add project root to Python path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import streamlit as st
from app.config import settings

st.set_page_config(page_title="Airlines Explorer | AvDB", page_icon="🏢", layout="wide")

st.title("🏢 Airline Network & Yield Explorer")
st.markdown("Inspect route networks, hub concentration, fare distributions, and RPM/ASM yields.")

with st.sidebar:
    st.header("Filters")
    selected_carrier = st.selectbox("Select Airline", ["Delta Air Lines (DL)", "American Airlines (AA)", "United Airlines (UA)", "Southwest Airlines (WN)", "Alaska Airlines (AS)", "JetBlue (B6)"])
    selected_year = st.slider("Analysis Year", min_value=2018, max_value=2024, value=2023)

st.info(f"Viewing analytics for **{selected_carrier}** in **{selected_year}**.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Routes", "—")
col2.metric("System Load Factor", "—")
col3.metric("Avg Passenger Yield ($/mile)", "—")
col4.metric("Total Departures", "—")

