# Unified Deployment Guide

Deploy frontend and backend together as a single Cloud Run service with one command.

## Quick Deploy

### PowerShell (Windows)

```powershell
.\deploy-cloudrun-unified.ps1 -ProjectId "your-project-id" -Region "us-central1"
```

### Bash (Linux/Mac)

```bash
chmod +x deploy-cloudrun-unified.sh
./deploy-cloudrun-unified.sh your-project-id us-central1
```

## How It Works

The unified deployment:

1. **Builds Next.js frontend** as standalone output
2. **Packages FastAPI backend** with all dependencies
3. **Combines both** in a single Docker container
4. **Serves frontend** from FastAPI using StaticFiles
5. **Routes API calls** to `/api/*` endpoints
6. **Deploys as one service** to Cloud Run

## Architecture

```
┌─────────────────────────────────────┐
│     Cloud Run Container             │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   FastAPI (Port 8080)        │  │
│  │                              │  │
│  │  • /api/* → API endpoints    │  │
│  │  • /_next/static → Static    │  │
│  │  • /* → Frontend (SPA)       │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   Next.js Frontend (Built)   │  │
│  │   • Static files             │  │
│  │   • Standalone output        │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

## Configuration

### Environment Variables

Set these when deploying:

```bash
gcloud run services update lead-discovery-app \
  --update-secrets=GOOGLE_SHEETS_CREDENTIALS_PATH=credentials-json:latest \
  --update-env-vars="GOOGLE_SHEETS_SPREADSHEET_ID=YOUR_SHEET_ID,GOOGLE_SHEETS_WORKSHEET_NAME=Leads,GOOGLE_MAPS_API_KEY=YOUR_API_KEY" \
  --region=us-central1 \
  --project=YOUR_PROJECT_ID
```

### Secrets

1. **Store credentials:**
   ```bash
   gcloud secrets create credentials-json --data-file=credentials.json --project=YOUR_PROJECT_ID
   ```

2. **Grant access:**
   ```bash
   gcloud secrets add-iam-policy-binding credentials-json \
     --member="serviceAccount:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor" \
     --project=YOUR_PROJECT_ID
   ```

## Benefits

✅ **Single deployment** - One command, one service  
✅ **Simpler architecture** - No CORS issues  
✅ **Lower cost** - One service instead of two  
✅ **Easier management** - One URL, one service to monitor  
✅ **Faster** - No network latency between frontend/backend  

## Local Testing

Test the unified build locally:

```bash
# Build the Docker image
docker build -t lead-discovery-app --build-arg NEXT_PUBLIC_API_URL=/api .

# Run locally
docker run -p 8080:8080 \
  -e GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id \
  -e GOOGLE_MAPS_API_KEY=your_api_key \
  -v $(pwd)/credentials.json:/app/credentials/credentials.json:ro \
  lead-discovery-app
```

Visit: `http://localhost:8080`

## Troubleshooting

### Frontend not loading

Check that:
1. Frontend was built successfully (check Cloud Build logs)
2. Static files are mounted correctly
3. FastAPI is serving from correct path

### API calls failing

Verify:
1. API routes are prefixed with `/api`
2. CORS is configured correctly
3. Backend is running on port 8000 internally

### Build fails

Check:
1. `cloudbuild.yaml` is in project root
2. `Dockerfile` is in project root
3. All dependencies are listed in `requirements.txt` and `backend/requirements.txt`

## Updating

To update the deployment:

```bash
# Rebuild and redeploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/lead-discovery-app \
  --project=YOUR_PROJECT_ID --config=cloudbuild.yaml

gcloud run deploy lead-discovery-app \
  --image gcr.io/YOUR_PROJECT_ID/lead-discovery-app \
  --platform managed --region us-central1 \
  --project=YOUR_PROJECT_ID
```

Or use the deployment script again - it will update the existing service.

## Files

- `Dockerfile` - Unified container build
- `cloudbuild.yaml` - Cloud Build configuration
- `deploy-cloudrun-unified.ps1` - PowerShell deployment script
- `deploy-cloudrun-unified.sh` - Bash deployment script
- `backend/main.py` - FastAPI with frontend serving logic

## Next Steps

1. Deploy using the script
2. Configure secrets and environment variables
3. Test the application
4. Set up monitoring and alerts

For detailed Cloud Run setup, see [DEPLOYMENT_GCP.md](./DEPLOYMENT_GCP.md).

