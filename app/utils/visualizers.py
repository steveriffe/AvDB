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
    "accent_green": "#30D158",
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

FAMILY_COLORS = {
    "Widebody": "#BF5AF2",              # Purple
    "Mainline Narrowbody": "#0A84FF",   # Apple Blue
    "Regional Jet": "#30D158",          # Green
    "Turboprop / Regional Prop": "#FF9F0A", # Orange
    "Other / Uncategorized": "#8E8E93"  # Muted Gray
}


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
    
    # Scale width from 1.5 to 7.5 based on volume
    df_plot["arc_width"] = (df_plot["operational_passengers"] / max_pax * 5.5 + 1.5).round(2)
    # Scale destination radius from 10,000 to 45,000 meters
    df_plot["node_radius"] = (df_plot["operational_passengers"] / max_pax * 32000 + 9000).round(0)

    # Formatted display strings for tooltip
    df_plot["fmt_pax"] = df_plot["operational_passengers"].apply(lambda x: f"{x/1e6:.2f}M" if x >= 1e6 else f"{x:,}")
    df_plot["fmt_fare"] = df_plot["avg_od_fare"].apply(lambda x: f"${x:.0f}" if pd.notnull(x) and x > 0 else "N/A")
    df_plot["fmt_lf"] = df_plot["load_factor_pct"].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "—")
    df_plot["fmt_deps"] = df_plot["departures_performed"].apply(lambda x: f"{x:,}")

    # 1. Great-Circle Arc Layer
    arc_layer = pdk.Layer(
        "ArcLayer",
        data=df_plot,
        get_source_position=["origin_lon", "origin_lat"],
        get_target_position=["dest_lon", "dest_lat"],
        get_source_color=[10, 132, 255, 170],   # Apple Cobalt Blue
        get_target_color=[255, 159, 10, 210],   # Warm Orange Glow
        get_width="arc_width",
        width_min_pixels=1.5,
        width_max_pixels=9,
        pickable=True,
        auto_highlight=True,
    )

    # 2. Destination Node Layer
    dest_node_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_plot,
        get_position=["dest_lon", "dest_lat"],
        get_radius="node_radius",
        get_fill_color=[255, 255, 255, 210],
        get_line_color=[10, 132, 255, 230],
        line_width_min_pixels=2,
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
        get_radius=42000,
        get_fill_color=[10, 132, 255, 255],
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

    # Apple Glassmorphism Tooltip
    tooltip = {
        "html": """
            <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-size: 12px; padding: 10px 14px; background: rgba(18, 18, 22, 0.94); border: 1px solid rgba(255,255,255,0.14); border-radius: 12px; backdrop-filter: blur(20px); box-shadow: 0 12px 32px rgba(0,0,0,0.5); color: #FFFFFF; min-width: 200px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-size: 16px; font-weight: 700; color: #64D2FF; letter-spacing: -0.02em;">{dest}</span>
                    <span style="background: rgba(10, 132, 255, 0.2); border: 1px solid rgba(10, 132, 255, 0.4); color: #64D2FF; font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 6px;">LF: {fmt_lf}</span>
                </div>
                <div style="font-size: 12px; font-weight: 500; color: #E5E5EA; margin-bottom: 2px;">{dest_name}</div>
                <div style="font-size: 11px; color: #8E8E93; margin-bottom: 8px;">{dest_city}, {dest_state} ({dest_country})</div>
                <hr style="margin: 6px 0; border: 0; border-top: 1px solid rgba(255,255,255,0.08);"/>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 6px;">
                    <div><span style="color: #8E8E93; font-size: 10px; text-transform: uppercase;">Passengers</span><br/><b style="font-size: 13px; color: #F5F5F7;">{fmt_pax}</b></div>
                    <div><span style="color: #8E8E93; font-size: 10px; text-transform: uppercase;">Inferred Fare</span><br/><b style="font-size: 13px; color: #30D158;">{fmt_fare}</b></div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 6px;">
                    <div><span style="color: #8E8E93; font-size: 10px; text-transform: uppercase;">Departures</span><br/><b style="font-size: 12px; color: #F5F5F7;">{fmt_deps}</b></div>
                    <div><span style="color: #8E8E93; font-size: 10px; text-transform: uppercase;">Seats / Dep</span><br/><b style="font-size: 12px; color: #F5F5F7;">{avg_gauge_seats}</b></div>
                </div>
                <div style="font-size: 10px; color: #8E8E93; margin-top: 4px;"><b>Carriers:</b> {operating_carriers}</div>
            </div>
        """,
        "style": {"backgroundColor": "transparent", "color": "white"}
    }

    map_style = mapbox_style or "dark"

    return pdk.Deck(
        layers=[arc_layer, dest_node_layer, origin_node_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style=map_style,
        api_keys={"mapbox": mapbox_api_key} if mapbox_api_key else None
    )


def build_top_routes_bar_chart(df_routes: pd.DataFrame, top_n: int = 8) -> go.Figure:
    """
    Renders a sleek horizontal bar chart for top outbound routes in Apple Cobalt Blue.
    Uses native Plotly hover card formatting without unsupported inline CSS span tags.
    """
    if df_routes.empty:
        return go.Figure()

    df_top = df_routes.head(top_n).sort_values("operational_passengers", ascending=True).copy()
    df_top["label"] = df_top["dest"] + " — " + df_top["dest_city"].fillna(df_top["dest"])
    df_top["fmt_pax"] = df_top["operational_passengers"].apply(lambda x: f"{x/1e6:.2f}M" if x >= 1e6 else f"{x:,}")
    df_top["fmt_fare"] = df_top["avg_od_fare"].apply(lambda x: f"${x:.0f}" if pd.notnull(x) and x > 0 else "N/A")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_top["label"],
        x=df_top["operational_passengers"],
        orientation="h",
        marker=dict(
            color="#0A84FF",
            line=dict(width=0),
            opacity=0.92
        ),
        customdata=df_top[["fmt_pax", "load_factor_pct", "fmt_fare", "departures_performed", "avg_gauge_seats"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Passengers: <b>%{customdata[0]}</b><br>"
            "Avg Load Factor: <b>%{customdata[1]:.1f}%</b><br>"
            "Inferred Fare: <b>%{customdata[2]}</b><br>"
            "Departures: <b>%{customdata[3]:,}</b><br>"
            "Avg Gauge: <b>%{customdata[4]} seats</b>"
            "<extra></extra>"
        )
    ))

    fig.update_layout(
        title=dict(text=f"Top {top_n} Outbound Destinations (Passenger Volume)", font=dict(size=13, color="#F5F5F7")),
        margin=dict(l=10, r=10, t=32, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=290,
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
        hovertemplate="<b>%{label}</b><br>Seats: %{value:,.0f}<br>Capacity Share: %{percent}<extra></extra>"
    )])

    fig.update_layout(
        title=dict(text="Carrier Capacity Share (Seats Available)", font=dict(size=13, color="#F5F5F7")),
        margin=dict(l=10, r=10, t=32, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=290,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=9.5, color="#8E8E93")
        )
    )
    return fig


def build_airport_fleet_bar_chart(df_fleet: pd.DataFrame, top_n: int = 7) -> go.Figure:
    """
    Renders an Apple-inspired horizontal bar chart showing top aircraft models by passenger volume.
    Uses native Plotly hover card formatting.
    """
    if df_fleet.empty:
        return go.Figure()

    df_top = df_fleet.head(top_n).sort_values("operational_passengers", ascending=True).copy()
    df_top["fmt_pax"] = df_top["operational_passengers"].apply(lambda x: f"{x/1e6:.2f}M" if x >= 1e6 else f"{x:,}")
    
    colors = [FAMILY_COLORS.get(fam, "#8E8E93") for fam in df_top["aircraft_family"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_top["aircraft_description"],
        x=df_top["operational_passengers"],
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(width=0),
            opacity=0.92
        ),
        customdata=df_top[["aircraft_family", "fmt_pax", "avg_gauge_seats", "load_factor_pct", "departures_performed"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Category: <b>%{customdata[0]}</b><br>"
            "Passengers: <b>%{customdata[1]}</b><br>"
            "Gauge: <b>%{customdata[2]} seats/dep</b><br>"
            "Load Factor: <b>%{customdata[3]:.1f}%</b><br>"
            "Departures: <b>%{customdata[4]:,}</b>"
            "<extra></extra>"
        )
    ))

    fig.update_layout(
        title=dict(text=f"Fleet Equipment Mix (Top {top_n} Aircraft Types)", font=dict(size=13, color="#F5F5F7")),
        margin=dict(l=10, r=10, t=32, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=290,
        xaxis=dict(
            showgrid=True, 
            gridcolor="rgba(255,255,255,0.06)", 
            tickfont=dict(color="#8E8E93", size=10),
            title=None
        ),
        yaxis=dict(
            showgrid=False, 
            tickfont=dict(color="#F5F5F7", size=10.5),
            title=None
        ),
    )
    return fig


def build_unserved_markets_scatter_chart(df_unserved: pd.DataFrame) -> go.Figure:
    """
    Renders an interactive scatter plot of unserved connecting O&D markets:
    Connecting Pax Daily Each Way (PDEW) vs. Yield ($/mile) colored by Business/Leisure profile.
    """
    if df_unserved.empty:
        return go.Figure()

    color_map = {
        "💼 Business Heavy": "#30D158",   # Apple Green (High Yield)
        "🏖️ Leisure Heavy": "#FF9F0A",   # Orange
        "⚖️ Balanced Mix": "#0A84FF"      # Apple Blue
    }

    fig = px.scatter(
        df_unserved,
        x="pdew",
        y="yield_per_mile",
        size="annual_connecting_pax",
        color="market_type",
        color_discrete_map=color_map,
        hover_name="dest_city",
        hover_data={
            "dest": True,
            "annual_connecting_pax": ":,",
            "avg_fare": ":$.0f",
            "distance_miles": ":,.0f",
            "aligned_carrier": True,
            "pdew": False,
            "market_type": False
        },
        labels={
            "pdew": "Connecting Pax Daily Each Way (PDEW)",
            "yield_per_mile": "O&D Fare Yield ($/mile)",
            "market_type": "Market Segment"
        }
    )

    fig.update_layout(
        title=dict(text="🎯 Unserved Connecting Markets: Demand Density vs Yield Profile", font=dict(size=14, color="#F5F5F7")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8E8E93")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8E8E93")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#F5F5F7", size=10))
    )
    return fig


def build_carrier_premium_bar_chart(df_comp: pd.DataFrame) -> go.Figure:
    """
    Renders horizontal bar chart comparing fares and yields across operators on a route.
    """
    if df_comp.empty:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_comp["unique_carrier"] + " — " + df_comp["carrier_name"],
        x=df_comp["avg_fare"],
        orientation="h",
        marker=dict(color="#0A84FF", opacity=0.9),
        customdata=df_comp[["passenger_share_pct", "yield_per_mile", "fare_premium_vs_min"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Avg O&D Fare: <b>$%{x:.0f}</b><br>"
            "Passenger Share: <b>%{customdata[0]:.1f}%</b><br>"
            "Yield: <b>$%{customdata[1]:.4f}/mi</b><br>"
            "Premium vs Min Carrier: <b>+$%{customdata[2]:.0f}</b>"
            "<extra></extra>"
        )
    ))

    fig.update_layout(
        title=dict(text="Carrier Fare Comparison on Route", font=dict(size=13, color="#F5F5F7")),
        margin=dict(l=10, r=10, t=32, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=240,
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8E8E93")),
        yaxis=dict(showgrid=False, tickfont=dict(color="#F5F5F7"))
    )
    return fig
