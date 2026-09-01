"""
AvDB Visualizers & Chart Builders
Plotly and PyDeck implementations with Apple-inspired minimalist aesthetics.
"""
import os
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, Dict, Any


# Clean luxury color palette
PALETTE = {
    "bg": "#0D0E11",
    "text": "#F5F5F7",
    "muted_text": "#8E8E93",
    "accent_blue": "#0A84FF",
    "accent_cyan": "#64D2FF",
    "accent_orange": "#FF9F0A",
    "accent_pink": "#FF375F",
    "accent_purple": "#BF5AF2",
    "grid": "rgba(255, 255, 255, 0.05)"
}

CHART_COLORS = [
    "#0A84FF", "#30D158", "#FF9F0A", "#BF5AF2", "#FF375F", 
    "#64D2FF", "#FFD60A", "#AC8E68", "#5E5CE6", "#63E6E2"
]


def build_route_map_deck(
    df_routes: pd.DataFrame, 
    origin_meta: Dict[str, Any],
    mapbox_api_key: Optional[str] = None,
    mapbox_style: Optional[str] = None
) -> pdk.Deck:
    """
    Builds an immersive PyDeck Great-Circle Arc and Node map for airport routes.
    """
    if df_routes.empty:
        return pdk.Deck(initial_view_state=pdk.ViewState(latitude=39.8, longitude=-98.5, zoom=3.5))

    origin_lat = float(origin_meta.get("latitude", df_routes["origin_lat"].iloc[0]))
    origin_lon = float(origin_meta.get("longitude", df_routes["origin_lon"].iloc[0]))

    # Add dynamic visual scaling attributes
    df_plot = df_routes.copy()
    max_pax = df_plot["operational_passengers"].max() or 1
    
    # Scale width from 1 to 8 based on volume
    df_plot["arc_width"] = (df_plot["operational_passengers"] / max_pax * 6 + 1.2).round(2)
    # Scale destination radius from 10,000 to 50,000 meters
    df_plot["node_radius"] = (df_plot["operational_passengers"] / max_pax * 35000 + 8000).round(0)

    # 1. Great-Circle Arc Layer
    arc_layer = pdk.Layer(
        "ArcLayer",
        data=df_plot,
        get_source_position=["origin_lon", "origin_lat"],
        get_target_position=["dest_lon", "dest_lat"],
        get_source_color=[10, 132, 255, 160],   # Apple Accent Blue
        get_target_color=[255, 159, 10, 200],   # Warm Orange
        get_width="arc_width",
        width_min_pixels=1.5,
        width_max_pixels=10,
        pickable=True,
        auto_highlight=True,
    )

    # 2. Destination Node Layer
    dest_node_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_plot,
        get_position=["dest_lon", "dest_lat"],
        get_radius="node_radius",
        get_fill_color=[255, 255, 255, 200],
        get_line_color=[10, 132, 255, 220],
        line_width_min_pixels=1.5,
        stroked=True,
        filled=True,
        pickable=True,
        auto_highlight=True,
    )

    # 3. Origin Hub Node Layer
    origin_df = pd.DataFrame([{
        "lon": origin_lon,
        "lat": origin_lat,
        "name": origin_meta.get("airport_name", "Origin Airport"),
        "code": origin_meta.get("airport_code", "Origin")
    }])
    
    origin_node_layer = pdk.Layer(
        "ScatterplotLayer",
        data=origin_df,
        get_position=["lon", "lat"],
        get_radius=45000,
        get_fill_color=[10, 132, 255, 240],
        get_line_color=[255, 255, 255, 255],
        line_width_min_pixels=3,
        stroked=True,
        filled=True,
        pickable=True,
    )

    # View State centered on origin
    view_state = pdk.ViewState(
        latitude=origin_lat,
        longitude=origin_lon,
        zoom=3.8,
        min_zoom=2,
        max_zoom=10,
        pitch=25,
        bearing=0,
    )

    # Tooltip definition
    tooltip = {
        "html": """
            <div style="font-family: -apple-system, sans-serif; font-size: 12px; padding: 6px 10px; background: rgba(18, 18, 20, 0.9); border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; color: #FFFFFF;">
                <b style="font-size: 14px; color: #64D2FF;">{dest} — {dest_name}</b><br/>
                <span style="color: #8E8E93;">City:</span> {dest_city}, {dest_state} ({dest_country})<br/>
                <hr style="margin: 4px 0; border: 0; border-top: 1px solid rgba(255,255,255,0.1);"/>
                <span style="color: #8E8E93;">Passengers:</span> <b>{operational_passengers}</b><br/>
                <span style="color: #8E8E93;">Departures:</span> <b>{departures_performed}</b><br/>
                <span style="color: #8E8E93;">Avg Load Factor:</span> <b>{load_factor_pct}%</b><br/>
                <span style="color: #8E8E93;">Inferred Avg Fare:</span> <b>${avg_od_fare}</b><br/>
                <span style="color: #8E8E93;">Carriers:</span> {operating_carriers}
            </div>
        """,
        "style": {"backgroundColor": "transparent", "color": "white"}
    }

    # Map Style handling
    map_style = mapbox_style or "dark"

    return pdk.Deck(
        layers=[arc_layer, dest_node_layer, origin_node_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style=map_style,
        api_keys={"mapbox": mapbox_api_key} if mapbox_api_key else None
    )


def build_top_routes_bar_chart(df_routes: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Renders a sleek horizontal bar chart for top outbound routes."""
    if df_routes.empty:
        return go.Figure()

    df_top = df_routes.head(top_n).sort_values("operational_passengers", ascending=True).copy()
    
    df_top["label"] = df_top["dest"] + " (" + df_top["dest_city"].fillna("") + ")"

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_top["label"],
        x=df_top["operational_passengers"],
        orientation="h",
        marker=dict(
            color=df_top["load_factor_pct"],
            colorscale=[[0, "#0A84FF"], [1, "#30D158"]],
            colorbar=dict(title=dict(text="Load Factor %", font=dict(size=10, color="#8E8E93")), thickness=8),
            line=dict(width=0)
        ),
        hovertemplate="<b>%{y}</b><br>Passengers: %{x:,.0f}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(text=f"Top {top_n} Outbound Destinations (by Passenger Volume)", font=dict(size=14, color="#F5F5F7")),
        margin=dict(l=10, r=10, t=35, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=310,
        xaxis=dict(
            showgrid=True, 
            gridcolor="rgba(255,255,255,0.06)", 
            tickfont=dict(color="#8E8E93", size=10),
            title=None
        ),
        yaxis=dict(
            showgrid=False, 
            tickfont=dict(color="#F5F5F7", size=11),
            title=None
        ),
    )
    return fig


def build_carrier_market_share_donut(df_carriers: pd.DataFrame) -> go.Figure:
    """Renders an Apple-inspired carrier seat capacity donut chart."""
    if df_carriers.empty:
        return go.Figure()

    df_plot = df_carriers.head(6).copy()
    
    fig = go.Figure(data=[go.Pie(
        labels=df_plot["unique_carrier"] + " — " + df_plot["carrier_name"],
        values=df_plot["total_seats"],
        hole=0.68,
        marker=dict(colors=CHART_COLORS),
        textinfo="percent",
        textfont=dict(size=11, color="#F5F5F7"),
        hovertemplate="<b>%{label}</b><br>Seats: %{value:,.0f}<br>Share: %{percent}<extra></extra>"
    )])

    fig.update_layout(
        title=dict(text="Carrier Capacity Share (Seats Available)", font=dict(size=14, color="#F5F5F7")),
        margin=dict(l=10, r=10, t=35, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=310,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=10, color="#8E8E93")
        )
    )
    return fig

