"""
Configuration for B2B Lead Discovery System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json")
GOOGLE_SHEETS_SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "")
GOOGLE_SHEETS_WORKSHEET_NAME = os.getenv("GOOGLE_SHEETS_WORKSHEET_NAME", "Leads")

# Google Maps API (Optional - can use scraping instead)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

# Execution Settings
DEFAULT_DELAY_BETWEEN_REQUESTS = 3  # seconds (human-like delay)
DEFAULT_DELAY_BETWEEN_SEARCHES = 5  # seconds between different searches
MAX_LONG_RUNNING_HOURS = 24
MAX_RESULTS_PER_CATEGORY = 50  # Safety limit per category

# Search Settings
MIN_RATING_THRESHOLD = 0.0  # Minimum rating to consider (0 = no filter)
MAX_RATING_THRESHOLD = 4.5  # Maximum rating (lower = more likely to need help)

# Lead Scoring Weights
SCORE_WEIGHTS = {
    "has_phone": 10,
    "has_email": 8,
    "has_address": 5,
    "low_rating": 15,  # Rating < 3.5
    "medium_rating": 10,  # Rating 3.5-4.0
    "few_reviews": 8,  # < 50 reviews
    "outdated_platform": 12,  # Wix, basic WordPress
    "no_online_booking": 15,
    "no_https": 10,
    "weak_website": 10,  # Basic template, poor design
}

# Excluded Terms (businesses to skip)
EXCLUDED_TERMS = [
    "job portal",
    "job board",
    "recruitment",
    "government",
    "municipal",
    "franchise",
    "chain",
    "aggregator",
    "directory",
    "justdial",
    "yelp",
]

# Target Categories (default - can be customized)
# Focus on appointment-based services and businesses that benefit from automation
DEFAULT_CATEGORIES = [
    # Healthcare & Wellness (appointment-heavy)
    "dental clinic",
    "medical clinic",
    "doctor office",
    "veterinary clinic",
    "physiotherapy clinic",
    "chiropractic clinic",
    "massage therapy",
    "acupuncture clinic",
    "psychology clinic",
    "counseling center",
    
    # Beauty & Personal Care (appointment-based)
    "beauty salon",
    "hair salon",
    "barber shop",
    "nail salon",
    "spa",
    "esthetician",
    "tattoo parlor",
    "piercing studio",
    "laser hair removal",
    "cosmetic clinic",
    
    # Fitness & Sports (membership + appointments)
    "fitness center",
    "gym",
    "yoga studio",
    "pilates studio",
    "martial arts school",
    "dance studio",
    "personal trainer",
    "swimming pool",
    "tennis club",
    "golf club",
    
    # Professional Services (appointment-based)
    "law firm",
    "accounting firm",
    "consulting firm",
    "financial advisor",
    "insurance agency",
    "real estate agency",
    "real estate agent",
    "mortgage broker",
    "tax preparer",
    
    # Education & Training (scheduling needed)
    "coaching institute",
    "tutoring center",
    "driving school",
    "music school",
    "language school",
    "art school",
    "training center",
    "bootcamp",
    
    # Home Services (appointment-based)
    "plumber",
    "electrician",
    "hvac contractor",
    "handyman",
    "carpenter",
    "roofer",
    "painter",
    "landscaping service",
    "lawn care service",
    "cleaning service",
    "moving company",
    
    # Automotive (appointment-based)
    "auto repair shop",
    "car mechanic",
    "auto body shop",
    "car wash",
    "tire shop",
    "auto detailing",
    
    # Food & Hospitality (reservations/bookings)
    "restaurant",
    "cafe",
    "catering service",
    "food truck",
    "bakery",
    "pizzeria",
    
    # Photography & Events (booking-based)
    "photography studio",
    "wedding photographer",
    "event planner",
    "caterer",
    "florist",
    "dj service",
    "party rental",
    
    # Retail & E-commerce (online presence important)
    "e-commerce store",
    "retail store",
    "boutique",
    "jewelry store",
    "furniture store",
    "pet store",
    
    # Other Service Businesses
    "dry cleaner",
    "laundromat",
    "tailor",
    "shoe repair",
    "locksmith",
    "appliance repair",
    "computer repair",
    "phone repair",
    
    # Creative & Media (project-based)
    "digital marketing agency",
    "web design agency",
    "graphic design studio",
    "advertising agency",
    "video production",
    "printing service",
    
    # Manufacturing & Trade
    "small manufacturer",
    "welding shop",
    "machine shop",
    "fabrication shop",
    
    # Pet Services (appointment-based)
    "pet grooming",
    "dog daycare",
    "pet boarding",
    "pet training",
]

