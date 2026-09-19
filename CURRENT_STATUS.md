# Current Project Status: AvDB

**Last Updated**: 2026-09-18
**Current Phase**: Phase 20 Delivered (Fleet & Alliances HTML Rendering Fixes, Cabin Class 4-Tier Standardization, Worldwide Airport Coordinate Resolution, and Flighty CSV Parser Robustness)
---

## 🎯 Active Focus
Delivered UI fixes and personal travel log parser robustness:
1. **Fleet & Alliances HTML Leakage Resolution (`3_💺_Fleet_Routes.py`, `5_🌐_Alliances.py`)**:
   - Resolved raw HTML code block leaks on the Fleet and Alliances pages where multiline indented strings passed to `st.markdown` were misinterpreted as `<pre><code>` blocks.
   - Converted engineering spec cards, primary operator pills, and alliance profile cards to `st.html(...)` with unindented HTML structures.
2. **Cabin Class 4-Tier Canonical Standardization (`app/utils/flighty.py`, `4_📱_Flighty_Traveler.py`)**:
   - Built `standardize_cabin_class(...)` mapping micro-brands (Polaris, Delta One, Club World, Comfort+, Premium Class, Economy Plus, Main Cabin Extra, PREMIUM_ECONOMY, etc.) into the 4 canonical industry tiers: **First**, **Business**, **Premium Economy**, **Economy**.
   - Updated the Cabin Class Distribution donut chart to use discrete color mapping: First (`#BF5AF2`), Business (`#0A84FF`), Premium Economy (`#30D158`), Economy (`#FF9F0A`).
3. **Flighty CSV Ingestion Robustness & Worldwide Airport Resolution (`app/utils/flighty.py`)**:
   - Resolved `AttributeError: 'float' object has no attribute 'strip'` when encountering `NaN` or non-string aircraft models, headers, and seats.
   - Built global airport coordinates cache with fallback to `data/ref_airports.csv`, resolving 100% of global airports (79 / 79 in real user travel log) with exact latitude, longitude, and cities.
   - Added `ICAO_TO_IATA` dictionary supporting 3-letter ICAO carrier codes (`SWA`, `ASA`, `BAW`, `VIR`, `EZY`, `RYR`, `ETD`, etc.) for seamless alliance and logo matching.
   - Added Flighty `Seat Type` detection (`WINDOW`, `AISLE`, `MIDDLE`) augmenting seat position classification.
   - Validated real user flight export (`FlightyExport-2026-09-19.csv`) with 308 flights passing 100% of tests.
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
- [x] **Curated Static Peeks for Anchorage 2025 and Alaska Airlines 2025 (`app/data/ref_demo_peeks.py`)**.
- [x] **Verified High-Resolution Photography Catalog with Photographer Credits (`app/data/ref_demo_images.py`)**.
- [x] **Interactive 3D Great-Circle Route Cartography (PyDeck) on Pre-Sign-In Landing**.
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
