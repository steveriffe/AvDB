# Current Project Status: AvDB

**Last Updated**: 2026-09-17
**Current Phase**: Phase 17 Delivered (Custom 1990s Aviation Mapbox Style "Jetway Amber", Universal Basemap Default, and Cloud Run Deployment)
---

## 🎯 Active Focus
Delivered a custom 1990s aviation-inspired Mapbox style created programmatically via the Mapbox Styles API:
1. **Custom Style "Jetway Amber" (`mapbox://styles/steveriffe/cmu6drl9x001301rh8c4y170c`)**:
   - Created live via Mapbox Styles API POST endpoint using the admin access token.
   - Inspired by the era of 1990s aviation:
     * **Land**: `hsl(35, 8%, 14%)` — warm graphite, evocative of airport terminal linoleum and 1990s carpet tones.
     * **Water**: `hsl(196, 30%, 9%)` — deep CRT cathode ray blue-green.
     * **Aeroway / Runways**: `hsl(42, 55%, 32%)` — amber highlight, evoking SOLARI split-flap departure boards and amber runway lighting.
     * **Boundaries**: `hsl(210, 30%, 40%)` — faded chartroom blue, like printed aeronautical sectional charts.
     * **Labels**: Warm cream and glowing amber on dark, styled like CRT monitors and paper boarding pass stock.
     * **Atmosphere / Fog**: `hsl(38, 15%, 8%)` warm amber horizon haze.
2. **Platform-Wide Default**:
   - Wired as the universal default across `MAP_THEMES["retro"]`, `app/utils/visualizers.py`, `app/utils/flighty.py`, `1_✈️_Airports.py`, `2_🏢_Airlines.py`, and the pre-sign-in landing preview sandbox.
   - Added `MAPBOX_STYLE_URL_RETRO` to `.env` and Cloud Run deployment configuration.
3. **Deployment**:
   - 100% test pass rate across all suites (`tests/run_all_tests.py`).
   - Live on Cloud Run revision `avdb-00018-fsf` at `https://avdb.riffe.co.uk`.
---

## 📊 Live BigQuery Analytical Marts (`db1b-1.reporting` & `db1b-1.user_travel`)

| Mart / Vault Table | Rows | Partitioning | Clustering | Core Dimensions & Metrics |
| :--- | :--- | :--- | :--- | :--- |
| `mart_airport_network_summary` | **8,532,624** | `flight_date` (MONTH) | `origin`, `dest`, `unique_carrier` | Direct destinations, pax volume, seat capacity, load factors, DB1B inferred fares, GPS coordinates. |
| `mart_airline_network_performance` | **8,532,624** | `flight_date` (MONTH) | `unique_carrier`, `origin`, `dest` | Available Seat Miles (ASM), RPM, load factors, route market share %, yield per passenger-mile. |
| `mart_fleet_route_dynamics` | **13,604,268** | `flight_date` (MONTH) | `aircraft_family`, `unique_carrier`, `origin` | Equipment types (A320/A321, B738, E175, Widebodies), avg gauge (seats/dep), stage length economics. |
| `ref_regional_route_attribution` | **7,024** | — | `origin`, `dest`, `op_carrier` | Route-specific empirical marketing carrier shares from 79.8M DB1B ticket survey coupons. |
| `user_travel.user_flight_logs` | **User Vault** | `created_at` (DAY) | `user_email`, `origin`, `dest`, `carrier_code` | User Flighty segments, subfleet variants, seat positions, CO2 emissions, fail-safe purge controls. |
| `ref_airports` | **50,409** | — | `airport_code` | Master airport GPS coordinates, classifications, metro area flags. |
| `ref_city_markets` | **10 Metro Areas** | — | — | Catchment mapping (WAS, NYC, CHI, DFW, LON, etc.). |
| `ref_airport_code_history` | **Historical Mappings** | — | — | Airport closures & relocations (TXL/SXF $\rightarrow$ BER, PFN $\rightarrow$ ECP, etc.). |

---

## ✅ Recently Completed
- [x] **Image-Rich Pre-Sign-In Demo Experience (`app/components/landing.py`) with Zero-BigQuery Wallet Protection**.
- [x] **Dave Pierce 275-Flight Oil & Gas Travel Chronicle (2000–2025) across ANC, IAH, HKG, YHZ, HNL, DPS**.
- [x] **Curated Static Peeks for Anchorage 2025 and Alaska Airlines 2025 (`app/data/ref_demo_peeks.py`)**.
- [x] **Verified High-Resolution Photography Catalog with Photographer Credits (`app/data/ref_demo_images.py`)**.
- [x] **Interactive 3D Great-Circle Route Cartography (PyDeck) on Pre-Sign-In Landing**.
- [x] **One-Click Dave Pierce Preset in Flighty Traveler (`app/pages/4_📱_Flighty_Traveler.py`)**.
- [x] **Empirical Route-Level Regional Carrier Attribution Engine (`db1b-1.reporting.ref_regional_route_attribution`)**.
- [x] **Longitudinal Time-Series Query Engine (1990–2026) across Airports, Airlines, Fleet, and Alliances**.
- [x] **Global Airline Alliances Lens (`app/pages/5_🌐_Alliances.py`) with NW/KL Wings Alliance**.
- [x] **BigQuery User Travel Vault (`db1b-1.user_travel.user_flight_logs`) with 1,000-Flight Cap & Typed `DELETE` Purge**.
- [x] **Deployed to Google Cloud Run (`avdb-00015-86c`) at `https://avdb.riffe.co.uk`**.
- [x] **Unified Test Suite Passed 100% (`tests/run_all_tests.py`)**.

---

## ⏳ Next Immediate Steps & Audit Roadmap
1. **Phase 1 DB1B Historical Ingestion (2000–2025 Q2)**: Build and run automated PREZIP downloader for quarterly `DB1BMarket` files into `db1b-1.DB1B_RAW.historical_db1b_market`.
2. **Phase 2 Historical Fare Ingestion (1990–1999)**: Ingest early DB1B (1993–1999) and DB1A (1990–1992) from NBER / TranStats archives as planned in `playbook.md`.
3. **Frequent Flyer Partnerships (FFP)**: Formulate data model and catalog for historical airline reciprocal loyalty agreements.
