import os
import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional
from google.cloud import bigquery
from app.config import settings

@st.cache_resource
def get_bigquery_client(project_id: Optional[str] = None) -> bigquery.Client:
    """Instantiate and cache a BigQuery client using GCP ADC or Project ID."""
    proj = project_id or settings.gcp_project_id or None
    return bigquery.Client(project=proj)

@st.cache_data(ttl=3600, show_spinner=False)
def run_query(query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Execute a parameterized SQL query against BigQuery with 1-hour cache.
    """
    client = get_bigquery_client()
    job_config = bigquery.QueryJobConfig()
    
    if params:
        query_params = []
        for key, val in params.items():
            if isinstance(val, int):
                param_type = "INT64"
            elif isinstance(val, float):
                param_type = "FLOAT64"
            elif isinstance(val, bool):
                param_type = "BOOL"
            elif isinstance(val, list):
                param_type = "ARRAY<STRING>"
            else:
                param_type = "STRING"
            query_params.append(bigquery.ScalarQueryParameter(key, param_type, val))
        job_config.query_parameters = query_params

    query_job = client.query(query, job_config=job_config)
    return query_job.to_dataframe()

