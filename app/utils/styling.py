"""
Steve Riffe Enterprise Consulting Design System: Unified Portfolio Styles for AvDB
Aligns AvDB Streamlit Dashboard with the unified portfolio aesthetic (fonts, canvas, glass surfaces,
vibrant orange & electric sky accents, JetBrains Mono metrics, and seamless portal navigation).
"""
import textwrap
import streamlit as st
from app.utils.formatting import fmt_integer, fmt_volume, fmt_currency, fmt_percent

def render_html(html_str: str, unsafe_allow_html: bool = True, **kwargs):
    """Renders HTML cleanly using st.html or st.markdown without Markdown code-block indentation escaping."""
    clean = textwrap.dedent(html_str).strip()
    if hasattr(st, "html"):
        st.html(clean)
    else:
        st.markdown(clean, unsafe_allow_html=unsafe_allow_html)


def apply_apple_style():
    """
    Injects the Steve Riffe Unified Portfolio Design System into the Streamlit session:
    - Fonts: Plus Jakarta Sans, Inter, JetBrains Mono
    - Canvas: #0B192C deep canvas with 28px dot matrix grid & radial ambient glow
    - Surfaces: rgba(17, 29, 51, 0.85) glassmorphism with blur(14px)
    - Accents: #FF6B00 Vibrant Orange, #38BDF8 Electric Sky, #10B981 Emerald
    """
    css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

            :root {
                --canvas-bg: #0B192C;
                --canvas-deep: #060911;
                --surface: #111D33;
                --surface-hover: #16243D;
                --surface-elevated: rgba(17, 29, 51, 0.85);
                
                --brand-blue: #2563EB;
                --brand-blue-dark: #1D4ED8;
                --electric-sky: #38BDF8;
                --vibrant-orange: #FF6B00;
                --vibrant-orange-hover: #EA580C;
                --vibrant-orange-glow: rgba(255, 107, 0, 0.25);
                --emerald-active: #10B981;
                
                --text-primary: #FFFFFF;
                --text-secondary: #CBD5E1;
                --text-muted: #94A3B8;
                --border-subtle: rgba(255, 255, 255, 0.08);
                --border-highlight: rgba(56, 189, 248, 0.25);
                --border-orange: rgba(255, 107, 0, 0.35);
            }

            /* Global Background & Typography */
            html, body, [data-testid="stAppViewContainer"] {
                background-color: #0B192C !important;
                background-image: 
                    radial-gradient(circle at 15% 15%, rgba(37, 99, 235, 0.09) 0%, transparent 45%),
                    radial-gradient(circle at 85% 85%, rgba(255, 107, 0, 0.07) 0%, transparent 40%),
                    radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px) !important;
                background-size: 100% 100%, 100% 100%, 28px 28px !important;
                color: #CBD5E1 !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                -webkit-font-smoothing: antialiased;
            }

            [data-testid="stHeader"] {
                background: rgba(11, 25, 44, 0.75) !important;
                backdrop-filter: blur(14px) !important;
                border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            }

            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: #08111F !important;
                border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            }
            [data-testid="stSidebarNav"] {
                background-color: transparent !important;
            }

            /* Headings */
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
                color: #FFFFFF !important;
                letter-spacing: -0.02em !important;
            }

            /* Monospace */
            code, pre, .font-mono {
                font-family: 'JetBrains Mono', monospace !important;
            }

            /* Custom Scrollbars */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #060911;
            }
            ::-webkit-scrollbar-thumb {
                background: #1e293b;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #334155;
            }

            /* Metric Container (Glass Card) */
            .metric-container {
                display: flex;
                flex-direction: column;
                justify-content: center;
                background: rgba(17, 29, 51, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 16px 20px;
                margin-bottom: 12px;
                backdrop-filter: blur(14px);
                -webkit-backdrop-filter: blur(14px);
                box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.4);
                transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            }
            .metric-container:hover {
                border-color: rgba(56, 189, 248, 0.35);
                transform: translateY(-2px);
                box-shadow: 0 16px 32px -8px rgba(0, 0, 0, 0.5), 0 0 20px -4px rgba(56, 189, 248, 0.2);
            }
            .metric-label {
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 0.78rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.07em;
                color: #94A3B8;
                margin-bottom: 4px;
            }
            .metric-value {
                font-family: 'JetBrains Mono', monospace;
                font-size: 1.85rem;
                font-weight: 800;
                color: #FFFFFF;
                letter-spacing: -0.02em;
            }
            .metric-delta {
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.78rem;
                font-weight: 600;
                color: #10B981;
                margin-top: 4px;
            }

            /* Catchment Badge Pill */
            .catchment-badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: rgba(56, 189, 248, 0.12);
                border: 1px solid rgba(56, 189, 248, 0.35);
                color: #38BDF8;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.8rem;
                font-weight: 600;
                padding: 4px 12px;
                border-radius: 20px;
                margin-top: 6px;
                margin-bottom: 16px;
            }

            /* Filter Card */
            .filter-card {
                background: rgba(17, 29, 51, 0.65);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 14px 18px;
                margin-bottom: 18px;
                backdrop-filter: blur(10px);
            }

            /* Map Container Card */
            .map-card {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
                margin-top: 10px;
                margin-bottom: 24px;
            }

            /* Primary Action Button (Vibrant Orange) */
            .stButton > button[kind="primary"] {
                background: #FF6B00 !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 10px !important;
                font-weight: 700 !important;
                box-shadow: 0 4px 14px rgba(255, 107, 0, 0.35) !important;
                transition: all 0.2s ease !important;
            }
            .stButton > button[kind="primary"]:hover {
                background: #EA580C !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 20px rgba(255, 107, 0, 0.5) !important;
            }

            /* Secondary Button */
            .stButton > button[kind="secondary"] {
                background: rgba(17, 29, 51, 0.9) !important;
                color: #FFFFFF !important;
                border: 1px solid rgba(255, 255, 255, 0.14) !important;
                border-radius: 10px !important;
                font-weight: 600 !important;
                transition: all 0.2s ease !important;
            }
            .stButton > button[kind="secondary"]:hover {
                background: #1a2a46 !important;
                border-color: #38BDF8 !important;
            }

            /* Streamlit Page Link Nav Button */
            [data-testid="stPageLink-NavLink"] {
                background: rgba(17, 29, 51, 0.9) !important;
                border: 1px solid rgba(255, 107, 0, 0.4) !important;
                border-radius: 10px !important;
                color: #FF6B00 !important;
                font-weight: 700 !important;
                transition: all 0.2s ease !important;
                padding: 6px 12px !important;
            }
            [data-testid="stPageLink-NavLink"]:hover {
                background: rgba(255, 107, 0, 0.15) !important;
                border-color: #FF6B00 !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 14px rgba(255, 107, 0, 0.3) !important;
            }
            [data-testid="stPageLink-NavLink"] p {
                color: #FF6B00 !important;
                font-weight: 700 !important;
                font-size: 0.88rem !important;
            }

            /* Remove standard Streamlit padding clutter */
            .block-container {
                padding-top: 1.8rem;
                padding-bottom: 3rem;
            }
        </style>
    """
    render_html(css)


def render_portal_nav_link():
    """Renders a sleek, neutral AvDB platform identity badge in the Streamlit sidebar without external backlinks."""
    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 10px 14px; margin-bottom: 14px; background: rgba(17, 29, 51, 0.85); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 28px; height: 28px; border-radius: 8px; background: linear-gradient(135deg, #2563EB, #0F172A); border: 1px solid rgba(56, 189, 248, 0.4); display: flex; align-items: center; justify-content: center; font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 800; color: #FFFFFF;">
                        ✈️
                    </div>
                    <div>
                        <div style="font-size: 12px; font-weight: 700; color: #FFFFFF; line-height: 1.2;">AvDB Platform</div>
                        <div style="font-size: 10px; font-family: 'JetBrains Mono', monospace; color: #38BDF8;">Aviation Intelligence</div>
                    </div>
                </div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #10B981; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); padding: 2px 7px; border-radius: 6px;">v2.5</span>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_kpi_card(label: str = None, value: str = "", delta: str = None, subtitle: str = None, logo_url: str = None, title: str = None):
    """Renders a sleek portfolio-style KPI card with optional logo, delta, and subtitle."""
    card_label = label or title or ""
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ''
    sub_html = f'<div style="font-size: 0.76rem; color: #94A3B8; margin-top: 4px; font-family: \'JetBrains Mono\', monospace;">{subtitle}</div>' if subtitle else ''
    
    if logo_url:
        card_content = (
            f'<div style="display: flex; justify-content: space-between; align-items: flex-start;">'
            f'<div>'
            f'<div class="metric-label">{card_label}</div>'
            f'<div class="metric-value">{value}</div>'
            f'</div>'
            f'<img src="{logo_url}" style="height: 28px; max-width: 65px; object-fit: contain; margin-top: 2px; border-radius: 4px; flex-shrink: 0;" alt=""/>'
            f'</div>'
            f'{delta_html}'
            f'{sub_html}'
        )
    else:
        card_content = (
            f'<div class="metric-label">{card_label}</div>'
            f'<div class="metric-value">{value}</div>'
            f'{delta_html}'
            f'{sub_html}'
        )
        
    html = f'<div class="metric-container">{card_content}</div>'
    render_html(html)


def render_feature_card(title: str, description: str, page_path: str = None, link_text: str = "Open →", link_url: str = None, icon: str = None):
    """Renders a portfolio glassmorphic feature card with interactive in-session navigation."""
    html = f"""
        <div class="metric-container" style="min-height: 145px; margin-bottom: 8px;">
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.15rem; font-weight: 700; color: #FFFFFF; margin-bottom: 8px;">{title}</div>
            <div style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.5;">
                {description}
            </div>
        </div>
    """
    render_html(html)
    if page_path:
        st.page_link(page_path, label=link_text, icon=icon, use_container_width=True)
    elif link_url:
        st.markdown(f'<a href="{link_url}" target="_self" style="color: #FF6B00; font-weight: 700; text-decoration: none; font-size: 0.92rem; font-family: \'Plus Jakarta Sans\', sans-serif;">{link_text}</a>', unsafe_allow_html=True)

