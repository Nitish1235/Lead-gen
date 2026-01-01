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
    "Sweden": {
        "code": "SE",
        "google_domain": "google.se",
        "locale": "sv-SE",
    },
    "Norway": {
        "code": "NO",
        "google_domain": "google.no",
        "locale": "no-NO",
    },
    "Denmark": {
        "code": "DK",
        "google_domain": "google.dk",
        "locale": "da-DK",
    },
    "Finland": {
        "code": "FI",
        "google_domain": "google.fi",
        "locale": "fi-FI",
    },
    "Poland": {
        "code": "PL",
        "google_domain": "google.pl",
        "locale": "pl-PL",
    },
    "Belgium": {
        "code": "BE",
        "google_domain": "google.be",
        "locale": "nl-BE",
    },
    "Switzerland": {
        "code": "CH",
        "google_domain": "google.ch",
        "locale": "de-CH",
    },
    "Austria": {
        "code": "AT",
        "google_domain": "google.at",
        "locale": "de-AT",
    },
    "Portugal": {
        "code": "PT",
        "google_domain": "google.pt",
        "locale": "pt-PT",
    },
    "Greece": {
        "code": "GR",
        "google_domain": "google.gr",
        "locale": "el-GR",
    },
    "Turkey": {
        "code": "TR",
        "google_domain": "google.com.tr",
        "locale": "tr-TR",
    },
    "Russia": {
        "code": "RU",
        "google_domain": "google.ru",
        "locale": "ru-RU",
    },
    "China": {
        "code": "CN",
        "google_domain": "google.cn",
        "locale": "zh-CN",
    },
    "Hong Kong": {
        "code": "HK",
        "google_domain": "google.com.hk",
        "locale": "zh-HK",
    },
    "Taiwan": {
        "code": "TW",
        "google_domain": "google.com.tw",
        "locale": "zh-TW",
    },
    "Thailand": {
        "code": "TH",
        "google_domain": "google.co.th",
        "locale": "th-TH",
    },
    "Malaysia": {
        "code": "MY",
        "google_domain": "google.com.my",
        "locale": "en-MY",
    },
    "Indonesia": {
        "code": "ID",
        "google_domain": "google.co.id",
        "locale": "id-ID",
    },
    "Philippines": {
        "code": "PH",
        "google_domain": "google.com.ph",
        "locale": "en-PH",
    },
    "Vietnam": {
        "code": "VN",
        "google_domain": "google.com.vn",
        "locale": "vi-VN",
    },
    "Saudi Arabia": {
        "code": "SA",
        "google_domain": "google.com.sa",
        "locale": "ar-SA",
    },
    "Israel": {
        "code": "IL",
        "google_domain": "google.co.il",
        "locale": "iw-IL",
    },
    "Egypt": {
        "code": "EG",
        "google_domain": "google.com.eg",
        "locale": "ar-EG",
    },
    "Nigeria": {
        "code": "NG",
        "google_domain": "google.com.ng",
        "locale": "en-NG",
    },
    "Kenya": {
        "code": "KE",
        "google_domain": "google.co.ke",
        "locale": "en-KE",
    },
    "Chile": {
        "code": "CL",
        "google_domain": "google.cl",
        "locale": "es-CL",
    },
    "Colombia": {
        "code": "CO",
        "google_domain": "google.com.co",
        "locale": "es-CO",
    },
    "Peru": {
        "code": "PE",
        "google_domain": "google.com.pe",
        "locale": "es-PE",
    },
    "Venezuela": {
        "code": "VE",
        "google_domain": "google.co.ve",
        "locale": "es-VE",
    },
    "Ecuador": {
        "code": "EC",
        "google_domain": "google.com.ec",
        "locale": "es-EC",
    },
    "Uruguay": {
        "code": "UY",
        "google_domain": "google.com.uy",
        "locale": "es-UY",
    },
    "Costa Rica": {
        "code": "CR",
        "google_domain": "google.co.cr",
        "locale": "es-CR",
    },
    "Panama": {
        "code": "PA",
        "google_domain": "google.com.pa",
        "locale": "es-PA",
    },
    "Guatemala": {
        "code": "GT",
        "google_domain": "google.com.gt",
        "locale": "es-GT",
    },
    "Czech Republic": {
        "code": "CZ",
        "google_domain": "google.cz",
        "locale": "cs-CZ",
    },
    "Hungary": {
        "code": "HU",
        "google_domain": "google.hu",
        "locale": "hu-HU",
    },
    "Romania": {
        "code": "RO",
        "google_domain": "google.ro",
        "locale": "ro-RO",
    },
    "Ukraine": {
        "code": "UA",
        "google_domain": "google.com.ua",
        "locale": "uk-UA",
    },
    "Pakistan": {
        "code": "PK",
        "google_domain": "google.com.pk",
        "locale": "en-PK",
    },
    "Bangladesh": {
        "code": "BD",
        "google_domain": "google.com.bd",
        "locale": "en-BD",
    },
    "Sri Lanka": {
        "code": "LK",
        "google_domain": "google.lk",
        "locale": "en-LK",
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

