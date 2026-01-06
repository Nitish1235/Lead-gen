# Backend Flow Architecture

## Overview

The B2B Lead Discovery System uses a **layered architecture** with FastAPI as the web framework and a modular discovery engine. The system is designed to run discovery processes independently of the web server lifecycle.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                        │
│                    React UI Components                            │
└───────────────────────────┬─────────────────────────────────────┘
                             │ HTTP REST API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (backend/main.py)             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Layer (APIRouter)                                    │  │
│  │  - /api/status    - Get discovery status                 │  │
│  │  - /api/start     - Start discovery                      │  │
│  │  - /api/stop      - Stop discovery                       │  │
│  │  - /api/leads     - Get discovered leads                 │  │
│  │  - /api/countries - Get supported countries              │  │
│  │  - /api/cities    - Get cities for country               │  │
│  │  - /api/categories- Get categories                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Application Lifecycle Manager                            │  │
│  │  - Lazy imports (prevents startup failures)               │  │
│  │  - Global discovery_app instance                          │  │
│  │  - In-memory lead storage (current_leads)                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │ Thread Creation
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              LeadDiscoveryApp (main.py)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Core Components                                          │  │
│  │  - SheetsManager    → Google Sheets integration          │  │
│  │  - LeadScorer       → Lead scoring algorithm             │  │
│  │  - WebsiteAnalyzer  → Website analysis                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Discovery Orchestrator                                   │  │
│  │  - start() method: Main discovery loop                    │  │
│  │  - Iterates: Categories → Cities                         │  │
│  │  - Non-daemon thread (continues after server shutdown)    │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                     │
        ▼                   ▼                     ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ MapsDiscoverer│  │ LeadScorer   │  │WebsiteAnalyzer│
│              │  │              │  │              │
│ - Google Maps│  │ - Score calc │  │ - Platform   │
│   search     │  │ - Weights    │  │   detection  │
│ - Places API │  │ - Rating     │  │ - HTTPS check │
│ - Scraping   │  │   analysis   │  │ - Booking    │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                  │
       └─────────────────┼──────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Process Business    │
              │  → Create Lead Dict  │
              │  → Check Duplicates   │
              │  → Score Lead        │
              └──────────┬─────────────┘
                        │
                        ▼
              ┌──────────────────────┐
              │   SheetsManager       │
              │  - Get/Create Sheet   │
              │  - Append Lead        │
              │  - Check Duplicates  │
              └──────────┬─────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Google Sheets API  │
              │   (Country-wise tabs)│
              └──────────────────────┘
```

## Detailed Flow

### 1. Application Startup (`backend/main.py`)

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Phase
    1. Lazy import LeadDiscoveryApp (prevents startup failures)
    2. Initialize discovery_app instance
    3. Set up lead_callback → on_lead_found()
    4. FastAPI app ready to serve requests
    
    # Shutdown Phase
    - Discovery threads continue running (non-daemon)
    - Only explicit /api/stop will stop discovery
```

**Key Features:**
- **Lazy Loading**: Heavy imports only when needed
- **Graceful Degradation**: API starts even if credentials fail
- **Persistent Discovery**: Threads survive server shutdown

---

### 2. API Request Flow

#### 2.1 Start Discovery (`POST /api/start`)

```
Frontend Request
    ↓
POST /api/start
{
  "country": "United States",
  "city": "New York",
  "categories": ["dental clinic", "restaurant"]
}
    ↓
Backend Validation
    ↓
Create Non-Daemon Thread
    ↓
Thread.start() → discovery_app.start()
    ↓
Return {"success": true} (immediate response)
    ↓
Discovery runs in background independently
```

**Thread Characteristics:**
- **Non-Daemon**: Continues after client disconnects
- **Independent**: Not affected by server shutdown signals
- **Named**: "LeadDiscoveryThread" for debugging

---

#### 2.2 Discovery Process (`main.py` → `start()`)

```
start(country, city, categories)
    ↓
1. Validate country configuration
    ↓
2. Get all cities for country
    ↓
3. Reorder cities (start from selected city)
    ↓
4. Outer Loop: For each category
    │
    ├─ Inner Loop: For each city
    │   │
    │   ├─ _discover_category_leads(country, city, category)
    │   │   │
    │   │   ├─ Initialize MapsDiscoverer(country)
    │   │   │
    │   │   ├─ Search businesses
    │   │   │   ├─ Try: Google Places API (if key available)
    │   │   │   └─ Fallback: HTML scraping
    │   │   │
    │   │   ├─ For each business:
    │   │   │   │
    │   │   │   ├─ _process_business_to_lead()
    │   │   │   │   │
    │   │   │   │   ├─ Extract: name, phone, email, website, address
    │   │   │   │   ├─ Analyze website (WebsiteAnalyzer)
    │   │   │   │   │   ├─ Platform detection (Wix, WordPress, etc.)
    │   │   │   │   │   ├─ HTTPS check
    │   │   │   │   │   ├─ Booking system detection
    │   │   │   │   │   └─ Design quality assessment
    │   │   │   │   │
    │   │   │   │   ├─ Calculate lead score (LeadScorer)
    │   │   │   │   │   ├─ has_phone: +10
    │   │   │   │   │   ├─ has_email: +8
    │   │   │   │   │   ├─ low_rating: +15
    │   │   │   │   │   ├─ outdated_platform: +12
    │   │   │   │   │   └─ ... (see config.SCORE_WEIGHTS)
    │   │   │   │   │
    │   │   │   │   └─ Build lead dictionary
    │   │   │   │
    │   │   │   ├─ Check duplicates (SheetsManager)
    │   │   │   │   └─ Query Google Sheets by phone/website
    │   │   │   │
    │   │   │   ├─ If not duplicate:
    │   │   │   │   ├─ Append to Google Sheets
    │   │   │   │   │   ├─ Get/Create worksheet (country-wise)
    │   │   │   │   │   ├─ Ensure headers exist
    │   │   │   │   │   └─ Append row
    │   │   │   │   │
    │   │   │   │   └─ Call lead_callback(lead)
    │   │   │   │       └─ Append to current_leads[] (in-memory)
    │   │   │   │
    │   │   │   └─ Delay between businesses (human-like)
    │   │   │
    │   │   └─ Return leads list
    │   │
    │   └─ Delay between cities
    │
    └─ Delay between categories
```

**Discovery Strategy:**
- **Category-First**: Complete all cities for Category 1, then Category 2, etc.
- **Sequential Processing**: One business at a time (not parallel)
- **Human-like Delays**: Configurable delays between requests
- **Stop Signal Check**: Checks `should_stop` flag frequently

---

### 3. Component Details

#### 3.1 MapsDiscoverer (`maps_discoverer.py`)

**Purpose**: Search Google Maps for businesses

**Methods:**
- `search_with_places_api()`: Uses Google Places API (preferred)
- `search_businesses()`: HTML scraping fallback
- `should_exclude()`: Filter out aggregators, chains, etc.

**Country Awareness:**
- Uses country-specific Google domain (e.g., `google.co.in` for India)
- Proper locale handling for search queries

---

#### 3.2 LeadScorer (`lead_scorer.py`)

**Purpose**: Calculate lead quality score

**Scoring Factors:**
```python
SCORE_WEIGHTS = {
    "has_phone": 10,
    "has_email": 8,
    "has_address": 5,
    "low_rating": 15,        # Rating < 3.5
    "medium_rating": 10,     # Rating 3.5-4.0
    "few_reviews": 8,        # < 50 reviews
    "outdated_platform": 12, # Wix, basic WordPress
    "no_online_booking": 15,
    "no_https": 10,
    "weak_website": 10,
}
```

**Output**: Integer score (higher = better lead)

---

#### 3.3 WebsiteAnalyzer (`website_analyzer.py`)

**Purpose**: Analyze business websites

**Checks:**
- Platform detection (Wix, WordPress, Shopify, custom)
- HTTPS availability
- Online booking system presence
- Design quality (template vs custom)
- Mobile responsiveness

**Output**: Dictionary with analysis results

---

#### 3.4 SheetsManager (`sheets_manager.py`)

**Purpose**: Manage Google Sheets operations

**Key Methods:**
- `_get_or_create_worksheet(country)`: Get/create country-wise worksheet
- `append_lead(lead_data)`: Append lead to sheet
- `check_duplicate(phone, website, country, city)`: Check if lead exists

**Worksheet Strategy:**
- **Country-wise sheets**: One worksheet per country
- **Automatic creation**: Uses `addSheet` API request
- **Caching**: Caches worksheet names to avoid repeated API calls

**Data Structure:**
```
Worksheet: "United-States"
Columns: Country | City | Category | Business Name | Phone | Email | Website | Address | Rating | Review Count | Lead Score | Run ID | Timestamp
```

---

### 4. Data Flow

#### 4.1 Lead Processing Pipeline

```
Google Maps Business
    ↓
MapsDiscoverer.search()
    ↓
Business Dictionary
{
  "name": "...",
  "phone": "...",
  "website": "...",
  ...
}
    ↓
_process_business_to_lead()
    ↓
Lead Dictionary
{
  "country": "...",
  "city": "...",
  "category": "...",
  "business_name": "...",
  "phone": "...",
  "email": "...",
  "website": "...",
  "address": "...",
  "rating": 4.2,
  "review_count": 150,
  "lead_score": 85,
  "run_id": "abc12345",
  "timestamp": "2026-01-02T10:30:00"
}
    ↓
SheetsManager.check_duplicate()
    ↓
If not duplicate:
    ├─ SheetsManager.append_lead()
    │   └─ Google Sheets API
    │
    └─ lead_callback(lead)
        └─ current_leads.append(lead)
```

---

### 5. State Management

#### 5.1 Global State (`backend/main.py`)

```python
discovery_app: LeadDiscoveryApp | None  # Singleton instance
current_leads: List[Dict]                # In-memory lead storage
```

#### 5.2 Discovery State (`main.py`)

```python
self.is_running: bool           # Discovery active flag
self.should_stop: bool           # Stop signal flag
self.run_id: str                 # Unique run identifier
self.current_country: str | None
self.current_city: str | None
self.current_category: str | None
```

---

### 6. Error Handling

#### 6.1 Startup Errors
- **Credentials missing**: API starts but discovery disabled
- **Import failures**: Lazy loading prevents startup crashes
- **Config errors**: Graceful degradation with warnings

#### 6.2 Runtime Errors
- **API failures**: Logged, discovery continues
- **Network errors**: Retry logic in MapsDiscoverer
- **Sheet errors**: Logged, lead skipped (not lost)

#### 6.3 Thread Safety
- **Non-daemon threads**: Continue after main process signals
- **Callback safety**: Thread-safe lead storage
- **State updates**: Atomic flag checks

---

### 7. Configuration

#### 7.1 Environment Variables
```python
GOOGLE_SHEETS_CREDENTIALS_PATH  # Path to credentials.json or JSON content
GOOGLE_SHEETS_SPREADSHEET_ID    # Target spreadsheet ID
GOOGLE_SHEETS_WORKSHEET_NAME    # Default worksheet name (deprecated)
GOOGLE_MAPS_API_KEY             # Optional Places API key
```

#### 7.2 Config Settings (`config.py`)
```python
DEFAULT_DELAY_BETWEEN_REQUESTS = 3      # Seconds between businesses
DEFAULT_DELAY_BETWEEN_SEARCHES = 5      # Seconds between cities/categories
MAX_RESULTS_PER_CATEGORY = 50           # Safety limit
SCORE_WEIGHTS = {...}                    # Lead scoring weights
EXCLUDED_TERMS = [...]                   # Filter terms
DEFAULT_CATEGORIES = [...]               # 100+ categories
```

---

### 8. API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/status` | GET | Get discovery status |
| `/api/start` | POST | Start discovery |
| `/api/stop` | POST | Stop discovery |
| `/api/leads` | GET | Get discovered leads |
| `/api/countries` | GET | List supported countries |
| `/api/cities` | GET | Get cities for country |
| `/api/categories` | GET | List categories |
| `/api/stats` | GET | Get lead statistics |

---

### 9. Threading Model

```
Main Process (FastAPI/Uvicorn)
    │
    ├─ Request Handler Threads (FastAPI)
    │   └─ Handle HTTP requests
    │
    └─ Discovery Thread (Non-Daemon)
        └─ LeadDiscoveryApp.start()
            └─ Runs independently
                └─ Survives server shutdown
```

**Key Points:**
- Discovery runs in **separate thread**
- **Non-daemon**: Continues after main process exits
- **Independent lifecycle**: Not tied to HTTP request lifecycle
- **Persistent**: Continues even if browser closes

---

### 10. Persistence Strategy

#### 10.1 Google Sheets (Primary Storage)
- **Append-only**: Leads never deleted
- **Country-wise organization**: One worksheet per country
- **Real-time writes**: Leads saved immediately
- **Duplicate prevention**: Check before append

#### 10.2 In-Memory (Temporary)
- **current_leads[]**: Recent leads for API responses
- **Not persistent**: Cleared on restart
- **Fast access**: For real-time UI updates

---

## Summary

The backend architecture follows a **modular, layered design**:

1. **API Layer**: FastAPI handles HTTP requests/responses
2. **Application Layer**: LeadDiscoveryApp orchestrates discovery
3. **Service Layer**: Specialized components (Maps, Scoring, Analysis, Sheets)
4. **Persistence Layer**: Google Sheets API

**Key Design Principles:**
- ✅ **Lazy Loading**: Prevents startup failures
- ✅ **Graceful Degradation**: System works even with partial failures
- ✅ **Independent Execution**: Discovery survives server lifecycle
- ✅ **Country-Aware**: Proper internationalization
- ✅ **Human-like Behavior**: Delays and sequential processing
- ✅ **Append-Only**: Data integrity through immutability

