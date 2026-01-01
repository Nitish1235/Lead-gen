# GCP Cloud Run Deployment Guide

This guide covers deploying the B2B Lead Discovery System on Google Cloud Platform using **Cloud Run** (serverless containers). This is the recommended deployment method for production use.

## Overview

This deployment uses:
- **Cloud Run** for both frontend (Next.js) and backend (FastAPI)
- **Secret Manager** for storing credentials securely
- **Container Registry** for Docker images
- **Cloud Build** for automated builds

**Benefits:**
- ✅ Fully serverless (pay per request)
- ✅ Auto-scaling (0 to N instances)
- ✅ Free tier: 2 million requests, 360,000 GB-seconds/month
- ✅ HTTPS by default
- ✅ Easy CI/CD integration

**Estimated Cost:** $0-10/month (within free tier for moderate usage)

---

## Prerequisites

1. **Google Cloud Platform account** with billing enabled
2. **gcloud CLI** installed and configured
   ```bash
   # Install gcloud CLI: https://cloud.google.com/sdk/docs/install
   # Authenticate
   gcloud auth login
   # Set your project
   gcloud config set project YOUR_PROJECT_ID
   ```
3. **Docker** installed (for local testing, optional)
4. **Google Sheets API** credentials (`credentials.json`)
5. **Google Maps API key**

---

## Quick Start (Unified Deployment)

### Option 1: Using PowerShell Script (Windows)

```powershell
# Navigate to project root
cd "F:\SAAS\Lead Gen"

# Deploy unified frontend+backend (replace with your project ID)
.\deploy-cloudrun-unified.ps1 -ProjectId "your-project-id" -Region "us-central1"
```

### Option 2: Using Bash Script (Linux/Mac)

```bash
# Make script executable
chmod +x deploy-cloudrun-unified.sh

# Deploy unified frontend+backend
./deploy-cloudrun-unified.sh your-project-id us-central1
```

**Note:** This deploys both frontend and backend together as a single service. See [UNIFIED_DEPLOYMENT.md](./UNIFIED_DEPLOYMENT.md) for more details.

---

## Manual Deployment Steps

### Step 1: Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### Step 2: Store Credentials in Secret Manager

```bash
# Create secret from credentials.json file
gcloud secrets create credentials-json \
  --data-file=credentials.json \
  --project=YOUR_PROJECT_ID

# Grant Cloud Run service account access
# First, get your service account email:
SERVICE_ACCOUNT=$(gcloud run services describe lead-discovery-backend \
  --platform managed \
  --region us-central1 \
  --format 'value(spec.template.spec.serviceAccountName)' \
  --project=YOUR_PROJECT_ID)

# If service account is empty, use default compute service account
SERVICE_ACCOUNT="${SERVICE_ACCOUNT:-PROJECT_NUMBER-compute@developer.gserviceaccount.com}"

# Grant access
gcloud secrets add-iam-policy-binding credentials-json \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor" \
  --project=YOUR_PROJECT_ID
```

**Alternative:** You can also mount credentials as a file in Cloud Run using secrets.

### Step 3: Set Environment Variables

Create a `.env.yaml` file (or use `--set-env-vars`):

```yaml
GOOGLE_SHEETS_CREDENTIALS_PATH: /secrets/credentials-json
GOOGLE_SHEETS_SPREADSHEET_ID: your_spreadsheet_id
GOOGLE_SHEETS_WORKSHEET_NAME: Leads
GOOGLE_MAPS_API_KEY: your_maps_api_key
PYTHONUNBUFFERED: "1"
```

### Step 4: Deploy Unified Application

```bash
# Build and push Docker image (unified frontend + backend)
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/lead-discovery-app \
  --project=YOUR_PROJECT_ID \
  --config=cloudbuild.yaml

# Deploy to Cloud Run (single service)
gcloud run deploy lead-discovery-app \
  --image gcr.io/YOUR_PROJECT_ID/lead-discovery-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --max-instances 10 \
  --port 8080 \
  --update-secrets=GOOGLE_SHEETS_CREDENTIALS_PATH=credentials-json:latest \
  --set-env-vars="GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id,GOOGLE_SHEETS_WORKSHEET_NAME=Leads,GOOGLE_MAPS_API_KEY=your_api_key,PYTHONUNBUFFERED=1" \
  --project=YOUR_PROJECT_ID

# Get service URL
SERVICE_URL=$(gcloud run services describe lead-discovery-app \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)' \
  --project=YOUR_PROJECT_ID)

echo "Application URL: $SERVICE_URL"
```

**Note:** The unified deployment serves both frontend and backend from a single URL. No CORS configuration needed!

---

## Dockerfile Overview

### Unified Dockerfile (`Dockerfile`)

- **Stage 1 (Frontend Builder):** Node.js 20-alpine
  - Builds Next.js frontend as standalone output
  
- **Stage 2 (Runtime):** Python 3.11-slim
  - Installs Chrome, Python dependencies
  - Copies built frontend from Stage 1
  - FastAPI serves both API (`/api/*`) and frontend (`/*`)
  - Exposes: PORT 8080 (Cloud Run sets this automatically)

For details, see the `Dockerfile` in the project root.

---

## Configuration Files

### Backend Configuration

Environment variables needed:
- `GOOGLE_SHEETS_CREDENTIALS_PATH`: Path to credentials file (or secret)
- `GOOGLE_SHEETS_SPREADSHEET_ID`: Your Google Sheet ID
- `GOOGLE_SHEETS_WORKSHEET_NAME`: Worksheet name (default: "Leads")
- `GOOGLE_MAPS_API_KEY`: Your Maps API key
- `PORT`: Set automatically by Cloud Run
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins

### Frontend Configuration

Environment variables needed:
- `NEXT_PUBLIC_API_URL`: Backend API URL (set during build)
- `PORT`: Set automatically by Cloud Run

---

## Updating/Re-deploying

### Update Application

```bash
# Rebuild and redeploy unified application
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/lead-discovery-app \
  --project=YOUR_PROJECT_ID \
  --config=cloudbuild.yaml

gcloud run deploy lead-discovery-app \
  --image gcr.io/YOUR_PROJECT_ID/lead-discovery-app \
  --platform managed \
  --region us-central1 \
  --project=YOUR_PROJECT_ID
```

Or simply run the deployment script again - it will update the existing service.

---

## Monitoring & Logs

### View Logs

```bash
# Backend logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=lead-discovery-backend" --limit 50

# Frontend logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=lead-discovery-frontend" --limit 50

# Real-time logs
gcloud run services logs tail lead-discovery-backend --region us-central1
```

### View Metrics

```bash
# Service details
gcloud run services describe lead-discovery-app --region us-central1

# List all services
gcloud run services list
```

---

## Costs & Free Tier

### Cloud Run Free Tier (Always Free)

- **2 million requests/month**
- **360,000 GB-seconds/month** (memory × time)
- **180,000 vCPU-seconds/month** (CPU × time)
- **1 GB network egress/month**

### Typical Usage Cost

For moderate usage (1000 requests/day, ~5GB memory, 1 CPU):
- **Compute**: ~$0-2/month (within free tier)
- **Network egress**: ~$0-1/month (first 1GB free)
- **Total**: **$0-3/month**

### Cost Optimization Tips

1. **Use minimum memory** required (512Mi for frontend, 2Gi for backend)
2. **Set max instances** to limit scaling (default: 10)
3. **Use CPU allocation** of 1 (default)
4. **Enable request concurrency** (default: 80) to reduce instances
5. **Set timeout** appropriately (backend: 3600s, frontend: 300s)
6. **Monitor usage** in GCP Console → Cloud Run → Metrics

---

## Security Best Practices

### 1. Use Secret Manager for Credentials

```bash
# Store credentials
gcloud secrets create credentials-json --data-file=credentials.json

# Mount as file in Cloud Run
gcloud run services update lead-discovery-backend \
  --update-secrets=GOOGLE_SHEETS_CREDENTIALS_PATH=credentials-json:latest \
  --region us-central1
```

### 2. Restrict Access (Optional)

```bash
# Remove public access, require authentication
gcloud run services update lead-discovery-backend \
  --no-allow-unauthenticated \
  --region us-central1

# Grant specific users/service accounts access
gcloud run services add-iam-policy-binding lead-discovery-backend \
  --member="user:your-email@example.com" \
  --role="roles/run.invoker" \
  --region us-central1
```

### 3. Set Resource Limits

```bash
# Limit CPU and memory
gcloud run services update lead-discovery-backend \
  --cpu 1 \
  --memory 1Gi \
  --max-instances 5 \
  --region us-central1
```

### 4. Enable VPC Connector (if needed)

If accessing private resources:
```bash
gcloud run services update lead-discovery-backend \
  --vpc-connector YOUR_CONNECTOR \
  --vpc-egress all-traffic \
  --region us-central1
```

---

## Troubleshooting

### Build Fails

```bash
# Check build logs
gcloud builds list --limit 5
gcloud builds log BUILD_ID
```

### Service Won't Start

```bash
# Check service logs
gcloud run services logs read lead-discovery-backend --limit 100

# Check service status
gcloud run services describe lead-discovery-backend --region us-central1
```

### Credentials Not Found

1. Verify secret exists:
   ```bash
   gcloud secrets list
   ```

2. Check service account permissions:
   ```bash
   gcloud secrets get-iam-policy credentials-json
   ```

3. Verify secret is mounted:
   ```bash
   gcloud run services describe lead-discovery-app --format="value(spec.template.spec.containers[0].env)" --region us-central1
   ```

### CORS Errors

In unified deployment, CORS is not an issue since frontend and backend are on the same domain. If you see CORS errors, check that the API routes are prefixed with `/api`.

### Out of Memory

Increase memory allocation:
```bash
gcloud run services update lead-discovery-app \
  --memory 4Gi \
  --region us-central1
```

---

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}
      - run: |
          gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/lead-discovery-backend \
            --config=backend/cloudbuild.yaml
          gcloud run deploy lead-discovery-backend \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/lead-discovery-backend \
            --platform managed --region us-central1

  deploy-frontend:
    runs-on: ubuntu-latest
    needs: deploy-backend
    steps:
      - uses: actions/checkout@v3
      - uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}
      - run: |
          BACKEND_URL=$(gcloud run services describe lead-discovery-backend \
            --platform managed --region us-central1 \
            --format 'value(status.url)')
          gcloud builds submit \
            --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/lead-discovery-frontend \
            --substitutions=_NEXT_PUBLIC_API_URL=$BACKEND_URL \
            --config=frontend/cloudbuild.yaml
          gcloud run deploy lead-discovery-frontend \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/lead-discovery-frontend \
            --platform managed --region us-central1
```

---

## Next Steps

1. ✅ Deploy backend and frontend
2. ✅ Configure credentials in Secret Manager
3. ✅ Set environment variables
4. ✅ Test the deployed application
5. ✅ Set up monitoring and alerts
6. ✅ Configure custom domain (optional)
7. ✅ Set up CI/CD pipeline (optional)

---

## Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Secret Manager Documentation](https://cloud.google.com/secret-manager/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Pricing Calculator](https://cloud.google.com/products/calculator)

---

## Quick Reference Commands

```bash
# List services
gcloud run services list

# View service details (unified service)
gcloud run services describe lead-discovery-app --region us-central1

# View logs
gcloud run services logs tail lead-discovery-app --region us-central1

# Update service
gcloud run services update lead-discovery-app --region us-central1

# Delete service
gcloud run services delete lead-discovery-app --region us-central1

# View secrets
gcloud secrets list

# View secret value (base64 encoded)
gcloud secrets versions access latest --secret=credentials-json
```

---

For questions or issues, refer to:
- [GCP Documentation](https://cloud.google.com/docs)
- [Cloud Run Troubleshooting](https://cloud.google.com/run/docs/troubleshooting)
- [Support](https://cloud.google.com/support)
