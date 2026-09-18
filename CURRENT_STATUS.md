# Current Project Status: AvDB

**Last Updated**: 2026-09-17
**Current Phase**: Phase 11 Delivered (Portfolio Design System, Resilient Vector SVG Logos, 40+ Aircraft Fleet DB with Verified Photo Attribution, Live Warehouse KPIs & Automated BTS Ingestion Checker)
---

## 🎯 Active Focus
Delivered platform modernization, visual resilience, and pipeline automation:
1. **Airline Vector SVG Logo System (`app/data/ref_logos_svg.py`)**:
   - Replaced fragile external Wikimedia URLs with self-contained, inline Vector SVG data URIs for all major US legacy, low-cost, historical merged airlines, and international carriers.
   - Built automatic carrier monogram generator (`generate_carrier_monogram_svg()`) providing instant fallbacks for uncataloged codes.
2. **Fleet Database Expansion & Rigorous Photo Attribution (`app/data/ref_aircraft_specs.py`)**:
   - Expanded technical specifications and photographic assets from 12 models to 40+ canonical commercial aircraft types spanning MD-80s, 717, 727, 737 Classics/NG/MAX, 757/767, 777, 787, 747, A220, A320ceo/neo, A330/A350/A380, CRJ series, ERJ/E-Jets, Dash 8, Saab 340, and Cessna 208.
   - Verified high-res photography with explicit photographer credits (e.g. Anna Zvereva, Alan Wilson, Delta Flight Museum), Creative Commons / Public Domain license types, and outbound source links.
   - Enhanced Fleet Explorer (`app/pages/3_💺_Fleet_Routes.py`) with a dedicated two-column technical showcase card.
3. **User Access & Traffic Audit**:
   - Extracted Cloud Run access logs from Google Cloud Logging. Confirmed only 1 human user (Seattle, WA) has accessed the application, with remaining requests from automated scrapers (Censys, Web2Objects) and Microsoft Skype/Teams link previewers.
4. **Portfolio Design System Alignment (`app/utils/styling.py`)**:
   - Aligned styling with `https://riffe.co.uk` using `Plus Jakarta Sans`, `Inter`, and `JetBrains Mono` typography.
   - Injected `#0B192C` canvas with a 28px dot-matrix grid, `#111D33` glass surface cards, `#FF6B00` brand orange accents, `#38BDF8` electric sky highlights, and `#10B981` emerald status indicators.
   - Added persistent portal navigation badge (`← Back to Portfolio Portal (riffe.co.uk)`) in the sidebar.
5. **Live Warehouse KPIs (`app/utils/queries.py`)**:
   - Replaced hardcoded landing stats with `get_platform_live_kpis()` querying zero-cost BigQuery `__TABLES__` metadata, displaying live warehouse counts (93.9M+ total records, 14.04M T-100 segments, 79.86M OD40 records, 13.60M fleet dynamics records).
6. **Automated BTS Data Update Checker**:
   - Created `scripts/check_bts_updates.py` to compare warehouse horizons against BTS TranStats release schedules and check GCS staging buckets (`gs://db1b-1/`).
   - Configured scheduled weekly GitHub Actions workflow (`.github/workflows/check_data_updates.yml`) running every Monday at 08:00 UTC.
7. **Comprehensive Test Suite & Verification**:
   - Executed full suite via `tests/run_all_tests.py` with 100% passes across landing page auth, aircraft specs, alliances, mergers, Flighty parser, and API endpoints.

---

## 📊 Live BigQuery Analytical Marts (`db1b-1.reporting`)

| Mart Table | Rows | Partitioning | Clustering | Core Dimensions & Metrics |
| :--- | :--- | :--- | :--- | :--- |
| `mart_airport_network_summary` | **8,532,624** | `flight_date` (MONTH) | `origin`, `dest`, `unique_carrier` | Direct destinations, pax volume, seat capacity, load factors, DB1B inferred fares, GPS coordinates. |
| `mart_airline_network_performance` | **8,532,624** | `flight_date` (MONTH) | `unique_carrier`, `origin`, `dest` | Available Seat Miles (ASM), RPM, load factors, route market share %, yield per passenger-mile. |
| `mart_fleet_route_dynamics` | **13,604,268** | `flight_date` (MONTH) | `aircraft_family`, `unique_carrier`, `origin` | Equipment types (A320/A321, B738, E175, Widebodies), avg gauge (seats/dep), stage length economics. |
| `ref_airports` | **50,409** | — | `airport_code` | Master airport GPS coordinates, classifications, metro area flags. |
| `ref_city_markets` | **10 Metro Areas** | — | — | Catchment mapping (WAS, NYC, CHI, DFW, LON, etc.). |
| `ref_airport_code_history` | **Historical Mappings** | — | — | Airport closures & relocations (TXL/SXF $\rightarrow$ BER, PFN $\rightarrow$ ECP, etc.). |

---

## ✅ Recently Completed
- [x] **Vector SVG Logo Engine & Monogram Fallbacks (`app/data/ref_logos_svg.py`)**.
- [x] **40+ Aircraft Technical Database Expansion & Photography Credits (`app/data/ref_aircraft_specs.py`)**.
- [x] **Cloud Run User Traffic & Bot Access Audit**.
- [x] **Portfolio Design System Harmonization (Fonts, Tokens, Grid, and Portal Link)**.
- [x] **Dynamic BigQuery Storage Metadata Live KPIs (`get_platform_live_kpis`)**.
- [x] **Automated Data Update Checker (`scripts/check_bts_updates.py` & `.github/workflows/check_data_updates.yml`)**.
- [x] **Unified Test Suite Regression Pass (`tests/run_all_tests.py`)**.

---

## ⏳ Next Immediate Steps & Audit Roadmap
1. **Deploy Updates to Cloud Run**: Execute `./scripts/deploy.sh` to release the modernized UI, vector logos, expanded fleet database, and live KPIs to `https://avdb.riffe.co.uk`.
2. **Phase 1 DB1B Historical Ingestion (2000–2025 Q2)**: Build and run automated PREZIP downloader for quarterly `DB1BMarket` files into `db1b-1.DB1B_RAW.historical_db1b_market`.
3. **Phase 2 Historical Fare Ingestion (1990–1999)**: Ingest early DB1B (1993–1999) and DB1A (1990–1992) from NBER / TranStats archives as planned in `playbook.md`.
