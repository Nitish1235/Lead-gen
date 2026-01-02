# B2B Lead Discovery System

A personal, high-precision B2B lead intelligence system for discovering businesses worldwide that are ideal clients for software development, automation, cloud infrastructure, and AI services.

## Core Philosophy

- **Quality over quantity**: Focus on highly relevant, actionable leads
- **Single-user, manual control**: Run only when you start it, stop immediately when requested
- **Minimal infrastructure**: Uses Google Sheets as the only database, optimized for free GCP credits
- **No over-engineering**: Clean, simple, maintainable code

## Features

- 🌍 **Country-aware discovery**: Search businesses in any country with proper Google domain and locale handling
- 🔍 **Intelligent search**: Focuses on Google Maps listings with phone numbers, addresses, and weak websites
- 📊 **Lead scoring**: Automatic scoring based on quality signals (rating, website quality, contact info)
- 🎯 **Target categories**: 100+ pre-configured categories (salons, barbers, medical clinics, fitness centers, home services, and more)
- 🚫 **Smart filtering**: Excludes aggregators, job boards, large chains, government entities
- 📈 **Google Sheets storage**: All leads saved to Google Sheets (append-only, human-readable)
- 🌐 **Website analysis**: Detects platform (Wix, WordPress, Shopify), booking systems, HTTPS, etc.
- ⏸️ **Manual control**: Start/stop execution, sequential processing with human-like delays

## Requirements

- Python 3.8+
- Google Cloud Platform account (free tier sufficient)
- Google Sheets API credentials
- (Optional) Google Places API key for more reliable results

## Setup

### 1. Clone and Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Google Sheets API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable **Google Sheets API** and **Google Drive API**
4. Create a **Service Account**:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Give it a name (e.g., "lead-discovery")
   - Grant role: "Editor" (for Sheets)
   - Click "Done"
5. Create credentials:
   - Click on the service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose JSON format
   - Download the JSON file
   - Save it as `credentials.json` in the project root
6. Create a Google Sheet:
   - Create a new Google Sheet
   - Copy the Sheet ID from the URL (between `/d/` and `/edit`)
   - Share the sheet with the service account email (from credentials.json)
   - Give "Editor" permissions

### 3. Configuration

Create a `.env` file (or set environment variables):

```env
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id_here
GOOGLE_SHEETS_WORKSHEET_NAME=Leads
GOOGLE_MAPS_API_KEY=your_api_key_here  # Optional but recommended
```

**Note**: You can also edit `config.py` directly if you prefer.

### 4. (Optional but Recommended) Google Places API

For reliable business discovery, get a Google Places API key. **Without this, you may see "REQUEST_DENIED" errors.**

1. In Google Cloud Console, enable **Places API (New)**
2. Create an API key
3. Enable billing (required, but $200 free credit/month is usually enough)
4. Add the key to `.env` as `GOOGLE_MAPS_API_KEY`

See [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) for detailed setup instructions.

**Note**: The system will use Places API if available, otherwise it will attempt HTML scraping (less reliable and may fail).

## Usage

### Web UI (Recommended)

Launch the modern web interface:

```bash
python run_ui.py
```

Or directly with Streamlit:

```bash
streamlit run web_app.py
```

The web UI provides:
- 🎨 Modern, intuitive interface
- 📊 Real-time progress tracking
- 📋 Live lead display as they're discovered
- 📈 Statistics and analytics
- ⚙️ Easy configuration
- 🎯 Visual category selection

### Command Line Interface

Run the traditional CLI:

```bash
python main.py
```

Commands:
- `start <country> <city> [categories...]` - Start discovery
  - Example: `start United States New York` (uses all default categories)
  - Example: `start India Mumbai barber shop hair salon` (search specific categories)
  - Example: `start United States Los Angeles dental clinic spa fitness center`
- `stop` - Stop current discovery
- `status` - Show current status
- `countries` - List all supported countries
- `search-countries <query>` - Search countries
- `exit` - Exit application

### Example Session

```
> countries
Supported countries (20):
  1. United States
  2. India
  3. United Kingdom
  ...

> start United States New York
B2B Lead Discovery Started
Run ID: a3f5b2c1
Country: United States
City: New York
Categories: 105
Mode: Standard

[1/105] Searching: dental clinic
Location: New York, United States
Found 15 businesses, evaluating...
  [1/15] Processing: ABC Dental Clinic
    ✓ Saved (Score: 85)
  [2/15] Processing: XYZ Dentistry
    ✓ Saved (Score: 72)
  ...
```

### Programmatic Usage

You can also use the system programmatically:

```python
from main import LeadDiscoveryApp

app = LeadDiscoveryApp()
app.start(
    country="United States",
    city="San Francisco",
    categories=["dental clinic", "real estate agency"],  # Optional
)
```

## Configuration

Edit `config.py` to customize:

- **Categories**: Modify `DEFAULT_CATEGORIES` list
- **Lead scoring weights**: Adjust `SCORE_WEIGHTS` dictionary
- **Excluded terms**: Add terms to `EXCLUDED_TERMS` list
- **Delays**: Adjust `DEFAULT_DELAY_BETWEEN_REQUESTS` and `DEFAULT_DELAY_BETWEEN_SEARCHES`
- **Limits**: Change `MAX_RESULTS_PER_CATEGORY`

## Lead Scoring

Leads are scored based on:

- **Contact information** (phone, email, address)
- **Rating signals** (lower ratings = more likely to need help)
- **Review count** (fewer reviews = growing business)
- **Website quality**:
  - Platform (Wix, WordPress, basic builders = higher score)
  - No online booking system
  - No HTTPS
  - Weak/outdated design

Higher scores indicate better lead quality.

## Google Sheets Schema

Leads are saved with the following columns:

- Country
- City
- Category
- Business Name
- Phone
- Email
- Website
- Address
- Rating
- Review Count
- Lead Score
- Run ID
- Timestamp

## Target Categories

The system includes **100+ pre-configured business categories**, organized by type:

### Appointment-Based Services (High Priority)
- **Beauty & Personal Care**: Hair salons, barber shops, nail salons, spas, tattoo parlors, etc.
- **Healthcare & Wellness**: Dental clinics, medical clinics, veterinary clinics, massage therapy, etc.
- **Fitness & Sports**: Gyms, yoga studios, dance studios, martial arts schools, etc.
- **Professional Services**: Law firms, accounting firms, consulting, real estate agencies, etc.
- **Education & Training**: Coaching institutes, tutoring centers, driving schools, music schools, etc.

### Service Businesses
- **Home Services**: Plumbers, electricians, HVAC contractors, landscapers, cleaners, etc.
- **Automotive**: Auto repair shops, car mechanics, car washes, detailing, etc.
- **Other Services**: Locksmiths, appliance repair, computer repair, dry cleaners, etc.

### Event & Booking-Based
- **Food & Hospitality**: Restaurants, cafes, catering services, bakeries, etc.
- **Photography & Events**: Photography studios, event planners, florists, DJ services, etc.

### Retail & E-commerce
- Retail stores, boutiques, jewelry stores, e-commerce stores, etc.

### Creative & Media
- Digital marketing agencies, web design agencies, graphic design studios, etc.

**Note**: You can customize categories in `config.py` or specify categories when starting a search.

## Supported Countries

The system supports 20+ countries including:

- United States, Canada, United Kingdom
- India, Australia, New Zealand
- Germany, France, Spain, Italy, Netherlands
- Brazil, Mexico, Argentina
- South Africa, UAE, Singapore
- Japan, South Korea
- And more...

Use `countries` command to see the full list.

## Safety & Rate Limits

- Sequential execution (no parallel requests)
- Human-like delays between requests (3-5 seconds)
- Respects Google's rate limits
- Graceful error handling
- Safe stop on Ctrl+C

## Cost Optimization

- Uses Google Sheets API (free tier: 300 requests/minute)
- Optional Google Places API ($200 free credit/month)
- No proxies or expensive infrastructure
- Designed for near-zero monthly cost

## Troubleshooting

### "Credentials file not found"
- Make sure `credentials.json` is in the project root
- Check the path in `.env` or `config.py`

### "Permission denied" on Google Sheets
- Share the Google Sheet with the service account email
- Ensure the service account has "Editor" permissions

### "No leads found"
- Check if Google Places API key is set (recommended)
- Try different cities/categories
- HTML scraping without API key is unreliable

### "Places API error"
- Verify API key is correct
- Ensure Places API is enabled in Google Cloud Console
- Check API quota/limits

## Architecture

```
main.py              # Main application with CLI
config.py            # Configuration
countries.py         # Country mappings
sheets_manager.py    # Google Sheets integration
maps_discoverer.py   # Google Maps/Places discovery
website_analyzer.py  # Website analysis
lead_scorer.py       # Lead scoring & justification
```

## Deployment

For deploying to Google Cloud Platform, see [DEPLOYMENT_GCP.md](DEPLOYMENT_GCP.md).

Quick options:
- **Local use**: Follow QUICKSTART.md (recommended for personal use)
- **GCP VM**: See DEPLOYMENT_GCP.md Option 1 (best for automated/long runs)
- **Cloud Run**: See DEPLOYMENT_GCP.md Option 2 (for API access)

## License

Personal use only. Not for resale or commercial distribution.

## Contributing

This is a personal tool. If you fork it, customize it for your needs!

