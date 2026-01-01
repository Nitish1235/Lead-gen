# GCP Deployment Guide

This guide covers deploying the B2B Lead Discovery System on Google Cloud Platform, optimized for free tier usage and personal use.

## Deployment Options Overview

**Recommended for Personal Use**: Option 1 (Compute Engine VM)  
**For API Access**: Option 2 (Cloud Run)  
**Simplest**: Option 3 (Local with GCP Credentials)

---

## Option 1: Compute Engine VM (Recommended)

Run the system on a GCP VM you can SSH into. Best for maintaining manual control.

### Prerequisites

- Google Cloud Platform account
- GCP project created
- Billing enabled (free tier is fine)

### Step 1: Create VM Instance

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **Compute Engine** > **VM instances**
3. Click **Create Instance**

**Configuration:**
- **Name**: `lead-discovery-vm`
- **Region**: Choose closest to you (for lower latency)
- **Machine type**: `e2-micro` (free tier eligible, or `e2-small` for better performance)
- **Boot disk**: 
  - OS: **Ubuntu 22.04 LTS**
  - Disk size: 20 GB (standard persistent disk)
- **Firewall**: 
  - ✅ Allow HTTP traffic
  - ✅ Allow HTTPS traffic
- Click **Create**

**Cost**: ~$0/month (free tier) or ~$6/month (e2-small)

### Step 2: SSH into VM

1. Click **SSH** button next to your VM instance
2. Or use gcloud CLI:
   ```bash
   gcloud compute ssh lead-discovery-vm --zone=YOUR_ZONE
   ```

### Step 3: Install Dependencies on VM

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install -y python3 python3-pip git

# Install Chrome (for Selenium if needed)
sudo apt install -y wget gnupg
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install -y google-chrome-stable

# Install ChromeDriver dependencies
sudo apt install -y unzip
```

### Step 4: Deploy Application

```bash
# Clone your repository (or upload files)
git clone YOUR_REPO_URL
cd lead-gen

# Or upload files manually using:
# gcloud compute scp --recurse ./ lead-discovery-vm:~/lead-gen --zone=YOUR_ZONE

# Install Python dependencies
pip3 install -r requirements.txt --user

# Create credentials directory
mkdir -p ~/.config/lead-discovery
```

### Step 5: Setup Google Sheets Credentials

**Option A: Upload credentials file**

```bash
# From your local machine:
gcloud compute scp credentials.json lead-discovery-vm:~/lead-gen/ --zone=YOUR_ZONE

# On VM, move to secure location:
mv ~/lead-gen/credentials.json ~/.config/lead-discovery/
```

**Option B: Create new service account on VM**

1. Follow the Google Sheets API setup from QUICKSTART.md
2. Download credentials directly to VM

### Step 6: Configure Environment

```bash
# Create .env file
cd ~/lead-gen
nano .env
```

Add your configuration:
```env
GOOGLE_SHEETS_CREDENTIALS_PATH=/home/YOUR_USERNAME/.config/lead-discovery/credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id_here
GOOGLE_SHEETS_WORKSHEET_NAME=Leads
GOOGLE_MAPS_API_KEY=your_api_key_here
```

### Step 7: Test Run

```bash
cd ~/lead-gen
python3 main.py
```

You should see the interactive CLI. Test with a small search:
```
> start United States New York dental clinic
```

### Step 8: Run in Background (Optional)

For long-running searches, use `screen` or `tmux`:

```bash
# Install screen
sudo apt install -y screen

# Start screen session
screen -S lead-discovery

# Run your search
python3 main.py
# > start United States New York

# Detach: Press Ctrl+A, then D
# Reattach later: screen -r lead-discovery
```

### Step 9: Stop/Start VM (Cost Control)

**Stop VM** (when not in use):
```bash
# From local machine or console
gcloud compute instances stop lead-discovery-vm --zone=YOUR_ZONE
```

**Start VM** (when needed):
```bash
gcloud compute instances start lead-discovery-vm --zone=YOUR_ZONE
```

**Note**: Stopped VMs don't incur compute costs (only storage).

---

## Option 2: Cloud Run (Serverless API)

Deploy as a serverless container for API access. More complex but fully serverless.

### Prerequisites

- Docker installed locally
- Cloud Run API enabled
- Container Registry API enabled

### Step 1: Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create API entry point (you'd need to create this)
# For now, this is a template - you'd need to wrap main.py in a web framework
CMD ["python", "api_server.py"]
```

### Step 2: Create API Server (if needed)

This would require creating a Flask/FastAPI wrapper around the discovery logic. This adds complexity and may not align with your manual control principle.

**Recommendation**: Skip Cloud Run unless you need API access. Stick with Option 1 (VM) for simplicity.

---

## Option 3: Local Deployment with GCP Credentials (Simplest)

Run locally but use GCP for APIs only. No deployment needed.

### Setup

1. Follow QUICKSTART.md for local setup
2. Use Google Sheets API (free tier)
3. Use Google Places API (free $200/month credit)
4. Run `python main.py` locally

**Pros**: 
- Simplest setup
- No infrastructure costs
- Full control
- Fast iteration

**Cons**: 
- Requires local machine to run
- Uses local network/IP

**Best for**: Personal use, development, testing

---

## GCP Services & Costs

### Free Tier (Always Free)

- **Compute Engine**: 
  - 1 e2-micro VM instance per month (US regions: Oregon, Iowa, South Carolina)
  - 30 GB-month standard persistent disk
  - 1 GB network egress per month
  
- **Cloud Storage**: 5 GB standard storage, 5,000 Class A operations, 50,000 Class B operations

- **Cloud Run**: 2 million requests, 360,000 GB-seconds, 180,000 vCPU-seconds

### Paid (Minimal Cost)

- **Google Sheets API**: Free (300 requests/minute)
- **Google Places API**: $200 free credit/month
- **Compute Engine e2-small**: ~$6/month if not using free tier
- **Network egress**: ~$0.12/GB after free tier

### Cost Optimization Tips

1. **Use free tier VM** (e2-micro in eligible regions)
2. **Stop VM when not in use** (saves compute costs)
3. **Use preemptible VMs** (60-80% cheaper, but can be terminated)
4. **Set budget alerts** in GCP Console
5. **Delete unused resources**

---

## Security Best Practices

### 1. Secure Credentials

```bash
# Set proper permissions
chmod 600 ~/.config/lead-discovery/credentials.json

# Don't commit credentials to git
echo "credentials.json" >> .gitignore
echo ".env" >> .gitignore
```

### 2. Use Service Account with Least Privilege

- Only grant necessary roles (Editor for Sheets, not Owner)
- Use separate service accounts for different purposes
- Rotate keys periodically

### 3. Firewall Rules

- Only allow necessary ports (SSH: 22, HTTP: 80, HTTPS: 443)
- Use IAP (Identity-Aware Proxy) for SSH if possible
- Restrict source IPs if you have a static IP

### 4. Enable Cloud Logging

Monitor your VM activity:
```bash
# View logs
gcloud logging read "resource.type=gce_instance" --limit 50
```

---

## Maintenance & Updates

### Update Application Code

```bash
# SSH into VM
gcloud compute ssh lead-discovery-vm --zone=YOUR_ZONE

# Pull latest changes
cd ~/lead-gen
git pull

# Or upload new files
# From local: gcloud compute scp --recurse ./ lead-discovery-vm:~/lead-gen --zone=YOUR_ZONE

# Reinstall dependencies if needed
pip3 install -r requirements.txt --user --upgrade
```

### Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

### Backup Configuration

```bash
# Backup .env and credentials
tar -czf backup-$(date +%Y%m%d).tar.gz .env ~/.config/lead-discovery/

# Download backup
# From local: gcloud compute scp lead-discovery-vm:~/backup-*.tar.gz . --zone=YOUR_ZONE
```

---

## Troubleshooting

### VM Won't Start

1. Check quotas in GCP Console
2. Verify billing is enabled
3. Check zone availability

### Can't Connect via SSH

1. Check firewall rules (allow port 22)
2. Verify VM is running
3. Try using browser SSH in console

### Python Dependencies Fail

```bash
# Use --user flag
pip3 install -r requirements.txt --user

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Chrome/Selenium Issues

```bash
# Verify Chrome installation
google-chrome --version

# Install ChromeDriver manually if needed
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+')
wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION} -O chromedriver_version
CHROMEDRIVER_VERSION=$(cat chromedriver_version)
wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

### API Quota Exceeded

1. Check API quotas in GCP Console
2. Implement delays between requests (already in config)
3. Consider using Cloud Scheduler for rate limiting

---

## Quick Reference Commands

### VM Management

```bash
# List instances
gcloud compute instances list

# Start VM
gcloud compute instances start lead-discovery-vm --zone=YOUR_ZONE

# Stop VM
gcloud compute instances stop lead-discovery-vm --zone=YOUR_ZONE

# SSH into VM
gcloud compute ssh lead-discovery-vm --zone=YOUR_ZONE

# Copy file to VM
gcloud compute scp local-file.txt lead-discovery-vm:~/remote-path/ --zone=YOUR_ZONE

# Copy file from VM
gcloud compute scp lead-discovery-vm:~/remote-file.txt ./local-path/ --zone=YOUR_ZONE
```

### Monitoring

```bash
# View VM metrics
gcloud compute instances describe lead-discovery-vm --zone=YOUR_ZONE

# View logs
gcloud logging read "resource.type=gce_instance" --limit 50

# Check disk usage
gcloud compute disks list
```

---

## Recommended Setup for Personal Use

**Best Practice**:

1. Use **Option 1 (Compute Engine VM)** with e2-micro (free tier)
2. Deploy in US region (Oregon, Iowa, or South Carolina) for free tier
3. Stop VM when not in use
4. Use screen/tmux for long-running searches
5. Set up budget alerts ($5-10/month limit)
6. Run locally for development (Option 3)
7. Use VM for production/long-running searches

**Estimated Monthly Cost**: $0-5 (staying in free tier)

---

## Next Steps

1. Choose deployment option
2. Follow setup steps
3. Test with small search
4. Set up monitoring/alerts
5. Configure automated backups (optional)

For questions or issues, refer to:
- [GCP Documentation](https://cloud.google.com/docs)
- [Compute Engine Documentation](https://cloud.google.com/compute/docs)
- [Billing Documentation](https://cloud.google.com/billing/docs)

