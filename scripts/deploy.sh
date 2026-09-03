#!/usr/bin/env bash
# ==============================================================================
# AvDB Production Cloud Run Deployment & Custom Domain Mapping Script
# ==============================================================================
set -e

PROJECT_ID=${GCP_PROJECT_ID:-"db1b-1"}
REGION=${GCP_REGION:-"us-central1"}
SERVICE_NAME="avdb"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"
ALLOWED_EMAILS=${ALLOWED_EMAILS:-"steve@riffe.co.uk"}

echo "🚀 Building container image for AvDB..."
gcloud builds submit --tag "${IMAGE_NAME}" --project "${PROJECT_ID}" -f docker/Dockerfile .

echo "📦 Deploying ${SERVICE_NAME} to Google Cloud Run (Wallet Protection Guardrails Active)..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE_NAME}" \
  --platform managed \
  --region "${REGION}" \
  --project "${PROJECT_ID}" \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 2 \
  --concurrency 80 \
  --cpu 1 \
  --memory 2Gi \
  --set-env-vars GCP_PROJECT_ID="${PROJECT_ID}",ALLOWED_EMAILS="${ALLOWED_EMAILS}",GOOGLE_CLIENT_ID="${GOOGLE_CLIENT_ID}",GOOGLE_CLIENT_SECRET="${GOOGLE_CLIENT_SECRET}"

echo "🌐 Mapping custom domain avdb.riffe.co.uk to Cloud Run..."
gcloud beta run domain-mappings create \
  --service "${SERVICE_NAME}" \
  --domain "avdb.riffe.co.uk" \
  --region "${REGION}" \
  --project "${PROJECT_ID}" || echo "Domain mapping already exists or pending DNS verification."

echo "✅ Deployment completed!"
echo "👉 Check Cloud Run domain mapping status with: gcloud beta run domain-mappings describe --domain avdb.riffe.co.uk --region ${REGION}"
