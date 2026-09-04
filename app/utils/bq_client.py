"""
BigQuery Client Utility with Smart Multi-Tier Authentication
Supports standard ADC, active gcloud CLI token fallback, and Cloud Run IAM.
"""
import os
import subprocess
import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional
import google.auth
from google.oauth2.credentials import Credentials
from google.cloud import bigquery
from app.config import settings


def get_credentials():
    """
    Attempts to retrieve valid Google Cloud credentials with automatic gcloud CLI fallback.
    """
    # 1. Check for active gcloud CLI token (reliable for local dev)
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
        if token:
            return Credentials(token)
    except Exception:
        pass

    # 2. Fall back to standard ambient credentials (Cloud Run / compute)
    try:
        creds, _ = google.auth.default()
        return creds
    except Exception:
        pass

    return None


@st.cache_resource
def get_bigquery_client(project_id: Optional[str] = None) -> bigquery.Client:
    """Instantiate and cache a BigQuery client with smart credential resolution."""
    proj = project_id or settings.gcp_project_id or "db1b-1"
    creds = get_credentials()
    if creds:
        return bigquery.Client(project=proj, credentials=creds)
    return bigquery.Client(project=proj)


@st.cache_data(ttl=3600, show_spinner=False)
def run_query(query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Execute a parameterized SQL query against BigQuery with 1-hour cache.
    """
    client = get_bigquery_client()
    job_config = bigquery.QueryJobConfig()
    # 🛡️ Wallet Protection Guardrail: Max 10 GB scanned per query (~$0.06 ceiling)
    job_config.maximum_bytes_billed = 10_000_000_000

    
    if params:
        query_params = []
        for key, val in params.items():
            if val is None:
                query_params.append(bigquery.ScalarQueryParameter(key, "STRING", None))
            elif isinstance(val, int):
                query_params.append(bigquery.ScalarQueryParameter(key, "INT64", val))
            elif isinstance(val, float):
                query_params.append(bigquery.ScalarQueryParameter(key, "FLOAT64", val))
            elif isinstance(val, bool):
                query_params.append(bigquery.ScalarQueryParameter(key, "BOOL", val))
            elif isinstance(val, list):
                query_params.append(bigquery.ArrayQueryParameter(key, "STRING", val))
            else:
                query_params.append(bigquery.ScalarQueryParameter(key, "STRING", str(val)))
        job_config.query_parameters = query_params

    try:
        query_job = client.query(query, job_config=job_config)
        return query_job.to_dataframe()
    except Exception as e:
        # If token expired mid-session, try refreshing token
        token_creds = get_credentials()
        if token_creds:
            fresh_client = bigquery.Client(project=client.project, credentials=token_creds)
            return fresh_client.query(query, job_config=job_config).to_dataframe()
        raise e
