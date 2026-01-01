# GCP Quick Start (5 Minutes)

Fastest way to get the Lead Discovery system running on GCP.

## Prerequisites
- GCP account with billing enabled
- Google Cloud SDK installed (or use web console)

## Quick Setup (Compute Engine VM)

### 1. Create VM (Web Console)

1. Go to [Compute Engine > VM Instances](https://console.cloud.google.com/compute/instances)
2. Click **Create Instance**
3. Settings:
   - Name: `lead-discovery`
   - Region: `us-central1` (Oregon) or `us-east1` (Iowa) for free tier
   - Machine: `e2-micro` (free tier)
   - Boot disk: Ubuntu 22.04 LTS, 20 GB
4. Click **Create**

### 2. Setup VM (One Command)

SSH into VM (click **SSH** button in console), then run:

```bash
# Download and run setup script
curl -o- https://raw.githubusercontent.com/YOUR_REPO/gcp_setup.sh | bash

# OR manually copy setup script and run:
# Copy gcp_setup.sh to VM, then:
chmod +x gcp_setup.sh
./gcp_setup.sh
```

### 3. Upload Your Files

From your local machine:

```bash
# Set your project and zone
gcloud config set project YOUR_PROJECT_ID
gcloud config set compute/zone us-central1-a

# Upload application files
gcloud compute scp --recurse . lead-discovery:~/lead-gen/ --exclude='.git,__pycache__,*.pyc'

# Upload credentials
gcloud compute scp credentials.json lead-discovery:~/.config/lead-discovery/ --zone=us-central1-a
```

### 4. Configure

SSH into VM:

```bash
cd ~/lead-gen
nano .env
```

Add:
```env
GOOGLE_SHEETS_CREDENTIALS_PATH=/home/YOUR_USER/.config/lead-discovery/credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id
GOOGLE_MAPS_API_KEY=your_api_key
```

### 5. Run!

```bash
python3 main.py
```

## Stop VM (Save Costs)

When not in use, stop the VM:

```bash
gcloud compute instances stop lead-discovery --zone=us-central1-a
```

Start when needed:
```bash
gcloud compute instances start lead-discovery --zone=us-central1-a
```

## Cost

- **Free tier**: $0/month (e2-micro in eligible regions)
- **Stopped VM**: $0 compute cost (only storage ~$0.50/month)

## Full Guide

For detailed instructions, troubleshooting, and security best practices, see [DEPLOYMENT_GCP.md](DEPLOYMENT_GCP.md).

