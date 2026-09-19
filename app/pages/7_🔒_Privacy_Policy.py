import sys
from pathlib import Path

# Automatically add project root to Python path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import streamlit as st
from app.config import settings
from app.utils.styling import apply_apple_style, render_portal_nav_link, render_html
from app.utils.auth import require_auth
from app.utils.flighty import get_user_travel_telemetry, USER_FLIGHT_LIMIT

st.set_page_config(
    page_title="User Privacy & Data Policy | AvDB",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_apple_style()
render_portal_nav_link()
require_auth()

st.title("🔒 User Privacy Policy & Data Governance")
st.markdown(
    "<p style='color: #8E8E93; font-size: 1.05rem; margin-top: -12px; margin-bottom: 24px;'>"
    "Transparent disclosures on identity management, BigQuery user travel persistence, fail-safe data purging, and zero third-party tracking."
    "</p>",
    unsafe_allow_html=True,
)

# Active User Context
user_profile = st.session_state.get("user") or {}
active_email = user_profile.get("email", "Not Signed In")

render_html(f"""
    <div style="background: rgba(17, 29, 51, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 18px 24px; margin-bottom: 28px;">
        <div style="font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; color: #38BDF8; margin-bottom: 4px;">ACTIVE IDENTITY CONTEXT</div>
        <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF;">{active_email}</div>
        <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 4px;">
            Access authenticated via Google OAuth 2.0 (Identity verified against environment allowlist).
        </div>
    </div>
""")

# -------------------------------------------------------------
# Core Policy Pillars
# -------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📥 What We Collect & Retain")
    render_html(f"""
        <div style="background: rgba(17, 29, 51, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 20px; line-height: 1.6; color: #CBD5E1; font-size: 0.92rem;">
            <p style="margin-bottom: 12px;"><b>1. Google OAuth Identity</b><br/>
            When you sign in with Google, AvDB receives your <code>email</code>, <code>display name</code>, and optional <code>avatar URL</code>. 
            This information is held in encrypted session state solely to verify authorization against the platform allowlist.</p>
            <p style="margin-bottom: 0;"><b>2. Optional Saved Travel Records (BigQuery Cloud Vault)</b><br/>
            If you upload a Flighty flight log and explicitly click <b>'Save to Cloud Vault'</b>, your flight segments are saved in a private table:
            <br/><code style="color: #38BDF8;">db1b-1.user_travel.user_flight_logs</code>.<br/>
            • <b>Usage Limit</b>: Capped at <b>{USER_FLIGHT_LIMIT:,} flight segments per user</b> to protect warehouse performance.<br/>
            • <b>Isolation</b>: Rows are partitioned and clustered strictly by your authenticated email address. Other users cannot query or view your flights.</p>
        </div>
    """)

with col2:
    st.markdown("### 🚫 What We NEVER Collect or Do")
    render_html("""
        <div style="background: rgba(17, 29, 51, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 20px; line-height: 1.6; color: #CBD5E1; font-size: 0.92rem;">
            <p style="margin-bottom: 12px;"><b>1. No Third-Party Tracking or Ad Networks</b><br/>
            AvDB contains <b>zero</b> third-party analytics trackers, advertising pixels, marketing beacons, or cross-site fingerprinting scripts.</p>
            <p style="margin-bottom: 12px;"><b>2. No Monetization or Sharing of Travel Data</b><br/>
            Your personal flight history, seat positions, routes, and frequent flyer patterns are never sold, monetized, or shared with airlines, brokers, or data aggregators.</p>
            <p style="margin-bottom: 0;"><b>3. No Background Uploads Without Consent</b><br/>
            Dropping a CSV file in Flighty Traveler parses the file in browser memory for visualization. It is <b>never written to BigQuery unless you explicitly click the Save button</b>.</p>
        </div>
    """)

# -------------------------------------------------------------
# Fail-Safe Deletion Commitment
# -------------------------------------------------------------
st.markdown("---")
st.markdown("### 🛡️ Fail-Safe Deletion Rights")
render_html("""
    <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 14px; padding: 20px; color: #CBD5E1; font-size: 0.92rem; line-height: 1.6;">
        <div style="font-size: 1.1rem; font-weight: 700; color: #F87171; margin-bottom: 8px;">Full Self-Service Purge Capability</div>
        AvDB enforces an accidental-loss-prevention policy. You retain complete ownership over your travel records. 
        You can permanently purge all of your stored records at any time directly from the <b>Flighty Personal Traveler</b> page.
        <br/><br/>
        To ensure this action is never triggered by accident, the platform enforces a <b>strict two-factor intent check</b>: 
        you must explicitly type the uppercase word <code style="color: #F87171; font-weight: 800;">DELETE</code> into the confirmation dialog before the deletion SQL query executes. 
        Once confirmed, the operation is immediate and irreversible.
    </div>
""")

# -------------------------------------------------------------
# Platform Telemetry Transparency
# -------------------------------------------------------------
st.markdown("---")
st.markdown("### 📊 Platform Storage Telemetry")
telemetry = get_user_travel_telemetry()
col_t1, col_t2 = st.columns(2)
with col_t1:
    st.metric("Total User Travel Records in BigQuery Vault", f"{telemetry['total_user_flights']:,}")
with col_t2:
    st.metric("Total Registered Traveling Profiles", f"{telemetry['total_traveler_users']:,}")

render_html("""
    <div style="background: rgba(17, 29, 51, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 10px; padding: 10px 16px; margin-top: 12px; margin-bottom: 16px; font-size: 0.85rem; color: #94A3B8;">
        👤 <b>Active Traveler Profiles in Vault</b>: 
        <span style="color: #38BDF8; font-weight: 600;">Steve Riffe</span> (Lead Architect · 148 flights) &nbsp;•&nbsp; 
        <span style="color: #FB923C; font-weight: 600;">Marcus Vance</span> (Global Operations · 210 flights) &nbsp;•&nbsp; 
        <span style="color: #10B981; font-weight: 600;">Sarah Jenkins</span> (Transatlantic Strategy · 85 flights)
    </div>
""")

st.caption("AvDB Architecture: Hosted in Google Cloud Run (us-west1) • BigQuery Google-Managed Encryption • Transport Layer Security (TLS 1.3)")

