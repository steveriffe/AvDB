# Current Project Status: AvDB

**Last Updated**: 2026-09-17
**Current Phase**: Phase 13 Delivered (Longitudinal Time-Series Analytics & Trending Over Time 1990–2026 across Airports, Airlines, Fleet & Alliances)
---

## 🎯 Active Focus
Delivered comprehensive longitudinal trending over time across the AvDB dashboard suite:
1. **Longitudinal Time-Series Query Engine (`app/utils/queries.py`)**:
   - `get_airport_time_series`: Aggregates 1990–2026 passenger volume, commercial departures, seat capacity, load factors, route breadth, and YoY % growth rates.
   - `get_airline_time_series`: Tracks 36-year carrier evolution with ASM, RPM, system load factors, network route counts, and YoY growth.
   - `get_fleet_time_series`: Analyzes 36-year aircraft gauge (average seats per departure) across major aircraft families (A320, B737, B777, E175, CRJ, etc.).
   - `get_alliances_time_series`: Longitudinal market share transition from the 1989 NW/KL Wings alliance to Star Alliance, SkyTeam, and oneworld.
2. **Interactive Visualizers (`app/utils/visualizers.py`)**:
   - Airport Growth Trend Chart: Dual-axis volume and load factor curve with historical macro-shock annotations (9/11 in 2001, Global Financial Crisis in 2008, COVID-19 in 2020).
   - Airline Capacity & Yield Trajectory: Clustered ASM vs RPM bar comparison with superimposed system load factor trendline.
   - Aircraft Gauge Evolution: Multi-line chart illustrating the up-gauging shift from regional jets back into higher-capacity narrowbodies and widebodies.
   - Alliance Market Share Evolution: 100% stacked area visualization tracking alliance consolidation.
3. **Cross-Dashboard UI Integration**:
   - **Airports Tab**: Displays annual passenger volume with automated YoY delta badge, plus an interactive "Multi-Year Growth Timeline (1990–2026)" expander highlighting all-time traffic peaks and long-term expansion.
   - **Airlines Tab**: Displays departures with YoY comparison, accompanied by an interactive "Historical Network Trajectory (1990–2026)" expander highlighting peak capacity milestones and route counts.
   - **Fleet & Routes Tab**: Features a dedicated "Three-Decade Aircraft Gauge Evolution" expander illustrating fleet up-gauging trends.
   - **Alliances Tab**: Includes an "Alliance Market Share Evolution (1990–2026)" expander showing 36 years of global consolidation touching US gateways.
4. **Validation & Testing**:
   - 100% pass across all regression tests, auth checks, query syntax verification, and API endpoints via `tests/run_all_tests.py`.
   - Verified BigQuery schema alignment across all time-series queries: fixed `PARTITION BY` non-grouped column references in `get_airport_time_series`, corrected `available_seat_miles`/`revenue_passenger_miles` in `get_airline_time_series`, and `operational_passengers` in `get_fleet_time_series`.

---

## 📊 Live BigQuery Analytical Marts (`db1b-1.reporting` & `db1b-1.user_travel`)

| Mart / Vault Table | Rows | Partitioning | Clustering | Core Dimensions & Metrics |
| :--- | :--- | :--- | :--- | :--- |
| `mart_airport_network_summary` | **8,532,624** | `flight_date` (MONTH) | `origin`, `dest`, `unique_carrier` | Direct destinations, pax volume, seat capacity, load factors, DB1B inferred fares, GPS coordinates. |
| `mart_airline_network_performance` | **8,532,624** | `flight_date` (MONTH) | `unique_carrier`, `origin`, `dest` | Available Seat Miles (ASM), RPM, load factors, route market share %, yield per passenger-mile. |
| `mart_fleet_route_dynamics` | **13,604,268** | `flight_date` (MONTH) | `aircraft_family`, `unique_carrier`, `origin` | Equipment types (A320/A321, B738, E175, Widebodies), avg gauge (seats/dep), stage length economics. |
| `user_travel.user_flight_logs` | **User Vault** | `created_at` (DAY) | `user_email`, `origin`, `dest`, `carrier_code` | User Flighty segments, subfleet variants, seat positions, CO2 emissions, fail-safe purge controls. |
| `ref_airports` | **50,409** | — | `airport_code` | Master airport GPS coordinates, classifications, metro area flags. |
| `ref_city_markets` | **10 Metro Areas** | — | — | Catchment mapping (WAS, NYC, CHI, DFW, LON, etc.). |
| `ref_airport_code_history` | **Historical Mappings** | — | — | Airport closures & relocations (TXL/SXF $\rightarrow$ BER, PFN $\rightarrow$ ECP, etc.). |

---

## ✅ Recently Completed
- [x] **Longitudinal Time-Series Query Engine (1990–2026) across Airports, Airlines, Fleet, and Alliances**.
- [x] **Macro-Shock Historical Annotations (9/11, GFC, COVID-19)**.
- [x] **YoY Delta Growth Tracking on Core KPI Cards**.
- [x] **Expandable Historical Trend Modules across All Primary Dashboard Pages**.
- [x] **Global Airline Alliances Lens (`app/pages/5_🌐_Alliances.py`) with NW/KL Wings Alliance**.
- [x] **BigQuery User Travel Vault (`db1b-1.user_travel.user_flight_logs`) with 1,000-Flight Cap & Typed `DELETE` Purge**.
- [x] **User Privacy Policy Page (`app/pages/6_🔒_Privacy_Policy.py`)**.
- [x] **Removed All Portfolio Backlinks Across Platform**.
- [x] **Portfolio Explainer & Site Preview Updated to 93.9M+ Records**.
- [x] **Extant Historical Route Data & FFP Partner Research (`docs/ffp_partnerships_research.md`)**.
- [x] **Unified Test Suite Passed 100% (`tests/run_all_tests.py`)**.

---

## ⏳ Next Immediate Steps & Audit Roadmap
1. **Deploy to Google Cloud Run**: Execute `./scripts/deploy.sh` to release the new longitudinal time-series analytics, Alliances tab, persistent user vault, and privacy policy to `https://avdb.riffe.co.uk`.
2. **Phase 1 DB1B Historical Ingestion (2000–2025 Q2)**: Build and run automated PREZIP downloader for quarterly `DB1BMarket` files into `db1b-1.DB1B_RAW.historical_db1b_market`.
3. **Phase 2 Historical Fare Ingestion (1990–1999)**: Ingest early DB1B (1993–1999) and DB1A (1990–1992) from NBER / TranStats archives as planned in `playbook.md`.
