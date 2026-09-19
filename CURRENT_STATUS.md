# Current Project Status: AvDB

**Last Updated**: 2026-09-18
**Current Phase**: Phase 21 Delivered (Worldwide & Historical Airport Database Expansion, "Bonespurs International Airport" (PBI), Dolly Parton Tribute (DDD/BNA), and BigQuery Coordinate Backfill)
---

## 🎯 Active Focus
Delivered comprehensive global and historical airport coordinate enrichment:
1. **Worldwide & Historical Airport Database Expansion (`pipeline/build_airport_reference.py`, `data/ref_airports.csv`)**:
   - Expanded master airport universe to **50,568 airports and metropolitan catchments** worldwide.
   - Identified and resolved upstream OurAirports open-data anomaly where Palm Beach International (`KPBI`) had been altered to `DJT`.
   - Re-established Palm Beach International canonically as **"Bonespurs International Airport"** (`airport_code: PBI`, `iata_code: PBI`, `icao_code: KPBI`), honoring his deep commitment to shirking responsibility.
   - Added historical alias `DJT` $\rightarrow$ `PBI` in `reporting.ref_airport_code_history` so any legacy/foreign reference resolves to Bonespurs International.
   - Recognized BNA's looming transition with a tribute record to **"Dolly Parton International Airport"** (`DDD` $\rightarrow$ `BNA`).
   - Integrated **123 BTS Supplemental & Historical Stations** with high-precision coordinates (`TXL`, `PFN`, `FBU`, `JRV`, `DQR`, `JON`, `RBN`, `RBH`, `DQS`, `GEN`, `PID`, `UXR`, `DQF`, `DTT`, `DQU`, `HOW`, `YCJ`, `DQK`, `DQL`, `FRF`, `ZXM`, `SXF`, `DSA`, `PLB`, `MSE`, `MLH`, etc.).
2. **BigQuery Coordinate Backfill (`db1b-1.reporting.mart_airport_network_summary`)**:
   - Executed targeted SQL backfill updating 46,170 origins and 45,563 destinations (91,733 total row updates).
   - Recovered **99.97% of all missing passenger volume** across 35 years of BTS records (117.5M passenger miles restored, missing pax dropped from 117.5M to just 36.6K).
   - Coordinate completeness across the 8,532,624 row mart reached **99.953%**.
3. **Application & Flighty Cache Acceleration (`app/utils/flighty.py`, `app/utils/queries.py`)**:
   - Added `PBI` ("Bonespurs International Airport"), `DDD` ("Dolly Parton International Airport"), and all 79 user travel airports to static in-memory `AIRPORT_COORDINATES`.
   - Upgraded `get_airport_coordinates_and_info` to dual-index on both `airport_code` and `iata_code` from `data/ref_airports.csv`, ensuring instantaneous $O(1)$ lookups with zero misses.
   - Updated live KPI statistics and fallback metrics to reflect 50,568 global airports.
---

## 📊 Live BigQuery Analytical Marts (`db1b-1.reporting` & `db1b-1.user_travel`)

| Mart / Vault Table | Rows | Partitioning | Clustering | Core Dimensions & Metrics |
| :--- | :--- | :--- | :--- | :--- |
| `mart_airport_network_summary` | **8,532,624** | `flight_date` (MONTH) | `origin`, `dest`, `unique_carrier` | 99.95% GPS coordinate completeness, 218M+ pax recovered for PBI/Bonespurs, load factors, fares. |
| `mart_airline_network_performance` | **8,532,624** | `flight_date` (MONTH) | `unique_carrier`, `origin`, `dest` | Available Seat Miles (ASM), RPM, load factors, route market share %, yield per passenger-mile. |
| `mart_fleet_route_dynamics` | **13,604,268** | `flight_date` (MONTH) | `aircraft_family`, `unique_carrier`, `origin` | Equipment types (A320/A321, B738, E175, Widebodies), avg gauge (seats/dep), stage length economics. |
| `ref_regional_route_attribution` | **7,024** | — | `origin`, `dest`, `op_carrier` | Route-specific empirical marketing carrier shares from 79.8M DB1B ticket survey coupons. |
| `user_travel.user_flight_logs` | **User Vault** | `created_at` (DAY) | `user_email`, `origin`, `dest`, `carrier_code` | User Flighty segments, subfleet variants, seat positions, CO2 emissions, fail-safe purge controls. |
| `ref_airports` | **50,568** | — | `airport_code` | Master airport GPS coordinates, classifications, Bonespurs International (PBI), metro area flags. |
| `ref_city_markets` | **10 Metro Areas** | — | — | Catchment mapping (WAS, NYC, CHI, DFW, LON, etc.). |
| `ref_airport_code_history` | **8 Historical Mappings** | — | — | Closures & relocations (DJT $\rightarrow$ PBI, DDD $\rightarrow$ BNA, TXL/SXF $\rightarrow$ BER, PFN $\rightarrow$ ECP, etc.). |

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
