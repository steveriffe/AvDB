# Current Project Status: AvDB

**Last Updated**: 2026-09-18
**Current Phase**: Phase 19 Delivered (Alliances Regional Attribution, Member Carrier Ranking, Fleet Associated Airlines, and Local High-Resolution Carrier Logo Asset Catalog)
---

## 🎯 Active Focus
Delivered major data integrity and UI enhancements for alliances, fleet equipment, and airline branding:
1. **Local High-Resolution Carrier Logo Asset Catalog (`app/assets/logos/`)**:
   - Downloaded and cataloged 61 transparent airline emblems (PNG/SVG) locally in the repository (< 200 KB total).
   - Zero external CDN dependencies, eliminating 404/429 latency and image breakage.
   - Built `get_carrier_logo_url(code)` with base64 Data URI caching (`@lru_cache`).
   - Built `get_carrier_name(code)` with comprehensive friendly airline names, preventing truncated labels ("Alaska Airlines", not "Alas").
2. **Alliances Regional Attribution & Realistic Market Shares**:
   - Integrated route-level regional carrier attribution (`db1b-1.reporting.ref_regional_route_attribution`) into alliance performance queries (`get_alliance_performance_metrics`, `get_alliances_time_series`, `get_alliance_fleet_deployment`).
   - Attributed ~130M regional passenger trips from feeder operators (SkyWest, Republic, Horizon, Endeavor, Envoy, PSA, Piedmont, etc.) to marketing airlines (AA, DL, UA, AS).
   - Real-world 2024 shares: oneworld (26.1%), SkyTeam (19.6%), Star Alliance (18.2%), Independent (36.1% led by Southwest at 177.6M pax).
   - Filtered out DOT air-taxi / commuter survey codes (`02Q`, `07Q`, etc.) with `passengers >= 10,000`.
   - Ranked member carriers by annual passenger volume descending instead of alphabetical order.
3. **Fleet Associated Airlines / Primary Operators**:
   - Updated regional aircraft specs (`ref_aircraft_specs.py`) to list recognized marketing mainlines and major regional operators (`AA`, `DL`, `UA`, `AS`, `OO`, `YX`, `QX`, `9E`, `OH`, `PT`, `C5`).
   - Restyled the Primary Operators strip on the Fleet page with authentic 20x20px emblems, carrier codes, and full airline names in glassmorphic pills.
4. **Alliances UI Modernization**:
   - Replaced squished 10-column cards with responsive flexbox pills displaying the authentic airline emblem, carrier code, friendly name, and annual US passenger volume.
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
