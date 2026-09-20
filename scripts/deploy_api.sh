#!/usr/bin/env bash
# ==============================================================================
# AvDB Native FastAPI Backend Deployment Script to Google Cloud Run
# ==============================================================================
set -e

PROJECT_ID=${GCP_PROJECT_ID:-"db1b-1"}
REGION=${GCP_REGION:-"us-west1"}
SERVICE_NAME="avdb-api"
IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/avdb/api:latest"

echo "🔧 Ensuring required GCP APIs are enabled..."
gcloud services enable cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com --project "${PROJECT_ID}"

echo "🚀 Building container image for AvDB API..."
gcloud builds submit --config=cloudbuild-api.yaml --substitutions=_IMAGE_NAME="${IMAGE_NAME}" --project "${PROJECT_ID}" .

echo "📦 Deploying ${SERVICE_NAME} to Google Cloud Run (Public Unauthenticated Access)..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE_NAME}" \
  --platform managed \
  --region "${REGION}" \
  --project "${PROJECT_ID}" \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 4 \
  --concurrency 80 \
  --cpu 1 \
  --memory 1Gi \
  --set-env-vars GCP_PROJECT_ID="${PROJECT_ID}",BQ_DATASET_REPORTING="reporting",BQ_DATASET_STAGING="staging"

echo "✅ AvDB API Deployment completed!"
API_URL=$(gcloud run services describe "${SERVICE_NAME}" --platform managed --region "${REGION}" --project "${PROJECT_ID}" --format="value(status.url)")
echo "👉 API Endpoint: ${API_URL}"
