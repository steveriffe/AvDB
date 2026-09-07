# Current Project Status: AvDB

**Last Updated**: 2026-09-07
**Current Phase**: Phase 10.1–10.5 Delivered (Complete 1990–2026 Analytical Marts Backfill, Q4 2025 OD40 Parquet Load, Filter Alignment & Test Suite, Live on Cloud Run revision avdb-00010-qp5)
---

## 🎯 Active Focus
Delivered historical aviation backfill (1990–2026) and dashboard filter resolution:
1. **Full Historical Mart Re-materialization (1990–2026)**:
   - Discovered that the reporting marts were previously sliced with `WHERE year >= 2018`, causing zero records for historical carriers (e.g. Continental in 2005, Northwest in 2005, Alaska in 2010, US Airways in 2010, America West in 2000, TWA in 2000).
   - Re-materialized all 3 primary analytical marts in BigQuery across 36 years (1990–2026) using 14.03M rows from `bts_t100_data.t100_segments`.
   - `mart_airport_network_summary`: Expanded from 2.52M to **8,532,624 rows**.
   - `mart_airline_network_performance`: Expanded from 2.52M to **8,532,624 rows**.
   - `mart_fleet_route_dynamics`: Expanded from 4.04M to **13,604,268 rows**.
2. **Q4 2025 OD40 Fare Ingestion**:
   - Ingested remaining October, November, and December 2025 parquet files from `gs://db1b-1/` into `db1b-1.DB1B_RAW.OD40_DB1B_RAW`.
   - Expanded table from 40.3M to **79,858,500 rows** across all 6 months of 2025 H2.
3. **Double-Checked 10% vs 40% Sampling Logic**:
   - Verified that `db1b-1.DB1B_RAW.v_market_demand_itinerary` properly weights legacy 10% DB1B surveys with `10.0` and modernized 40% OD40 monthly surveys with `2.5` (`1 / 0.40 = 2.5`), preventing sample distortion.
   - Weighted fare averaging accurately computes passenger-weighted average ticket prices across all months.
4. **Dashboard Filter & Year Alignment**:
   - Expanded year selection dropdowns across Airports, Airlines, and Fleet Explorers to support analysis back to 1990 (`[2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2015, 2010, 2005, 2000, 1995, 1990]`).
   - Hardened `get_airline_yield_curve` to gracefully display stage lengths and passenger volumes when historical ticket survey fare data is pending ingestion.
5. **Comprehensive Filter Unit Testing (`tests/test_all_filters.py`)**:
   - Built and executed automated unit test matrix asserting non-zero operations, direct routes, and hubs across historical carriers:
     - Alaska Airlines (`AS`, 2010): 151,654 departures, 10 hubs, 229 routes.
     - Continental Airlines (`CO`, 2005): 371,321 departures, 10 hubs, 400 routes.
     - Northwest Airlines (`NW`, 2005): 524,707 departures, 10 hubs, 400 routes.
     - US Airways (`US`, 2010): 450,833 departures, 10 hubs, 400 routes.
     - America West (`HP`, 2000): 215,311 departures, 10 hubs, 216 routes.
     - Trans World Airlines (`TW`, 2000): 277,599 departures, 10 hubs, 273 routes.
     - AirTran Airways (`FL`, 2008): 259,869 departures, 10 hubs, 357 routes.
   - All tests passed with 100% assertions satisfied.

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
- [x] **Complete Historical Analytical Marts Backfill (1990–2026)**.
- [x] **Q4 2025 Parquet Ingestion (Oct–Dec 2025)**.
- [x] **10% vs 40% Sampling Logic Verification**.
- [x] **Dashboard Filter Alignment Across All Pages**.
- [x] **Automated Filter & Query Unit Testing Matrix (`tests/test_all_filters.py`)**.
- [x] **Unified Regression Test Suite Passed (`tests/run_all_tests.py`)**.

---

## ⏳ Next Immediate Steps & Audit Roadmap
1. **Deploy Updates to Cloud Run**: Trigger `./scripts/deploy.sh` to roll out updated filters and year selections to `https://avdb.riffe.co.uk`.
2. **Phase 1 DB1B Historical Ingestion (2000–2025 Q2)**: Build and run automated PREZIP downloader for quarterly `DB1BMarket` files into `db1b-1.DB1B_RAW.historical_db1b_market`.
3. **Phase 2 Historical Fare Ingestion (1990–1999)**: Ingest early DB1B (1993–1999) and DB1A (1990–1992) from NBER / TranStats archives as planned in `playbook.md`.
