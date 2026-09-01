import streamlit as st
from app.config import settings

st.set_page_config(page_title="Fleet & Routes | AvDB", page_icon="💺", layout="wide")

st.title("💺 Fleet Deployment & Aircraft Routing")
st.markdown("Explore aircraft type allocation, gauge trends (seats per departure), and stage length matching.")

with st.sidebar:
    st.header("Filters")
    selected_family = st.selectbox("Aircraft Family / Category", ["All Mainline & Regional", "Airbus A320 Family (A319/A320/A321)", "Airbus A220", "Boeing 737 Family (737-700/800/900/MAX)", "Boeing 777/787 Widebody", "Embraer E-Jets (E175/E190)", "Bombardier CRJ Series"])
    selected_year = st.slider("Analysis Year", min_value=2018, max_value=2024, value=2023)

st.info(f"Viewing fleet utilization and route dynamics for **{selected_family}** in **{selected_year}**.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Operating Airframes", "—")
col2.metric("Avg Seats / Departure (Gauge)", "—")
col3.metric("Avg Stage Length (miles)", "—")
col4.metric("Annual Flight Hours / Deps", "—")

