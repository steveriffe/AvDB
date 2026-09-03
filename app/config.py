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
    allowed_emails_raw: str = os.getenv("ALLOWED_EMAILS", "steve@riffe.co.uk")
    redirect_uri_override: str = os.getenv("REDIRECT_URI_OVERRIDE", "")

    @property
    def allowed_emails(self) -> list[str]:
        return [email.strip().lower() for email in self.allowed_emails_raw.split(",") if email.strip()]

settings = Settings()


