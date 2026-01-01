# Manual Deployment via Google Cloud Console

Step-by-step guide for deploying the Lead Discovery System manually using Google Cloud Console (web UI).

---

## Prerequisites

1. Google Cloud Platform account with billing enabled
2. A GCP project created
3. `credentials.json` file ready
4. Google Sheets and Maps API keys

---

## Step 1: Enable Required APIs

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project from the dropdown at the top
3. Navigate to **APIs & Services** > **Library**
4. Enable the following APIs (search for each and click "Enable"):
   - **Cloud Build API**
   - **Cloud Run API**
   - **Container Registry API** (or **Artifact Registry API**)
   - **Secret Manager API**

---

## Step 2: Store Credentials in Secret Manager

1. Go to **Security** > **Secret Manager**
2. Click **CREATE SECRET**
3. Fill in the form:
   - **Name**: `credentials-json`
   - **Secret value**: 
     - Click "Upload file" and select your `credentials.json` file
     - OR paste the contents of `credentials.json` into the text area
4. Click **CREATE SECRET**

---

## Step 3: Prepare Your Code

1. **Upload your code to Cloud Source Repositories** (recommended) OR **prepare to upload via Cloud Build**

### Option A: Using Cloud Source Repositories (Recommended)

1. Go to **Source Repositories**
2. Click **ADD REPOSITORY**
3. Select **Create new repository**
4. Name it (e.g., `lead-discovery-app`)
5. Follow the instructions to push your code using Git

### Option B: Using Cloud Storage or Direct Upload

- You can also use Cloud Build with a Cloud Storage bucket
- Or use `gcloud` CLI just to upload source (one-time setup)

---

## Step 4: Create Cloud Build Trigger (Build Docker Image)

### Method 1: Build from Source Code

1. Go to **Cloud Build** > **Triggers**
2. Click **CREATE TRIGGER**
3. Configure the trigger:
   - **Name**: `build-lead-discovery-app`
   - **Event**: Select your source repository (or choose "Manual")
   - **Source**: Select branch (e.g., `main`)
   - **Configuration**: **Cloud Build configuration file (yaml or json)**
   - **Location**: `cloudbuild.yaml`
4. Click **CREATE**

### Method 2: Build Manually via Cloud Build

1. Go to **Cloud Build** > **History**
2. Click **RUN** > **Run a build**
3. Configure:
   - **Cloud Build configuration file**: Select `cloudbuild.yaml` from your repository
   - OR use **Inline editor** and paste the configuration:
     ```yaml
     steps:
       - name: 'gcr.io/cloud-builders/docker'
         args: 
           - 'build'
           - '--build-arg'
           - 'NEXT_PUBLIC_API_URL=/api'
           - '-t'
           - 'gcr.io/$PROJECT_ID/lead-discovery-app'
           - '-f'
           - 'Dockerfile'
           - '.'
     
     images:
       - 'gcr.io/$PROJECT_ID/lead-discovery-app'
     
     options:
       machineType: 'E2_HIGHCPU_8'
       logging: CLOUD_LOGGING_ONLY
     
     timeout: '1800s'
     ```
   - **Source**: 
     - Connect your repository, OR
     - Upload source code as ZIP
4. Click **RUN**

5. Wait for the build to complete (5-15 minutes)
6. Verify the image was created:
   - Go to **Container Registry** > **Images**
   - You should see: `gcr.io/YOUR_PROJECT_ID/lead-discovery-app`

---

## Step 5: Deploy to Cloud Run

1. Go to **Cloud Run** > **Services**
2. Click **CREATE SERVICE**

### Basic Settings

3. Fill in the service details:
   - **Service name**: `lead-discovery-app`
   - **Region**: Choose a region (e.g., `us-central1`)
   - **Deploy one revision from an existing container image**
   - Click **SELECT** next to container image
   - Browse to: `gcr.io/YOUR_PROJECT_ID/lead-discovery-app:latest`
   - Click **SELECT**

### Container Configuration

4. Expand **Container** section:
   - **Container port**: `8080`
   - **CPU allocation and pricing**: 
     - Select **CPU is always allocated** (or **CPU is only allocated during request processing** for cost savings)
   - **Memory**: `2 GiB` (2048 MiB)
   - **Minimum instances**: `0` (for cost savings)
   - **Maximum instances**: `10`
   - **Timeout**: `3600` seconds (1 hour)

### Authentication

5. Expand **Authentication** section:
   - Select **Allow unauthenticated invocations** (if you want public access)
   - OR **Require authentication** (for private access)

### Secrets and Environment Variables

6. Expand **Variables & Secrets** section:

   **Add Secrets:**
   - Click **ADD SECRET**
   - **Secret**: Select `credentials-json` (created in Step 2)
   - **Reference method**: **Mounted as volume**
   - **Mount path**: `/app/credentials`
   - **Version**: `latest`
   - Click **ADD SECRET**
   
   **Add Environment Variables:**
   - Click **ADD VARIABLE**
   - Add each variable:
     ```
     Name: GOOGLE_SHEETS_CREDENTIALS_PATH
     Value: /app/credentials/credentials-json
     ```
     ```
     Name: GOOGLE_SHEETS_SPREADSHEET_ID
     Value: your_spreadsheet_id_here
     ```
     ```
     Name: GOOGLE_SHEETS_WORKSHEET_NAME
     Value: Leads
     ```
     ```
     Name: GOOGLE_MAPS_API_KEY
     Value: your_maps_api_key_here
     ```
     ```
     Name: PYTHONUNBUFFERED
     Value: 1
     ```

### Service Account Permissions

7. If using Secret Manager, grant permissions:
   - Go to **Secret Manager** > Select `credentials-json`
   - Click **PERMISSIONS** tab
   - Click **GRANT ACCESS**
   - **Principal**: Find your Cloud Run service account
     - Format: `PROJECT_NUMBER-compute@developer.gserviceaccount.com`
     - OR use: `YOUR_PROJECT_ID@appspot.gserviceaccount.com`
   - **Role**: Select **Secret Manager Secret Accessor**
   - Click **SAVE**

### Deployment

8. Click **CREATE** (or **DEPLOY**)
9. Wait for deployment to complete (1-3 minutes)

---

## Step 6: Access Your Application

1. After deployment completes, you'll see the service URL
2. Example: `https://lead-discovery-app-xxxxx-uc.a.run.app`
3. Click the URL or copy it to access your application

---

## Step 7: Verify Deployment

1. **Check Service Status:**
   - Go to **Cloud Run** > **Services** > `lead-discovery-app`
   - Status should show as "Active"
   - Check the **LOGS** tab for any errors

2. **Test the Application:**
   - Open the service URL in your browser
   - You should see the frontend interface
   - Try starting a small discovery test

3. **Check Logs:**
   - In Cloud Run service page, click **LOGS** tab
   - Verify there are no errors
   - Look for "Discovery app initialized successfully" message

---

## Updating the Deployment

### Update Code and Redeploy

**Option 1: Using Cloud Build Trigger**
1. Push new code to your repository
2. Cloud Build trigger will automatically build a new image
3. Go to **Cloud Run** > **Services** > `lead-discovery-app`
4. Click **EDIT & DEPLOY NEW REVISION**
5. Update the container image to the latest version
6. Click **DEPLOY**

**Option 2: Manual Build and Deploy**
1. Go to **Cloud Build** > **History**
2. Click **RUN** > **Run a build** (same as Step 4)
3. Wait for build to complete
4. Go to **Cloud Run** > **Services** > `lead-discovery-app`
5. Click **EDIT & DEPLOY NEW REVISION**
6. Update container image tag or select latest
7. Click **DEPLOY**

---

## Troubleshooting

### Build Fails

1. **Check Build Logs:**
   - Go to **Cloud Build** > **History**
   - Click on the failed build
   - Review the logs for errors

2. **Common Issues:**
   - Missing `Dockerfile` or `cloudbuild.yaml`
   - Docker build timeout (increase timeout in cloudbuild.yaml)
   - Insufficient permissions (check IAM roles)

### Service Won't Start

1. **Check Service Logs:**
   - Go to **Cloud Run** > **Services** > `lead-discovery-app`
   - Click **LOGS** tab
   - Look for error messages

2. **Common Issues:**
   - Missing environment variables
   - Secret not mounted correctly
   - Port configuration (should be 8080)
   - Memory too low (increase to 2Gi or more)

### Credentials Not Found

1. **Verify Secret:**
   - Go to **Secret Manager**
   - Check that `credentials-json` exists
   - Verify the content is correct

2. **Check Service Account Permissions:**
   - Go to **IAM & Admin** > **IAM**
   - Find your service account
   - Verify it has **Secret Manager Secret Accessor** role

3. **Check Environment Variable:**
   - In Cloud Run service, verify `GOOGLE_SHEETS_CREDENTIALS_PATH` is set correctly
   - Should be: `/app/credentials/credentials-json`

### Frontend Not Loading

1. **Check Build Logs:**
   - Verify frontend built successfully
   - Check for Next.js build errors

2. **Check Service Logs:**
   - Look for file serving errors
   - Verify static files are in the container

---

## Quick Reference: Important Settings

### Cloud Run Service Configuration

- **Service Name**: `lead-discovery-app`
- **Region**: `us-central1` (or your preferred region)
- **Container Image**: `gcr.io/YOUR_PROJECT_ID/lead-discovery-app:latest`
- **Container Port**: `8080`
- **Memory**: `2 GiB`
- **CPU**: `2` (or 1 for cost savings)
- **Min Instances**: `0`
- **Max Instances**: `10`
- **Timeout**: `3600` seconds

### Required Environment Variables

```
GOOGLE_SHEETS_CREDENTIALS_PATH=/app/credentials/credentials-json
GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id
GOOGLE_SHEETS_WORKSHEET_NAME=Leads
GOOGLE_MAPS_API_KEY=your_api_key
PYTHONUNBUFFERED=1
```

### Required Secrets

- **Secret Name**: `credentials-json`
- **Mount Path**: `/app/credentials`
- **File Path in Container**: `/app/credentials/credentials-json`

---

## Cost Estimation

- **Cloud Build**: First 120 build-minutes/day free, then ~$0.003/minute
- **Cloud Run**: 
  - Free tier: 2M requests, 360K GB-seconds/month
  - Typical usage: $0-3/month
- **Secret Manager**: First 6 secrets free, then $0.06/secret/month
- **Total**: Usually $0-5/month for moderate usage

---

## Next Steps

1. ✅ Verify deployment is working
2. ✅ Test discovery functionality
3. ✅ Set up monitoring and alerts (optional)
4. ✅ Configure custom domain (optional)
5. ✅ Set up automated deployments with triggers (optional)

---

## Support Resources

- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Secret Manager Documentation](https://cloud.google.com/secret-manager/docs)
- [Cloud Run Troubleshooting](https://cloud.google.com/run/docs/troubleshooting)

---

For CLI-based deployment, see:
- [DEPLOYMENT_GCP.md](./DEPLOYMENT_GCP.md)
- [CLOUD_RUN_QUICKSTART.md](./CLOUD_RUN_QUICKSTART.md)
- [UNIFIED_DEPLOYMENT.md](./UNIFIED_DEPLOYMENT.md)

