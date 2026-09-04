import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class APISettings(BaseSettings):
    app_name: str = "AvDB Native API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

    # GCP & BigQuery Settings
    gcp_project_id: str = os.getenv("GCP_PROJECT_ID", "db1b-1")
    dataset_reporting: str = os.getenv("BIGQUERY_DATASET_REPORTING", "db1b-1.reporting")
    max_bytes_billed: int = int(os.getenv("MAX_BYTES_BILLED", "10000000000"))  # 10 GB limit

    # Cache Settings
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))  # 1 hour
    redis_url: str = os.getenv("REDIS_URL", "")

    # CORS configuration for iOS App, local dev, and web clients
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://127.0.0.1:8000",
        "https://avdb.riffe.co.uk",
        "https://api.avdb.riffe.co.uk",
        "*"  # Allow all for iOS native clients
    ]

    # Mapbox configuration
    mapbox_token: str = os.getenv("MAPBOX_ACCESS_TOKEN_PUBLIC", os.getenv("MAPBOX_API_KEY", ""))
    mapbox_style_personal: str = os.getenv("MAPBOX_STYLE_URL_PERSONAL", "")
    mapbox_style_love: str = os.getenv("MAPBOX_STYLE_URL_LOVE", "")
    mapbox_style_mono: str = os.getenv("MAPBOX_STYLE_URL_MONO", "")

settings = APISettings()
