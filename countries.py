"""
Country configuration and mappings for country-aware search
"""
from typing import Dict, List, Optional

# Country data: google_domain, business_terminology, phone_format
COUNTRIES: Dict[str, Dict[str, str]] = {
    "United States": {
        "code": "US",
        "google_domain": "google.com",
        "locale": "en-US",
    },
    "India": {
        "code": "IN",
        "google_domain": "google.co.in",
        "locale": "en-IN",
    },
    "United Kingdom": {
        "code": "GB",
        "google_domain": "google.co.uk",
        "locale": "en-GB",
    },
    "Canada": {
        "code": "CA",
        "google_domain": "google.ca",
        "locale": "en-CA",
    },
    "Australia": {
        "code": "AU",
        "google_domain": "google.com.au",
        "locale": "en-AU",
    },
    "Germany": {
        "code": "DE",
        "google_domain": "google.de",
        "locale": "de-DE",
    },
    "France": {
        "code": "FR",
        "google_domain": "google.fr",
        "locale": "fr-FR",
    },
    "Spain": {
        "code": "ES",
        "google_domain": "google.es",
        "locale": "es-ES",
    },
    "Italy": {
        "code": "IT",
        "google_domain": "google.it",
        "locale": "it-IT",
    },
    "Netherlands": {
        "code": "NL",
        "google_domain": "google.nl",
        "locale": "nl-NL",
    },
    "Brazil": {
        "code": "BR",
        "google_domain": "google.com.br",
        "locale": "pt-BR",
    },
    "Mexico": {
        "code": "MX",
        "google_domain": "google.com.mx",
        "locale": "es-MX",
    },
    "Argentina": {
        "code": "AR",
        "google_domain": "google.com.ar",
        "locale": "es-AR",
    },
    "South Africa": {
        "code": "ZA",
        "google_domain": "google.co.za",
        "locale": "en-ZA",
    },
    "United Arab Emirates": {
        "code": "AE",
        "google_domain": "google.ae",
        "locale": "en-AE",
    },
    "Singapore": {
        "code": "SG",
        "google_domain": "google.com.sg",
        "locale": "en-SG",
    },
    "Japan": {
        "code": "JP",
        "google_domain": "google.co.jp",
        "locale": "ja-JP",
    },
    "South Korea": {
        "code": "KR",
        "google_domain": "google.co.kr",
        "locale": "ko-KR",
    },
    "New Zealand": {
        "code": "NZ",
        "google_domain": "google.co.nz",
        "locale": "en-NZ",
    },
    "Ireland": {
        "code": "IE",
        "google_domain": "google.ie",
        "locale": "en-IE",
    },
}


def get_country_config(country_name: str) -> Optional[Dict[str, str]]:
    """Get configuration for a country by name"""
    return COUNTRIES.get(country_name)


def search_countries(query: str) -> List[str]:
    """Search countries by name (case-insensitive)"""
    query_lower = query.lower()
    return [
        name for name in COUNTRIES.keys()
        if query_lower in name.lower() or query_lower in name.lower().replace(" ", "")
    ]


def list_all_countries() -> List[str]:
    """Get list of all supported countries"""
    return list(COUNTRIES.keys())


def get_google_domain(country_name: str) -> str:
    """Get Google domain for a country"""
    config = get_country_config(country_name)
    return config["google_domain"] if config else "google.com"

