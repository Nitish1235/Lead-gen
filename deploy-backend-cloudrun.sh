#!/bin/bash
# Deploy Backend to Cloud Run

set -e

PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"us-central1"}
SERVICE_NAME="lead-discovery-backend"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying Backend to Cloud Run..."
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Service: ${SERVICE_NAME}"

# Enable required APIs
echo "📦 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com --project=${PROJECT_ID}
gcloud services enable run.googleapis.com --project=${PROJECT_ID}
gcloud services enable containerregistry.googleapis.com --project=${PROJECT_ID}

# Build and push Docker image
echo "🔨 Building Docker image..."
gcloud builds submit --tag ${IMAGE_NAME} --project=${PROJECT_ID} --config=backend/cloudbuild.yaml

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --max-instances 10 \
  --set-env-vars="PYTHONUNBUFFERED=1" \
  --project=${PROJECT_ID}

# Get service URL
BACKEND_URL=$(gcloud run services describe ${SERVICE_NAME} --platform managed --region ${REGION} --format 'value(status.url)' --project=${PROJECT_ID})
echo "✅ Backend deployed!"
echo "Backend URL: ${BACKEND_URL}"
echo ""
echo "⚠️  Don't forget to:"
echo "1. Set GOOGLE_SHEETS_CREDENTIALS_PATH secret (if using Secret Manager)"
echo "2. Upload credentials.json as a secret:"
echo "   gcloud secrets create credentials-json --data-file=credentials.json --project=${PROJECT_ID}"
echo "3. Grant Cloud Run service account access to the secret"
echo "4. Update service with secret:"
echo "   gcloud run services update ${SERVICE_NAME} --update-secrets=GOOGLE_SHEETS_CREDENTIALS_PATH=credentials-json:latest --region=${REGION} --project=${PROJECT_ID}"

