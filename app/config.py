import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    gcp_project_id: str = os.getenv("GCP_PROJECT_ID", "")
    gcp_region: str = os.getenv("GCP_REGION", "us-central1")
    dataset_raw: str = os.getenv("BIGQUERY_DATASET_RAW", "avdb_raw")
    dataset_analytics: str = os.getenv("BIGQUERY_DATASET_ANALYTICS", "avdb_marts")
    app_title: str = "AvDB — Aviation Intelligence Dashboard"
    page_icon: str = "✈️"

settings = Settings()

