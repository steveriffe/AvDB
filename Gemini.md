# AvDB — AI Assistant Guidelines & Context

## Project Overview
**AvDB** is an aviation analytics platform and interactive Streamlit web dashboard. It processes US Bureau of Transportation Statistics (BTS) datasets—primarily **T-100 Segment/Market**, **On-Time Performance**, and **DB1B (Origin and Destination 10% Ticket Survey)**—enhanced with aircraft reference tables and geographic data, hosted in Google BigQuery and visualized via Streamlit.

## Core Lenses & Analytical Objectives
1. **Airports Lens**:
   - Route network additions/terminations, passenger traffic trends.
   - Carrier seat/passenger capacity mix and market share.
   - Origin-Destination (O&D) fare yields and stage lengths.
2. **Airlines Lens**:
   - Network density and expansion.
   - Fleet deployment across routes.
   - Average fares, yield per RPM/ASM, and load factors.
3. **Fleet / Aircraft Lens**:
   - Aircraft type utilization by route and gauge (seats per departure).
   - Regional vs. mainline fleet shifts.
   - Route economics and fuel/equipment matching insights.

---

## Technical Stack & Conventions

- **Data Warehouse**: Google Cloud BigQuery
- **ETL / Ingestion**: Python (`google-cloud-bigquery`, `pyarrow`, `polars`, `requests`, `playwright`/`beautifulsoup` for scraping where required).
- **Transformation / Modeling**: BigQuery SQL / dbt models (Staging `stg_` -> Intermediate `int_` -> Marts `mart_`).
- **Dashboard / Frontend**: Streamlit (Python 3.11+) with `st.navigation` multi-page structure.
- **Visualization**: Plotly, PyDeck / deck.gl (geospatial great-circle routes), Altair.
- **Local Dev & Auth**: Google Cloud Application Default Credentials (`gcloud auth application-default login`), isolated Python `.venv`.
- **Deployment**: Containerized Docker on Google Cloud Run with Custom Domain & SSL.

---

## Golden Rules for AI Pair Programming

1. **BigQuery Efficiency**:
   - Always query pre-aggregated marts in dashboard code. Avoid raw table scans over DB1B/T-100 millions of rows in interactive UI runs.
   - Leverage BigQuery partitioning on date columns (`fl_date`, `year`, `quarter`) and clustering on key dimensions (`origin`, `dest`, `op_unique_carrier`).
2. **Streamlit Best Practices**:
   - Cache expensive BigQuery data calls using `@st.cache_data(ttl=3600, show_spinner=False)`.
   - Never put database secrets in code. Use `st.secrets` in production and standard GCP ADC locally.
   - Modularize UI components into helper functions in `app/utils/`.
3. **State Management & Version Control**:
   - Update `CURRENT_STATUS.md` at the end of each session or major milestone.
   - Update `playbook.md` task checkboxes as features are delivered.
   - **Git Commit Discipline**: Automatically stage and commit code changes at every milestone with clear, semantic commit messages (e.g., `feat: ...`, `fix: ...`, `refactor: ...`, `docs: ...`).
4. **Data Integrity**:
   - DB1B fares contain dollar amounts reported in tenths or needing standard outlier filtering ($20 - $2,500 typical valid passenger ticket bounds; check `roundtrip` indicator).
   - T-100 uses both Carrier Reported codes and Standard DOT codes; maintain clear mapping in intermediate models.

5. **Permissions & Command Execution Scoping**:
   - **Full Execution Permission**: Pre-approved for Python (`./.venv/bin/python3`), BigQuery (`bq`), GCP (`gcloud`), Streamlit (`streamlit`), and Git (`git`).
   - **Scope & Paths**: Full Read/Write within `/Users/steveriffe/Documents/Tech/GitHub/AvDB` and Read-Only across `/Users/steveriffe/Documents/Tech/`.
   - **Prefix-Matchable Command Formatting**: Always format commands with simple, direct binary prefixes (e.g., `./.venv/bin/python3 script.py` rather than inline code strings `python -c "..."` or complex subshell pipes) so auto-approval rules stay prefix-matched without re-prompting.

