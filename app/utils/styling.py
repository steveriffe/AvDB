"""
AvDB Apple-esque Clean & Minimal Styling Helpers
"""
import streamlit as st

def apply_apple_style():
    """Injects clean, minimalist, Apple-inspired CSS design elements."""
    st.markdown("""
        <style>
            /* Typography & General Flow */
            html, body, [class*="css"] {
                font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
                letter-spacing: -0.015em;
            }
            
            /* Metric Card Container */
            .metric-container {
                display: flex;
                flex-direction: column;
                justify-content: center;
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 16px 20px;
                margin-bottom: 12px;
                backdrop-filter: blur(16px);
                transition: transform 0.2s ease, border-color 0.2s ease;
            }
            .metric-container:hover {
                border-color: rgba(255, 255, 255, 0.18);
                transform: translateY(-1px);
            }
            .metric-label {
                font-size: 0.82rem;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                color: #8E8E93;
                margin-bottom: 4px;
            }
            .metric-value {
                font-size: 1.85rem;
                font-weight: 600;
                color: #F5F5F7;
                letter-spacing: -0.03em;
            }
            .metric-delta {
                font-size: 0.78rem;
                font-weight: 500;
                color: #30D158;
                margin-top: 4px;
            }

            /* Catchment Badge Pill */
            .catchment-badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: rgba(10, 132, 255, 0.12);
                border: 1px solid rgba(10, 132, 255, 0.3);
                color: #64D2FF;
                font-size: 0.82rem;
                font-weight: 500;
                padding: 4px 12px;
                border-radius: 20px;
                margin-top: 6px;
                margin-bottom: 16px;
            }

            /* Filter Card */
            .filter-card {
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 14px;
                padding: 14px 18px;
                margin-bottom: 18px;
            }

            /* Map Container Card */
            .map-card {
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.24);
                margin-top: 10px;
                margin-bottom: 24px;
            }
            
            /* Remove standard Streamlit padding clutter */
            .block-container {
                padding-top: 1.8rem;
                padding-bottom: 3rem;
            }
        </style>
    """, unsafe_allow_html=True)


def render_kpi_card(label: str = None, value: str = "", delta: str = None, subtitle: str = None, logo_url: str = None, title: str = None):
    """Renders a sleek Apple-style KPI card with optional logo and subtitle."""
    card_label = label or title or ""
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ''
    sub_html = f'<div style="font-size: 0.76rem; color: #8E8E93; margin-top: 4px;">{subtitle}</div>' if subtitle else ''
    
    if logo_url:
        card_content = f"""
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div class="metric-label">{card_label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                <img src="{logo_url}" style="height: 28px; max-width: 65px; object-fit: contain; filter: brightness(1.1); margin-top: 2px;" alt=""/>
            </div>
            {delta_html}
            {sub_html}
        """
    else:
        card_content = f"""
            <div class="metric-label">{card_label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
            {sub_html}
        """
        
    st.markdown(f"""
        <div class="metric-container">
            {card_content}
        </div>
    """, unsafe_allow_html=True)

