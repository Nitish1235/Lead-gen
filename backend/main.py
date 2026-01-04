"""
FastAPI backend for Lead Discovery System
Provides REST API for the Next.js frontend
"""
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Import config (lightweight import - should always work)
try:
    import config
except Exception as e:
    print(f"⚠ Warning: Failed to import config: {e}")
    config = None

# Import countries directly (doesn't require credentials)
try:
    from countries import list_all_countries
    print(f"✓ Countries module imported successfully")
    # Test that it works
    test_countries = list_all_countries()
    print(f"✓ Found {len(test_countries)} countries")
except Exception as e:
    import traceback
    print(f"⚠ Warning: Failed to import countries: {e}")
    print(f"⚠ Traceback: {traceback.format_exc()}")
    list_all_countries = None

# Lazy import of LeadDiscoveryApp - import only when needed to avoid startup failures
# This allows the FastAPI app to start even if main.py has import issues
LeadDiscoveryApp = None

def _lazy_import_discovery_app():
    """Lazy import of LeadDiscoveryApp and related modules"""
    global LeadDiscoveryApp
    if LeadDiscoveryApp is None:
        try:
            from main import LeadDiscoveryApp
        except Exception as e:
            print(f"⚠ Error: Failed to import discovery modules: {e}")
            raise
    return LeadDiscoveryApp

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
        LeadDiscoveryAppClass = _lazy_import_discovery_app()
        discovery_app = LeadDiscoveryAppClass(lead_callback=on_lead_found)
        print("✓ Discovery app initialized successfully")
    except Exception as e:
        import traceback
        print(f"⚠ Warning: Failed to initialize discovery app: {e}")
        print(f"⚠ Error details: {traceback.format_exc()}")
        print("⚠ The API will still start, but discovery features won't work until credentials are configured.")
        creds_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH', 'not set')
        # Don't print full credentials if it's JSON content (security)
        if creds_path and creds_path.strip().startswith('{'):
            print(f"⚠ Credentials provided as JSON (length: {len(creds_path)} chars)")
        else:
            print(f"⚠ Credentials path: {creds_path}")
        discovery_app = None
    
    yield
    
    # Shutdown (if needed)
    pass


app = FastAPI(title="Lead Discovery API", version="1.0.0", lifespan=lifespan)

# Create API router to ensure API routes are matched before catch-all
api_router = APIRouter(prefix="/api")

# Add middleware to log all requests for debugging
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"📥 Request: {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        print(f"📤 Response: {request.method} {request.url.path} -> {response.status_code}")
        return response
    except Exception as e:
        import traceback
        print(f"⚠⚠⚠ Exception in middleware for {request.method} {request.url.path}: {str(e)}")
        print(f"⚠ Traceback: {traceback.format_exc()}")
        # For API routes, return JSON error instead of raising
        if request.url.path.startswith("/api/"):
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=500,
                content={"error": str(e), "path": request.url.path}
            )
        raise

# CORS middleware for Next.js frontend
# In unified deployment, frontend is served from same origin, so allow all
# For development, allow localhost origins
allowed_origins_env = os.environ.get("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    allowed_origins = allowed_origins_env.split(",")
else:
    # Default: allow same origin (unified deployment) and localhost (development)
    allowed_origins = ["*"]  # Allow all in unified deployment

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount static files for frontend (in unified deployment)
# Check if frontend directory exists (unified deployment)
frontend_path = os.path.join(parent_dir, "frontend")
if os.path.exists(frontend_path):
    # Next.js export creates static files in the frontend directory
    # Mount static assets (_next directory if it exists)
    static_path = os.path.join(frontend_path, "_next")
    if os.path.exists(static_path):
        app.mount("/_next", StaticFiles(directory=static_path), name="next-static")


@api_router.get("")
async def root():
    return {"message": "Lead Discovery API", "version": "1.0.0"}

@api_router.get("/test")
async def test():
    """Test endpoint to verify API routes work"""
    return {"status": "ok", "message": "API routes are working"}


@api_router.get("/status")
async def get_status():
    """Get current discovery status"""
    try:
        print(f"✓ /api/status called - discovery_app is {'initialized' if discovery_app else 'None'}")
        if not discovery_app:
            # Return a status indicating the app is not initialized
            # This should return 200 OK with initialized: false, NOT 503
            status_response = {
                "is_running": False,
                "run_id": None,
                "current_country": None,
                "current_city": None,
                "current_category": None,
                "initialized": False,
                "error": "Discovery app not initialized. Please check credentials.json and Google Sheets configuration."
            }
            print(f"✓ Returning status: {status_response}")
            return status_response
        
        status = discovery_app.get_status()
        status["initialized"] = True
        print(f"✓ Returning status: {status}")
        return status
    except Exception as e:
        import traceback
        error_msg = f"Error in get_status: {str(e)}"
        print(f"⚠ {error_msg}")
        print(f"⚠ Traceback: {traceback.format_exc()}")
        # Return error status, not raise 503
        return {
            "is_running": False,
            "run_id": None,
            "current_country": None,
            "current_city": None,
            "current_category": None,
            "initialized": False,
            "error": error_msg
        }


@api_router.post("/start")
async def start_discovery(request: DiscoveryRequest):
    """Start lead discovery"""
    global current_leads
    
    print(f"📥 /api/start called - country: {request.country}, city: {request.city}, categories: {request.categories}")
    print(f"📥 discovery_app is {'initialized' if discovery_app else 'None'}")
    
    if not discovery_app:
        error_msg = "Discovery app not initialized. Please check credentials.json and Google Sheets configuration."
        print(f"⚠ {error_msg}")
        creds_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH', 'not set')
        # Don't print full credentials if it's JSON content (security)
        if creds_path and creds_path.strip().startswith('{'):
            print(f"⚠ Credentials provided as JSON (length: {len(creds_path)} chars)")
        else:
            print(f"⚠ Credentials path: {creds_path}")
        raise HTTPException(status_code=503, detail=error_msg)
    
    if discovery_app.is_running:
        raise HTTPException(status_code=400, detail="Discovery already running")
    
    try:
        # Clear previous leads for new run
        current_leads.clear()
        
        # Start discovery (non-blocking - runs in background)
        # Use daemon=False to ensure discovery continues even if client disconnects
        # The discovery should run independently of browser/client connections
        import threading
        thread = threading.Thread(
            target=discovery_app.start,
            args=(request.country, request.city, request.categories),
            daemon=False  # Changed to False so discovery continues after browser closes
        )
        thread.start()
        
        print(f"✓ Discovery started successfully")
        return {"success": True, "message": "Discovery started"}
    except Exception as e:
        import traceback
        error_msg = f"Failed to start discovery: {str(e)}"
        print(f"⚠ {error_msg}")
        print(f"⚠ Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)


@api_router.post("/stop")
async def stop_discovery():
    """Stop lead discovery"""
    if not discovery_app:
        raise HTTPException(status_code=503, detail="Discovery app not initialized. Please check credentials.json and Google Sheets configuration.")
    
    try:
        discovery_app.stop()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/leads")
async def get_leads(run_id: Optional[str] = None):
    """Get discovered leads"""
    # Filter by run_id if provided
    if run_id:
        filtered = [lead for lead in current_leads if lead.get("run_id") == run_id]
        return filtered
    return current_leads


@api_router.get("/countries")
async def get_countries():
    """Get list of all supported countries"""
    global list_all_countries
    
    if list_all_countries is None:
        # Try to import again
        try:
            from countries import list_all_countries as _list_all_countries
            list_all_countries = _list_all_countries
            print("✓ Countries module imported successfully on demand")
        except Exception as e:
            import traceback
            error_msg = f"Countries module not loaded. Import error: {str(e)}"
            print(f"⚠ {error_msg}")
            print(f"⚠ Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=error_msg)
    
    try:
        countries = list_all_countries()
        if not countries or len(countries) == 0:
            print(f"⚠ Warning: list_all_countries() returned empty list. COUNTRIES dict might be empty.")
            # Try to check COUNTRIES directly
            try:
                import countries as countries_module
                print(f"⚠ COUNTRIES dict size: {len(countries_module.COUNTRIES) if hasattr(countries_module, 'COUNTRIES') else 'NOT FOUND'}")
            except:
                pass
        print(f"✓ Returning {len(countries)} countries")
        return countries
    except Exception as e:
        import traceback
        error_msg = f"Failed to load countries: {str(e)}"
        print(f"⚠ Error in get_countries: {error_msg}")
        print(f"⚠ Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)


@api_router.get("/categories")
async def get_categories():
    """Get list of all supported categories"""
    if config is None:
        raise HTTPException(status_code=500, detail="Config not loaded")
    return config.DEFAULT_CATEGORIES


@api_router.get("/cities")
async def get_cities(country: Optional[str] = None):
    """Get cities for a country, organized by tier"""
    try:
        from countries import get_cities_by_tier
        
        if not country:
            raise HTTPException(status_code=400, detail="Country parameter is required")
        
        cities_by_tier = get_cities_by_tier(country)
        
        if not cities_by_tier or (not cities_by_tier.get("Tier 1") and not cities_by_tier.get("Tier 2") and not cities_by_tier.get("Tier 3")):
            raise HTTPException(status_code=404, detail=f"No cities found for country: {country}")
        
        return cities_by_tier
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_msg = f"Failed to load cities: {str(e)}"
        print(f"⚠ Error in get_cities: {error_msg}")
        print(f"⚠ Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)


@api_router.get("/stats")
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


# Include API router AFTER all routes are defined but BEFORE catch-all route
# This ensures API routes are matched before the catch-all route
app.include_router(api_router)

# Debug: Log registered routes on startup
@app.on_event("startup")
async def log_routes():
    print("=" * 60)
    print("Registered Routes:")
    for route in app.routes:
        if hasattr(route, 'path'):
            methods = ', '.join(sorted(route.methods)) if hasattr(route, 'methods') and route.methods else 'N/A'
            path = route.path
            print(f"  {methods:15} {path}")
    print("=" * 60)
    print(f"Total routes: {len(app.routes)}")
    print(f"API router included: {api_router in [r for r in app.routes if hasattr(r, 'routes')]}")
    print("=" * 60)


# Serve frontend for all non-API routes (SPA routing)
# This must be LAST so API routes are matched first
# Next.js export mode creates index.html in the frontend directory
# IMPORTANT: This catch-all must NOT match /api/* routes - FastAPI should match specific routes first
if os.path.exists(frontend_path):
    # Use a more specific path pattern that excludes /api/*
    # FastAPI will match this only if no other route matches
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # CRITICAL: This should NEVER be reached for /api/* paths
        # If we reach here, it means the router routes didn't match (BUG!)
        if full_path.startswith("api/") or full_path == "api":
            print(f"⚠⚠⚠ ERROR: Catch-all matched API path '/{full_path}' - Router failed!")
            print(f"⚠ This means /api/* routes are not working. Check router registration.")
            raise HTTPException(
                status_code=404, 
                detail=f"API route '/api/{full_path.split('/', 1)[1] if '/' in full_path else ''}' not found. Router may not be registered."
            )
        
        if full_path.startswith("_next/"):
            raise HTTPException(status_code=404)
        
        # Try to serve the requested file
        requested_file = os.path.join(frontend_path, full_path)
        
        # If it's a file, serve it
        if os.path.isfile(requested_file):
            return FileResponse(requested_file)
        
        # If it's a directory or doesn't exist, serve index.html (SPA routing)
        index_path = os.path.join(frontend_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        
        raise HTTPException(status_code=404, detail="Frontend not found")


if __name__ == "__main__":
    import uvicorn
    import os
    # Cloud Run sets PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

