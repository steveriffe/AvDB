"""
Steve Riffe Unified Portfolio Design System: HTML Landing Homepage & Access Control UI Component for AvDB
"""
import streamlit as st
from app.config import settings
from app.utils.auth import get_google_auth_url, get_redirect_uri, logout
from app.utils.styling import render_html
from app.utils.queries import get_platform_live_kpis


def render_landing_page():
    """
    Renders the public landing homepage with feature highlights, live warehouse scale,
    portfolio-aligned styling, and a prominent Google Sign-In call to action.
    """
    redirect_uri = get_redirect_uri()
    auth_url = get_google_auth_url(redirect_uri)
    kpis = get_platform_live_kpis()

    render_html("""
        <style>
        .landing-portal-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 18px;
            margin-bottom: 24px;
            background: rgba(17, 29, 51, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            backdrop-filter: blur(14px);
        }
        .portal-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
        }
        .portal-avatar {
            width: 34px;
            height: 34px;
            border-radius: 8px;
            background: linear-gradient(135deg, #2563EB, #0F172A);
            border: 1px solid rgba(56, 189, 248, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 800;
            color: #FFFFFF;
            font-size: 13px;
        }
        .portal-text-name {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            color: #FFFFFF;
            font-size: 14px;
            line-height: 1.2;
        }
        .portal-text-sub {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #94A3B8;
        }
        .landing-hero {
            background: linear-gradient(135deg, rgba(17, 29, 51, 0.95) 0%, rgba(6, 9, 17, 0.98) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 48px 36px;
            text-align: center;
            margin-bottom: 28px;
            box-shadow: 0 20px 48px -12px rgba(0, 0, 0, 0.6), 0 0 32px -4px rgba(56, 189, 248, 0.1);
            backdrop-filter: blur(16px);
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(56, 189, 248, 0.12);
            color: #38BDF8;
            border: 1px solid rgba(56, 189, 248, 0.3);
            font-size: 0.78rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            padding: 5px 14px;
            border-radius: 20px;
            margin-bottom: 18px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .hero-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 2.9rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 16px;
            letter-spacing: -0.03em;
            line-height: 1.15;
        }
        .hero-subtitle {
            font-size: 1.15rem;
            color: #CBD5E1;
            max-width: 700px;
            margin: 0 auto 32px auto;
            line-height: 1.6;
            font-weight: 400;
        }
        .cta-button-orange {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #FF6B00;
            color: #FFFFFF !important;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            font-size: 1.05rem;
            padding: 14px 34px;
            border-radius: 12px;
            text-decoration: none !important;
            box-shadow: 0 4px 18px rgba(255, 107, 0, 0.4);
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .cta-button-orange:hover {
            background: #EA580C;
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(255, 107, 0, 0.6);
        }
        .feature-card {
            background: rgba(17, 29, 51, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            height: 100%;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            backdrop-filter: blur(14px);
        }
        .feature-card:hover {
            border-color: rgba(56, 189, 248, 0.35);
            transform: translateY(-3px);
            box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.5), 0 0 20px -4px rgba(56, 189, 248, 0.2);
        }
        .feature-icon {
            font-size: 2.2rem;
            margin-bottom: 12px;
        }
        .feature-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 8px;
        }
        .feature-desc {
            font-size: 0.92rem;
            color: #CBD5E1;
            line-height: 1.5;
        }
        .metric-badge-box {
            text-align: center;
            background: rgba(17, 29, 51, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 18px 12px;
            backdrop-filter: blur(12px);
            transition: all 0.2s ease;
        }
        .metric-badge-box:hover {
            border-color: rgba(56, 189, 248, 0.3);
            transform: translateY(-2px);
        }
        .metric-val {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.85rem;
            font-weight: 800;
            color: #FFFFFF;
        }
        .metric-lbl {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #94A3B8;
            margin-top: 4px;
        }
        </style>
    """)

    # Top AvDB Platform Bar
    render_html("""
        <div class="landing-portal-bar">
            <div class="portal-brand">
                <div class="portal-avatar">✈️</div>
                <div>
                    <div class="portal-text-name">AvDB Aviation Intelligence</div>
                    <div class="portal-text-sub">US BTS T-100 & DB1B/OD40 Cloud Analytics</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #10B981; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 3px 8px; border-radius: 6px;">● Production Ready</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #38BDF8; background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.25); padding: 3px 8px; border-radius: 6px;">Google Cloud Run</span>
            </div>
        </div>
    """)

    # Hero Section
    render_html(f"""
        <div class="landing-hero">
            <div class="hero-badge">BigQuery Aviation Intelligence · {kpis['total_records_formatted']} System Records</div>
            <div class="hero-title">AvDB Aviation Platform <span style="color: #FF6B00;">.</span></div>
            <div class="hero-subtitle">
                Interactive U.S. BTS T-100 operations and DB1B ticket yield analytics modeled in Google BigQuery, featuring geodesic great-circle cartography, multi-airport catchment systems, and complete fleet dynamics.
            </div>
            <a href="{auth_url}" target="_self" class="cta-button-orange">
                <span style="margin-right: 10px;">🔐</span> Sign in with Google
            </a>
            <div style="margin-top: 16px; color: #94A3B8; font-size: 0.85rem; font-family: 'JetBrains Mono', monospace;">
                Protected access • Google OAuth 2.0 • Google Cloud Run
            </div>
        </div>
    """)

    # Dynamic BigQuery Warehouse Scale Strip
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_html(f"""
            <div class="metric-badge-box">
                <div class="metric-val" style="color: #FB923C;">{kpis['t100_rows_formatted']}</div>
                <div class="metric-lbl">T-100 Operations Mart</div>
            </div>
        """)
    with col2:
        render_html(f"""
            <div class="metric-badge-box">
                <div class="metric-val" style="color: #38BDF8;">{kpis['od40_rows_formatted']}</div>
                <div class="metric-lbl">DB1B OD40 Survey Mart</div>
            </div>
        """)
    with col3:
        render_html(f"""
            <div class="metric-badge-box">
                <div class="metric-val" style="color: #FFFFFF;">{kpis['ref_airports_formatted']}</div>
                <div class="metric-lbl">Global Airport Coordinates</div>
            </div>
        """)
    with col4:
        render_html(f"""
            <div class="metric-badge-box">
                <div class="metric-val" style="color: #10B981;">{kpis['fleet_rows_formatted']}</div>
                <div class="metric-lbl">Fleet Dynamics Mart</div>
            </div>
        """)

    render_html("<div style='margin-top: 36px;'></div>")

    # Feature Grid
    st.markdown("### 🧭 Analytical Lenses & Features")
    fcol1, fcol2, fcol3 = st.columns(3)

    with fcol1:
        render_html("""
            <div class="feature-card">
                <div class="feature-icon">✈️</div>
                <div class="feature-title">Airports Lens</div>
                <div class="feature-desc">
                    Comprehensive passenger traffic trends, catchment metro area analysis, route churn, and interactive Great-Circle destination mapping.
                </div>
            </div>
        """)

    with fcol2:
        render_html("""
            <div class="feature-card">
                <div class="feature-icon">🏢</div>
                <div class="feature-title">Airlines Lens</div>
                <div class="feature-desc">
                    Carrier route networks, hub concentration metrics, average fares, Stage Length vs. Yield per RPM curves, and corporate merger timelines.
                </div>
            </div>
        """)

    with fcol3:
        render_html("""
            <div class="feature-card">
                <div class="feature-icon">💺</div>
                <div class="feature-title">Fleet & Routes</div>
                <div class="feature-desc">
                    Aircraft gauge transitions, equipment utilization by route, regional vs. mainline shifts, and verified engineering specifications & photography.
                </div>
            </div>
        """)

    # Privacy & Data Governance Footer Strip
    render_html("""
        <div style="margin-top: 48px; padding-top: 24px; border-top: 1px solid rgba(255, 255, 255, 0.08); display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 16px; font-size: 0.85rem; color: #94A3B8;">
                <span>🔒 <b>Privacy Assured</b>: Authenticated Google identity used strictly for access control</span>
                <span>•</span>
                <span>Travel logs committed to private BigQuery vault (capped at 1,000 flights)</span>
                <span>•</span>
                <span>Self-service fail-safe purge anytime</span>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #64748B;">
                BTS Data Attribution: US DOT TranStats (T-100 & DB1B/OD40)
            </div>
        </div>
    """)


def render_unauthorized_page(user_info: dict):
    """
    Renders an access denied message if the authenticated user is not in the allowlist.
    """
    email = user_info.get("email", "Unknown")
    name = user_info.get("name", "Traveler")

    render_html(f"""
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 16px; padding: 36px; text-align: center; max-width: 600px; margin: 60px auto;">
            <div style="font-size: 3rem; margin-bottom: 12px;">🚫</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #F5F5F7; margin-bottom: 8px;">Access Restricted</div>
            <div style="color: #CBD5E1; font-size: 1rem; line-height: 1.5; margin-bottom: 24px;">
                Hello <b>{name}</b> ({email}), your Google account is authenticated, but not on the authorized allowlist for this environment.
            </div>
        </div>
    """)
    if st.button("Sign Out / Switch Account", type="primary"):
        logout()
