# Current Project Status: AvDB

**Last Updated**: 2026-09-02
**Current Phase**: Phase 5 — Production Containerization, Google OAuth & Custom Domain Deployment (Complete)

---

## 🎯 Active Focus
Successfully built and deployed the **AvDB Aviation Intelligence Platform** to **Google Cloud Run** (`avdb.riffe.co.uk`) with Google OAuth 2.0 authentication, an Apple-inspired HTML landing homepage, email allowlist protection (`steve@riffe.co.uk`), BigQuery cost safeguards ($1\text{ GB max}$ scanned per query), and Cloud Run auto-scaling down to zero instances ($0\text{ base cost}$ when idle).

---

## 📊 Live BigQuery Analytical Marts (`db1b-1.reporting`)

| Mart Table | Rows | Partitioning | Clustering | Core Dimensions & Metrics |
| :--- | :--- | :--- | :--- | :--- |
| `mart_airport_network_summary` | **2,521,106** | `flight_date` (MONTH) | `origin`, `dest`, `unique_carrier` | Direct destinations, pax volume, seat capacity, load factors, DB1B inferred fares, GPS coordinates. |
| `mart_airline_network_performance` | **2,521,106** | `flight_date` (MONTH) | `unique_carrier`, `origin`, `dest` | Available Seat Miles (ASM), RPM, load factors, route market share %, yield per passenger-mile. |
| `mart_fleet_route_dynamics` | **4,040,085** | `flight_date` (MONTH) | `aircraft_family`, `unique_carrier`, `origin` | Equipment types (A320/A321, B738, E175, Widebodies), avg gauge (seats/dep), stage length economics. |
| `ref_airports` | **50,409** | — | `airport_code` | Master airport GPS coordinates, classifications, metro area flags. |
| `ref_city_markets` | **10 Metro Areas** | — | — | Catchment mapping (WAS, NYC, CHI, DFW, LON, etc.). |
| `ref_airport_code_history` | **Historical Mappings** | — | — | Airport closures & relocations (TXL/SXF $\rightarrow$ BER, PFN $\rightarrow$ ECP, etc.). |

---

## ✅ Recently Completed
- [x] **Production Cloud Run & IONOS Custom Domain (`avdb.riffe.co.uk`)**:
  - Pushed container image to Artifact Registry (`us-central1-docker.pkg.dev/db1b-1/avdb/app:latest`).
  - Deployed Cloud Run service with `--min-instances=0` and `--max-instances=2`.
  - Configured CNAME domain mapping for `avdb.riffe.co.uk` $\rightarrow$ `ghs.googlehosted.com.`.
- [x] **Google OAuth 2.0 & Access Control**:
  - Streamlit-integrated Google Sign-In module (`app/utils/auth.py`).
  - Email allowlist guard (`ALLOWED_EMAILS=steve@riffe.co.uk`) with custom "Access Pending" card for unlisted guests.
  - Sidebar account profile pill & Sign Out button.
- [x] **Apple-Modern HTML Landing Homepage (`app/components/landing.py`)**:
  - Unauthenticated visitor landing hero, feature overview, and metric scale highlights.
- [x] **Wallet & Query Safeguards**:
  - Enforced `maximum_bytes_billed = 1 GB` limit on all BigQuery queries in `app/utils/bq_client.py`.

---

## ⏳ Next Immediate Steps & Audit Roadmap
1. **IONOS DNS Record Check**: Verify CNAME propagation (`avdb.riffe.co.uk` $\rightarrow$ `ghs.googlehosted.com.`) for automatic SSL certificate issuance.
2. **O&D Market Audit for Mega-Hubs (ORD, ATL, DFW)**: Revisit unserved connecting market proposals for mega-hubs to ensure seasonal/low-frequency nonstop routes (e.g. FAI, FAT, EUG, BZN) are distinguished from true unserved markets.
3. **Cargo & Freight Lens (Phase 4.5)**: Dedicated dashboard tab for cargo operators (FedEx, UPS, Atlas Air) to track freight tons and mail volume.

