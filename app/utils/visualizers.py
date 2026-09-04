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
from app.config import settings


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


# Map Themes & Cartography Styles
MAP_THEMES = {
    "personal": settings.mapbox_style_personal or "mapbox://styles/steveriffe/ck6vgf67d0ize1isbb0zwh9vi",
    "love": settings.mapbox_style_love or "mapbox://styles/steveriffe/clo1pnnf2005301q29moshbss",
    "mono": settings.mapbox_style_mono or "mapbox://styles/steveriffe/clkd2zev8001401px6p3m3s8u",
    "dark-v11": "mapbox://styles/mapbox/dark-v11",
    "light-v11": "mapbox://styles/mapbox/light-v11",
    "midnight": "https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json",
    "paper": "https://basemaps.cartocdn.com/gl/positron-nolabels-gl-style/style.json",
    "slate": "dark",
}

ROUTE_COLORWAYS = {
    "cobalt": {
        "line": [10, 132, 255, 195],       # Classic Airline / Apple Cobalt Blue
        "highlight": [100, 210, 255, 255],
        "core": [10, 132, 255, 255],
    },
    "crimson": {
        "line": [224, 40, 40, 205],        # Vintage Northwest / Delta Red
        "highlight": [255, 110, 110, 255],
        "core": [224, 40, 40, 255],
    },
    "gold": {
        "line": [245, 166, 35, 210],       # Continental / Warm Amber Gold
        "highlight": [255, 215, 0, 255],
        "core": [245, 166, 35, 255],
    },
    "emerald": {
        "line": [48, 209, 88, 205],        # Clean Emerald Green
        "highlight": [120, 255, 150, 255],
        "core": [48, 209, 88, 255],
    }
}

CARRIER_BRAND_COLORS = {
    "UA": [0, 90, 180, 200],      # United Classic Blue
    "DL": [186, 12, 47, 210],     # Delta Crimson
    "AA": [0, 114, 206, 200],     # American Blue
    "WN": [245, 130, 32, 210],    # Southwest Orange
    "AS": [0, 110, 140, 220],     # Alaska Teal / Navy
    "B6": [0, 56, 118, 210],      # JetBlue
    "NK": [245, 200, 0, 220],     # Spirit Gold
    "F9": [0, 102, 68, 210],      # Frontier Forest Green
    "G4": [245, 130, 32, 210],    # Allegiant Orange
}


def _format_location(city: Any, state: Any, country: Any = "US") -> str:
    """Safely formats city, state, and country string without accidental trailing parenthesis trimming."""
    city_str = str(city).strip() if pd.notnull(city) and str(city).strip() else ""
    state_str = str(state).strip() if pd.notnull(state) and str(state).strip() else ""
    country_str = str(country).strip() if pd.notnull(country) and str(country).strip() else "US"
    
    parts = [p for p in [city_str, state_str] if p]
    base = ", ".join(parts)
    if base and country_str:
        return f"{base} ({country_str})"
    return base or country_str or ""


def _build_retro_tooltip(theme: str = "midnight") -> dict:
    """Builds a clean Apple/retro route map hover card adapted to light or dark cartography."""
    is_paper = theme == "paper"
    bg = "rgba(250, 250, 252, 0.96)" if is_paper else "rgba(18, 18, 22, 0.94)"
    border = "rgba(0, 0, 0, 0.14)" if is_paper else "rgba(255, 255, 255, 0.14)"
    text_color = "#1D1D1F" if is_paper else "#FFFFFF"
    sub_color = "#6E6E73" if is_paper else "#8E8E93"
    accent_hdr = "#0066CC" if is_paper else "#64D2FF"
    badge_bg = "rgba(0, 102, 204, 0.1)" if is_paper else "rgba(10, 132, 255, 0.2)"
    badge_border = "rgba(0, 102, 204, 0.3)" if is_paper else "rgba(10, 132, 255, 0.4)"
    badge_color = "#0066CC" if is_paper else "#64D2FF"
    metric_color = "#1D1D1F" if is_paper else "#F5F5F7"
    fare_color = "#248A3D" if is_paper else "#30D158"
    hr_color = "rgba(0, 0, 0, 0.08)" if is_paper else "rgba(255, 255, 255, 0.08)"
    shadow = "0 8px 24px rgba(0,0,0,0.12)" if is_paper else "0 12px 32px rgba(0,0,0,0.5)"

    return {
        "html": f"""
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro', 'Inter', 'Helvetica Neue', Arial, sans-serif; font-size: 12px; padding: 10px 14px; background: {bg}; border: 1px solid {border}; border-radius: 12px; backdrop-filter: blur(20px); box-shadow: {shadow}; color: {text_color}; min-width: 220px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-size: 15px; font-weight: 700; color: {accent_hdr}; letter-spacing: -0.02em;">{{tooltip_header}}</span>
                    <span style="background: {badge_bg}; border: 1px solid {badge_border}; color: {badge_color}; font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 6px;">{{badge_text}}</span>
                </div>
                <div style="font-size: 12px; font-weight: 500; color: {metric_color}; margin-bottom: 2px;">{{dest_name}}</div>
                <div style="font-size: 11px; color: {sub_color}; margin-bottom: 8px;">{{location_str}}</div>
                <hr style="margin: 6px 0; border: 0; border-top: 1px solid {hr_color};"/>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 6px;">
                    <div><span style="color: {sub_color}; font-size: 10px; text-transform: uppercase;">{{label_metric1}}</span><br/><b style="font-size: 13px; color: {metric_color};">{{val_metric1}}</b></div>
                    <div><span style="color: {sub_color}; font-size: 10px; text-transform: uppercase;">{{label_metric2}}</span><br/><b style="font-size: 13px; color: {fare_color};">{{val_metric2}}</b></div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 6px;">
                    <div><span style="color: {sub_color}; font-size: 10px; text-transform: uppercase;">{{label_metric3}}</span><br/><b style="font-size: 12px; color: {metric_color};">{{val_metric3}}</b></div>
                    <div><span style="color: {sub_color}; font-size: 10px; text-transform: uppercase;">{{label_metric4}}</span><br/><b style="font-size: 12px; color: {metric_color};">{{val_metric4}}</b></div>
                </div>
                <div style="font-size: 10px; color: {sub_color}; margin-top: 4px;"><b>{{extra_label}}:</b> {{extra_val}}</div>
            </div>
        """,
        "style": {"backgroundColor": "transparent", "color": text_color}
    }


def build_route_map_deck(
    df_routes: pd.DataFrame, 
    origin_meta: Dict[str, Any],
    theme: str = "midnight",
    colorway: str = "cobalt",
    label_density: str = "top30",
    mapbox_api_key: Optional[str] = None,
    mapbox_style: Optional[str] = None
) -> pdk.Deck:
    """
    Builds a clean 1990s airline in-flight route map using 2D geodesic great-circle lines,
    crisp destination node pins, IATA code typography, and a distinctive concentric hub marker.
    """
    if df_routes.empty:
        return pdk.Deck(
            initial_view_state=pdk.ViewState(latitude=39.8, longitude=-98.5, zoom=3.5, pitch=0, bearing=0)
        )

    origin_lat = float(origin_meta.get("latitude", df_routes["origin_lat"].iloc[0]))
    origin_lon = float(origin_meta.get("longitude", df_routes["origin_lon"].iloc[0]))

    # Route colorway selection
    color_spec = ROUTE_COLORWAYS.get(colorway, ROUTE_COLORWAYS["cobalt"])
    line_rgba = color_spec["line"]
    highlight_rgba = color_spec["highlight"]
    hub_core_rgba = color_spec["core"]

    df_plot = df_routes.copy()
    max_pax = df_plot["operational_passengers"].max() or 1
    
    # Crisp 1990s line weighting (1.4 to 3.2px)
    df_plot["route_width"] = (df_plot["operational_passengers"] / max_pax * 1.8 + 1.4).round(2)
    # Destination node radius in pixels
    df_plot["node_radius_px"] = (df_plot["operational_passengers"] / max_pax * 2.0 + 3.5).round(1)

    # Formatted display strings for tooltip
    df_plot["tooltip_header"] = df_plot["dest"]
    df_plot["badge_text"] = df_plot["load_factor_pct"].apply(lambda x: f"LF: {x:.1f}%" if pd.notnull(x) else "—")
    df_plot["dest_name"] = df_plot["dest_name"].fillna(df_plot["dest"])
    df_plot["location_str"] = df_plot.apply(
        lambda r: _format_location(r.get("dest_city"), r.get("dest_state"), r.get("dest_country", "US")),
        axis=1
    )
    df_plot["label_metric1"] = "Passengers"
    df_plot["val_metric1"] = df_plot["operational_passengers"].apply(lambda x: f"{x/1e6:.2f}M" if x >= 1e6 else f"{x:,}")
    df_plot["label_metric2"] = "Inferred Fare"
    df_plot["val_metric2"] = df_plot["avg_od_fare"].apply(lambda x: f"${x:.0f}" if pd.notnull(x) and x > 0 else "N/A")
    df_plot["label_metric3"] = "Departures"
    df_plot["val_metric3"] = df_plot["departures_performed"].apply(lambda x: f"{x:,}")
    df_plot["label_metric4"] = "Seats / Dep"
    df_plot["val_metric4"] = df_plot["avg_gauge_seats"].apply(lambda x: f"{x:.0f}" if pd.notnull(x) else "—")
    df_plot["extra_label"] = "Operating Carriers"
    df_plot["extra_val"] = df_plot["operating_carriers"].fillna("Direct Service")

    # Legacy variables for compatibility
    df_plot["fmt_pax"] = df_plot["val_metric1"]
    df_plot["fmt_fare"] = df_plot["val_metric2"]
    df_plot["fmt_lf"] = df_plot["load_factor_pct"].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "—")
    df_plot["fmt_deps"] = df_plot["val_metric3"]

    # 1. 2D Surface Geodesic Great-Circle Layer (Flat on map, getHeight=0)
    route_layer = pdk.Layer(
        "GreatCircleLayer",
        data=df_plot,
        get_source_position=["origin_lon", "origin_lat"],
        get_target_position=["dest_lon", "dest_lat"],
        get_source_color=line_rgba,
        get_target_color=line_rgba,
        get_width="route_width",
        width_min_pixels=1.5,
        width_max_pixels=4.0,
        get_height=0,  # 2D surface geodesic curve!
        pickable=True,
        auto_highlight=True,
        highlight_color=highlight_rgba,
    )

    # 2. Destination Node Pin Layer (Crisp fixed-pixel dots)
    node_fill = [255, 255, 255, 235] if theme != "paper" else [30, 35, 45, 235]
    node_stroke = line_rgba[:3] + [240] if theme != "paper" else [255, 255, 255, 255]

    dest_node_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_plot,
        get_position=["dest_lon", "dest_lat"],
        get_radius="node_radius_px",
        radius_min_pixels=3.2,
        radius_max_pixels=6.0,
        radius_units="pixels",
        get_fill_color=node_fill,
        get_line_color=node_stroke,
        line_width_min_pixels=1.5,
        stroked=True,
        filled=True,
        pickable=True,
        auto_highlight=True,
        highlight_color=highlight_rgba,
    )

    # 3. Origin Hub Node Setup (Thoroughly resolves all values so no placeholder curly brackets remain)
    total_pax = df_plot["operational_passengers"].sum()
    total_deps = df_plot["departures_performed"].sum()
    total_seats = df_plot["total_seats"].sum() if "total_seats" in df_plot.columns else 0
    network_lf = (total_pax / total_seats * 100) if total_seats > 0 else 0.0
    dest_count = len(df_plot["dest"].dropna().unique())
    avg_fare_mean = df_plot["avg_od_fare"].dropna().mean() if not df_plot["avg_od_fare"].dropna().empty else 0

    all_carriers = []
    for c_str in df_plot["operating_carriers"].dropna():
        all_carriers.extend([c.strip() for c in c_str.split(",") if c.strip()])
    top_carriers_str = ", ".join(pd.Series(all_carriers).value_counts().head(5).index) if all_carriers else "Direct Carriers"

    origin_code = origin_meta.get("airport_code", df_routes["origin"].iloc[0] if "origin" in df_routes.columns else "HUB")
    origin_name = origin_meta.get("airport_name", df_routes["origin_name"].iloc[0] if "origin_name" in df_routes.columns else f"{origin_code} International")
    origin_city = origin_meta.get("city", df_routes["origin_city"].iloc[0] if "origin_city" in df_routes.columns else "")
    origin_state = origin_meta.get("state", df_routes["origin_state"].iloc[0] if "origin_state" in df_routes.columns else "")
    origin_country = origin_meta.get("country", df_routes["origin_country"].iloc[0] if "origin_country" in df_routes.columns else "US")
    origin_location = _format_location(origin_city, origin_state, origin_country) or origin_name

    origin_dict = {
        "lon": origin_lon,
        "lat": origin_lat,
        "code": origin_code,
        "name": origin_name,
        "hub_label": f"★ {origin_code}",
        "tooltip_header": f"🏛️ {origin_code} [ORIGIN HUB]",
        "badge_text": f"LF: {network_lf:.1f}% Avg",
        "dest_name": origin_name,
        "location_str": origin_location,
        "label_metric1": "Total Outbound Pax",
        "val_metric1": f"{total_pax/1e6:.2f}M" if total_pax >= 1e6 else f"{total_pax:,}",
        "label_metric2": "Network Reach",
        "val_metric2": f"{dest_count} Destinations",
        "label_metric3": "Departures",
        "val_metric3": f"{total_deps:,}",
        "label_metric4": "Avg Network Gauge",
        "val_metric4": f"{(total_seats/total_deps):.0f} seats" if total_deps > 0 else "—",
        "extra_label": "Top Operating Carriers",
        "extra_val": top_carriers_str,
        # Legacy mappings
        "dest": f"🏛️ {origin_code}",
        "dest_city": origin_city,
        "dest_state": origin_state,
        "dest_country": origin_country,
        "fmt_pax": f"{total_pax/1e6:.2f}M" if total_pax >= 1e6 else f"{total_pax:,}",
        "fmt_fare": f"${avg_fare_mean:.0f}" if avg_fare_mean > 0 else "—",
        "fmt_lf": f"{network_lf:.1f}%",
        "fmt_deps": f"{total_deps:,}",
        "avg_gauge_seats": f"{(total_seats/total_deps):.0f}" if total_deps > 0 else "—",
        "operating_carriers": top_carriers_str,
    }
    origin_df = pd.DataFrame([origin_dict])

    # Concentric Bullseye Ring Marker for Origin Hub
    hub_ring_stroke = [255, 255, 255, 240] if theme != "paper" else [30, 35, 45, 240]
    origin_ring_layer = pdk.Layer(
        "ScatterplotLayer",
        data=origin_df,
        get_position=["lon", "lat"],
        get_radius=10,
        radius_min_pixels=8.5,
        radius_max_pixels=13.0,
        radius_units="pixels",
        get_line_color=hub_ring_stroke,
        line_width_min_pixels=2.2,
        stroked=True,
        filled=False,
        pickable=False,
    )

    origin_core_layer = pdk.Layer(
        "ScatterplotLayer",
        data=origin_df,
        get_position=["lon", "lat"],
        get_radius=5.5,
        radius_min_pixels=4.5,
        radius_max_pixels=7.5,
        radius_units="pixels",
        get_fill_color=hub_core_rgba,
        get_line_color=[255, 255, 255, 255] if theme != "paper" else [30, 35, 45, 255],
        line_width_min_pixels=1.8,
        stroked=True,
        filled=True,
        pickable=True,
        auto_highlight=True,
        highlight_color=highlight_rgba,
    )

    hub_text_color = [255, 255, 255, 255] if theme != "paper" else [20, 25, 35, 255]
    origin_text_layer = pdk.Layer(
        "TextLayer",
        data=origin_df,
        get_position=["lon", "lat"],
        get_text="hub_label",
        get_size=12,
        get_color=hub_text_color,
        get_pixel_offset=[12, -4],
        get_text_anchor='"start"',
        get_alignment_baseline='"center"',
        font_family='-apple-system, BlinkMacSystemFont, "SF Pro", "Inter", "Helvetica Neue", Arial, sans-serif',
        font_weight='"bold"',
        pickable=False,
    )

    layers = [route_layer, dest_node_layer, origin_ring_layer, origin_core_layer, origin_text_layer]

    # 4. Destination 3-Letter IATA Code Typography Layer
    if label_density != "none":
        if label_density == "top30":
            df_labels = df_plot.head(30)
        else:  # "all"
            df_labels = df_plot

        label_color = [240, 240, 245, 230] if theme != "paper" else [25, 30, 40, 240]
        dest_text_layer = pdk.Layer(
            "TextLayer",
            data=df_labels,
            get_position=["dest_lon", "dest_lat"],
            get_text="dest",
            get_size=10.5,
            get_color=label_color,
            get_pixel_offset=[6, -2],
            get_text_anchor='"start"',
            get_alignment_baseline='"center"',
            font_family='-apple-system, BlinkMacSystemFont, "SF Pro", "Inter", "Helvetica Neue", Arial, sans-serif',
            font_weight='"bold"',
            pickable=False,
        )
        layers.append(dest_text_layer)

    # 2D Flat Planar View State (pitch=0, bearing=0)
    view_state = pdk.ViewState(
        latitude=origin_lat,
        longitude=origin_lon,
        zoom=3.8,
        min_zoom=2.2,
        max_zoom=10,
        pitch=0,     # Pure 2D!
        bearing=0,
    )

    token = mapbox_api_key or settings.mapbox_token or os.getenv("MAPBOX_ACCESS_TOKEN_PUBLIC", "") or os.getenv("MAPBOX_API_KEY", "")
    map_style = mapbox_style or MAP_THEMES.get(theme, MAP_THEMES["personal"] if token else MAP_THEMES["midnight"])

    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip=_build_retro_tooltip(theme),
        map_style=map_style,
        api_keys={"mapbox": token} if token else None
    )


def build_airline_network_deck(
    df_routes: pd.DataFrame,
    hub_codes: list[str],
    carrier_code: str = "UA",
    carrier_name: str = "Airline",
    theme: str = "midnight",
    colorway: str = "auto",
    label_density: str = "hubs_only",
    mapbox_api_key: Optional[str] = None,
    mapbox_style: Optional[str] = None
) -> pdk.Deck:
    """
    Builds a nationwide carrier route network map in classic 1990s airline atlas style.
    Highlights primary hubs with bullseye markers and draws network routes flat on the map surface.
    """
    if df_routes.empty:
        return pdk.Deck(
            initial_view_state=pdk.ViewState(latitude=39.8, longitude=-98.5, zoom=3.5, pitch=0, bearing=0)
        )

    # Resolve colorway (auto uses carrier brand color)
    if colorway == "auto" and carrier_code in CARRIER_BRAND_COLORS:
        line_rgba = CARRIER_BRAND_COLORS[carrier_code]
        highlight_rgba = [255, 255, 255, 255]
        hub_core_rgba = line_rgba[:3] + [255]
    else:
        color_spec = ROUTE_COLORWAYS.get(colorway, ROUTE_COLORWAYS["cobalt"])
        line_rgba = color_spec["line"]
        highlight_rgba = color_spec["highlight"]
        hub_core_rgba = color_spec["core"]

    df_plot = df_routes.copy()
    max_pax = df_plot["operational_passengers"].max() or 1
    df_plot["route_width"] = (df_plot["operational_passengers"] / max_pax * 1.6 + 1.3).round(2)

    df_plot["tooltip_header"] = df_plot["origin"] + " ➔ " + df_plot["dest"]
    df_plot["badge_text"] = df_plot["load_factor_pct"].apply(lambda x: f"LF: {x:.1f}%" if pd.notnull(x) else "—")
    df_plot["dest_name"] = df_plot["dest_name"].fillna(df_plot["dest"])
    df_plot["location_str"] = df_plot.apply(
        lambda r: _format_location(r.get("dest_city"), r.get("dest_state"), r.get("dest_country", "US")), axis=1
    )
    df_plot["label_metric1"] = "Passengers"
    df_plot["val_metric1"] = df_plot["operational_passengers"].apply(lambda x: f"{x/1e6:.2f}M" if x >= 1e6 else f"{x:,}")
    df_plot["label_metric2"] = "Inferred Fare"
    df_plot["val_metric2"] = df_plot["avg_od_fare"].apply(lambda x: f"${x:.0f}" if pd.notnull(x) and x > 0 else "N/A")
    df_plot["label_metric3"] = "Departures"
    df_plot["val_metric3"] = df_plot["departures_performed"].apply(lambda x: f"{x:,}")
    df_plot["label_metric4"] = "Seats / Dep"
    df_plot["val_metric4"] = df_plot["avg_gauge_seats"].apply(lambda x: f"{x:.0f}" if pd.notnull(x) else "—")
    df_plot["extra_label"] = "Carrier"
    df_plot["extra_val"] = f"{carrier_name} ({carrier_code})"

    # 1. 2D Geodesic Great-Circle Route Network
    route_layer = pdk.Layer(
        "GreatCircleLayer",
        data=df_plot,
        get_source_position=["origin_lon", "origin_lat"],
        get_target_position=["dest_lon", "dest_lat"],
        get_source_color=line_rgba,
        get_target_color=line_rgba,
        get_width="route_width",
        width_min_pixels=1.2,
        width_max_pixels=3.5,
        get_height=0,
        pickable=True,
        auto_highlight=True,
        highlight_color=highlight_rgba,
    )

    # 2. Extract unique airports in network
    origins = df_plot[["origin", "origin_name", "origin_city", "origin_lat", "origin_lon"]].rename(
        columns={"origin": "airport_code", "origin_name": "name", "origin_city": "city", "origin_lat": "lat", "origin_lon": "lon"}
    )
    dests = df_plot[["dest", "dest_name", "dest_city", "dest_lat", "dest_lon"]].rename(
        columns={"dest": "airport_code", "dest_name": "name", "dest_city": "city", "dest_lat": "lat", "dest_lon": "lon"}
    )
    df_airports = pd.concat([origins, dests]).drop_duplicates(subset=["airport_code"]).dropna(subset=["lat", "lon"])
    df_airports["is_hub"] = df_airports["airport_code"].isin(hub_codes)

    df_hubs = df_airports[df_airports["is_hub"]].copy()
    df_spokes = df_airports[~df_airports["is_hub"]].copy()

    # Tooltip data for hub nodes
    df_hubs["tooltip_header"] = "🏛️ " + df_hubs["airport_code"] + " [PRIMARY HUB]"
    df_hubs["badge_text"] = "HUB"
    df_hubs["dest_name"] = df_hubs["name"].fillna(df_hubs["airport_code"])
    df_hubs["location_str"] = df_hubs["city"].fillna("")
    df_hubs["label_metric1"] = "Role"
    df_hubs["val_metric1"] = "Primary Network Hub"
    df_hubs["label_metric2"] = "Carrier"
    df_hubs["val_metric2"] = carrier_code
    df_hubs["label_metric3"] = "Network"
    df_hubs["val_metric3"] = carrier_name
    df_hubs["label_metric4"] = "Type"
    df_hubs["val_metric4"] = "Transfer Gateway"
    df_hubs["extra_label"] = "Status"
    df_hubs["extra_val"] = "Core Hub Operations"
    df_hubs["hub_label"] = "★ " + df_hubs["airport_code"]

    # Spoke nodes
    node_fill = [255, 255, 255, 220] if theme != "paper" else [30, 35, 45, 220]
    spoke_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_spokes,
        get_position=["lon", "lat"],
        radius_min_pixels=2.8,
        radius_max_pixels=4.5,
        radius_units="pixels",
        get_fill_color=node_fill,
        get_line_color=line_rgba[:3] + [220] if theme != "paper" else [255, 255, 255, 255],
        line_width_min_pixels=1.2,
        stroked=True,
        filled=True,
        pickable=False,
    )

    # Hub Outer Rings & Cores
    hub_ring_stroke = [255, 255, 255, 240] if theme != "paper" else [30, 35, 45, 240]
    hub_ring_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_hubs,
        get_position=["lon", "lat"],
        radius_min_pixels=8.0,
        radius_max_pixels=12.0,
        radius_units="pixels",
        get_line_color=hub_ring_stroke,
        line_width_min_pixels=2.0,
        stroked=True,
        filled=False,
        pickable=False,
    )

    hub_core_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_hubs,
        get_position=["lon", "lat"],
        radius_min_pixels=4.5,
        radius_max_pixels=7.0,
        radius_units="pixels",
        get_fill_color=hub_core_rgba,
        get_line_color=[255, 255, 255, 255] if theme != "paper" else [30, 35, 45, 255],
        line_width_min_pixels=1.5,
        stroked=True,
        filled=True,
        pickable=True,
        auto_highlight=True,
        highlight_color=highlight_rgba,
    )

    # Hub Typography Labels
    hub_label_color = [255, 255, 255, 255] if theme != "paper" else [20, 25, 35, 255]
    hub_text_layer = pdk.Layer(
        "TextLayer",
        data=df_hubs,
        get_position=["lon", "lat"],
        get_text="hub_label",
        get_size=11.5,
        get_color=hub_label_color,
        get_pixel_offset=[10, -4],
        get_text_anchor='"start"',
        get_alignment_baseline='"center"',
        font_family='-apple-system, BlinkMacSystemFont, "SF Pro", "Inter", "Helvetica Neue", Arial, sans-serif',
        font_weight='"bold"',
        pickable=False,
    )

    layers = [route_layer, spoke_layer, hub_ring_layer, hub_core_layer, hub_text_layer]

    # Additional text labels for top spoke destinations if requested
    if label_density == "all":
        spoke_label_color = [235, 235, 240, 210] if theme != "paper" else [35, 40, 50, 210]
        spoke_text_layer = pdk.Layer(
            "TextLayer",
            data=df_spokes.head(35),
            get_position=["lon", "lat"],
            get_text="airport_code",
            get_size=9.5,
            get_color=spoke_label_color,
            get_pixel_offset=[5, -2],
            get_text_anchor='"start"',
            get_alignment_baseline='"center"',
            font_family='-apple-system, BlinkMacSystemFont, "SF Pro", "Inter", "Helvetica Neue", Arial, sans-serif',
            font_weight='"bold"',
            pickable=False,
        )
        layers.append(spoke_text_layer)

    # Centered on Continental US
    view_state = pdk.ViewState(
        latitude=39.5,
        longitude=-98.35,
        zoom=3.6,
        min_zoom=2.5,
        max_zoom=10,
        pitch=0,
        bearing=0,
    )

    token = mapbox_api_key or settings.mapbox_token or os.getenv("MAPBOX_ACCESS_TOKEN_PUBLIC", "") or os.getenv("MAPBOX_API_KEY", "")
    map_style = mapbox_style or MAP_THEMES.get(theme, MAP_THEMES["personal"] if token else MAP_THEMES["midnight"])

    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip=_build_retro_tooltip(theme),
        map_style=map_style,
        api_keys={"mapbox": token} if token else None
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
