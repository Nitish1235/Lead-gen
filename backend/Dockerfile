# Backend Dockerfile for Cloud Run (FastAPI)
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome (for Selenium if needed)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend requirements
COPY backend/requirements.txt /app/backend_requirements.txt

# Copy root requirements (main app dependencies)
COPY requirements.txt /app/root_requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/backend_requirements.txt && \
    pip install --no-cache-dir -r /app/root_requirements.txt

# Copy application code
# Copy backend code
COPY backend/ /app/backend/

# Copy root modules (main.py, config.py, etc.)
COPY main.py config.py countries.py lead_scorer.py maps_discoverer.py \
     sheets_manager.py website_analyzer.py /app/

# Create directory for credentials
RUN mkdir -p /app/credentials

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PORT=8080

# Cloud Run requires listening on PORT env variable
# Uvicorn will use this via the command
CMD exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT} --workers 1

