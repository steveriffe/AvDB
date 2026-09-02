# Current Project Status: AvDB

**Last Updated**: 2026-09-01
**Current Phase**: Phase 4 — Streamlit Dashboard Engineering (Phase 4.1 - 4.4 Complete)

---

## 🎯 Active Focus
Delivered charter noise filtering ($\ge 10$ flights/yr default), repaired Plotly bar chart hover tooltips, introduced **Unserved Connecting Market Proposals** with Business vs. Leisure yield tagging and carrier strategy alignment, built out **Route Carrier Competition & Fare Premiums**, and fully engineered **Airlines Explorer** (`2_🏢_Airlines.py`) and **Fleet Explorer** (`3_💺_Fleet_Routes.py`).

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
- [x] **Airports Explorer Enhancements**:
  - **Min Flight Frequency Selector**: Default $\ge 10$ flights/yr to filter out 1-off charters (e.g. EUG $\rightarrow$ MAF C5), with options for Weekly+ ($\ge 50$) and Daily ($\ge 365$).
  - **Plotly Tooltip Repair**: Fixed left & right bar charts to render clean multi-line hover cards without raw HTML tags.
  - **Target Destination Proposals**: Extracted top unserved 1-stop connecting O&D markets, PDEW, average fare, yield ($/mile), Business vs. Leisure tags, and hub-strategy aligned carrier assignments.
  - **Multi-Carrier Route Competition**: Route-level carrier market share and fare/yield premium matrix (e.g. Alaska vs Spirit).
- [x] **Airlines Explorer (`app/pages/2_🏢_Airlines.py`)**:
  - Hub & Focus City concentration analysis.
  - Network Yield Curve scatter plot (Stage Length vs Yield $/mile).
  - Hub-aligned strategic expansion target proposals.
- [x] **Fleet Explorer (`app/pages/3_💺_Fleet_Routes.py`)**:
  - Top aircraft models by seat capacity and category (Widebody, Mainline, Regional Jet, Turboprop).
  - Gauge vs. Stage Length economics scatter plot.
  - Detailed equipment deployment table.

---

## ⏳ Next Immediate Steps
1. **Cargo & Freight Lens (Phase 4.5)**: Dedicated dashboard tab for cargo operators (FedEx, UPS, Atlas Air) to track freight tons and mail volume.
2. **Containerization & Deployment (Phase 5)**: Multi-stage Docker containerization and Google Cloud Run deployment with custom SSL domain.
