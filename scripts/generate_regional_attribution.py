"""
Generates and populates the BigQuery reference table:
`db1b-1.reporting.ref_regional_route_attribution`

Calculates the exact empirical marketing carrier attribution shares
from the DOT DB1B 10% Ticket Survey (79.8M records across legs 1-3)
for all regional operating carriers (SkyWest, Horizon, Endeavor, Envoy,
PSA, Piedmont, CommuteAir, GoJet, Mesa, Republic, Compass, Air Wisconsin).

Resolves multi-carrier routes (e.g. SkyWest on EUG-SEA split between DL and AS)
and provides deterministic fallbacks for single-mainline subsidiaries.
"""
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from app.utils.bq_client import get_bigquery_client
from google.cloud import bigquery

DDL_SQL = """
CREATE OR REPLACE TABLE `db1b-1.reporting.ref_regional_route_attribution`
CLUSTER BY op_carrier, origin, dest
AS
WITH coupon_legs AS (
  -- Leg 1
  SELECT 
    OpCarrier_1 AS op_carrier,
    Apt_1 AS origin,
    Apt_2 AS dest,
    CASE 
      WHEN MktCarrier_1 = 'HA' THEN 'AS' -- Alaska/Hawaiian unified network
      ELSE MktCarrier_1 
    END AS mkt_carrier
  FROM `db1b-1.DB1B_RAW.OD40_DB1B_RAW`
  WHERE OpCarrier_1 IN ('OO', 'QX', 'YX', '9E', 'MQ', 'OH', 'PT', 'C5', 'G7', 'YV', 'ZW', 'CP')
    AND Apt_1 IS NOT NULL AND Apt_2 IS NOT NULL AND MktCarrier_1 IS NOT NULL

  UNION ALL

  -- Leg 2
  SELECT 
    OpCarrier_2 AS op_carrier,
    Apt_2 AS origin,
    Apt_3 AS dest,
    CASE 
      WHEN MktCarrier_2 = 'HA' THEN 'AS'
      ELSE MktCarrier_2 
    END AS mkt_carrier
  FROM `db1b-1.DB1B_RAW.OD40_DB1B_RAW`
  WHERE OpCarrier_2 IN ('OO', 'QX', 'YX', '9E', 'MQ', 'OH', 'PT', 'C5', 'G7', 'YV', 'ZW', 'CP')
    AND Apt_2 IS NOT NULL AND Apt_3 IS NOT NULL AND MktCarrier_2 IS NOT NULL

  UNION ALL

  -- Leg 3
  SELECT 
    OpCarrier_3 AS op_carrier,
    Apt_3 AS origin,
    Apt_4 AS dest,
    CASE 
      WHEN MktCarrier_3 = 'HA' THEN 'AS'
      ELSE MktCarrier_3 
    END AS mkt_carrier
  FROM `db1b-1.DB1B_RAW.OD40_DB1B_RAW`
  WHERE OpCarrier_3 IN ('OO', 'QX', 'YX', '9E', 'MQ', 'OH', 'PT', 'C5', 'G7', 'YV', 'ZW', 'CP')
    AND Apt_3 IS NOT NULL AND Apt_4 IS NOT NULL AND MktCarrier_3 IS NOT NULL
),
coupon_agg AS (
  SELECT 
    op_carrier,
    origin,
    dest,
    mkt_carrier,
    COUNT(*) AS sample_coupons
  FROM coupon_legs
  GROUP BY 1, 2, 3, 4
),
route_totals AS (
  SELECT 
    op_carrier,
    origin,
    dest,
    SUM(sample_coupons) AS route_total_coupons
  FROM coupon_agg
  GROUP BY 1, 2, 3
)
SELECT 
  c.op_carrier,
  c.origin,
  c.dest,
  c.mkt_carrier,
  c.sample_coupons,
  ROUND(SAFE_DIVIDE(c.sample_coupons, r.route_total_coupons), 4) AS attribution_share,
  (c.sample_coupons >= (r.route_total_coupons * 0.5)) AS is_primary
FROM coupon_agg c
JOIN route_totals r
  ON c.op_carrier = r.op_carrier 
 AND c.origin = r.origin 
 AND c.dest = r.dest
WHERE r.route_total_coupons >= 5; -- Filter out rare mis-ticketed anomalies
"""

def main():
    client = get_bigquery_client("db1b-1")
    print("🚀 Generating `db1b-1.reporting.ref_regional_route_attribution` from DB1B...")

    t0 = time.time()
    job_config = bigquery.QueryJobConfig()
    job_config.maximum_bytes_billed = 15_000_000_000 # 15 GB billing safeguard
    
    query_job = client.query(DDL_SQL, job_config=job_config)
    print(f"   Job submitted: ID={query_job.job_id}. Waiting for completion...")
    query_job.result()
    t1 = time.time()

    table = client.get_table("db1b-1.reporting.ref_regional_route_attribution")
    mb_scanned = (query_job.total_bytes_billed or 0) / (1024 * 1024)
    print(f"✅ Generated in {t1 - t0:.1f}s!")
    print(f"   Bytes billed: {mb_scanned:.2f} MB")
    print(f"   Table rows: {table.num_rows:,}")
    print(f"   Table size: {(table.num_bytes or 0) / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    main()
