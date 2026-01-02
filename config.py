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
    # =========================
    # Healthcare & Wellness
    # =========================
    "dental clinic",
    "medical clinic",
    "doctor office",
    "private hospital",
    "veterinary clinic",
    "physiotherapy clinic",
    "chiropractic clinic",
    "orthopedic clinic",
    "skin clinic",
    "dermatology clinic",
    "cosmetic clinic",
    "aesthetic clinic",
    "fertility clinic",
    "ivf clinic",
    "diagnostic center",
    "pathology lab",
    "radiology center",
    "imaging center",
    "mental health clinic",
    "psychology clinic",
    "counseling center",
    "psychiatry clinic",
    "nutritionist",
    "dietitian",
    "ayurveda clinic",
    "homeopathy clinic",
    "naturopathy clinic",

    # =========================
    # Beauty & Personal Care
    # =========================
    "beauty salon",
    "hair salon",
    "barber shop",
    "nail salon",
    "spa",
    "massage spa",
    "wellness spa",
    "esthetician",
    "makeup studio",
    "bridal makeup artist",
    "tattoo parlor",
    "piercing studio",
    "laser hair removal",
    "skin care center",

    # =========================
    # Fitness, Sports & Lifestyle
    # =========================
    "fitness center",
    "gym",
    "crossfit gym",
    "yoga studio",
    "pilates studio",
    "martial arts school",
    "karate school",
    "taekwondo academy",
    "dance studio",
    "zumba studio",
    "personal trainer",
    "swimming academy",
    "tennis academy",
    "badminton academy",
    "sports academy",
    "golf club",

    # =========================
    # Professional & Financial Services
    # =========================
    "law firm",
    "law office",
    "accounting firm",
    "chartered accountant",
    "bookkeeping service",
    "consulting firm",
    "business consultant",
    "financial advisor",
    "investment advisor",
    "insurance agency",
    "tax consultant",
    "audit firm",
    "company registration service",

    # =========================
    # Real Estate & Property
    # =========================
    "real estate agency",
    "real estate agent",
    "property consultant",
    "property dealer",
    "real estate broker",
    "commercial real estate",
    "property management company",
    "rental agency",
    "vacation rental agency",

    # =========================
    # Education & Training
    # =========================
    "coaching institute",
    "tutoring center",
    "private tutor",
    "driving school",
    "music school",
    "dance academy",
    "language school",
    "english academy",
    "computer training institute",
    "coding bootcamp",
    "it training center",
    "exam coaching center",
    "study abroad consultant",
    "career counseling center",

    # =========================
    # Home & Local Services
    # =========================
    "plumber",
    "electrician",
    "hvac contractor",
    "air conditioning service",
    "handyman",
    "carpenter",
    "painter",
    "interior designer",
    "home renovation",
    "contractor",
    "construction company",
    "roofer",
    "waterproofing service",
    "landscaping service",
    "lawn care service",
    "cleaning service",
    "house cleaning",
    "office cleaning",
    "pest control service",
    "moving company",
    "packers and movers",

    # =========================
    # Automotive Services
    # =========================
    "auto repair shop",
    "car mechanic",
    "auto service center",
    "auto body shop",
    "car detailing",
    "car wash",
    "tire shop",
    "battery service",
    "vehicle inspection center",
    "motorcycle repair shop",

    # =========================
    # Food, Hospitality & Travel
    # =========================
    "restaurant",
    "fine dining restaurant",
    "cafe",
    "coffee shop",
    "bakery",
    "pizzeria",
    "cloud kitchen",
    "catering service",
    "food truck",
    "hotel",
    "boutique hotel",
    "resort",
    "guest house",
    "hostel",
    "travel agency",
    "tour operator",
    "tourism company",

    # =========================
    # Events, Media & Creative
    # =========================
    "photography studio",
    "wedding photographer",
    "videography service",
    "event planner",
    "wedding planner",
    "event management company",
    "dj service",
    "sound system rental",
    "party rental service",
    "florist",
    "decoration service",

    # =========================
    # Retail, D2C & Commerce
    # =========================
    "retail store",
    "boutique",
    "clothing store",
    "fashion boutique",
    "shoe store",
    "jewelry store",
    "optical store",
    "furniture store",
    "electronics store",
    "mobile phone shop",
    "computer store",
    "pet store",
    "organic food store",
    "grocery store",
    "e-commerce store",
    "online store",

    # =========================
    # Repair & Technical Services
    # =========================
    "computer repair",
    "laptop repair",
    "phone repair",
    "mobile repair",
    "appliance repair",
    "ac repair service",
    "refrigerator repair",
    "washing machine repair",
    "it service provider",
    "managed it services",

    # =========================
    # Digital, Tech & Agencies
    # =========================
    "digital marketing agency",
    "seo agency",
    "social media agency",
    "performance marketing agency",
    "web design agency",
    "web development company",
    "software development company",
    "it consulting company",
    "automation services",
    "ai consulting company",

    # =========================
    # Manufacturing & B2B
    # =========================
    "small manufacturer",
    "manufacturing company",
    "fabrication shop",
    "machine shop",
    "welding shop",
    "cnc machining",
    "industrial supplier",
    "packaging company",
    "printing company",

    # =========================
    # Pet Services
    # =========================
    "pet grooming",
    "dog grooming",
    "dog daycare",
    "pet boarding",
    "pet training",
    "pet clinic",
    "animal hospital",
]

