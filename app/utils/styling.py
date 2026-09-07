import textwrap
import streamlit as st

def render_html(html_str: str):
    """Renders HTML cleanly using st.html without Markdown code-block indentation escaping."""
    clean = textwrap.dedent(html_str).strip()
    if hasattr(st, "html"):
        st.html(clean)
    else:
        st.markdown(clean, unsafe_allow_html=True)


def apply_apple_style():
    """Injects clean, minimalist, Apple-inspired CSS design elements."""
    css = """
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
    """
    render_html(css)


def render_kpi_card(label: str = None, value: str = "", delta: str = None, subtitle: str = None, logo_url: str = None, title: str = None):
    """Renders a sleek Apple-style KPI card with optional logo and subtitle."""
    card_label = label or title or ""
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ''
    sub_html = f'<div style="font-size: 0.76rem; color: #8E8E93; margin-top: 4px;">{subtitle}</div>' if subtitle else ''
    
    if logo_url:
        card_content = (
            f'<div style="display: flex; justify-content: space-between; align-items: flex-start;">'
            f'<div>'
            f'<div class="metric-label">{card_label}</div>'
            f'<div class="metric-value">{value}</div>'
            f'</div>'
            f'<img src="{logo_url}" style="height: 28px; max-width: 65px; object-fit: contain; filter: brightness(1.1); margin-top: 2px;" alt=""/>'
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


def render_feature_card(title: str, description: str, link_url: str, link_text: str = "Open →"):
    """Renders an Apple-style interactive feature card container with a navigation link."""
    html = f"""
        <div class="metric-container" style="min-height: 190px;">
            <div style="font-size: 1.25rem; font-weight: 600; color: #F5F5F7; margin-bottom: 8px;">{title}</div>
            <div style="color: #8E8E93; font-size: 0.88rem; line-height: 1.5; margin-bottom: 14px;">
                {description}
            </div>
            <a href="{link_url}" target="_self" style="color: #0A84FF; font-weight: 500; text-decoration: none; font-size: 0.92rem;">{link_text}</a>
        </div>
    """
    render_html(html)


