# AvDB Architecture & Technical Design

## 1. Datasets & Domain Model

AvDB integrates public US Department of Transportation (DOT) Bureau of Transportation Statistics (BTS) databases with reference lookups:

### A. BTS T-100 Segment (Air Carrier Statistics)
- **Granularity**: Monthly carrier-route segment (Origin -> Destination -> Carrier -> Aircraft Type).
- **Core Metrics**: Departures performed, Seats available (capacity), Passengers transported, Freight/Mail, Aircraft type code.
- **Use Case**: True physical capacity, seat load factors, route frequencies, aircraft gauge.

### B. BTS DB1B (Origin and Destination Survey)
- **Granularity**: 10% sample of all airline passenger tickets sold (quarterly).
- **Sub-tables**:
  - `DB1B_Ticket`: Overall itinerary ticket characteristics, total dollar amount, number of passengers.
  - `DB1B_Market`: O&D market-level summary, nonstop miles, operating/ticketing carrier.
  - `DB1B_Coupon`: Individual flight segment coupons within each ticket (coupons 1 to 16), airport sequence, break points.
- **Use Case**: Yields, average passenger fares, passenger routing choices, connecting vs. nonstop demand.

### C. Reference Dimensions
- **Airport Master**: IATA/ICAO codes, airport name, city, state, metro area code, latitude/longitude.
- **FAA Aircraft Registry / Master**: Tail number (N-number) to aircraft manufacturer, model series, engine type, seat capacity range.
- **Carrier Master**: IATA 2-letter / DOT carrier codes and full airline names.

---

## 2. BigQuery Data Warehouse Architecture

```text
Google Cloud BigQuery
├── avdb_raw/
│   ├── raw_t100_segment_all
│   ├── raw_db1b_coupon
│   ├── raw_db1b_market
│   ├── raw_db1b_ticket
│   ├── ref_airports
│   └── ref_aircraft_types
├── avdb_staging/
│   ├── stg_t100_segments
│   ├── stg_db1b_coupons
│   └── stg_db1b_tickets
└── avdb_marts/
    ├── mart_airport_network_summary
    ├── mart_airline_market_performance
    └── mart_fleet_route_economics
```

### Partitioning & Clustering Strategy:
- **`raw_t100_*`**: Partitioned by `year`, Clustered by `origin`, `dest`, `unique_carrier`.
- **`raw_db1b_*`**: Partitioned by `year`, `quarter`, Clustered by `origin`, `dest`, `op_carrier`.
- **Marts**: Pre-aggregated tables with summary metrics clustered by primary dimensions for sub-second Streamlit dashboard responses.

---

## 3. Streamlit Application Architecture

```text
app/
├── main.py                  # Homepage & navigation controller (st.navigation)
├── config.py                # Environment configs & styling
├── utils/
│   ├── bq_client.py         # Cached BigQuery client & parameterized queries
│   ├── visualizers.py       # Plotly & PyDeck chart builders (Great-circle routes)
│   └── formatting.py        # Currency, percentage, and number formatting helpers
└── pages/
    ├── 1_✈️_Airports.py      # Airport route dynamics, passenger volume, carrier share
    ├── 2_🏢_Airlines.py      # Network maps, fare distributions, route profitability
    └── 3_💺_Fleet_Routes.py  # Equipment utilization, gauge trends, stage lengths
```

### Query & Cache Pattern:
```python
import streamlit as st
from google.cloud import bigquery

@st.cache_data(ttl=3600, show_spinner=False)
def query_airport_routes(project_id: str, airport_code: str, year: int) -> pd.DataFrame:
    client = bigquery.Client(project=project_id)
    query = """
        SELECT dest, carrier, total_passengers, avg_fare, seats
        FROM `avdb_marts.mart_airport_network_summary`
        WHERE origin = @airport_code AND year = @year
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("airport_code", "STRING", airport_code),
            bigquery.ScalarQueryParameter("year", "INT64", year),
        ]
    )
    return client.query(query, job_config=job_config).to_dataframe()
```

---

## 4. Deployment & Hosting Strategy

- **Google Cloud Run**: Serverless container instance scaling from 0 to N.
- **Authentication**: Native Cloud Run default compute service account with `roles/bigquery.dataViewer` and `roles/bigquery.jobUser`.
- **Custom Domain**: Configured via Cloud Run Domain Mapping or Cloudflare DNS Proxy with free SSL.

