# PowerShell script to deploy to Cloud Run
# Usage: .\deploy-cloudrun.ps1 -ProjectId "your-project-id" -Region "us-central1"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-central1",
    
    [Parameter(Mandatory=$false)]
    [string]$BackendUrl = ""
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Deploying Lead Discovery System to Cloud Run..." -ForegroundColor Green
Write-Host "Project: $ProjectId"
Write-Host "Region: $Region"
Write-Host ""

# Enable required APIs
Write-Host "📦 Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable cloudbuild.googleapis.com --project=$ProjectId
gcloud services enable run.googleapis.com --project=$ProjectId
gcloud services enable containerregistry.googleapis.com --project=$ProjectId
gcloud services enable secretmanager.googleapis.com --project=$ProjectId

# Deploy Backend
Write-Host ""
Write-Host "🔨 Building and deploying Backend..." -ForegroundColor Cyan
$backendImage = "gcr.io/$ProjectId/lead-discovery-backend"
gcloud builds submit --tag $backendImage --project=$ProjectId --config=backend/cloudbuild.yaml

gcloud run deploy lead-discovery-backend `
    --image $backendImage `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --memory 2Gi `
    --cpu 2 `
    --timeout 3600 `
    --max-instances 10 `
    --set-env-vars="PYTHONUNBUFFERED=1" `
    --project=$ProjectId

$backendUrl = gcloud run services describe lead-discovery-backend --platform managed --region $Region --format 'value(status.url)' --project=$ProjectId
Write-Host "✅ Backend deployed at: $backendUrl" -ForegroundColor Green

# Deploy Frontend
Write-Host ""
Write-Host "🔨 Building and deploying Frontend..." -ForegroundColor Cyan
$frontendImage = "gcr.io/$ProjectId/lead-discovery-frontend"
$apiUrl = if ($BackendUrl) { $BackendUrl } else { $backendUrl }

gcloud builds submit `
    --tag $frontendImage `
    --substitutions=_NEXT_PUBLIC_API_URL=$apiUrl `
    --project=$ProjectId `
    --config=frontend/cloudbuild.yaml

gcloud run deploy lead-discovery-frontend `
    --image $frontendImage `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --memory 512Mi `
    --cpu 1 `
    --timeout 300 `
    --max-instances 10 `
    --set-env-vars="NEXT_PUBLIC_API_URL=$apiUrl" `
    --project=$ProjectId

$frontendUrl = gcloud run services describe lead-discovery-frontend --platform managed --region $Region --format 'value(status.url)' --project=$ProjectId
Write-Host ""
Write-Host "✅ Frontend deployed at: $frontendUrl" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  Next steps:" -ForegroundColor Yellow
Write-Host "1. Upload credentials.json to Secret Manager:"
Write-Host "   gcloud secrets create credentials-json --data-file=credentials.json --project=$ProjectId"
Write-Host ""
Write-Host "2. Grant Cloud Run service account access:"
Write-Host "   gcloud secrets add-iam-policy-binding credentials-json --member=`"serviceAccount:YOUR_SERVICE_ACCOUNT@$ProjectId.iam.gserviceaccount.com`" --role=`"roles/secretmanager.secretAccessor`" --project=$ProjectId"
Write-Host ""
Write-Host "3. Update backend service with secret:"
Write-Host "   gcloud run services update lead-discovery-backend --update-secrets=GOOGLE_SHEETS_CREDENTIALS_PATH=credentials-json:latest --region=$Region --project=$ProjectId"

