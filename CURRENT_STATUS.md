# Current Project Status: AvDB

**Last Updated**: 2026-08-31
**Current Phase**: Phase 2 & 3 — Data Profiling & Analytics Mart Design

---

## 🎯 Active Focus
Completed initial BigQuery discovery and data profiling across datasets in project `db1b-1`. Scoping out analytics mart queries and geospatial reference enhancements.

---

## 📊 BigQuery Data Assets Discovered (`db1b-1`)

| Dataset | Table / View | Description | Rows / Coverage |
| :--- | :--- | :--- | :--- |
| `DB1B_RAW` | `OD40_DB1B_RAW` | Modern DOT OD40 10% Ticket Survey | **40.3M rows** (2025 modern format) |
| `DB1B_RAW` | `v_market_demand_itinerary` | Survey O&D market demand & fare aggregation | View joining ticket itinerary segments |
| `bts_t100_data` | `t100_segments` | T-100 Segment operational flights & capacity | **14.0M rows** (1990 – 2026-04, partitioned by month) |
| `bts_t100_data` | `market_all_carriers` | T-100 Market carrier routes & passenger totals | Monthly partition, clustered by origin, carrier, dest |
| `t100_data` | `L_AIRCRAFT_TYPE` | BTS Aircraft Type lookup table (Code -> Aircraft Name) | e.g. 698 -> Boeing 737-800, 694 -> A321neo |
| `t100_data` | `v_airport_fleet_mix` | Joined view of T-100 operations & aircraft types | Operational pax, seats, load factor |
| `t100_data` | `v_fleet_yield_analysis` | Joined operational capacity & DB1B ticket yield | Yield, avg fare, load factors |
| `reporting` | *(empty)* | Dedicated analytics marts destination | Ready for pre-aggregated dashboard marts |

---

## ✅ Recently Completed
- [x] Initialized Git repository, `.gitignore`, and Git commit discipline.
- [x] Connected to GCP project `db1b-1` via Application Default Credentials.
- [x] Configured local environment `.env` (`GCP_PROJECT_ID=db1b-1`, `BIGQUERY_DATASET_ANALYTICS=reporting`).
- [x] Successfully profiled 14.0M rows of T-100 and 40.3M rows of DB1B OD40 data.
- [x] Validated prototype SQL queries for route load factors, aircraft type matching, and inferred fares.

---

## ⏳ Next Immediate Steps
1. **Analytics Marts Creation**: Write SQL scripts to materialize pre-aggregated summary tables into `db1b-1.reporting` (`mart_airport_routes_summary`, `mart_airline_network_performance`, `mart_fleet_route_dynamics`).
2. **Airport Coordinates Enrichment**: Ingest airport latitude/longitude lookup table to enable PyDeck great-circle route maps.
3. **Wire up Streamlit Pages**: Connect `app/pages/1_✈️_Airports.py`, `2_🏢_Airlines.py`, and `3_💺_Fleet_Routes.py` to live BigQuery data with interactive Plotly & PyDeck visuals.
