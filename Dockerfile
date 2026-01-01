# Combined Dockerfile for Frontend + Backend (Cloud Run)
# This builds both Next.js frontend and FastAPI backend in one container

# ============================================
# Stage 1: Build Frontend
# ============================================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package.json first for better Docker layer caching
COPY frontend/package.json ./

# Install dependencies
RUN npm install

# Copy all remaining frontend files
COPY frontend/ ./

# Build Next.js (standalone mode for Docker deployment)
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL:-http://localhost:8000}

RUN npm run build

# ============================================
# Stage 2: Build Backend + Combine
# ============================================
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome (for Selenium if needed)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend requirements
COPY backend/requirements.txt /app/backend_requirements.txt
COPY requirements.txt /app/root_requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/backend_requirements.txt && \
    pip install --no-cache-dir -r /app/root_requirements.txt

# Copy backend code
COPY backend/ /app/backend/
COPY main.py config.py countries.py lead_scorer.py maps_discoverer.py \
     sheets_manager.py website_analyzer.py /app/

# Copy built frontend from builder
# Next.js standalone mode creates .next/standalone directory with server.js, .next, node_modules, etc.
# Copy the entire standalone directory structure
COPY --from=frontend-builder /app/frontend/.next/standalone /app/frontend/

# Copy static files to expected location (FastAPI expects .next/static at root level)
# Standalone includes .next inside standalone, but we need it accessible at /app/frontend/.next/static
COPY --from=frontend-builder /app/frontend/.next/static /app/frontend/.next/static

# Ensure public directory exists (standalone may include it, but ensure it's accessible)
RUN mkdir -p /app/frontend/public

# Create directory for credentials
RUN mkdir -p /app/credentials

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PORT=8080

# Cloud Run requires listening on PORT env variable
# FastAPI will serve both API and static frontend files
CMD exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT} --workers 1
