# Research & Architectural Plan: Extant Historical Route Data & Frequent Flyer Program (FFP) Partnerships

**Document Purpose**: 
1. Survey extant historical route and timetable data sources that can be ingested into AvDB to bridge pre-1990 gaps.
2. Outline a comprehensive architectural plan and data schema for a future **Frequent Flyer Program (FFP) Historical Partnerships** lens.

---

## Part 1: Extant Historical Route & Timetable Data Sources

To extend AvDB's historical horizons prior to 1990 or augment existing T-100 / DB1B domestic segment coverage, several key extant datasets exist:

### 1. US Civil Aeronautics Board (CAB) Form 41 Historical Files (1970–1989)
- **Background**: Before the Airline Deregulation Act of 1978 and the eventual sunsetting of the CAB in 1984, US airlines submitted monthly and quarterly flight reports (Form 41) to the CAB. This collection was transitioned to the DOT Office of Airline Information.
- **Available Datasets**:
  - **CAB Schedule T-1 / T-2 / T-3**: Non-stop traffic by carrier, airport pair, passenger volume, and aircraft type from 1972 through 1989.
  - **Data Bank 1A (DB1A)**: 10% Ticket Survey records for 1979–1992 (the direct architectural predecessor to modern DB1B).
- **Format & Custody**: Maintained in the **National Archives and Records Administration (NARA)** Record Group 197 and archived digitally in raw ASCII/EBCDIC fixed-width magnetic tape formats, as well as curated research collections hosted by the **National Bureau of Economic Research (NBER)**.
- **Ingestion Feasibility**: **High**. Python fixed-width unpacking scripts can parse NBER/NARA text archives into BigQuery staging tables (`avdb_raw.cab_form41_t100_ancestor`).

### 2. Official Airline Guide (OAG) Historical Timetables & Schedules (1970s–Present)
- **Background**: OAG published monthly printed guides and electronic flight schedules detailing carrier, flight number, equipment type, departures, and intermediate stopovers.
- **Available Datasets**:
  - Global commercial schedules (including foreign-to-foreign routes like European domestic, Asian intra-regional, and transatlantic).
- **Format & Custody**: Commercial data licensing from OAG Aviation Worldwide Ltd. Academic and research licenses have historically been brokered through university transportation centers (e.g. Northwestern Transportation Library, MIT International Center for Air Transportation).
- **Ingestion Feasibility**: **Requires commercial licensing or research dataset donation**. Highly valuable for filling non-US international schedules.

### 3. TranStats Historical T-9 / ER-586 / Form 41 Schedules (Pre-1990)
- **Background**: BTS TranStats maintains legacy archives for early jet-age carriers (Pan Am, TWA, Eastern, Braniff, Western).
- **Available Datasets**:
  - **T-9 Non-Stop Segment**: Available in annual zipped text archives on TranStats data portal.
  - Covers 1974–1989 carrier operations by aircraft type and city-pair.
- **Ingestion Feasibility**: **High**. Downloadable via standard HTTPS requests using python `requests` and loadable directly via BigQuery `LOAD DATA`.

### 4. Community & Open Aviation Repositories
- **OpenFlights**: Community-maintained global airport coordinates, historical airline IATA/ICAO code changes, and route pair graphs (active 2005–2020).
- **Airline Route Mapper**: Historical route network snapshots from timetable collections.

---

## Part 2: Frequent Flyer Program (FFP) Historical Partnerships Lens (Plan Only)

### Concept & Historical Significance
Before formal multilateral alliances (Star Alliance in 1997, oneworld in 1999, SkyTeam in 2000), airlines expanded their virtual networks through **bilateral Frequent Flyer Program (FFP) partnerships**.
Even after global alliances matured, premier boutique airlines (e.g. **Alaska Airlines Mileage Plan**) famously maintained a flexible, multi-alliance "Swiss style" network of earn/burn partners with American Airlines, Delta, British Airways, KLM, Air France, Cathay Pacific, Qantas, Emirates, and Fiji Airways before joining oneworld in 2021.

Other historic bilateral pacts include:
- **Northwest WorldPerks & KLM Flying Dutchman**: The foundational transatlantic reciprocity pact (1989–2004) that formed the template for modern joint ventures.
- **Continental OnePass**: Shared across Continental, Eastern Air Lines, and later Virgin Atlantic, Copa Airlines, and Northwest.
- **USAir Frequent Traveler / Dividend Miles**: Early bilateral agreements with British Airways and Air France before Star Alliance integration.
- **Delta Frequent Flyer / SkyMiles**: Historical tie-ups with Swissair, Singapore Airlines (the "Global Excellence" alliance of 1989), and Virgin Atlantic.
- **American Airlines AAdvantage**: The pioneer program (1981) with historical partnerships spanning Canadian Airlines, Cathay Pacific, Qantas, and Gulf Air.

---

### Proposed BigQuery Schema Design: `reporting.ref_ffp_partnerships`

```sql
CREATE OR REPLACE TABLE `db1b-1.reporting.ref_ffp_partnerships` (
  partner_id STRING NOT NULL,           -- e.g. 'AS_BA_MILEAGE_PLAN'
  program_airline_code STRING NOT NULL, -- e.g. 'AS' (Alaska Airlines)
  program_name STRING NOT NULL,         -- e.g. 'Mileage Plan'
  partner_airline_code STRING NOT NULL, -- e.g. 'BA' (British Airways)
  partner_airline_name STRING NOT NULL, -- e.g. 'British Airways'
  effective_start_date DATE NOT NULL,   -- e.g. '1999-01-01'
  effective_end_date DATE,              -- e.g. '2021-03-30' (or NULL if ongoing)
  partnership_depth STRING NOT NULL,    -- 'Codeshare & Reciprocal Earn/Burn', 'Bilateral Reciprocal', 'Redemption Only'
  elite_benefits_included BOOLEAN,      -- Lounge access, priority boarding, baggage allowance
  tier_status_recognition BOOLEAN,      -- Reciprocal status tier match
  notes STRING,                         -- Detailed historical transition notes
  source_citation STRING                -- Press release, SEC 10-K, timetable citation
)
CLUSTER BY program_airline_code, partner_airline_code, effective_start_date;
```

---

### UI & Analytical Capabilities for Future FFP Page

1. **Carrier Program Selection & Timeline**:
   - Select an airline (e.g., Alaska Airlines `AS`, Northwest `NW`, American `AA`) to visualize its complete historical partner constellation over time.
   - Interactive slider (1980–2026) showing how partner webs expanded and consolidated as carriers were absorbed by Star, oneworld, or SkyTeam.
2. **Global Route Map with FFP Overlay**:
   - Geodesic route map showing routes where a member of the selected program could earn or redeem miles in a given year.
3. **Alliance Independent Matrix**:
   - Highlight non-aligned "free agent" years (e.g., Alaska Airlines 1983–2020) and how bilateral FFP agreements filled critical international gateway connectivity without the antitrust immunity requirements of a metal-neutral joint venture.

