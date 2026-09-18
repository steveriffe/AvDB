# Current Project Status: AvDB

**Last Updated**: 2026-09-17
**Current Phase**: Phase 12 Delivered (Airline Alliances Tab with NW/KL Wings Alliance, BigQuery Persistent Travel Vault with 1,000-Flight Cap & Fail-Safe DELETE, Privacy Policy, Zero External Backlinks, and FFP Partner Research)
---

## 🎯 Active Focus
Delivered dedicated alliances lens, BigQuery user flight vault, privacy governance, and FFP research:
1. **Global Alliances & Joint Ventures Lens (`app/pages/5_🌐_Alliances.py`)**:
   - Built a comprehensive comparative intelligence tab analyzing Star Alliance, SkyTeam, oneworld, and the pioneering **Northwest / KLM (NW/KL) Wings Alliance** (and Qualiflyer).
   - Metrics include system passenger volume, commercial departures, Available Seat Miles (ASM), Revenue Passenger Miles (RPM), system load factor %, and widebody vs. narrowbody fleet deployment mix.
   - Prominently highlights the **US-origin & gateway data boundary notice** clarifying BTS T-100 / DB1B coverage.
2. **BigQuery Persistent Travel Vault (`app/utils/flighty.py` & `app/pages/4_📱_Flighty_Traveler.py`)**:
   - Created `db1b-1.user_travel.user_flight_logs` (partitioned by creation date, clustered by user email, origin, dest, carrier).
   - Enforces a **1,000-flight safety limit** per user account.
   - Implemented transparent platform storage telemetry (total user flights, registered travelers).
   - Built **fail-safe user data purge controls**: requires typing exact uppercase `DELETE` before the permanent deletion SQL query executes.
3. **Dedicated User Privacy Policy (`app/pages/6_🔒_Privacy_Policy.py`)**:
   - Transparent disclosure on identity management (Google OAuth strictly for session authorization against allowlist).
   - Details cloud vault storage, user ownership, and complete absence of third-party ad networks, marketing beacons, or tracking pixels.
4. **Removal of External Backlinks**:
   - Completely stripped all portfolio backlink bars and links to `portfolio.riffe.co.uk` across AvDB landing, sidebars, and styling components.
5. **Site Preview & Explainer Update**:
   - Updated both AvDB's public landing page and the portfolio explainer files (`Portfolio/public/avdb.html` and `Portfolio/public/index.html`) to reflect the **93.9M+ record warehouse scale**.
6. **Extant Historical Route Data & Frequent Flyer Program (FFP) Research (`docs/ffp_partnerships_research.md`)**:
   - Audited extant pre-1990 data sources (CAB Form 41 Schedules T-1/T-2/T-3 1970–1989, TranStats T-9, OAG timetables, NBER archives).
   - Designed schema and architectural plan for a future **Frequent Flyer Program (FFP) Historical Partners** lens (tracking bilateral reciprocity for Alaska Mileage Plan, Northwest WorldPerks, Delta SkyMiles, AA AAdvantage).

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
- [x] **Global Airline Alliances Lens (`app/pages/5_🌐_Alliances.py`)**.
- [x] **Northwest / KLM (NW/KL) Wings Alliance Integration & Vector SVG Logo**.
- [x] **BigQuery User Travel Vault (`db1b-1.user_travel.user_flight_logs`)**.
- [x] **1,000 Flight Safety Limit & Typed `DELETE` Purge Workflow**.
- [x] **User Privacy Policy Page (`app/pages/6_🔒_Privacy_Policy.py`)**.
- [x] **Removed All Portfolio Backlinks Across Platform**.
- [x] **Portfolio Explainer & Site Preview Updated to 93.9M+ Records**.
- [x] **Extant Historical Route Data & FFP Partner Research (`docs/ffp_partnerships_research.md`)**.
- [x] **Unified Test Suite Passed 100% (`tests/run_all_tests.py`)**.

---

## ⏳ Next Immediate Steps & Audit Roadmap
1. **Deploy Updates to Cloud Run**: Execute `./scripts/deploy.sh` to release the Alliances tab, persistent user travel vault, and privacy policy to `https://avdb.riffe.co.uk`.
2. **Phase 1 DB1B Historical Ingestion (2000–2025 Q2)**: Build and run automated PREZIP downloader for quarterly `DB1BMarket` files into `db1b-1.DB1B_RAW.historical_db1b_market`.
3. **Phase 2 Historical Fare Ingestion (1990–1999)**: Ingest early DB1B (1993–1999) and DB1A (1990–1992) from NBER / TranStats archives as planned in `playbook.md`.
