# Current Project Status: AvDB

**Last Updated**: 2026-09-17
**Current Phase**: Phase 14 Delivered (Empirical Regional Carrier Attribution via DOT DB1B 10% Ticket Survey & Proportional Mainline Splitting)
---

## 🎯 Active Focus
Delivered empirical route-level regional carrier attribution and multi-carrier capacity splitting across the AvDB dashboard suite:
1. **Empirical BigQuery Route Attribution Table (`db1b-1.reporting.ref_regional_route_attribution`)**:
   - Materialized from 79.8M records in `OD40_DB1B_RAW` across 7,024 regional route pairs (`op_carrier`, `origin`, `dest`, `mkt_carrier`, `sample_coupons`, `attribution_share`, `is_primary`).
   - Replaced fragile hub-only heuristics with empirical ticketing data: e.g. on EUG-SEA, SkyWest (`OO`) tickets are proportionally attributed as 66.4% Delta (`DL`) and 33.6% Alaska (`AS`); EUG-LAX is 98.2% Alaska (`AS`); EUG-PDX is 99.9% Alaska (`AS`).
   - Integrated deterministic subsidiary mappings for dedicated regional operators: Horizon `QX` $\rightarrow$ `AS`, Endeavor `9E` $\rightarrow$ `DL`, Envoy/PSA/Piedmont `MQ`/`OH`/`PT` $\rightarrow$ `AA`, CommuteAir/GoJet `C5`/`G7` $\rightarrow$ `UA`, Compass `CP` $\rightarrow$ `DL`.
2. **Query Engine Modernization (`app/utils/queries.py`)**:
   - `get_airport_kpis`: Attributed regional flights so `leading_carrier` reflects true consumer brands (e.g. EUG correctly reflects Alaska Airlines `AS` as the market leader with ~36% share).
   - `get_airport_routes_dataset`: Route details aggregate marketing brands (`AS, DL`) rather than raw metal (`OO, QX`).
   - `get_airport_carrier_breakdown`: Proportional route splitting credits Alaska with mainline `AS` + Horizon `QX` + Alaska SkyWest `OO[AS]`, and Delta with `DL` + Delta SkyWest `OO[DL]`.
   - `get_route_carrier_competition`: Route-level competition head-to-head compares mainline brands directly.
   - `get_airport_time_series`: Fixed `top_carrier` over 1990–2026 to reflect marketing carriers, accurately showing Alaska (`AS`) dominant across 2013–2021 and 2025–2026 at EUG.
   - `get_airline_kpis`, `get_airline_hubs`, `get_airline_yield_curve`, `get_airline_routes_dataset`, `get_airline_time_series`: Added `include_regionals: bool = True` support, allowing airlines like Alaska (`AS`) to capture their full 46M-passenger network.
3. **UI Enhancements**:
   - **Airports Tab**: Added attribution methodology notice explaining the empirical DOT DB1B ticket survey route-splitting.
   - **Airlines Tab**: Added `Network Scope` selector ("Full Network (inc. Regionals)" vs "Mainline Metal Only") defaulting to Full Network.
4. **Validation & Testing**:
   - 100% pass across all regression tests, auth checks, query syntax verification, and API endpoints via `tests/run_all_tests.py`, including automated assertions in `test_regional_carrier_attribution()`.

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
- [x] **Empirical Route-Level Regional Carrier Attribution Engine (`db1b-1.reporting.ref_regional_route_attribution`)**.
- [x] **Proportional Multi-Carrier SkyWest Splitting on Dual-Hub Corridors (e.g. EUG-SEA, SEA-GEG, etc.)**.
- [x] **Network Scope Toggle in Airlines Explorer ("Full Network (inc. Regionals)" vs "Mainline Metal Only")**.
- [x] **Regional Carrier Attribution Test Suite (`test_regional_carrier_attribution`) passing 100%**.
- [x] **Longitudinal Time-Series Query Engine (1990–2026) across Airports, Airlines, Fleet, and Alliances**.
- [x] **Macro-Shock Historical Annotations (9/11, GFC, COVID-19)**.
- [x] **YoY Delta Growth Tracking on Core KPI Cards**.
- [x] **Expandable Historical Trend Modules across All Primary Dashboard Pages**.
- [x] **Global Airline Alliances Lens (`app/pages/5_🌐_Alliances.py`) with NW/KL Wings Alliance**.
- [x] **BigQuery User Travel Vault (`db1b-1.user_travel.user_flight_logs`) with 1,000-Flight Cap & Typed `DELETE` Purge**.
- [x] **User Privacy Policy Page (`app/pages/6_🔒_Privacy_Policy.py`)**.
- [x] **Deployed to Google Cloud Run (`avdb-00014-b4v`) at `https://avdb.riffe.co.uk`**.
- [x] **Unified Test Suite Passed 100% (`tests/run_all_tests.py`)**.

---

## ⏳ Next Immediate Steps & Audit Roadmap
1. **Phase 1 DB1B Historical Ingestion (2000–2025 Q2)**: Build and run automated PREZIP downloader for quarterly `DB1BMarket` files into `db1b-1.DB1B_RAW.historical_db1b_market`.
2. **Phase 2 Historical Fare Ingestion (1990–1999)**: Ingest early DB1B (1993–1999) and DB1A (1990–1992) from NBER / TranStats archives as planned in `playbook.md`.
3. **Frequent Flyer Partnerships (FFP)**: Formulate data model and catalog for historical airline reciprocal loyalty agreements.
