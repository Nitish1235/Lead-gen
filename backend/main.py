"""
FastAPI backend for Lead Discovery System
Provides REST API for the Next.js frontend
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List, Optional, Dict
import sys
import os

# Add parent directory to path to import our modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Change working directory to parent (root) so credentials.json can be found
os.chdir(parent_dir)

# Import from parent directory
from main import LeadDiscoveryApp
from countries import list_all_countries
import config

# Global app instance
discovery_app = None
current_leads: List[Dict] = []


class DiscoveryRequest(BaseModel):
    country: str
    city: str
    categories: Optional[List[str]] = None


def on_lead_found(lead: Dict):
    """Callback when a lead is found - store in memory"""
    current_leads.append(lead)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    global discovery_app
    try:
        discovery_app = LeadDiscoveryApp(lead_callback=on_lead_found)
        print("✓ Discovery app initialized successfully")
    except Exception as e:
        print(f"⚠ Warning: Failed to initialize discovery app: {e}")
        print("⚠ The API will still start, but discovery features won't work until credentials are configured.")
        discovery_app = None
    
    yield
    
    # Shutdown (if needed)
    pass


app = FastAPI(title="Lead Discovery API", version="1.0.0", lifespan=lifespan)

# CORS middleware for Next.js frontend
# Allow origins from environment variable or default to localhost for development
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Lead Discovery API", "version": "1.0.0"}


@app.get("/status")
async def get_status():
    """Get current discovery status"""
    if not discovery_app:
        raise HTTPException(status_code=503, detail="Discovery app not initialized. Please check credentials.json and Google Sheets configuration.")
    
    status = discovery_app.get_status()
    return status


@app.post("/start")
async def start_discovery(request: DiscoveryRequest):
    """Start lead discovery"""
    global current_leads
    
    if not discovery_app:
        raise HTTPException(status_code=503, detail="Discovery app not initialized. Please check credentials.json and Google Sheets configuration.")
    
    if discovery_app.is_running:
        raise HTTPException(status_code=400, detail="Discovery already running")
    
    try:
        # Clear previous leads for new run
        current_leads.clear()
        
        # Start discovery (non-blocking - runs in background)
        import threading
        thread = threading.Thread(
            target=discovery_app.start,
            args=(request.country, request.city, request.categories),
            daemon=True
        )
        thread.start()
        
        return {"success": True, "message": "Discovery started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stop")
async def stop_discovery():
    """Stop lead discovery"""
    if not discovery_app:
        raise HTTPException(status_code=503, detail="Discovery app not initialized. Please check credentials.json and Google Sheets configuration.")
    
    try:
        discovery_app.stop()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/leads")
async def get_leads(run_id: Optional[str] = None):
    """Get discovered leads"""
    # Filter by run_id if provided
    if run_id:
        filtered = [lead for lead in current_leads if lead.get("run_id") == run_id]
        return filtered
    return current_leads


@app.get("/countries")
async def get_countries():
    """Get list of all supported countries"""
    return list_all_countries()


@app.get("/categories")
async def get_categories():
    """Get list of all supported categories"""
    return config.DEFAULT_CATEGORIES


@app.get("/stats")
async def get_stats():
    """Get statistics about discovered leads"""
    if not current_leads:
        return {
            "total_leads": 0,
            "avg_score": 0,
            "by_category": {},
            "by_country": {},
        }
    
    total = len(current_leads)
    scores = [lead.get("lead_score", 0) for lead in current_leads if isinstance(lead.get("lead_score"), (int, float))]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Count by category
    by_category: Dict[str, int] = {}
    for lead in current_leads:
        category = lead.get("category", "Unknown")
        by_category[category] = by_category.get(category, 0) + 1
    
    # Count by country
    by_country: Dict[str, int] = {}
    for lead in current_leads:
        country = lead.get("country", "Unknown")
        by_country[country] = by_country.get(country, 0) + 1
    
    return {
        "total_leads": total,
        "avg_score": round(avg_score, 2),
        "by_category": by_category,
        "by_country": by_country,
    }


if __name__ == "__main__":
    import uvicorn
    import os
    # Cloud Run sets PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

