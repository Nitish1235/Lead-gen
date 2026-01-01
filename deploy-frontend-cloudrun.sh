#!/bin/bash
# Deploy Frontend to Cloud Run

set -e

PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"us-central1"}
BACKEND_URL=${3:-"https://your-backend-url.run.app"}
SERVICE_NAME="lead-discovery-frontend"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying Frontend to Cloud Run..."
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Backend URL: ${BACKEND_URL}"
echo "Service: ${SERVICE_NAME}"

# Enable required APIs
echo "📦 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com --project=${PROJECT_ID}
gcloud services enable run.googleapis.com --project=${PROJECT_ID}
gcloud services enable containerregistry.googleapis.com --project=${PROJECT_ID}

# Build and push Docker image
echo "🔨 Building Docker image with backend URL..."
gcloud builds submit \
  --tag ${IMAGE_NAME} \
  --substitutions=_NEXT_PUBLIC_API_URL=${BACKEND_URL} \
  --project=${PROJECT_ID} \
  --config=frontend/cloudbuild.yaml

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars="NEXT_PUBLIC_API_URL=${BACKEND_URL}" \
  --project=${PROJECT_ID}

# Get service URL
FRONTEND_URL=$(gcloud run services describe ${SERVICE_NAME} --platform managed --region ${REGION} --format 'value(status.url)' --project=${PROJECT_ID})
echo "✅ Frontend deployed!"
echo "Frontend URL: ${FRONTEND_URL}"
echo ""
echo "🎉 Your application is live at: ${FRONTEND_URL}"

