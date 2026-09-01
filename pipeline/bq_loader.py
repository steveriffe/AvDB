"""
AvDB BigQuery Ingestion and Pipeline Utilities
"""
import os
import pandas as pd
from google.cloud import bigquery
from app.config import settings

def load_dataframe_to_bq(
    df: pd.DataFrame,
    table_name: str,
    dataset_name: str = settings.dataset_raw,
    write_disposition: str = "WRITE_APPEND",
    time_partitioning_field: str = None
) -> bigquery.LoadJob:
    """
    Loads a pandas DataFrame into a BigQuery table with schema auto-detection or parquet format.
    """
    client = bigquery.Client(project=settings.gcp_project_id or None)
    table_id = f"{client.project}.{dataset_name}.{table_name}"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition=write_disposition,
    )
    if time_partitioning_field:
        job_config.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field=time_partitioning_field,
        )

    load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    load_job.result()  # Wait for table load to complete
    print(f"Loaded {len(df)} rows into {table_id}")
    return load_job

