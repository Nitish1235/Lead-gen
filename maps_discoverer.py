"""
Google Maps business discovery module with country-aware search
"""
import time
import re
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urlencode
import config
from countries import get_google_domain
from website_analyzer import WebsiteAnalyzer


class MapsDiscoverer:
    """Discovers businesses from Google Maps with country-aware search"""
    
    def __init__(self, country: str):
        self.country = country
        self.google_domain = get_google_domain(country)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        self.website_analyzer = WebsiteAnalyzer()
    
    def should_exclude(self, business_name: str, website: Optional[str] = None) -> bool:
        """Check if business should be excluded based on name/website"""
        name_lower = business_name.lower()
        website_lower = (website or "").lower()
        
        combined = f"{name_lower} {website_lower}"
        
        for term in config.EXCLUDED_TERMS:
            if term in combined:
                return True
        
        return False
    
    def search_businesses(
        self,
        category: str,
        city: str,
        max_results: int = 20,
        use_selenium: bool = False
    ) -> List[Dict]:
        """
        Search for businesses on Google Maps
        
        Args:
            category: Business category (e.g., "dental clinic")
            city: City name
            max_results: Maximum number of results to return
            use_selenium: Use Selenium for more reliable scraping (slower)
            
        Returns:
            List of business dictionaries
        """
        if use_selenium:
            return self._search_with_selenium(category, city, max_results)
        else:
            # HTML scraping is unreliable - recommend using Places API
            print("Note: HTML scraping is unreliable. Consider using Google Places API.")
            print("      Set GOOGLE_MAPS_API_KEY in config or use Selenium (slower but more reliable).")
            return []
    
    def _search_with_selenium(
        self,
        category: str,
        city: str,
        max_results: int = 20
    ) -> List[Dict]:
        """
        Search using Selenium (more reliable but slower)
        
        Args:
            category: Business category
            city: City name
            max_results: Maximum results
            
        Returns:
            List of business dictionaries
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
        except ImportError:
            print("Selenium not available. Install with: pip install selenium webdriver-manager")
            return []
        
        query = f"{category} in {city}"
        search_url = f"https://www.{self.google_domain}/maps/search/{quote(query)}"
        
        businesses = []
        driver = None
        
        try:
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in background
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Initialize driver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Navigate to search
            driver.get(search_url)
            
            # Wait for results to load
            time.sleep(5)  # Give maps time to load
            
            # Extract business listings
            # Google Maps class names change frequently, this is a general approach
            try:
                # Try to find business cards
                business_elements = driver.find_elements(By.CSS_SELECTOR, '[role="article"]')
                
                for element in business_elements[:max_results]:
                    try:
                        business = {}
                        
                        # Extract name
                        name_elem = element.find_element(By.CSS_SELECTOR, '[class*="fontHeadlineSmall"]')
                        business["name"] = name_elem.text.strip() if name_elem else ""
                        
                        # Click to get details (phone, address, website)
                        element.click()
                        time.sleep(2)
                        
                        # Extract details from side panel
                        try:
                            # Phone
                            phone_elem = driver.find_element(By.CSS_SELECTOR, '[data-item-id*="phone"]')
                            business["phone"] = phone_elem.text.strip() if phone_elem else ""
                        except:
                            business["phone"] = ""
                        
                        try:
                            # Address
                            address_elem = driver.find_element(By.CSS_SELECTOR, '[data-item-id*="address"]')
                            business["address"] = address_elem.text.strip() if address_elem else ""
                        except:
                            business["address"] = ""
                        
                        try:
                            # Website
                            website_elem = driver.find_element(By.CSS_SELECTOR, '[data-item-id*="authority"]')
                            business["website"] = website_elem.get_attribute("href") if website_elem else ""
                        except:
                            business["website"] = ""
                        
                        try:
                            # Rating
                            rating_elem = driver.find_element(By.CSS_SELECTOR, '[class*="fontDisplayLarge"]')
                            business["rating"] = float(rating_elem.text.strip()) if rating_elem else None
                        except:
                            business["rating"] = None
                        
                        if business.get("name"):
                            businesses.append(business)
                        
                        # Go back to results
                        driver.back()
                        time.sleep(1)
                        
                    except Exception as e:
                        print(f"  Error extracting business details: {e}")
                        continue
                
            except Exception as e:
                print(f"Error finding business elements: {e}")
            
            # Filter excluded businesses
            filtered_businesses = []
            for business in businesses:
                if not self.should_exclude(
                    business.get("name", ""),
                    business.get("website")
                ):
                    filtered_businesses.append(business)
            
            return filtered_businesses
            
        except Exception as e:
            print(f"Error with Selenium search: {e}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def search_with_places_api(
        self,
        category: str,
        city: str,
        api_key: str,
        max_results: int = 20
    ) -> List[Dict]:
        """
        Search using Google Places API Text Search (Legacy)
        
        Official API Documentation:
        https://developers.google.com/maps/documentation/places/web-service/legacy/search-text
        
        Args:
            category: Business category
            city: City name
            api_key: Google Places API key
            max_results: Maximum results (max 60, 20 per page)
            
        Returns:
            List of business dictionaries with fields:
            - name, address, rating, review_count, types, business_status, place_id
            - phone, website, email (from Place Details API if available)
        """
        if not api_key:
            print("Error: Google Places API key not provided")
            return []
        
        businesses = []
        
        try:
            # Build search query per official docs
            # Format: "business type in city, country"
            query = f"{category} in {city}, {self.country}"
            
            # Text Search API endpoint (Legacy)
            # Official endpoint: https://maps.googleapis.com/maps/api/place/textsearch/json
            search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            
            # Required parameters per official docs:
            # - query: The text string on which to search
            # - key: Your API key
            # Optional: type, location, radius, language, etc.
            params = {
                "query": query,
                "key": api_key,
            }
            
            # Make request
            print(f"      API Request: {query}")
            response = self.session.get(search_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Check response status per official docs
            status = data.get("status")
            if status != "OK":
                error_msg = data.get("error_message", "Unknown error")
                print(f"      Places API Text Search error: {status}")
                if error_msg:
                    print(f"      Error message: {error_msg}")
                
                # Handle specific error codes per official docs
                if status == "ZERO_RESULTS":
                    print(f"      No results found for query: {query}")
                elif status == "INVALID_REQUEST":
                    print(f"      Invalid request - check query format")
                elif status == "OVER_QUERY_LIMIT":
                    print(f"      Over query limit - check billing/quota")
                elif status == "REQUEST_DENIED":
                    print(f"      Request denied - check API key and permissions")
                
                return []
            
            # Extract results array per official docs
            # Response format: { "html_attributions": [], "results": [...], "status": "OK" }
            results = data.get("results", [])
            
            if not results:
                print(f"      No results in response")
                return []
            
            print(f"      Found {len(results)} results from API")
            
            # Process each place result (max_results limit)
            for idx, place in enumerate(results[:max_results], 1):
                try:
                    # Extract place_id (required for Place Details)
                    place_id = place.get("place_id")
                    if not place_id:
                        print(f"      [{idx}] Skipping: No place_id")
                        continue
                    
                    # Extract data from Text Search response per official docs
                    # Text Search returns: name, formatted_address, rating, user_ratings_total,
                    # place_id, business_status, types, geometry, etc.
                    business_name = place.get("name", "").strip()
                    if not business_name:
                        print(f"      [{idx}] Skipping: No name")
                        continue
                    
                    # Check if should exclude
                    if self.should_exclude(business_name):
                        print(f"      [{idx}] Excluded: {business_name}")
                        continue
                    
                    # Build business dict from Text Search data
                    business = {
                        "name": business_name,
                        "address": place.get("formatted_address", "").strip(),
                        "rating": place.get("rating"),  # Optional: 1.0 to 5.0
                        "review_count": place.get("user_ratings_total", 0),  # Optional: total reviews
                        "types": place.get("types", []),  # Array of place types
                        "business_status": place.get("business_status", "OPERATIONAL"),  # OPERATIONAL, CLOSED_TEMPORARILY, CLOSED_PERMANENTLY
                        "place_id": place_id,
                    }
                    
                    # Get additional details (phone, website) from Place Details API
                    # This is optional - we can still use the business without these
                    details = self._get_place_details(place_id, api_key)
                    if details:
                        business["phone"] = details.get("phone", "")
                        business["website"] = details.get("website", "")
                        business["email"] = details.get("email", "")
                    else:
                        # No details available - still use the business
                        business["phone"] = ""
                        business["website"] = ""
                        business["email"] = ""
                    
                    businesses.append(business)
                    print(f"      [{idx}] ✓ {business_name} (Rating: {business.get('rating', 'N/A')}, Reviews: {business.get('review_count', 0)})")
                    
                    # Rate limiting between requests
                    if idx < len(results[:max_results]):
                        time.sleep(config.DEFAULT_DELAY_BETWEEN_REQUESTS)
                    
                except Exception as e:
                    print(f"      [{idx}] Error processing place: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            print(f"      Successfully processed {len(businesses)} businesses")
            return businesses
            
        except requests.exceptions.RequestException as e:
            print(f"      Network error in Places API: {e}")
            return []
        except Exception as e:
            print(f"      Unexpected error in Places API: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_place_details(self, place_id: str, api_key: str) -> Optional[Dict]:
        """
        Get detailed information for a place using Place Details API (Legacy)
        
        Official API Documentation:
        https://developers.google.com/maps/documentation/places/web-service/legacy/details
        
        Args:
            place_id: Place ID from Text Search response
            api_key: Google Places API key
            
        Returns:
            Dict with phone, website, email (or None if failed)
        """
        try:
            # Place Details API endpoint (Legacy)
            # Official endpoint: https://maps.googleapis.com/maps/api/place/details/json
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            
            # Required parameters per official docs:
            # - place_id: The place_id from Text Search
            # - key: Your API key
            # - fields: Comma-separated list of fields to return (optional but recommended for cost control)
            params = {
                "place_id": place_id,
                "key": api_key,
                "fields": "formatted_phone_number,website"  # Only get what we need to save costs
            }
            
            response = self.session.get(details_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Check response status per official docs
            status = data.get("status")
            if status != "OK":
                # Don't print error for missing details - it's optional
                # Many places don't have phone/website in the database
                return None
            
            # Extract result object per official docs
            # Response format: { "html_attributions": [], "result": {...}, "status": "OK" }
            result = data.get("result", {})
            if not result:
                return None
            
            # Extract phone and website per official docs
            # formatted_phone_number: Contains the place's phone number in its local format
            # website: The authoritative website for this place
            details = {
                "phone": result.get("formatted_phone_number", "").strip(),
                "website": result.get("website", "").strip(),
            }
            
            # Extract email from website if available (not from API, we scrape it)
            if details.get("website"):
                try:
                    website_response = self.website_analyzer.session.get(
                        details["website"], 
                        timeout=5,
                        allow_redirects=True
                    )
                    website_response.raise_for_status()
                    email = self.website_analyzer.extract_email(website_response.text)
                    details["email"] = email if email else ""
                except Exception as e:
                    # Silently fail - email extraction is optional
                    details["email"] = ""
            else:
                details["email"] = ""
            
            return details
            
        except requests.exceptions.RequestException as e:
            # Network error - silently fail (details are optional)
            return None
        except Exception as e:
            # Other errors - silently fail (details are optional)
            return None

