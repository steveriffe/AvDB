# Current Project Status: AvDB

**Last Updated**: 2026-09-07
**Current Phase**: Phase 9.7 Delivered (Packaging Fix for app.data, Open Google Authentication, Auth Gating, Fleet & Historical KPI Bug Fixes)
---

## 🎯 Active Focus
Delivered the comprehensive analytical and engineering roadmap enhancements requested:
1. **Packaging & Build Fix for `app.data`**: Corrected `.dockerignore` and `.gcloudignore` from unanchored `data/` to `/data/` and `!app/data/`, ensuring `ref_mergers.py`, `ref_aircraft_specs.py`, `ref_alliances.py` are packaged into Cloud Run builds. Added `ENV PYTHONPATH=/app` in `Dockerfile`.
2. **Open Registration for All Google Authenticated Users**: Opened access so any user authenticating via Google can use AvDB (`ALLOWED_EMAILS=*`).
3. **Sidebar Auth Navigation Gating**: Hid `[data-testid='stSidebarNav']` when users are unauthenticated, preventing access to subpages before sign-in, and relocated `require_auth()` before heavy imports on all pages.
4. **Fleet Explorer KPI Keyword Fix**: Fixed `TypeError: unexpected keyword argument 'title'` in `render_kpi_card` and added backward-compatible `title` alias support.
5. **Historical Carriers & Airport Null-Safety**: Fixed `TypeError: '>=' not supported between instances of 'NoneType' and 'int'` when selecting historical carriers or empty route years.
6. **Mapbox Public Token Resolution**: Fixed `1_✈️_Airports.py` to use `settings.mapbox_token` instead of looking for unset `MAPBOX_API_KEY`.
7. **Unified Automated Test Suite**: Created `tests/run_all_tests.py` verifying all test suites and regression guards in a single run.

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
- [x] **Airline Alliances & Branding Tracker (Phase 6)**:
  - Built `app/data/ref_alliances.py` and `app/data/alliances_history.json` containing 50+ historical membership intervals across Star Alliance, oneworld, SkyTeam, Wings Alliance, and Qualiflyer.
  - Tracked historic alliance transitions (SAS: Star Alliance 1997 $\rightarrow$ SkyTeam 2024; Aer Lingus: oneworld $\rightarrow$ Independent; Continental: Wings $\rightarrow$ SkyTeam $\rightarrow$ Star Alliance $\rightarrow$ UA merger; US Airways: Star Alliance $\rightarrow$ oneworld $\rightarrow$ AA merger; Mexicana, TAM/LAN).
  - Integrated high-res SVG carrier logos and active alliance badges into the Airlines Explorer with expandable corporate transition timelines.
- [x] **Flighty Integration & Subfleet Analytics (Phase 7)**:
  - Built `app/utils/flighty.py` and `app/pages/4_📱_Flighty_Traveler.py` for drag-and-drop CSV export ingestion.
  - Built 3-tier subfleet taxonomy engine (Exact Subfleet e.g. 737-900ER vs 737-800 vs MAX 9; Generation e.g. 737 NextGen vs MAX; Family e.g. Boeing 737).
  - Designed personal 1990s in-flight route map with flight frequency arc weighting and custom Mapbox styles.
  - Provided a 1-click "Load Sample Log" generating 30 realistic flights for instant previewing.
- [x] **Native Apple iOS App & FastAPI Backend (Phase 8)**:
  - Built native Swift Package / Xcode structure in `ios/AvDB/` following Apple HIG and Liquid Glass styling.
  - Native 120Hz Apple MapKit geodesic route map with concentric hub bullseyes and IATA typography annotations.
  - Native `.fileImporter` iOS file picker for Flighty CSV files with offline parsing and lifetime flight KPIs.
  - Built production FastAPI backend service in `api/` with BigQuery wallet safeguards and in-memory caching.
  - Authored step-by-step pairing and physical iPhone deployment guide in `ios/README.md`.
- [x] **1990s Airline Route Map Cartography Overhaul (Phase 5)**:
  - Flat 2D `GreatCircleLayer` curves on the map surface (`pitch=0, bearing=0`).
  - Authentic 3-letter IATA typography labels (`TextLayer`) beside destination nodes.
  - Concentric bullseye hub markers with bold star badges (`★ ORD`).
  - Integrated custom Mapbox styles (`personal`, `love`, `mono`) and tokens.
- [x] **Production Cloud Run & IONOS Custom Domain (`avdb.riffe.co.uk`)**:
  - Live on Google Cloud Run with custom domain, local auth bypass (`LOCAL_DEV_BYPASS_AUTH=true`), and OAuth allowlist protection.

---

## ⏳ Next Immediate Steps & Audit Roadmap
1. **IONOS DNS Record Check**: Verify CNAME propagation (`avdb.riffe.co.uk` $\rightarrow$ `ghs.googlehosted.com.`) for automatic SSL certificate issuance.
2. **O&D Market Audit for Mega-Hubs (ORD, ATL, DFW)**: Revisit unserved connecting market proposals for mega-hubs to ensure seasonal/low-frequency nonstop routes (e.g. FAI, FAT, EUG, BZN) are distinguished from true unserved markets.
3. **Cargo & Freight Lens (Phase 4.5)**: Dedicated dashboard tab for cargo operators (FedEx, UPS, Atlas Air) to track freight tons and mail volume.

