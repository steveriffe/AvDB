# Current Project Status: AvDB

**Last Updated**: 2026-09-17
**Current Phase**: Phase 16 Delivered (Monochromatic Basemap Default Across Platform, Authentic Product Preview Sandbox, and Dave Pierce Easter Egg)
---

## 🎯 Active Focus
Delivered a realistic, representative, and resource-conscious preview of the AvDB platform:
1. **Monochromatic Basemap as Universal Default**:
   - Updated `app/utils/visualizers.py`, `app/utils/flighty.py`, `app/pages/1_✈️_Airports.py`, and `app/pages/2_🏢_Airlines.py` to make the monochromatic Mapbox basemap (`settings.mapbox_style_mono`) the universal first-choice default across all PyDeck route maps and flight maps.
2. **Authentic Product Preview Sandbox (`app/components/landing.py`)**:
   - Completely eliminated splashy external stock photos of tourist destinations and random aircraft, removing `app/data/ref_demo_images.py`.
   - Rebuilt pre-sign-in landing experience into an interactive 5-tab authentic product preview showcasing the actual tools:
     * **✈️ Airport Explorer Preview**: Interactive monochromatic PyDeck route map of Anchorage (`ANC`) 2025 routes, KPI cards (2.58M pax, +3.4% YoY, 28k dep), and top direct route table.
     * **🏢 Airline Network Preview**: Alaska Airlines (`AS`) 2025 network KPIs (46.2M pax, 382k dep, 172.4 gauge), top hub concentration table (SEA, PDX, ANC, SFO, LAX), and fleet mix table.
     * **💺 Fleet Dynamics Preview**: 36-year interactive Plotly aircraft gauge evolution curve (1990–2026: B737, A320, Regional Jets, Widebodies) illustrating down-gauging to 50-seat RJs and modern up-gauging.
     * **🌐 Alliances Preview**: 36-year global alliance consolidation stacked area chart (Star Alliance, SkyTeam, oneworld, NW/KL Wings 1989–2004).
     * **📱 Personal Traveler Preview**: Real explanation of the Flighty CSV integration, subfleet enrichment, and BigQuery vault.
3. **Dave Pierce as a Tasteful Easter Egg**:
   - Kept Dave Pierce's 275-flight Oil & Gas travel chronicle (2000–2025 across ANC, IAH, HKG, YHZ, HNL, DPS) tucked discreetly inside an interactive expander (`🥚 Easter Egg: Dave Pierce's Road Warrior Log (2000–2025)`) within the Personal Traveler preview tab.
   - Preserved one-click preset loader inside authenticated Flighty Traveler.
4. **Zero-BigQuery Wallet & Quota Protection**:
   - Guaranteed 0 byte BigQuery scans for all unauthenticated visitors and bots hitting the public root URL.
5. **Validation & Testing**:
   - 100% pass across all regression tests, auth checks, query syntax verification, and API endpoints via `tests/run_all_tests.py`.

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
