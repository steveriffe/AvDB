# Current Project Status: AvDB

**Last Updated**: 2026-08-31
**Current Phase**: Phase 4 — Streamlit Dashboard Engineering

---

## 🎯 Active Focus
Completed the Apple-styled **Airport Explorer** page with top KPIs, top 1/3 analytical charts, and large-format bottom 2/3 PyDeck Great-Circle route map. Next: Building the **Airline Network & Yield Explorer** (`app/pages/2_🏢_Airlines.py`).

---

## 📊 Live BigQuery Analytical Marts (`db1b-1.reporting`)

| Mart Table | Rows | Partitioning | Clustering | Core Dimensions & Metrics |
| :--- | :--- | :--- | :--- | :--- |
| `mart_airport_network_summary` | **2,521,106** | `flight_date` (MONTH) | `origin`, `dest`, `unique_carrier` | Direct destinations, pax volume, seat capacity, load factors, DB1B inferred fares, GPS coordinates. |
| `mart_airline_network_performance` | **2,521,106** | `flight_date` (MONTH) | `unique_carrier`, `origin`, `dest` | Available Seat Miles (ASM), RPM, load factors, route market share %, yield per passenger-mile. |
| `mart_fleet_route_dynamics` | **4,040,085** | `flight_date` (MONTH) | `aircraft_family`, `unique_carrier`, `origin` | Equipment types (A320/A321, B738, E175, Widebodies), avg gauge (seats/dep), stage length economics. |
| `ref_airports` | **50,409** | — | `airport_code` | Master airport GPS coordinates, classifications, metro area flags. |
| `ref_city_markets` | **10 Metro Areas** | — | — | Catchment mapping (WAS, NYC, CHI, DFW, LON, etc.). |
| `ref_airport_code_history` | **Historical Mappings** | — | — | Airport closures & relocations (TXL/SXF $\rightarrow$ BER, PFN $\rightarrow$ ECP, etc.). |

---

## ✅ Recently Completed
- [x] Initialized Git repository, `.gitignore`, and synced with GitHub (`steveriffe/AvDB`).
- [x] Built reference data ingestion (`ref_airports`, `ref_city_markets`, `ref_airport_code_history`).
- [x] Defined and materialized 3 analytical marts into `db1b-1:reporting` totaling over 9 million pre-aggregated rows.
- [x] Built **Apple-style UI design system** with sleek KPI cards, minimal typography, and catchment badge pills.
- [x] Built **Airports Explorer Page (`app/pages/1_✈️_Airports.py`)**:
  - Filter bar & 5 top-level KPI cards.
  - Top 1/3: Top 8 Outbound Destinations bar chart + Carrier Capacity Share donut chart.
  - Bottom 2/3: Large-scale PyDeck Great-Circle Arc and Node map with hover tooltips and Mapbox support.
  - Expandable route network data table.

---

## ⏳ Next Immediate Steps
1. **Airline Explorer (`app/pages/2_🏢_Airlines.py`)**: Implement airline network density, hub vs. spoke route breakdown, and fare yield comparisons.
2. **Fleet & Aircraft Page (`app/pages/3_💺_Fleet_Routes.py`)**: Implement gauge trend analysis (up-gauging/down-gauging) and stage-length fleet distribution.
