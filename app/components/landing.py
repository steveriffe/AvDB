"""
Apple-Modern HTML Landing Homepage & Access Control UI Component for AvDB
"""
import streamlit as st
from app.config import settings
from app.utils.auth import get_google_auth_url, get_redirect_uri, logout


def render_landing_page():
    """
    Renders the public landing homepage with feature highlights, platform scale,
    and a prominent Google Sign-In call to action.
    """
    redirect_uri = get_redirect_uri()
    auth_url = get_google_auth_url(redirect_uri)

    st.markdown("""
        <style>
        .landing-hero {
            background: linear-gradient(135deg, rgba(28, 28, 30, 0.8) 0%, rgba(10, 10, 12, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 48px 36px;
            text-align: center;
            margin-bottom: 32px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
        }
        .hero-badge {
            display: inline-block;
            background: rgba(10, 132, 255, 0.15);
            color: #0A84FF;
            border: 1px solid rgba(10, 132, 255, 0.3);
            font-size: 0.85rem;
            font-weight: 600;
            padding: 6px 16px;
            border-radius: 20px;
            margin-bottom: 20px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .hero-title {
            font-size: 2.8rem;
            font-weight: 700;
            color: #F5F5F7;
            margin-bottom: 16px;
            letter-spacing: -0.5px;
            line-height: 1.15;
        }
        .hero-subtitle {
            font-size: 1.2rem;
            color: #8E8E93;
            max-width: 680px;
            margin: 0 auto 32px auto;
            line-height: 1.6;
            font-weight: 400;
        }
        .cta-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #0A84FF;
            color: #FFFFFF !important;
            font-weight: 600;
            font-size: 1.1rem;
            padding: 14px 32px;
            border-radius: 12px;
            text-decoration: none !important;
            box-shadow: 0 4px 14px rgba(10, 132, 255, 0.4);
            transition: all 0.2s ease-in-out;
        }
        .cta-button:hover {
            background: #0071E3;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(10, 132, 255, 0.6);
        }
        .feature-card {
            background: rgba(28, 28, 30, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            height: 100%;
            transition: transform 0.2s ease;
        }
        .feature-card:hover {
            border-color: rgba(10, 132, 255, 0.3);
            transform: translateY(-4px);
        }
        .feature-icon {
            font-size: 2.2rem;
            margin-bottom: 12px;
        }
        .feature-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #F5F5F7;
            margin-bottom: 8px;
        }
        .feature-desc {
            font-size: 0.95rem;
            color: #8E8E93;
            line-height: 1.5;
        }
        .metric-badge-box {
            text-align: center;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 16px;
        }
        .metric-val {
            font-size: 1.8rem;
            font-weight: 700;
            color: #0A84FF;
        }
        .metric-lbl {
            font-size: 0.85rem;
            color: #8E8E93;
            margin-top: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown(f"""
        <div class="landing-hero">
            <div class="hero-badge">Enterprise Aviation Intelligence</div>
            <div class="hero-title">AvDB Analytics Platform</div>
            <div class="hero-subtitle">
                Interactive U.S. BTS T-100 operations & DB1B ticket yield analytics powered by Google BigQuery, great-circle route mapping, and automated fleet economics.
            </div>
            <a href="{auth_url}" target="_self" class="cta-button">
                <span style="margin-right: 10px;">🔐</span> Sign in with Google
            </a>
            <div style="margin-top: 14px; color: #6E6E73; font-size: 0.85rem;">
                Protected access • Google OAuth 2.0 • Hosted on Google Cloud Run
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Key Data Scale Strip
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="metric-badge-box">
                <div class="metric-val">2.52M</div>
                <div class="metric-lbl">T-100 Operations Rows</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-badge-box">
                <div class="metric-val">40.3M</div>
                <div class="metric-lbl">DB1B Ticket Survey Rows</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-badge-box">
                <div class="metric-val">50,409</div>
                <div class="metric-lbl">Global Airport Coordinates</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="metric-badge-box">
                <div class="metric-val">&lt; 1.2s</div>
                <div class="metric-lbl">BigQuery Query Latency</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)

    # Feature Grid
    st.markdown("### 🧭 Analytical Lenses & Features")
    fcol1, fcol2, fcol3 = st.columns(3)

    with fcol1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">✈️</div>
                <div class="feature-title">Airport Intelligence</div>
                <div class="feature-desc">
                    Analyze direct O&D route networks, carrier seat mix, catchment overlap (e.g. HOU vs IAH), and unserved market proposals with PDEW fare yields.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with fcol2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🏢</div>
                <div class="feature-title">Airline Explorer</div>
                <div class="feature-desc">
                    Inspect carrier network density, hub concentration, passenger market share, and revenue passenger mile (RPM) yield curves.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with fcol3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">💺</div>
                <div class="feature-title">Fleet & Gauge Dynamics</div>
                <div class="feature-desc">
                    Track equipment allocation (Widebody, Narrowbody, RJ), gauge shifts (seats per departure), and stage-length economics.
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_unauthorized_page(user_info: dict):
    """
    Renders clean access restriction page when user authenticates with Google
    but their email is not on the ALLOWED_EMAILS list.
    """
    email = user_info.get("email", "Unknown Email")
    name = user_info.get("name", "User")
    picture = user_info.get("picture", "")

    st.markdown("""
        <style>
        .restricted-card {
            background: linear-gradient(135deg, rgba(38, 38, 40, 0.9) 0%, rgba(20, 20, 22, 0.95) 100%);
            border: 1px solid rgba(255, 69, 58, 0.3);
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            margin: 40px auto;
            text-align: center;
            box-shadow: 0 16px 36px rgba(0,0,0,0.6);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="restricted-card">
            <div style="font-size: 3rem; margin-bottom: 12px;">🔒</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #FF453A; margin-bottom: 8px;">Access Pending Approval</div>
            <p style="color: #8E8E93; font-size: 1rem; line-height: 1.6; margin-bottom: 24px;">
                Hello <strong>{name}</strong> (<code>{email}</code>). Your account is authenticated via Google, but access to this private AvDB demo is restricted to authorized email addresses.
            </p>
            <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 16px; font-size: 0.9rem; color: #AEAEB2; margin-bottom: 24px;">
                To request access for your email address, please contact <strong>steve@riffe.co.uk</strong>.
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("Sign Out & Try Another Account", type="primary", use_container_width=True):
            logout()

