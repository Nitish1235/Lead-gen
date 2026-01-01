# Dockerfile for B2B Lead Discovery System (Cloud Run / Container)
# Note: This requires creating an API wrapper (not included)
# For most use cases, use Compute Engine VM instead (see DEPLOYMENT_GCP.md)

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for credentials (mounted as volume)
RUN mkdir -p /app/credentials

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_SHEETS_CREDENTIALS_PATH=/app/credentials/credentials.json

# Note: You would need to create an API server (api_server.py)
# that wraps the LeadDiscoveryApp class for Cloud Run
# CMD ["python", "api_server.py"]

# For now, default to main.py (if running interactively)
CMD ["python", "main.py"]

