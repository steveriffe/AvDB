# Current Project Status: AvDB

**Last Updated**: 2026-09-03
**Current Phase**: Phase 5 — Production Containerization, Google OAuth & Custom Domain Deployment (Complete) + Cartographic Redesign

---

## 🎯 Active Focus
Successfully modernized the **AvDB Route Mapping Engine** to authentic **1990s Airline In-Flight Route Map Cartography** across both the **Airports Explorer** and **Airlines Explorer**, replacing oversized 3D parabolic arches with clean 2D surface geodesic great-circle curves, crisp pin nodes, IATA 3-letter code typography via Deck.gl `TextLayer`, concentric bullseye hub markers, and resolving origin hub tooltip placeholder tokens.

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
- [x] **1990s Airline Route Map Cartography Overhaul**:
  - Replaced oversized 3D `ArcLayer` arches with flat 2D `GreatCircleLayer` curves on the map surface (`pitch=0, bearing=0`).
  - Added authentic 3-letter IATA typography labels (`TextLayer`) beside destination nodes with density controls (Top 30 vs All vs Dots Only).
  - Designed classic concentric bullseye hub markers with bold star badges (`★ ORD`).
  - Added vintage cartography presets: Midnight Navy (Dark Matter no-labels), Classic In-Flight Paper (Positron no-labels), and Minimal Slate.
  - Added customizable route colorways: Classic Cobalt, Vintage Crimson, Amber Gold, and Emerald Green.
- [x] **Origin Hub Node Tooltip Fix**:
  - Resolved origin hub node hover card metrics (`{dest}`, `{fmt_pax}`, `{dest_name}`, `{fmt_fare}`, `{fmt_deps}`) with real aggregated outbound values, direct destinations count, and top operating carriers. Zero curly bracket placeholders remaining.
- [x] **Nationwide Route Network Atlas on Airlines Explorer**:
  - Integrated full nationwide route system mapping for carriers on `app/pages/2_🏢_Airlines.py` with primary hub markers and carrier signature colorways.
- [x] **Streamlit 2026 API Modernization**:
  - Replaced deprecated `use_container_width=True` with `width="stretch"` across charts and tables.
- [x] **Production Cloud Run & IONOS Custom Domain (`avdb.riffe.co.uk`)**:
  - Containerized and running live on Google Cloud Run with custom domain and OAuth allowlist protection.

---

## ⏳ Next Immediate Steps & Audit Roadmap
1. **IONOS DNS Record Check**: Verify CNAME propagation (`avdb.riffe.co.uk` $\rightarrow$ `ghs.googlehosted.com.`) for automatic SSL certificate issuance.
2. **O&D Market Audit for Mega-Hubs (ORD, ATL, DFW)**: Revisit unserved connecting market proposals for mega-hubs to ensure seasonal/low-frequency nonstop routes (e.g. FAI, FAT, EUG, BZN) are distinguished from true unserved markets.
3. **Cargo & Freight Lens (Phase 4.5)**: Dedicated dashboard tab for cargo operators (FedEx, UPS, Atlas Air) to track freight tons and mail volume.

