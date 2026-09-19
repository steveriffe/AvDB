"""
High-Efficiency BTS DB1B Market Ingestion Pipeline
Downloads quarterly BTS TranStats DB1B Market PREZIP archives, filters valid fares ($20-$2,500),
pre-aggregates route-carrier passenger and revenue metrics in memory, and loads into BigQuery.

Avoids downloading 500GB+ raw coupon files (OD40) by utilizing lightweight DB1B Market summaries.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import io
import os
import zipfile
import urllib.request
import argparse
import pandas as pd
from datetime import datetime
from google.cloud import bigquery
from app.utils.bq_client import get_bigquery_client


BASE_URL = "https://transtats.bts.gov/PREZIP/Origin_and_Destination_Survey_DB1BMarket_{year}_{quarter}.zip"
DEST_TABLE = "db1b-1.reporting.agg_db1b_market_summary"

COLS_TO_LOAD = [
    "Year", "Quarter", "Origin", "Dest", 
    "OpCarrier", "RPCarrier", "TkCarrier", 
    "Passengers", "MktFare", "MktDistance"
]


def download_and_aggregate_quarter(year: int, quarter: int) -> pd.DataFrame:
    """Downloads one quarter of DB1B Market, cleans fares, and pre-aggregates by route-carrier."""
    url = BASE_URL.format(year=year, quarter=quarter)
    print(f"📥 [{year} Q{quarter}] Downloading from TranStats: {url}...")
    
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (AvDB Pipeline)"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        content = resp.read()
        
    print(f"📦 [{year} Q{quarter}] Downloaded {len(content) / (1024 * 1024):.1f} MB. Extracting CSV...")
    zf = zipfile.ZipFile(io.BytesIO(content))
    csv_filename = [f for f in zf.namelist() if f.endswith(".csv")][0]
    
    with zf.open(csv_filename) as f:
        df = pd.read_csv(
            f,
            usecols=lambda c: c.strip().strip('"') in COLS_TO_LOAD,
            dtype={
                "Year": int,
                "Quarter": int,
                "Origin": str,
                "Dest": str,
                "OpCarrier": str,
                "RPCarrier": str,
                "TkCarrier": str,
                "Passengers": float,
                "MktFare": float,
                "MktDistance": float
            },
            low_memory=False
        )
    
    # Standardize column names
    df.columns = [c.strip().strip('"') for c in df.columns]
    raw_rows = len(df)
    
    # Data Integrity & Outlier Filtering ($20 to $2,500 typical valid passenger ticket bounds)
    df = df[
        (df["Passengers"] > 0) &
        (df["MktFare"] >= 20.0) &
        (df["MktFare"] <= 2500.0) &
        (df["Origin"].str.len() == 3) &
        (df["Dest"].str.len() == 3)
    ].copy()
    
    # Carrier selection: Primary operating carrier with fallback to reporting/ticketing
    df["carrier"] = df["OpCarrier"].fillna("").astype(str).str.strip()
    empty_carrier = df["carrier"].str.len() == 0
    df.loc[empty_carrier, "carrier"] = df.loc[empty_carrier, "RPCarrier"].fillna("").astype(str).str.strip()
    empty_carrier = df["carrier"].str.len() == 0
    df.loc[empty_carrier, "carrier"] = df.loc[empty_carrier, "TkCarrier"].fillna("").astype(str).str.strip()
    
    # 10% survey expansion (standard BTS 10x multiplier for pre-2025 DB1B; 10x for 2015-2024)
    multiplier = 10.0
    df["survey_pax"] = df["Passengers"] * multiplier
    df["revenue"] = df["MktFare"] * df["survey_pax"]
    
    # Group by route and carrier
    agg = df.groupby(["Year", "Quarter", "Origin", "Dest", "carrier"]).agg(
        estimated_od_passengers=("survey_pax", "sum"),
        total_revenue=("revenue", "sum"),
        avg_distance_miles=("MktDistance", "mean")
    ).reset_index()
    
    agg["avg_od_fare"] = (agg["total_revenue"] / agg["estimated_od_passengers"]).round(2)
    agg["yield_per_mile"] = (agg["total_revenue"] / (agg["estimated_od_passengers"] * agg["avg_distance_miles"])).round(4)
    agg["estimated_od_passengers"] = agg["estimated_od_passengers"].round(0).astype(int)
    agg["total_revenue"] = agg["total_revenue"].round(2)
    agg["avg_distance_miles"] = agg["avg_distance_miles"].round(1)
    
    # Synthesize flight_date representation for partition alignment (Month 1 of quarter)
    month_start = (quarter - 1) * 3 + 1
    agg["quarter_date"] = pd.to_datetime(agg.apply(lambda r: f"{int(r['Year'])}-{month_start:02d}-01", axis=1))
    
    print(f"✅ [{year} Q{quarter}] Compressed {raw_rows:,} raw records into {len(agg):,} route-carrier summaries.")
    return agg


def ensure_destination_table_exists(client: bigquery.Client):
    """Creates or verifies the aggregated DB1B market destination table."""
    schema = [
        bigquery.SchemaField("quarter_date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("Year", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("Quarter", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("Origin", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("Dest", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("carrier", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("estimated_od_passengers", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("total_revenue", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("avg_distance_miles", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("avg_od_fare", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("yield_per_mile", "FLOAT", mode="NULLABLE"),
    ]
    
    table = bigquery.Table(DEST_TABLE, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.YEAR,
        field="quarter_date"
    )
    table.clustering_fields = ["Origin", "Dest", "carrier"]
    
    try:
        client.create_table(table, exists_ok=True)
        tbl_info = client.get_table(DEST_TABLE)
        existing_cols = {f.name: f.field_type for f in tbl_info.schema}
        expected_cols = {f.name: f.field_type for f in schema}
        missing_cols = set(expected_cols.keys()) - set(existing_cols.keys())
        if missing_cols:
            print(f"⚠️ Destination table {DEST_TABLE} missing columns: {missing_cols}")
        else:
            partition_str = f"Partitioned by {tbl_info.time_partitioning.field}" if tbl_info.time_partitioning else "No partition"
            cluster_str = f"Clustered by {', '.join(tbl_info.clustering_fields)}" if tbl_info.clustering_fields else "No cluster"
            print(f"✅ Verified destination table: {DEST_TABLE} ({tbl_info.num_rows:,} rows, {partition_str}, {cluster_str})")
    except Exception as e:
        print(f"Table verification notice: {e}")


def load_quarter_to_bigquery(df_agg: pd.DataFrame, client: bigquery.Client):
    """Loads aggregated dataframe to BigQuery, replacing the existing quarter if re-ingesting."""
    if df_agg.empty:
        return
    
    year = int(df_agg["Year"].iloc[0])
    quarter = int(df_agg["Quarter"].iloc[0])
    
    # Delete existing data for this quarter if re-running to avoid duplicates
    delete_dml = f"""
    DELETE FROM `{DEST_TABLE}`
    WHERE Year = {year} AND Quarter = {quarter};
    """
    try:
        del_job = client.query(delete_dml)
        del_job.result()
        if del_job.num_dml_affected_rows and del_job.num_dml_affected_rows > 0:
            print(f"🧹 Purged {del_job.num_dml_affected_rows:,} existing rows for {year} Q{quarter} from `{DEST_TABLE}`.")
    except Exception:
        pass
        
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION]
    )
    
    job = client.load_table_from_dataframe(df_agg, DEST_TABLE, job_config=job_config)
    job.result()
    print(f"🚀 Loaded {len(df_agg):,} rows for {year} Q{quarter} into `{DEST_TABLE}`.")


def backfill_mart_fares(client: bigquery.Client, year: int, quarter: int):
    """Updates reporting.mart_airport_network_summary and reporting.mart_airline_network_performance
    with average fares and yields from agg_db1b_market_summary."""
    month_start = (quarter - 1) * 3 + 1
    months = [month_start, month_start + 1, month_start + 2]
    months_str = ", ".join(str(m) for m in months)
    
    # 1. Backfill mart_airport_network_summary
    update_airports_sql = f"""
    UPDATE `db1b-1.reporting.mart_airport_network_summary` m
    SET 
        m.avg_od_fare = f.avg_od_fare,
        m.estimated_od_passengers = f.estimated_od_passengers
    FROM (
        SELECT 
            Year, Origin, Dest, carrier,
            ROUND(SAFE_DIVIDE(SUM(total_revenue), SUM(estimated_od_passengers)), 2) AS avg_od_fare,
            ROUND(SUM(estimated_od_passengers) / 3, 0) AS estimated_od_passengers
        FROM `{DEST_TABLE}`
        WHERE Year = {year} AND Quarter = {quarter}
        GROUP BY 1, 2, 3, 4
    ) f
    WHERE m.year = f.Year
      AND m.origin = f.Origin
      AND m.dest = f.Dest
      AND m.unique_carrier = f.carrier
      AND m.month IN ({months_str})
      AND m.avg_od_fare IS NULL;
    """
    
    # 2. Backfill mart_airline_network_performance
    update_airlines_sql = f"""
    UPDATE `db1b-1.reporting.mart_airline_network_performance` m
    SET 
        m.avg_od_fare = f.avg_od_fare,
        m.yield_per_mile = COALESCE(
            ROUND(SAFE_DIVIDE(f.avg_od_fare, NULLIF(m.avg_stage_length_miles, 0)), 4),
            f.yield_per_mile
        )
    FROM (
        SELECT 
            Year, Origin, Dest, carrier,
            ROUND(SAFE_DIVIDE(SUM(total_revenue), SUM(estimated_od_passengers)), 2) AS avg_od_fare,
            ROUND(SAFE_DIVIDE(SUM(total_revenue), NULLIF(SUM(estimated_od_passengers * avg_distance_miles), 0)), 4) AS yield_per_mile
        FROM `{DEST_TABLE}`
        WHERE Year = {year} AND Quarter = {quarter}
        GROUP BY 1, 2, 3, 4
    ) f
    WHERE m.year = f.Year
      AND m.origin = f.Origin
      AND m.dest = f.Dest
      AND m.unique_carrier = f.carrier
      AND m.month IN ({months_str})
      AND (m.avg_od_fare IS NULL OR m.yield_per_mile IS NULL);
    """
    
    try:
        job_airports = client.query(update_airports_sql)
        job_airports.result()
        airports_affected = job_airports.num_dml_affected_rows or 0
        print(f"✨ Backfilled fares into `mart_airport_network_summary` for {year} Q{quarter} ({airports_affected:,} rows updated).")
    except Exception as e:
        print(f"Notice: Failed to backfill airport mart fares for {year} Q{quarter}: {e}")
        airports_affected = 0

    try:
        job_airlines = client.query(update_airlines_sql)
        job_airlines.result()
        airlines_affected = job_airlines.num_dml_affected_rows or 0
        print(f"✨ Backfilled fares/yields into `mart_airline_network_performance` for {year} Q{quarter} ({airlines_affected:,} rows updated).")
    except Exception as e:
        print(f"Notice: Failed to backfill airline mart fares for {year} Q{quarter}: {e}")
        airlines_affected = 0
        
    return airports_affected, airlines_affected


def main():
    parser = argparse.ArgumentParser(description="BTS DB1B Market Historical Ingestion")
    parser.add_argument("--years", nargs="+", type=int, default=[2024], help="Years to ingest (e.g. 2024 2023)")
    parser.add_argument("--quarters", nargs="+", type=int, default=[1, 2, 3, 4], help="Quarters to ingest (1 2 3 4)")
    parser.add_argument("--backfill-only", action="store_true", help="Only run backfill against existing agg_db1b_market_summary data")
    args = parser.parse_args()
    
    client = get_bigquery_client()
    ensure_destination_table_exists(client)
    
    for y in args.years:
        for q in args.quarters:
            if args.backfill_only:
                print(f"\n🔄 [{y} Q{q}] Running backfill-only mode...")
                backfill_mart_fares(client, y, q)
                continue
                
            try:
                df_quarter = download_and_aggregate_quarter(y, q)
                load_quarter_to_bigquery(df_quarter, client)
                backfill_mart_fares(client, y, q)
            except Exception as e:
                print(f"❌ Error processing {y} Q{q}: {e}")

    print("\n🏁 Ingestion batch completed successfully.")


if __name__ == "__main__":
    main()
