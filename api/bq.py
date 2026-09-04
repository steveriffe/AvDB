"""
BigQuery Query Execution Layer for AvDB API
Includes automatic credential management, query parameterization,
guardrails against high bytes billed, and fallback mock data for offline/test environments.
"""
import os
import subprocess
import logging
from typing import Dict, Any, Optional, List
import pandas as pd
from api.config import settings
from api.cache import get_cache

logger = logging.getLogger("avdb_api.bq")

_bq_client = None
_cached_credentials = None

def get_credentials():
    """Attempts to retrieve valid Google Cloud credentials with caching."""
    global _cached_credentials
    if _cached_credentials is not None:
        return _cached_credentials

    # 1. Try gcloud CLI token first (reliable for local dev when ADC needs re-auth)
    try:
        token = subprocess.check_output(
            ["gcloud", "auth", "print-access-token"], 
            text=True, 
            stderr=subprocess.DEVNULL,
            timeout=8.0
        ).strip()
        if token:
            from google.oauth2.credentials import Credentials
            _cached_credentials = Credentials(token)
            return _cached_credentials
    except Exception:
        pass

    # 2. Fall back to standard ambient ADC (Cloud Run / compute)
    try:
        import google.auth
        creds, _ = google.auth.default()
        _cached_credentials = creds
        return creds
    except Exception:
        pass

    return None


def get_client():
    """Instantiate and cache a BigQuery client if possible."""
    global _bq_client
    if _bq_client is not None:
        return _bq_client

    try:
        from google.cloud import bigquery
        creds = get_credentials()
        if creds:
            _bq_client = bigquery.Client(project=settings.gcp_project_id, credentials=creds)
        else:
            _bq_client = bigquery.Client(project=settings.gcp_project_id)
        return _bq_client
    except Exception as e:
        logger.warning(f"Unable to initialize BigQuery client: {e}")
        return None


def execute_query(query: str, params: Optional[Dict[str, Any]] = None, cache_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Executes a query against BigQuery or checks cache.
    Returns list of dicts.
    """
    cache = get_cache()
    if cache_key:
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

    client = get_client()
    if client is None:
        logger.warning("No BigQuery client available; returning empty result or mock.")
        return []

    try:
        from google.cloud import bigquery
        job_config = bigquery.QueryJobConfig()
        job_config.maximum_bytes_billed = settings.max_bytes_billed

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

        job = client.query(query, job_config=job_config)
        df = job.to_dataframe()
        records = df.to_dict(orient="records")

        # Clean NaN values for valid JSON serialization
        for row in records:
            for k, v in row.items():
                if pd.isna(v):
                    row[k] = None

        if cache_key:
            cache.set(cache_key, records, ttl=settings.cache_ttl_seconds)

        return records
    except Exception as e:
        logger.error(f"BigQuery query failed: {e}")
        raise e
