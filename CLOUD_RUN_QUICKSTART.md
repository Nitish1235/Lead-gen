# Cloud Run Quick Start

Get your Lead Discovery System deployed to Cloud Run in minutes!

## Prerequisites

- Google Cloud account with billing enabled
- `gcloud` CLI installed and authenticated
- `credentials.json` file ready
- Google Sheets and Maps API keys

## Quick Deploy (PowerShell)

```powershell
# 1. Set your project ID
$PROJECT_ID = "your-project-id"

# 2. Store credentials in Secret Manager
gcloud secrets create credentials-json --data-file=credentials.json --project=$PROJECT_ID

# 3. Deploy everything
.\deploy-cloudrun.ps1 -ProjectId $PROJECT_ID -Region "us-central1"
```

## Quick Deploy (Bash)

```bash
# 1. Set your project ID
export PROJECT_ID="your-project-id"

# 2. Store credentials in Secret Manager
gcloud secrets create credentials-json --data-file=credentials.json --project=$PROJECT_ID

# 3. Deploy backend
./deploy-backend-cloudrun.sh $PROJECT_ID us-central1

# 4. Note the backend URL, then deploy frontend
# (Replace BACKEND_URL with actual URL from step 3)
./deploy-frontend-cloudrun.sh $PROJECT_ID us-central1 BACKEND_URL
```

## Manual Steps (If Scripts Don't Work)

### 1. Enable APIs

```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com \
  containerregistry.googleapis.com secretmanager.googleapis.com \
  --project=YOUR_PROJECT_ID
```

### 2. Store Credentials

```bash
gcloud secrets create credentials-json \
  --data-file=credentials.json \
  --project=YOUR_PROJECT_ID
```

### 3. Deploy Backend

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/lead-discovery-backend \
  --project=YOUR_PROJECT_ID --config=backend/cloudbuild.yaml

gcloud run deploy lead-discovery-backend \
  --image gcr.io/YOUR_PROJECT_ID/lead-discovery-backend \
  --platform managed --region us-central1 \
  --allow-unauthenticated --memory 2Gi --cpu 2 \
  --update-secrets=GOOGLE_SHEETS_CREDENTIALS_PATH=credentials-json:latest \
  --set-env-vars="GOOGLE_SHEETS_SPREADSHEET_ID=YOUR_SHEET_ID,GOOGLE_SHEETS_WORKSHEET_NAME=Leads,GOOGLE_MAPS_API_KEY=YOUR_API_KEY" \
  --project=YOUR_PROJECT_ID
```

### 4. Get Backend URL and Deploy Frontend

```bash
BACKEND_URL=$(gcloud run services describe lead-discovery-backend \
  --platform managed --region us-central1 \
  --format 'value(status.url)' --project=YOUR_PROJECT_ID)

gcloud builds submit \
  --tag gcr.io/YOUR_PROJECT_ID/lead-discovery-frontend \
  --substitutions=_NEXT_PUBLIC_API_URL=$BACKEND_URL \
  --project=YOUR_PROJECT_ID --config=frontend/cloudbuild.yaml

gcloud run deploy lead-discovery-frontend \
  --image gcr.io/YOUR_PROJECT_ID/lead-discovery-frontend \
  --platform managed --region us-central1 \
  --allow-unauthenticated --memory 512Mi \
  --set-env-vars="NEXT_PUBLIC_API_URL=$BACKEND_URL" \
  --project=YOUR_PROJECT_ID
```

### 5. Update Backend CORS

```bash
FRONTEND_URL=$(gcloud run services describe lead-discovery-frontend \
  --platform managed --region us-central1 \
  --format 'value(status.url)' --project=YOUR_PROJECT_ID)

gcloud run services update lead-discovery-backend \
  --update-env-vars="ALLOWED_ORIGINS=$FRONTEND_URL" \
  --region us-central1 --project=YOUR_PROJECT_ID
```

## Verify Deployment

1. Get your frontend URL:
   ```bash
   gcloud run services describe lead-discovery-frontend \
     --platform managed --region us-central1 \
     --format 'value(status.url)' --project=YOUR_PROJECT_ID
   ```

2. Open the URL in your browser

3. Test by starting a discovery with a small search

## Troubleshooting

### Check Logs

```bash
# Backend logs
gcloud run services logs tail lead-discovery-backend --region us-central1

# Frontend logs
gcloud run services logs tail lead-discovery-frontend --region us-central1
```

### Common Issues

1. **Credentials not found**: Make sure secret is created and mounted
2. **CORS errors**: Update `ALLOWED_ORIGINS` env var
3. **Build fails**: Check Cloud Build logs in GCP Console

## Costs

- **Free tier**: 2M requests/month, 360K GB-seconds/month
- **Typical usage**: $0-3/month for moderate use

## Next Steps

- Set up custom domain (optional)
- Configure monitoring and alerts
- Set up CI/CD pipeline
- Read full guide: [DEPLOYMENT_GCP.md](./DEPLOYMENT_GCP.md)

