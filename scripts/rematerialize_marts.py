"""
Rematerializes all analytical marts in `reporting` across 1990-2026.
Uses Google BigQuery client with wallet safeguards.
"""
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from app.utils.bq_client import get_bigquery_client
from google.cloud import bigquery

MODELS = [
    "analytics/models/mart_airport_network_summary.sql",
    "analytics/models/mart_airline_network_performance.sql",
    "analytics/models/mart_fleet_route_dynamics.sql"
]

def main():
    client = get_bigquery_client("db1b-1")
    print(f"🚀 Starting re-materialization of reporting marts (1990–2026) in project `db1b-1`...")

    for model_rel_path in MODELS:
        model_path = REPO_ROOT / model_rel_path
        model_name = model_path.stem
        print(f"\n=======================================================")
        print(f"🔨 Materializing: {model_name}")
        print(f"   Source SQL: {model_path}")
        print(f"=======================================================")
        
        with open(model_path, "r") as f:
            sql = f.read()

        job_config = bigquery.QueryJobConfig()
        # 10 GB billing safeguard
        job_config.maximum_bytes_billed = 10_000_000_000

        t0 = time.time()
        query_job = client.query(sql, job_config=job_config)
        print(f"   Job submitted: ID={query_job.job_id}. Waiting for completion...")
        query_job.result() # Wait for job to finish
        t1 = time.time()

        table = client.get_table(f"db1b-1.reporting.{model_name}")
        mb_scanned = (query_job.total_bytes_billed or 0) / (1024 * 1024)
        print(f"✅ Finished in {t1 - t0:.1f}s!")
        print(f"   Bytes billed: {mb_scanned:.2f} MB")
        print(f"   Table rows: {table.num_rows:,}")
        print(f"   Table size: {(table.num_bytes or 0) / (1024 * 1024):.2f} MB")

    print(f"\n🎉 All 3 reporting marts successfully re-materialized for 1990–2026!")

if __name__ == "__main__":
    main()

