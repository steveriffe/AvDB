# Current Project Status: AvDB

**Last Updated**: 2026-08-31
**Current Phase**: Phase 3 — Analytics Marts & Dashboard Engineering

---

## 🎯 Active Focus
Constructing the pre-aggregated BigQuery analytics marts in `db1b-1.reporting` (`mart_airport_network_summary`, `mart_airline_network_performance`, `mart_fleet_route_dynamics`) and building the interactive Streamlit UI pages.

---

## 📊 BigQuery Data Assets Available (`db1b-1`)

| Dataset | Table / View | Type | Rows / Scope | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `DB1B_RAW` | `OD40_DB1B_RAW` | Table | **40.3M rows** | Modern DOT OD40 10% Ticket Survey (2025) |
| `DB1B_RAW` | `v_market_demand_itinerary` | View | Monthly O&D | Passenger demand and average ticket fare calculations |
| `bts_t100_data` | `t100_segments` | Partitioned Table | **14.0M rows** | 1990 – 2026 segment operations, seats, and pax |
| `bts_t100_data` | `market_all_carriers` | Partitioned Table | Millions of rows | Market-level carrier metrics and passenger counts |
| `t100_data` | `L_AIRCRAFT_TYPE` | Lookup Table | Codes $\rightarrow$ Names | BTS aircraft family mappings (e.g. B738, A321neo) |
| `t100_data` | `v_fleet_yield_analysis` | Joined View | Operations + Fares | Route load factors, gauge, and inferred fares |
| `reporting` | `ref_airports` | Partitioned/Clustered | **50,409 rows** | Master physical airport coordinates & metro entries |
| `reporting` | `ref_city_markets` | Lookup Table | 10 Major Metro Areas | Catchment mapping (WAS, NYC, CHI, DFW, LON, etc.) |
| `reporting` | `ref_airport_code_history` | Lookup Table | Relocations / Closures | Historic aliases (TXL/SXF $\rightarrow$ BER, PFN $\rightarrow$ ECP, etc.) |

---

## ✅ Recently Completed
- [x] Initialized Git repository and environment configuration (`.env`, `pyproject.toml`, `.venv`).
- [x] Profiled existing BigQuery assets across `DB1B_RAW`, `bts_t100_data`, and `t100_data`.
- [x] Built and executed `pipeline/build_airport_reference.py` using Parquet to populate:
  - `reporting.ref_airports` (with coordinates, types, country, and metro flags).
  - `reporting.ref_city_markets` (with multi-airport catchment linkages).
  - `reporting.ref_airport_code_history` (with historical code changes and status).
- [x] Validated coordinate joins with 2024 T-100 flight segment data.

---

## ⏳ Next Immediate Steps
1. **Analytics Marts**: Materialize pre-aggregated summary tables into `db1b-1.reporting` for sub-second Streamlit performance.
2. **Streamlit Airport Explorer**: Build interactive PyDeck great-circle route map and carrier share charts in `app/pages/1_✈️_Airports.py`.
3. **Catchment Disambiguation in UI**: Display clear multi-airport catchment badges when city market codes (like `WAS` or `NYC`) are analyzed.
