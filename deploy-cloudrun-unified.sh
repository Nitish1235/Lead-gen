#!/bin/bash
# Deploy unified frontend+backend to Cloud Run

set -e

PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"us-central1"}
SERVICE_NAME="lead-discovery-app"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying Lead Discovery System (Unified) to Cloud Run..."
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Service: ${SERVICE_NAME}"

# Enable required APIs
echo "📦 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com --project=${PROJECT_ID}
gcloud services enable run.googleapis.com --project=${PROJECT_ID}
gcloud services enable containerregistry.googleapis.com --project=${PROJECT_ID}
gcloud services enable secretmanager.googleapis.com --project=${PROJECT_ID}

# Build and push Docker image
echo "🔨 Building unified Docker image..."
gcloud builds submit --tag ${IMAGE_NAME} --project=${PROJECT_ID} --config=cloudbuild.yaml

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
  --port 8080 \
  --set-env-vars="PYTHONUNBUFFERED=1" \
  --project=${PROJECT_ID}

# Get service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --platform managed --region ${REGION} --format 'value(status.url)' --project=${PROJECT_ID})

echo ""
echo "✅ Deployment complete!"
echo "Application URL: ${SERVICE_URL}"
echo ""
echo "⚠️  Next steps:"
echo "1. Upload credentials.json to Secret Manager:"
echo "   gcloud secrets create credentials-json --data-file=credentials.json --project=${PROJECT_ID}"
echo ""
echo "2. Grant Cloud Run service account access:"
echo "   gcloud secrets add-iam-policy-binding credentials-json --member=\"serviceAccount:YOUR_SERVICE_ACCOUNT@${PROJECT_ID}.iam.gserviceaccount.com\" --role=\"roles/secretmanager.secretAccessor\" --project=${PROJECT_ID}"
echo ""
echo "3. Update service with secret and environment variables:"
echo "   gcloud run services update ${SERVICE_NAME} --update-secrets=GOOGLE_SHEETS_CREDENTIALS_PATH=credentials-json:latest --update-env-vars=\"GOOGLE_SHEETS_SPREADSHEET_ID=YOUR_SHEET_ID,GOOGLE_SHEETS_WORKSHEET_NAME=Leads,GOOGLE_MAPS_API_KEY=YOUR_API_KEY\" --region=${REGION} --project=${PROJECT_ID}"

