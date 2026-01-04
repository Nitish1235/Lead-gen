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

def get_google_domain(country_name: str) -> str:
    """Get Google domain for a country"""
    config = get_country_config(country_name)
    return config["google_domain"] if config else "google.com"


# Cities organized by tier for each country
# Tier 1: Major metropolitan areas (largest cities)
# Tier 2: Secondary cities (regional centers)
# Tier 3: Smaller but significant cities
CITIES: Dict[str, Dict[str, List[str]]] = {
    "United States": {
        "Tier 1": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"],
        "Tier 2": ["Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington"],
        "Tier 3": ["Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City", "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore"]
    },
    "India": {
        "Tier 1": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Surat"],
        "Tier 2": ["Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Patna", "Vadodara", "Ghaziabad"],
        "Tier 3": ["Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Varanasi", "Srinagar", "Amritsar", "Allahabad"]
    },
    "United Kingdom": {
        "Tier 1": ["London", "Birmingham", "Manchester", "Glasgow", "Liverpool", "Leeds", "Sheffield", "Edinburgh", "Bristol", "Leicester"],
        "Tier 2": ["Coventry", "Cardiff", "Belfast", "Nottingham", "Kingston upon Hull", "Newcastle upon Tyne", "Stoke-on-Trent", "Southampton", "Derby", "Portsmouth"],
        "Tier 3": ["Brighton", "Reading", "Northampton", "Luton", "Bolton", "Ipswich", "Middlesbrough", "Peterborough", "Swindon", "Norwich"]
    },
    "Canada": {
        "Tier 1": ["Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton", "Ottawa", "Winnipeg", "Quebec City", "Hamilton", "Kitchener"],
        "Tier 2": ["London", "Victoria", "Halifax", "Oshawa", "Windsor", "Saskatoon", "Regina", "Sherbrooke", "Kelowna", "Barrie"],
        "Tier 3": ["Abbotsford", "Sudbury", "Kingston", "Saguenay", "Trois-Rivières", "Guelph", "Cambridge", "Coquitlam", "Thunder Bay", "St. John's"]
    },
    "Australia": {
        "Tier 1": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Newcastle", "Canberra", "Sunshine Coast", "Wollongong"],
        "Tier 2": ["Hobart", "Geelong", "Townsville", "Cairns", "Toowoomba", "Darwin", "Ballarat", "Bendigo", "Albury", "Launceston"],
        "Tier 3": ["Mackay", "Rockhampton", "Bunbury", "Bundaberg", "Coffs Harbour", "Wagga Wagga", "Hervey Bay", "Port Macquarie", "Tamworth", "Orange"]
    },
    "Germany": {
        "Tier 1": ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf", "Dortmund", "Essen", "Leipzig"],
        "Tier 2": ["Bremen", "Dresden", "Hannover", "Nuremberg", "Duisburg", "Bochum", "Wuppertal", "Bielefeld", "Bonn", "Münster"],
        "Tier 3": ["Karlsruhe", "Mannheim", "Augsburg", "Wiesbaden", "Gelsenkirchen", "Mönchengladbach", "Braunschweig", "Chemnitz", "Kiel", "Aachen"]
    },
    "France": {
        "Tier 1": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille"],
        "Tier 2": ["Rennes", "Reims", "Saint-Étienne", "Le Havre", "Toulon", "Grenoble", "Dijon", "Angers", "Nîmes", "Villeurbanne"],
        "Tier 3": ["Saint-Denis", "Le Mans", "Aix-en-Provence", "Clermont-Ferrand", "Brest", "Limoges", "Tours", "Amiens", "Perpignan", "Metz"]
    },
    "Spain": {
        "Tier 1": ["Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza", "Málaga", "Murcia", "Palma", "Las Palmas", "Bilbao"],
        "Tier 2": ["Alicante", "Córdoba", "Valladolid", "Vigo", "Gijón", "Hospitalet", "Granada", "Vitoria-Gasteiz", "A Coruña", "Elche"],
        "Tier 3": ["Santa Cruz de Tenerife", "Oviedo", "Móstoles", "Pamplona", "Almería", "Fuenlabrada", "Leganés", "Santander", "Burgos", "Salamanca"]
    },
    "Italy": {
        "Tier 1": ["Rome", "Milan", "Naples", "Turin", "Palermo", "Genoa", "Bologna", "Florence", "Bari", "Catania"],
        "Tier 2": ["Venice", "Verona", "Messina", "Padua", "Trieste", "Brescia", "Parma", "Prato", "Taranto", "Modena"],
        "Tier 3": ["Reggio Calabria", "Reggio Emilia", "Perugia", "Livorno", "Ravenna", "Cagliari", "Foggia", "Rimini", "Salerno", "Ferrara"]
    },
    "Netherlands": {
        "Tier 1": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven", "Groningen", "Tilburg", "Almere", "Breda", "Nijmegen"],
        "Tier 2": ["Enschede", "Haarlem", "Arnhem", "Zaanstad", "Amersfoort", "Apeldoorn", "Hoofddorp", "Maastricht", "Leiden", "Dordrecht"],
        "Tier 3": ["Zoetermeer", "Zwolle", "Deventer", "Delft", "Leeuwarden", "Alkmaar", "Heerlen", "Venlo", "Helmond", "Hengelo"]
    },
    "Brazil": {
        "Tier 1": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza", "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre"],
        "Tier 2": ["Belém", "Goiânia", "Guarulhos", "Campinas", "São Luís", "São Gonçalo", "Maceió", "Duque de Caxias", "Natal", "Teresina"],
        "Tier 3": ["Campo Grande", "Nova Iguaçu", "São Bernardo do Campo", "João Pessoa", "Santo André", "Osasco", "Jaboatão dos Guararapes", "São José dos Campos", "Ribeirão Preto", "Uberlândia"]
    },
    "Mexico": {
        "Tier 1": ["Mexico City", "Guadalajara", "Monterrey", "Puebla", "Tijuana", "León", "Juárez", "Torreón", "Querétaro", "San Luis Potosí"],
        "Tier 2": ["Mérida", "Mexicali", "Aguascalientes", "Tlalnepantla", "Chihuahua", "Naucalpan", "Cancún", "Saltillo", "Hermosillo", "Morelia"],
        "Tier 3": ["Culiacán", "Reynosa", "Tlajomulco de Zúñiga", "Tuxtla Gutiérrez", "Cuernavaca", "Acapulco", "Tepic", "Durango", "Chimalhuacán", "Veracruz"]
    },
    "Argentina": {
        "Tier 1": ["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "Tucumán", "La Plata", "Mar del Plata", "Salta", "Santa Fe", "San Juan"],
        "Tier 2": ["San Miguel de Tucumán", "Lanús", "Merlo", "González Catán", "Quilmes", "Almirante Brown", "Moreno", "Florencio Varela", "Berazategui", "Avellaneda"],
        "Tier 3": ["Bahía Blanca", "Corrientes", "Paraná", "Posadas", "Neuquén", "Formosa", "San Salvador de Jujuy", "La Rioja", "Catamarca", "Río Cuarto"]
    },
    "South Africa": {
        "Tier 1": ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Port Elizabeth", "Bloemfontein", "East London", "Nelspruit", "Polokwane", "Kimberley"],
        "Tier 2": ["Rustenburg", "Welkom", "Pietermaritzburg", "Benoni", "Tembisa", "Vereeniging", "Boksburg", "Klerksdorp", "Soweto", "Uitenhage"],
        "Tier 3": ["Brakpan", "Witbank", "Krugersdorp", "Botshabelo", "Newcastle", "Kroonstad", "Carletonville", "Midrand", "Centurion", "Vanderbijlpark"]
    },
    "United Arab Emirates": {
        "Tier 1": ["Dubai", "Abu Dhabi", "Sharjah", "Al Ain", "Ajman", "Ras Al Khaimah", "Fujairah", "Umm Al Quwain"],
        "Tier 2": ["Khor Fakkan", "Kalba", "Jebel Ali", "Dibba", "Madinat Zayed", "Liwa Oasis", "Ruwais", "Ghayathi"],
        "Tier 3": ["Ar-Rams", "Dhaid", "Hatta", "Masafi", "Al Madam", "Al Dhaid", "Al Quoz", "Jumeirah"]
    },
    "Singapore": {
        "Tier 1": ["Singapore", "Jurong", "Tampines", "Woodlands", "Yishun", "Ang Mo Kio", "Hougang", "Punggol", "Sengkang", "Pasir Ris"],
        "Tier 2": ["Choa Chu Kang", "Bukit Batok", "Bukit Panjang", "Clementi", "Queenstown", "Toa Payoh", "Bishan", "Serangoon", "Bedok", "Marina Bay"],
        "Tier 3": ["Orchard", "Raffles Place", "Sentosa", "Changi", "Paya Lebar", "Kallang", "Geylang", "Katong", "Novena", "Newton"]
    },
    "Japan": {
        "Tier 1": ["Tokyo", "Yokohama", "Osaka", "Nagoya", "Sapporo", "Fukuoka", "Kobe", "Kawasaki", "Kyoto", "Saitama"],
        "Tier 2": ["Hiroshima", "Sendai", "Chiba", "Kitakyushu", "Sakai", "Niigata", "Hamamatsu", "Kumamoto", "Sagamihara", "Shizuoka"],
        "Tier 3": ["Okayama", "Kagoshima", "Hachioji", "Utsunomiya", "Matsuyama", "Kanazawa", "Oita", "Nagasaki", "Toyama", "Gifu"]
    },
    "South Korea": {
        "Tier 1": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju", "Suwon", "Ulsan", "Changwon", "Goyang"],
        "Tier 2": ["Yongin", "Seongnam", "Bucheon", "Ansan", "Anyang", "Jeonju", "Cheonan", "Namyangju", "Hwaseong", "Cheongju"],
        "Tier 3": ["Gimhae", "Pohang", "Jeju", "Jinju", "Asan", "Gimpo", "Iksan", "Gunsan", "Suncheon", "Mokpo"]
    },
    "New Zealand": {
        "Tier 1": ["Auckland", "Wellington", "Christchurch", "Hamilton", "Tauranga", "Napier", "Palmerston North", "Dunedin", "Rotorua", "New Plymouth"],
        "Tier 2": ["Whangarei", "Invercargill", "Nelson", "Hastings", "Gisborne", "Timaru", "Taupo", "Whanganui", "Masterton", "Blenheim"],
        "Tier 3": ["Cambridge", "Queenstown", "Ashburton", "Oamaru", "Greymouth", "Wanganui", "Levin", "Feilding", "Tokoroa", "Hawera"]
    },
    "Ireland": {
        "Tier 1": ["Dublin", "Cork", "Limerick", "Galway", "Waterford", "Drogheda", "Kilkenny", "Wexford", "Sligo", "Clonmel"],
        "Tier 2": ["Dundalk", "Bray", "Ennis", "Tralee", "Carlow", "Naas", "Athlone", "Letterkenny", "Tullamore", "Mullingar"],
        "Tier 3": ["Celbridge", "Killarney", "Arklow", "Cobh", "Castlebar", "Midleton", "Mallow", "Ballina", "Thurles", "Newbridge"]
    },
    "Sweden": {
        "Tier 1": ["Stockholm", "Gothenburg", "Malmö", "Uppsala", "Västerås", "Örebro", "Linköping", "Helsingborg", "Jönköping", "Norrköping"],
        "Tier 2": ["Lund", "Umeå", "Gävle", "Borås", "Eskilstuna", "Södertälje", "Karlstad", "Halmstad", "Växjö", "Sundsvall"],
        "Tier 3": ["Luleå", "Trollhättan", "Östersund", "Borlänge", "Falun", "Kalmar", "Kristianstad", "Skellefteå", "Hudiksvall", "Motala"]
    },
    "Norway": {
        "Tier 1": ["Oslo", "Bergen", "Trondheim", "Stavanger", "Bærum", "Kristiansand", "Fredrikstad", "Sandnes", "Tromsø", "Sarpsborg"],
        "Tier 2": ["Skien", "Ålesund", "Sandefjord", "Haugesund", "Tønsberg", "Moss", "Porsgrunn", "Arendal", "Bodø", "Hamar"],
        "Tier 3": ["Ytrebygda", "Larvik", "Halden", "Harstad", "Lillehammer", "Molde", "Kongsberg", "Gjøvik", "Horten", "Mo i Rana"]
    },
    "Denmark": {
        "Tier 1": ["Copenhagen", "Aarhus", "Odense", "Aalborg", "Esbjerg", "Randers", "Kolding", "Horsens", "Vejle", "Roskilde"],
        "Tier 2": ["Herning", "Helsingør", "Silkeborg", "Næstved", "Fredericia", "Køge", "Holstebro", "Taastrup", "Slagelse", "Hillerød"],
        "Tier 3": ["Sønderborg", "Svendborg", "Holbæk", "Hjørring", "Frederikshavn", "Nykøbing Falster", "Ringsted", "Viborg", "Thisted", "Kalundborg"]
    },
    "Finland": {
        "Tier 1": ["Helsinki", "Espoo", "Tampere", "Vantaa", "Oulu", "Turku", "Jyväskylä", "Lahti", "Kuopio", "Pori"],
        "Tier 2": ["Kouvola", "Joensuu", "Lappeenranta", "Hämeenlinna", "Vaasa", "Seinäjoki", "Mikkeli", "Kotka", "Hyvinkää", "Järvenpää"],
        "Tier 3": ["Nurmijärvi", "Lohja", "Porvoo", "Kokkola", "Rovaniemi", "Tuusula", "Kirkkonummi", "Rauma", "Kemi", "Salo"]
    },
    "Poland": {
        "Tier 1": ["Warsaw", "Kraków", "Łódź", "Wrocław", "Poznań", "Gdańsk", "Szczecin", "Bydgoszcz", "Lublin", "Katowice"],
        "Tier 2": ["Białystok", "Gdynia", "Częstochowa", "Radom", "Sosnowiec", "Toruń", "Kielce", "Gliwice", "Zabrze", "Bytom"],
        "Tier 3": ["Olsztyn", "Bielsko-Biała", "Rzeszów", "Ruda Śląska", "Rybnik", "Tychy", "Dąbrowa Górnicza", "Płock", "Elbląg", "Opole"]
    },
    "Belgium": {
        "Tier 1": ["Brussels", "Antwerp", "Ghent", "Charleroi", "Liège", "Bruges", "Namur", "Leuven", "Mons", "Aalst"],
        "Tier 2": ["Mechelen", "La Louvière", "Kortrijk", "Hasselt", "Ostend", "Sint-Niklaas", "Tournai", "Genk", "Seraing", "Roeselare"],
        "Tier 3": ["Verviers", "Mouscron", "Beveren", "Dendermonde", "Beringen", "Turnhout", "Dilbeek", "Heist-op-den-Berg", "Sint-Truiden", "Lokeren"]
    },
    "Switzerland": {
        "Tier 1": ["Zurich", "Geneva", "Basel", "Bern", "Lausanne", "Winterthur", "St. Gallen", "Lucerne", "Lugano", "Biel"],
        "Tier 2": ["Thun", "Köniz", "La Chaux-de-Fonds", "Schaffhausen", "Fribourg", "Chur", "Neuchâtel", "Vernier", "Uster", "Sitten"],
        "Tier 3": ["Lancy", "Emmen", "Kriens", "Rapperswil-Jona", "Dübendorf", "Dietikon", "Montreux", "Wil", "Zug", "Frauenfeld"]
    },
    "Austria": {
        "Tier 1": ["Vienna", "Graz", "Linz", "Salzburg", "Innsbruck", "Klagenfurt", "Villach", "Wels", "Sankt Pölten", "Dornbirn"],
        "Tier 2": ["Steyr", "Wiener Neustadt", "Feldkirch", "Bregenz", "Leonding", "Klosterneuburg", "Baden", "Wolfsberg", "Leoben", "Traun"],
        "Tier 3": ["Amstetten", "Kapfenberg", "Hallein", "Kufstein", "Traiskirchen", "Schwechat", "Braunau am Inn", "Spittal an der Drau", "Ternitz", "Mödling"]
    },
    "Portugal": {
        "Tier 1": ["Lisbon", "Porto", "Amadora", "Braga", "Setúbal", "Coimbra", "Queluz", "Funchal", "Cacém", "Vila Nova de Gaia"],
        "Tier 2": ["Loures", "Felgueiras", "Évora", "Rio de Mouro", "Odivelas", "Aveiro", "Corroios", "Barreiro", "Montijo", "Agualva-Cacém"],
        "Tier 3": ["Rio Tinto", "Santarém", "Matosinhos", "Gondomar", "Guimarães", "Leiria", "Faro", "Viseu", "Póvoa de Varzim", "Vila do Conde"]
    },
    "Greece": {
        "Tier 1": ["Athens", "Thessaloniki", "Patras", "Piraeus", "Larissa", "Heraklion", "Peristeri", "Kallithea", "Acharnes", "Kalamaria"],
        "Tier 2": ["Nikaia", "Glyfada", "Volos", "Ilio", "Ilioupoli", "Keratsini", "Evosmos", "Chalandri", "Nea Smyrni", "Marousi"],
        "Tier 3": ["Zografou", "Egaleo", "Nea Ionia", "Ioannina", "Palaio Faliro", "Korydallos", "Trikala", "Vyronas", "Agia Paraskevi", "Galatsi"]
    },
    "Turkey": {
        "Tier 1": ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", "Adana", "Gaziantep", "Konya", "Kayseri", "Mersin"],
        "Tier 2": ["Eskişehir", "Diyarbakır", "Şanlıurfa", "Samsun", "Denizli", "Kahramanmaraş", "Van", "Batman", "Elazığ", "Erzurum"],
        "Tier 3": ["Malatya", "Trabzon", "Manisa", "Sivas", "Gebze", "Balıkesir", "Tarsus", "Kütahya", "Çorum", "Osmaniye"]
    },
    "Russia": {
        "Tier 1": ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan", "Nizhny Novgorod", "Chelyabinsk", "Samara", "Omsk", "Rostov-on-Don"],
        "Tier 2": ["Ufa", "Krasnoyarsk", "Voronezh", "Perm", "Volgograd", "Krasnodar", "Saratov", "Tyumen", "Izhevsk", "Barnaul"],
        "Tier 3": ["Ulyanovsk", "Irkutsk", "Khabarovsk", "Yaroslavl", "Vladivostok", "Makhachkala", "Tomsk", "Orenburg", "Kemerovo", "Novokuznetsk"]
    },
    "China": {
        "Tier 1": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu", "Hangzhou", "Wuhan", "Xi'an", "Nanjing", "Tianjin"],
        "Tier 2": ["Suzhou", "Dongguan", "Chongqing", "Shenyang", "Qingdao", "Zhengzhou", "Dalian", "Changsha", "Kunming", "Foshan"],
        "Tier 3": ["Harbin", "Jinan", "Fuzhou", "Shijiazhuang", "Xiamen", "Hefei", "Changchun", "Ningbo", "Nanchang", "Taiyuan"]
    },
    "Hong Kong": {
        "Tier 1": ["Hong Kong", "Kowloon", "Tsuen Wan", "Yuen Long", "Sha Tin", "Tuen Mun", "Tai Po", "Sai Kung", "Islands District", "North District"],
        "Tier 2": ["Wong Tai Sin", "Kwun Tong", "Sham Shui Po", "Yau Tsim Mong", "Central and Western", "Wan Chai", "Eastern", "Southern"],
        "Tier 3": ["Aberdeen", "Stanley", "Repulse Bay", "Discovery Bay", "Tung Chung", "Ma On Shan", "Fanling", "Sheung Shui", "Tin Shui Wai", "Tsing Yi"]
    },
    "Taiwan": {
        "Tier 1": ["Taipei", "Kaohsiung", "Taichung", "Tainan", "Hsinchu", "Keelung", "Chiayi", "Taoyuan", "Changhua", "Pingtung"],
        "Tier 2": ["Hualien", "Taitung", "Yilan", "Miaoli", "Nantou", "Yunlin", "Chiayi County", "Penghu", "Kinmen", "Lienchiang"],
        "Tier 3": ["Banqiao", "Zhonghe", "Yonghe", "Xinzhuang", "Sanchong", "Xindian", "Tucheng", "Shulin", "Yingge", "Danshui"]
    },
    "Thailand": {
        "Tier 1": ["Bangkok", "Nonthaburi", "Chiang Mai", "Hat Yai", "Pak Kret", "Nakhon Ratchasima", "Udon Thani", "Chon Buri", "Khon Kaen", "Ubon Ratchathani"],
        "Tier 2": ["Nakhon Si Thammarat", "Rayong", "Phuket", "Surat Thani", "Nakhon Sawan", "Lampang", "Ratchaburi", "Kanchanaburi", "Saraburi", "Pattaya"],
        "Tier 3": ["Ayutthaya", "Chiang Rai", "Nong Khai", "Mukdahan", "Trat", "Prachuap Khiri Khan", "Hua Hin", "Krabi", "Phitsanulok", "Sukhothai"]
    },
    "Malaysia": {
        "Tier 1": ["Kuala Lumpur", "George Town", "Ipoh", "Shah Alam", "Petaling Jaya", "Subang Jaya", "Kota Kinabalu", "Kuching", "Johor Bahru", "Malacca"],
        "Tier 2": ["Alor Setar", "Miri", "Kota Bharu", "Seremban", "Kuantan", "Tawau", "Sandakan", "Kuala Terengganu", "Sibu", "Taiping"],
        "Tier 3": ["Kulim", "Batu Pahat", "Muar", "Klang", "Butterworth", "Kangar", "Teluk Intan", "Temerloh", "Bentong", "Raub"]
    },
    "Indonesia": {
        "Tier 1": ["Jakarta", "Surabaya", "Bandung", "Medan", "Semarang", "Palembang", "Makassar", "Tangerang", "Depok", "Bekasi"],
        "Tier 2": ["South Tangerang", "Batam", "Bogor", "Pekanbaru", "Padang", "Malang", "Denpasar", "Bandar Lampung", "Pontianak", "Balikpapan"],
        "Tier 3": ["Jambi", "Manado", "Cimahi", "Mataram", "Palu", "Kupang", "Banjarmasin", "Yogyakarta", "Surakarta", "Cirebon"]
    },
    "Philippines": {
        "Tier 1": ["Manila", "Quezon City", "Caloocan", "Davao City", "Cebu City", "Zamboanga City", "Antipolo", "Pasig", "Taguig", "Valenzuela"],
        "Tier 2": ["Cagayan de Oro", "Parañaque", "Las Piñas", "Makati", "Bacolod", "General Santos", "Mandaluyong", "Muntinlupa", "San Jose del Monte", "Bacoor"],
        "Tier 3": ["Lapu-Lapu", "Marikina", "Muntinlupa", "San Pedro", "Butuan", "Iloilo City", "Cabuyao", "Dasmariñas", "Calamba", "Malabon"]
    },
    "Vietnam": {
        "Tier 1": ["Ho Chi Minh City", "Hanoi", "Da Nang", "Haiphong", "Can Tho", "Bien Hoa", "Hue", "Nha Trang", "Vung Tau", "Quy Nhon"],
        "Tier 2": ["Rach Gia", "Long Xuyen", "Cam Ranh", "Phan Thiet", "My Tho", "Ca Mau", "Bac Lieu", "Soc Trang", "Tan An", "Tra Vinh"],
        "Tier 3": ["Vinh", "Thai Nguyen", "Nam Dinh", "Thanh Hoa", "Pleiku", "Buon Ma Thuot", "Dong Hoi", "Tam Ky", "Kon Tum", "Lao Cai"]
    },
    "Saudi Arabia": {
        "Tier 1": ["Riyadh", "Jeddah", "Mecca", "Medina", "Dammam", "Khobar", "Taif", "Abha", "Tabuk", "Buraydah"],
        "Tier 2": ["Khamis Mushait", "Hail", "Najran", "Jazan", "Yanbu", "Al Jubail", "Dhahran", "Arar", "Sakaka", "Jizan"],
        "Tier 3": ["Qatif", "Unaizah", "Al Kharj", "Al Qatif", "Al Bahah", "Ar Rass", "Al Mubarraz", "Al Khafji", "Al Qurayyat", "Al Wajh"]
    },
    "Israel": {
        "Tier 1": ["Jerusalem", "Tel Aviv", "Haifa", "Rishon LeZion", "Petah Tikva", "Ashdod", "Netanya", "Beer Sheva", "Bnei Brak", "Holon"],
        "Tier 2": ["Ramat Gan", "Rehovot", "Bat Yam", "Ashkelon", "Herzliya", "Kfar Saba", "Hadera", "Modiin", "Nazareth", "Lod"],
        "Tier 3": ["Ra'anana", "Givatayim", "Kiryat Ata", "Eilat", "Ramat HaSharon", "Nahariya", "Kiryat Gat", "Acre", "Kiryat Bialik", "Tiberias"]
    },
    "Egypt": {
        "Tier 1": ["Cairo", "Alexandria", "Giza", "Shubra El Kheima", "Port Said", "Suez", "Luxor", "Mansoura", "El-Mahalla El-Kubra", "Tanta"],
        "Tier 2": ["Asyut", "Ismailia", "Faiyum", "Zagazig", "Aswan", "Damietta", "Damanhur", "Minya", "Beni Suef", "Qena"],
        "Tier 3": ["Sohag", "Hurghada", "Sharm El Sheikh", "Kafr el-Sheikh", "Arish", "Mallawi", "Bilbays", "Marsa Matruh", "Idku", "Rosetta"]
    },
    "Nigeria": {
        "Tier 1": ["Lagos", "Kano", "Ibadan", "Abuja", "Port Harcourt", "Benin City", "Kaduna", "Aba", "Maiduguri", "Ilorin"],
        "Tier 2": ["Warri", "Onitsha", "Abeokuta", "Enugu", "Zaria", "Jos", "Calabar", "Akure", "Owerri", "Uyo"],
        "Tier 3": ["Sokoto", "Bauchi", "Gombe", "Katsina", "Minna", "Makurdi", "Ado-Ekiti", "Ogbomoso", "Osogbo", "Ilesa"]
    },
    "Kenya": {
        "Tier 1": ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Malindi", "Kitale", "Garissa", "Kakamega"],
        "Tier 2": ["Ruiru", "Machakos", "Nyeri", "Meru", "Naivasha", "Kilifi", "Kericho", "Lamu", "Narok", "Embu"],
        "Tier 3": ["Athi River", "Voi", "Bungoma", "Busia", "Homa Bay", "Kitui", "Marsabit", "Mandera", "Wajir", "Isiolo"]
    },
    "Chile": {
        "Tier 1": ["Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta", "Temuco", "Rancagua", "Talca", "Arica", "Iquique"],
        "Tier 2": ["Puerto Montt", "Coquimbo", "Valdivia", "Osorno", "Chillán", "Calama", "Los Ángeles", "Punta Arenas", "Copiapó", "Curicó"],
        "Tier 3": ["Ovalle", "Quillota", "San Antonio", "Linares", "San Felipe", "Villa Alemana", "Coronel", "Melipilla", "Angol", "San Fernando"]
    },
    "Colombia": {
        "Tier 1": ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Cúcuta", "Bucaramanga", "Pereira", "Santa Marta", "Ibagué"],
        "Tier 2": ["Manizales", "Pasto", "Neiva", "Villavicencio", "Armenia", "Valledupar", "Montería", "Sincelejo", "Popayán", "Tunja"],
        "Tier 3": ["Riohacha", "Quibdó", "Florencia", "Yopal", "Mocoa", "Leticia", "San Andrés", "Providencia", "Arauca", "Mitú"]
    },
    "Peru": {
        "Tier 1": ["Lima", "Arequipa", "Trujillo", "Chiclayo", "Piura", "Iquitos", "Cusco", "Chimbote", "Huancayo", "Pucallpa"],
        "Tier 2": ["Tacna", "Ica", "Juliaca", "Sullana", "Cajamarca", "Chincha Alta", "Ayacucho", "Huánuco", "Tarapoto", "Puno"],
        "Tier 3": ["Tumbes", "Talara", "Huaraz", "Moquegua", "Cerro de Pasco", "Abancay", "Tingo María", "Jaén", "Chachapoyas", "Moyobamba"]
    },
    "Venezuela": {
        "Tier 1": ["Caracas", "Maracaibo", "Valencia", "Barquisimeto", "Ciudad Guayana", "Maturín", "Barcelona", "Maracay", "Ciudad Bolívar", "San Cristóbal"],
        "Tier 2": ["Puerto La Cruz", "Barinas", "Mérida", "Cumaná", "Cabimas", "Punto Fijo", "Guanare", "Carúpano", "Los Teques", "Acarigua"],
        "Tier 3": ["Puerto Cabello", "Valera", "Coro", "Calabozo", "Guanare", "El Tigre", "Ocumare del Tuy", "Carora", "Anaco", "Porlamar"]
    },
    "Ecuador": {
        "Tier 1": ["Quito", "Guayaquil", "Cuenca", "Santo Domingo", "Machala", "Durán", "Manta", "Portoviejo", "Loja", "Ambato"],
        "Tier 2": ["Esmeraldas", "Quevedo", "Riobamba", "Milagro", "Ibarra", "La Libertad", "Babahoyo", "Latacunga", "Tulcán", "Pasaje"],
        "Tier 3": ["Chone", "Montecristi", "Jipijapa", "Ventanas", "Naranjal", "El Carmen", "Pedernales", "Atacames", "Salinas", "Bahía de Caráquez"]
    },
    "Uruguay": {
        "Tier 1": ["Montevideo", "Salto", "Ciudad de la Costa", "Paysandú", "Las Piedras", "Rivera", "Maldonado", "Tacuarembó", "Melo", "Mercedes"],
        "Tier 2": ["Artigas", "Minas", "San José de Mayo", "Durazno", "Florida", "Treinta y Tres", "Rocha", "Fray Bentos", "Colonia del Sacramento", "Pando"],
        "Tier 3": ["Trinidad", "Canelones", "Carmelo", "Nueva Palmira", "Chuy", "La Paloma", "Piriápolis", "Punta del Este", "Atlántida", "Barros Blancos"]
    },
    "Costa Rica": {
        "Tier 1": ["San José", "Cartago", "Alajuela", "Heredia", "Liberia", "Puntarenas", "Limón", "San Isidro", "Quesada", "Desamparados"],
        "Tier 2": ["Curridabat", "San Francisco", "San Pedro", "Tibás", "Escazú", "Santa Ana", "San Rafael", "Moravia", "Goicoechea", "Sabanilla"],
        "Tier 3": ["Paraíso", "Turrialba", "Grecia", "Sarchí", "Palmares", "Naranjo", "Zarcero", "San Ramón", "Atenas", "Orotina"]
    },
    "Panama": {
        "Tier 1": ["Panama City", "San Miguelito", "Tocumen", "David", "Arraiján", "Colón", "Las Cumbres", "La Chorrera", "Pacora", "Santiago"],
        "Tier 2": ["Chitré", "Penonomé", "Aguadulce", "La Villa de Los Santos", "Pedregal", "Alcalde Díaz", "Juan Díaz", "Ancón", "Chilibre", "Chepo"],
        "Tier 3": ["Capira", "Chame", "San Carlos", "Antón", "Natá", "Parita", "Los Santos", "Las Tablas", "Guararé", "Macaracas"]
    },
    "Guatemala": {
        "Tier 1": ["Guatemala City", "Mixco", "Villa Nueva", "Quetzaltenango", "Escuintla", "San Juan Sacatepéquez", "Villa Canales", "Petapa", "Chinautla", "Chimaltenango"],
        "Tier 2": ["Chichicastenango", "Huehuetenango", "Cobán", "Jalapa", "Mazatenango", "Retalhuleu", "Zacapa", "Puerto Barrios", "Chiquimula", "Jutiapa"],
        "Tier 3": ["Totonicapán", "Sololá", "Antigua Guatemala", "Flores", "Panajachel", "San Pedro La Laguna", "Santiago Atitlán", "Livingston", "El Estor", "Poptún"]
    },
    "Czech Republic": {
        "Tier 1": ["Prague", "Brno", "Ostrava", "Plzeň", "Liberec", "Olomouc", "Ústí nad Labem", "Hradec Králové", "České Budějovice", "Pardubice"],
        "Tier 2": ["Zlín", "Havířov", "Kladno", "Most", "Opava", "Frýdek-Místek", "Karviná", "Jihlava", "Teplice", "Děčín"],
        "Tier 3": ["Chomutov", "Jablonec nad Nisou", "Mladá Boleslav", "Prostějov", "Přerov", "Třebíč", "Český Těšín", "Třinec", "Karlovy Vary", "Jindřichův Hradec"]
    },
    "Hungary": {
        "Tier 1": ["Budapest", "Debrecen", "Szeged", "Miskolc", "Pécs", "Győr", "Nyíregyháza", "Kecskemét", "Székesfehérvár", "Szombathely"],
        "Tier 2": ["Szolnok", "Tatabánya", "Kaposvár", "Békéscsaba", "Zalaegerszeg", "Érd", "Veszprém", "Sopron", "Baja", "Pápa"],
        "Tier 3": ["Szekszárd", "Eger", "Nagykanizsa", "Dunaújváros", "Hódmezővásárhely", "Salgótarján", "Szigetszentmiklós", "Ózd", "Szentendre", "Vác"]
    },
    "Romania": {
        "Tier 1": ["Bucharest", "Cluj-Napoca", "Timișoara", "Iași", "Constanța", "Craiova", "Brașov", "Galați", "Ploiești", "Oradea"],
        "Tier 2": ["Brăila", "Arad", "Pitești", "Sibiu", "Bacău", "Târgu Mureș", "Baia Mare", "Buzău", "Botoșani", "Satu Mare"],
        "Tier 3": ["Râmnicu Vâlcea", "Suceava", "Piatra Neamț", "Drobeta-Turnu Severin", "Focșani", "Târgoviște", "Tulcea", "Reșița", "Bistrița", "Slatina"]
    },
    "Ukraine": {
        "Tier 1": ["Kyiv", "Kharkiv", "Odesa", "Dnipro", "Donetsk", "Zaporizhzhia", "Lviv", "Kryvyi Rih", "Mykolaiv", "Mariupol"],
        "Tier 2": ["Luhansk", "Vinnytsia", "Sevastopol", "Simferopol", "Kherson", "Poltava", "Chernihiv", "Cherkasy", "Sumy", "Zhytomyr"],
        "Tier 3": ["Khmelnytskyi", "Rivne", "Ivano-Frankivsk", "Ternopil", "Lutsk", "Uzhhorod", "Chernivtsi", "Melitopol", "Kramatorsk", "Berdiansk"]
    },
    "Pakistan": {
        "Tier 1": ["Karachi", "Lahore", "Faisalabad", "Rawalpindi", "Multan", "Gujranwala", "Peshawar", "Quetta", "Islamabad", "Sargodha"],
        "Tier 2": ["Sialkot", "Bahawalpur", "Sukkur", "Jhang", "Sheikhupura", "Larkana", "Gujrat", "Kasur", "Mardan", "Mingaora"],
        "Tier 3": ["Nawabshah", "Chiniot", "Kotri", "Kāmoke", "Hafizabad", "Kohat", "Jacobabad", "Shikarpur", "Muzaffargarh", "Khanpur"]
    },
    "Bangladesh": {
        "Tier 1": ["Dhaka", "Chittagong", "Khulna", "Rajshahi", "Sylhet", "Comilla", "Rangpur", "Mymensingh", "Barisal", "Jessore"],
        "Tier 2": ["Narayanganj", "Gazipur", "Bogra", "Dinajpur", "Saidpur", "Cox's Bazar", "Tangail", "Jamalpur", "Pabna", "Naogaon"],
        "Tier 3": ["Kushtia", "Faridpur", "Gopalganj", "Madaripur", "Shariatpur", "Rajbari", "Manikganj", "Munshiganj", "Narsingdi", "Kishoreganj"]
    },
    "Sri Lanka": {
        "Tier 1": ["Colombo", "Kandy", "Galle", "Jaffna", "Negombo", "Trincomalee", "Batticaloa", "Ratnapura", "Matara", "Kalutara"],
        "Tier 2": ["Anuradhapura", "Badulla", "Kurunegala", "Polonnaruwa", "Chilaw", "Panadura", "Moratuwa", "Kegalle", "Hambantota", "Point Pedro"],
        "Tier 3": ["Nuwara Eliya", "Bandarawela", "Dambulla", "Sigiriya", "Ella", "Mirissa", "Unawatuna", "Hikkaduwa", "Bentota", "Weligama"]
    }
}


def get_cities_for_country(country_name: str) -> Optional[Dict[str, List[str]]]:
    """Get tiered cities for a country"""
    return CITIES.get(country_name)


def get_all_cities_for_country(country_name: str) -> List[str]:
    """Get all cities for a country as a flat list, organized by tier"""
    cities_data = get_cities_for_country(country_name)
    if not cities_data:
        return []
    
    # Return cities in tier order: Tier 1, Tier 2, Tier 3
    all_cities = []
    for tier in ["Tier 1", "Tier 2", "Tier 3"]:
        if tier in cities_data:
            all_cities.extend(cities_data[tier])
    return all_cities


def get_cities_by_tier(country_name: str) -> Dict[str, List[str]]:
    """Get cities organized by tier for a country"""
    cities_data = get_cities_for_country(country_name)
    if not cities_data:
        return {"Tier 1": [], "Tier 2": [], "Tier 3": []}
    return cities_data