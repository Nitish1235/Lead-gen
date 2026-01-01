"""
Main application for B2B Lead Discovery System
Manual start/stop control with sequential execution
"""
import os
import sys
import time
import signal
from datetime import datetime
from typing import List, Optional
import uuid
import config
from countries import list_all_countries, search_countries, get_country_config
from sheets_manager import SheetsManager
from maps_discoverer import MapsDiscoverer
from lead_scorer import LeadScorer
from website_analyzer import WebsiteAnalyzer
from website_analyzer import WebsiteAnalyzer


class LeadDiscoveryApp:
    """Main application class for lead discovery"""
    
    def __init__(self, lead_callback=None):
        self.sheets_manager = SheetsManager()
        self.lead_scorer = LeadScorer()
        self.website_analyzer = WebsiteAnalyzer()
        self.is_running = False
        self.should_stop = False
        self.run_id = str(uuid.uuid4())[:8]
        self.current_country = None
        self.current_city = None
        self.current_category = None
        self.lead_callback = lead_callback  # Callback function for when leads are found
        
        # Register signal handlers for graceful shutdown
        try:
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
        except (ValueError, OSError):
            # Signal handlers don't work in some environments (e.g., Streamlit)
            pass
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals"""
        print("\n\nStop signal received. Stopping gracefully...")
        self.should_stop = True
        self.is_running = False
    
    def start(
        self,
        country: str,
        city: str,
        categories: Optional[List[str]] = None,
        long_running: bool = False,
        max_hours: int = 24
    ):
        """
        Start lead discovery process
        
        Args:
            country: Country name
            city: City name
            categories: List of categories to search (default: all)
            long_running: Whether to run for extended period
            max_hours: Maximum hours to run (for long_running mode)
        """
        if self.is_running:
            print("Discovery already running. Stop it first.")
            return
        
        # Validate country
        country_config = get_country_config(country)
        if not country_config:
            print(f"Error: Country '{country}' not found.")
            print(f"Available countries: {', '.join(list_all_countries()[:10])}...")
            return
        
        self.current_country = country
        self.current_city = city
        self.is_running = True
        self.should_stop = False
        
        # Use default categories if none provided
        if categories is None:
            categories = config.DEFAULT_CATEGORIES
        
        print(f"\n{'='*60}")
        print(f"B2B Lead Discovery Started")
        print(f"{'='*60}")
        print(f"Run ID: {self.run_id}")
        print(f"Country: {country}")
        print(f"City: {city}")
        print(f"Categories: {len(categories)}")
        print(f"Mode: {'Long-running' if long_running else 'Standard'}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        max_seconds = max_hours * 3600 if long_running else None
        
        try:
            total_leads_found = 0
            
            for category_idx, category in enumerate(categories, 1):
                if self.should_stop:
                    print("\nStopping as requested...")
                    break
                
                # Check time limit for long-running mode
                if max_seconds and (time.time() - start_time) > max_seconds:
                    print(f"\nMaximum time limit ({max_hours} hours) reached.")
                    break
                
                self.current_category = category
                
                print(f"\n[{category_idx}/{len(categories)}] Searching: {category}")
                print(f"Location: {city}, {country}")
                print("-" * 60)
                
                # Discover businesses
                leads = self._discover_category_leads(country, city, category)
                
                if leads:
                    print(f"Found {len(leads)} leads for '{category}'")
                    total_leads_found += len(leads)
                else:
                    print(f"No leads found for '{category}'")
                
                # Delay between categories (except for last one)
                if category_idx < len(categories) and not self.should_stop:
                    print(f"\nWaiting {config.DEFAULT_DELAY_BETWEEN_SEARCHES} seconds before next category...")
                    time.sleep(config.DEFAULT_DELAY_BETWEEN_SEARCHES)
            
            print(f"\n{'='*60}")
            print(f"Discovery Complete")
            print(f"Total leads found: {total_leads_found}")
            print(f"Run ID: {self.run_id}")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"\nError during discovery: {e}")
            import traceback
            traceback.print_exc()
        
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            self.is_running = False
            self.should_stop = False
        except Exception as e:
            print(f"\nError during discovery: {e}")
            self.is_running = False
            self.should_stop = False
        finally:
            self.is_running = False
            self.should_stop = False
    
    def _discover_category_leads(self, country: str, city: str, category: str) -> List[dict]:
        """Discover and process leads for a category"""
        try:
            # Initialize discoverer
            discoverer = MapsDiscoverer(country)
            
            # Search for businesses
            print(f"Searching Google Maps...")
            
            # Try Places API first if key is available
            api_key = config.GOOGLE_MAPS_API_KEY
            if api_key:
                businesses = discoverer.search_with_places_api(
                    category, city, api_key,
                    max_results=config.MAX_RESULTS_PER_CATEGORY
                )
            else:
                # Fallback to HTML scraping (less reliable)
                print("Note: Using HTML scraping. Consider using Google Places API for better results.")
                businesses = discoverer.search_businesses(
                    category, city,
                    max_results=config.MAX_RESULTS_PER_CATEGORY
                )
            
            if not businesses:
                return []
            
            print(f"Found {len(businesses)} businesses, evaluating...")
            
            # Process each business into a lead
            leads = []
            for idx, business in enumerate(businesses, 1):
                if self.should_stop:
                    break
                
                print(f"  [{idx}/{len(businesses)}] Processing: {business.get('name', 'Unknown')}")
                
                lead = self._process_business_to_lead(business, country, city, category)
                
                if lead:
                    # Check for duplicates
                    is_duplicate = self.sheets_manager.check_duplicate(
                        lead.get("phone"),
                        lead.get("website")
                    )
                    
                    if not is_duplicate:
                        # Append to sheet immediately (append-only)
                        success = self.sheets_manager.append_lead(lead)
                        if success:
                            leads.append(lead)
                            print(f"    ✓ Saved (Score: {lead.get('lead_score', 0)})")
                            # Call callback if provided (for UI updates)
                            if self.lead_callback:
                                try:
                                    self.lead_callback(lead)
                                except Exception as e:
                                    print(f"      Warning: Callback error: {e}")
                        else:
                            print(f"    ✗ Failed to save")
                    else:
                        print(f"    ⊘ Duplicate (skipped)")
                
                # Human-like delay between businesses
                if idx < len(businesses) and not self.should_stop:
                    time.sleep(config.DEFAULT_DELAY_BETWEEN_REQUESTS)
            
            return leads
            
        except Exception as e:
            print(f"Error discovering leads for {category}: {e}")
            return []
    
    def _process_business_to_lead(
        self,
        business: dict,
        country: str,
        city: str,
        category: str
    ) -> Optional[dict]:
        """Convert a business dictionary to a lead dictionary"""
        try:
            name = business.get("name", "").strip()
            if not name:
                return None
            
            phone = business.get("phone", "").strip()
            email = business.get("email", "").strip()
            website = business.get("website", "").strip()
            address = business.get("address", "").strip()
            rating = business.get("rating")
            review_count = business.get("review_count", 0)
            
            # Get website analysis (may already be done)
            website_analysis = business.get("website_analysis", {})
            if not website_analysis and website:
                try:
                    website_analysis = self.website_analyzer.analyze(website)
                    # Extract email if not found
                    if not email and website_analysis.get("word_count", 0) > 0:
                        # Email extraction could be added here
                        pass
                except Exception as e:
                    print(f"      Warning: Website analysis failed: {e}")
                    website_analysis = {}
            
            # Calculate lead score
            score = self.lead_scorer.calculate_score(
                has_phone=bool(phone),
                has_email=bool(email),
                has_address=bool(address),
                rating=rating,
                review_count=review_count,
                website_analysis=website_analysis
            )
            
            # Generate justification
            justification = self.lead_scorer.generate_justification(
                business_name=name,
                has_phone=bool(phone),
                has_email=bool(email),
                rating=rating,
                review_count=review_count,
                website_analysis=website_analysis,
                category=category
            )
            
            # Build lead dictionary
            lead = {
                "country": country,
                "city": city,
                "category": category,
                "business_name": name,
                "phone": phone,
                "email": email,
                "website": website,
                "address": address,
                "rating": rating if rating else "",
                "review_count": review_count if review_count else 0,
                "lead_score": score,
                "value_justification": justification,
                "run_id": self.run_id,
                "timestamp": datetime.now().isoformat(),
            }
            
            return lead
            
        except Exception as e:
            print(f"      Error processing business: {e}")
            return None
    
    def stop(self):
        """Stop the discovery process"""
        if not self.is_running:
            print("No discovery process running.")
            return
        
        print("\nStopping discovery process...")
        self.should_stop = True
        self.is_running = False
    
    def get_status(self) -> dict:
        """Get current status"""
        return {
            "is_running": self.is_running,
            "run_id": self.run_id,
            "current_country": self.current_country,
            "current_city": self.current_city,
            "current_category": self.current_category,
        }


def interactive_mode():
    """Interactive command-line interface"""
    app = LeadDiscoveryApp()
    
    print("\n" + "="*60)
    print("B2B Lead Discovery System")
    print("="*60)
    print("\nCommands:")
    print("  start <country> <city> [categories...]")
    print("  stop")
    print("  status")
    print("  countries")
    print("  search-countries <query>")
    print("  exit")
    print("="*60 + "\n")
    
    while True:
        try:
            command = input("> ").strip()
            
            if not command:
                continue
            
            parts = command.split()
            cmd = parts[0].lower()
            
            if cmd == "exit" or cmd == "quit":
                if app.is_running:
                    print("Stopping discovery before exit...")
                    app.stop()
                print("Goodbye!")
                break
            
            elif cmd == "stop":
                app.stop()
            
            elif cmd == "status":
                status = app.get_status()
                print(f"\nStatus:")
                print(f"  Running: {status['is_running']}")
                if status['is_running']:
                    print(f"  Run ID: {status['run_id']}")
                    print(f"  Country: {status['current_country']}")
                    print(f"  City: {status['current_city']}")
                    print(f"  Category: {status['current_category']}")
                print()
            
            elif cmd == "countries":
                countries = list_all_countries()
                print(f"\nSupported countries ({len(countries)}):")
                for i, country in enumerate(countries, 1):
                    print(f"  {i}. {country}")
                print()
            
            elif cmd == "search-countries":
                if len(parts) < 2:
                    print("Usage: search-countries <query>")
                    continue
                query = " ".join(parts[1:])
                results = search_countries(query)
                if results:
                    print(f"\nFound {len(results)} countries:")
                    for country in results:
                        print(f"  - {country}")
                else:
                    print(f"\nNo countries found matching '{query}'")
                print()
            
            elif cmd == "start":
                if len(parts) < 3:
                    print("Usage: start <country> <city> [category1 category2 ...]")
                    print("Example: start United States New York")
                    print("Example: start India Mumbai dental clinic restaurant")
                    continue
                
                country = parts[1]
                city = parts[2]
                categories = parts[3:] if len(parts) > 3 else None
                
                # Validate country
                country_config = get_country_config(country)
                if not country_config:
                    print(f"\nError: Country '{country}' not found.")
                    print("Use 'countries' to see available countries.")
                    print("Use 'search-countries <query>' to search.\n")
                    continue
                
                # Start discovery
                app.start(country, city, categories)
            
            else:
                print(f"Unknown command: {cmd}")
                print("Type 'exit' to quit or see commands above.\n")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Use 'stop' to stop discovery or 'exit' to quit.")
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    interactive_mode()

