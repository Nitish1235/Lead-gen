# PowerShell script to deploy unified frontend+backend to Cloud Run
# Usage: .\deploy-cloudrun-unified.ps1 -ProjectId "your-project-id" -Region "us-central1"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-central1"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Deploying Lead Discovery System (Unified) to Cloud Run..." -ForegroundColor Green
Write-Host "Project: $ProjectId"
Write-Host "Region: $Region"
Write-Host ""

# Enable required APIs
Write-Host "📦 Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable cloudbuild.googleapis.com --project=$ProjectId
gcloud services enable run.googleapis.com --project=$ProjectId
gcloud services enable containerregistry.googleapis.com --project=$ProjectId
gcloud services enable secretmanager.googleapis.com --project=$ProjectId

# Build and push Docker image
Write-Host ""
Write-Host "🔨 Building unified Docker image..." -ForegroundColor Cyan
$imageName = "gcr.io/$ProjectId/lead-discovery-app"
gcloud builds submit --tag $imageName --project=$ProjectId --config=cloudbuild.yaml

# Deploy to Cloud Run
Write-Host ""
Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Cyan
gcloud run deploy lead-discovery-app `
    --image $imageName `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --memory 2Gi `
    --cpu 2 `
    --timeout 3600 `
    --max-instances 10 `
    --port 8080 `
    --set-env-vars="PYTHONUNBUFFERED=1" `
    --project=$ProjectId

# Get service URL
$serviceUrl = gcloud run services describe lead-discovery-app --platform managed --region $Region --format 'value(status.url)' --project=$ProjectId

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "Application URL: $serviceUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  Next steps:" -ForegroundColor Yellow
Write-Host "1. Upload credentials.json to Secret Manager:"
Write-Host "   gcloud secrets create credentials-json --data-file=credentials.json --project=$ProjectId"
Write-Host ""
Write-Host "2. Grant Cloud Run service account access:"
Write-Host "   gcloud secrets add-iam-policy-binding credentials-json --member=`"serviceAccount:YOUR_SERVICE_ACCOUNT@$ProjectId.iam.gserviceaccount.com`" --role=`"roles/secretmanager.secretAccessor`" --project=$ProjectId"
Write-Host ""
Write-Host "3. Update service with secret and environment variables:"
Write-Host "   gcloud run services update lead-discovery-app --update-secrets=GOOGLE_SHEETS_CREDENTIALS_PATH=credentials-json:latest --update-env-vars=`"GOOGLE_SHEETS_SPREADSHEET_ID=YOUR_SHEET_ID,GOOGLE_SHEETS_WORKSHEET_NAME=Leads,GOOGLE_MAPS_API_KEY=YOUR_API_KEY`" --region=$Region --project=$ProjectId"

