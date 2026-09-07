import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    gcp_project_id: str = os.getenv("GCP_PROJECT_ID", "")
    gcp_region: str = os.getenv("GCP_REGION", "us-west1")

    dataset_raw: str = os.getenv("BIGQUERY_DATASET_RAW", "avdb_raw")
    dataset_analytics: str = os.getenv("BIGQUERY_DATASET_ANALYTICS", "avdb_marts")
    app_title: str = "AvDB — Aviation Intelligence Dashboard"
    page_icon: str = "✈️"

    # Google OAuth & Security Settings
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    allowed_emails_raw: str = os.getenv("ALLOWED_EMAILS", "*")
    redirect_uri_override: str = os.getenv("REDIRECT_URI_OVERRIDE", "")

    # Local Dev Bypass (Strictly disabled in Cloud Run or production environments)
    local_dev_bypass_auth: bool = (
        os.getenv("LOCAL_DEV_BYPASS_AUTH", "false").lower() in ("true", "1", "yes")
        and not bool(os.getenv("K_SERVICE"))
    )

    # Mapbox Settings
    mapbox_token: str = os.getenv("MAPBOX_ACCESS_TOKEN_PUBLIC", os.getenv("MAPBOX_API_KEY", ""))
    mapbox_style_personal: str = os.getenv("MAPBOX_STYLE_URL_PERSONAL", "")
    mapbox_style_love: str = os.getenv("MAPBOX_STYLE_URL_LOVE", "")
    mapbox_style_mono: str = os.getenv("MAPBOX_STYLE_URL_MONO", "")

    @property
    def allowed_emails(self) -> list[str]:
        return [email.strip().lower() for email in self.allowed_emails_raw.split(",") if email.strip()]

settings = Settings()


