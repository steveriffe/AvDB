# Current Project Status: AvDB

**Last Updated**: 2026-09-17
**Current Phase**: Phase 15 Delivered (Image-Rich Pre-Sign-In Demo Site, Dave Pierce Oil & Gas Road Warrior Dataset 2000–2025, and Zero-BigQuery Wallet Protection)
---

## 🎯 Active Focus
Delivered a high-fidelity, image-rich interactive demo experience accessible before signing in, with **zero BigQuery scan cost**:
1. **Dave Pierce Oil & Gas Road Warrior Dataset (`app/data/dave_roadwarrior_dataset.py`)**:
   - Deterministic 275-flight travel chronicle spanning 26 years (2000–2025) for Dave Pierce, Senior Petroleum Reservoir Engineer & Offshore Operations Director.
   - Centered on 4 core energy nodes: Anchorage (`ANC`), Houston (`IAH`), Hong Kong (`HKG`), and Halifax (`YHZ`), plus reluctant family holidays to Honolulu (`HNL`) and Bali (`DPS`) where Dave shunned the beach to review offshore well logs.
   - Realistically split across Continental/United (`CO`/`UA` ~44.4%), Air Canada (`AC` ~25.8%), Alaska Airlines (`AS` ~21.1%), and Singapore/Garuda (~8.7%).
   - Chronologically accurate fleet matching across 4 distinct eras (737-400, 777-200ER CO 99 polar route, 787-9 Dreamliner, A220-300, 737 MAX 9).
2. **Curated Pre-Computed Platform Peeks (`app/data/ref_demo_peeks.py`)**:
   - Zero-BigQuery snapshots of **Anchorage (`ANC`) 2025** (2.58M pax, 42 direct routes, Alaska Airlines 58.4% share, top 5 routes) and **Alaska Airlines (`AS`) 2025** (46.2M system pax, 172.4 avg gauge, top 5 hubs).
   - Protects BigQuery quotas and budget from unauthenticated web traffic while providing authentic analytical depth.
3. **High-Resolution Photography & Licensing Attribution (`app/data/ref_demo_images.py`)**:
   - High-res photography of all core hubs (ANC, IAH, HKG, YHZ, HNL, DPS) and primary aircraft (777-200ER, 737-900ER, A220-300, 787-9) with verified photographer credits and open licensing.
4. **Interactive Pre-Sign-In UI Component (`app/components/landing.py`)**:
   - 3-tab navigation: Road Warrior Demo, Curated Platform Peeks, and Platform Overview & Sign-In.
   - Geodesic 3D Great-Circle route cartography (PyDeck), Plotly longitudinal analytics (YoY trends, alliance loyalty, seating preference, carrier mix), and a searchable, filterable 275-flight table with CSV export.
5. **Authenticated Flighty Traveler Integration (`app/pages/4_📱_Flighty_Traveler.py`)**:
   - One-click sidebar preset button: `"Load Dave Pierce Log (2000–2025)"` for instant personal analytics exploration.
6. **Validation & Testing**:
   - 100% pass across all regression tests, auth checks, query syntax verification, and API endpoints via `tests/run_all_tests.py`, including new automated tests in `test_dave_pierce_dataset()`.

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
