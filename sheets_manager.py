"""
Google Sheets integration for storing leads
"""
import os
import re
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config


class SheetsManager:
    """Manages Google Sheets operations for lead storage"""
    
    def __init__(self):
        self.credentials = None
        self.service = None
        self.spreadsheet_id = config.GOOGLE_SHEETS_SPREADSHEET_ID
        self._worksheet_cache = {}  # Cache worksheet names by country
        self._duplicate_cache = {}  # Cache duplicate check results (phone/website -> bool)
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Sheets API service"""
        try:
            creds_path = config.GOOGLE_SHEETS_CREDENTIALS_PATH
            
            # Check if creds_path is actually JSON content (starts with {)
            # This happens when Cloud Run secrets are set as environment variables
            if creds_path and creds_path.strip().startswith('{'):
                import json
                import tempfile
                # Parse the JSON to validate it
                try:
                    creds_data = json.loads(creds_path)
                    # Write to a temporary file
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                        json.dump(creds_data, f)
                        temp_file_path = f.name
                    creds_path = temp_file_path
                    print(f"✓ Credentials provided as JSON, wrote to temp file: {temp_file_path}")
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON in GOOGLE_SHEETS_CREDENTIALS_PATH: {e}")
            
            # Try service account first (recommended for automation)
            if os.path.exists(creds_path):
                creds = service_account.Credentials.from_service_account_file(
                    creds_path,
                    scopes=[
                        'https://www.googleapis.com/auth/spreadsheets'
                    ]
                )
                self.service = build('sheets', 'v4', credentials=creds)
                print(f"✓ Google Sheets service initialized from: {creds_path}")
            else:
                raise FileNotFoundError(
                    f"Credentials file not found: {creds_path}\n"
                    "Please download credentials.json from Google Cloud Console or set GOOGLE_SHEETS_CREDENTIALS_PATH"
                )
            
            # Validate spreadsheet ID
            if not self.spreadsheet_id:
                raise ValueError(
                    "GOOGLE_SHEETS_SPREADSHEET_ID is not set. "
                    "Please create a Google Sheet and set the spreadsheet ID in config.py or .env"
                )
            
        except Exception as e:
            raise Exception(f"Failed to initialize Google Sheets service: {e}")
    
    def _get_worksheet_name(self, country: str) -> str:
        """Generate worksheet name in format: country (country-wise sheets)"""
        # Clean name: remove special characters, replace spaces with hyphens
        clean_country = re.sub(r'[^\w\s-]', '', country).strip().replace(' ', '-')
        return clean_country
    
    def _worksheet_exists(self, worksheet_name: str) -> bool:
        """Check if worksheet exists in the spreadsheet"""
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            for sheet in spreadsheet.get('sheets', []):
                if sheet['properties']['title'] == worksheet_name:
                    return True
            return False
        except HttpError as e:
            print(f"Error checking if worksheet exists: {e}")
            return False
    
    def _create_worksheet(self, worksheet_name: str) -> bool:
        """
        Create a new worksheet (tab) in the spreadsheet using addSheet request
        
        Args:
            worksheet_name: Name of the worksheet to create
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Use batchUpdate with addSheet request
            request_body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': worksheet_name
                        }
                    }
                }]
            }
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=request_body
            ).execute()
            
            print(f"✓ Created worksheet '{worksheet_name}' in spreadsheet")
            return True
            
        except HttpError as e:
            # If worksheet already exists, that's fine
            if 'already exists' in str(e).lower() or e.resp.status == 400:
                print(f"✓ Worksheet '{worksheet_name}' already exists")
                return True
            print(f"Error creating worksheet '{worksheet_name}': {e}")
            return False
        except Exception as e:
            print(f"Unexpected error creating worksheet: {e}")
            return False
    
    def _get_or_create_worksheet(self, country: str) -> Optional[str]:
        """
        Get existing worksheet name or create new one for country (country-wise sheets)
        
        Args:
            country: Country name
            
        Returns:
            Worksheet name if successful, None otherwise
        """
        # Check cache first (country-only cache key)
        cache_key = country
        if cache_key in self._worksheet_cache:
            return self._worksheet_cache[cache_key]
        
        # Generate worksheet name (country-only)
        worksheet_name = self._get_worksheet_name(country)
        
        # Check if worksheet exists
        if not self._worksheet_exists(worksheet_name):
            # Create new worksheet
            if not self._create_worksheet(worksheet_name):
                return None
        
        # Cache the result
        self._worksheet_cache[cache_key] = worksheet_name
        
        return worksheet_name
    
    def _ensure_headers(self, worksheet_name: str):
        """Ensure worksheet exists with proper headers"""
        try:
            # Check if headers exist
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{worksheet_name}!A1:Z1"
            ).execute()
            
            values = result.get('values', [])
            if not values or len(values) == 0:
                # Add headers
                headers = [
                    "Country", "City", "Category", "Business Name",
                    "Phone", "Email", "Website", "Address",
                    "Rating", "Review Count",
                    "Run ID", "Timestamp"
                ]
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=f"{worksheet_name}!A1",
                    valueInputOption='RAW',
                    body={'values': [headers]}
                ).execute()
                print(f"✓ Added headers to worksheet '{worksheet_name}'")
            
        except HttpError as e:
            raise Exception(f"Google Sheets API error: {e}")
    
    def append_lead(self, lead_data: Dict) -> bool:
        """
        Append a single lead to the appropriate worksheet (creates worksheet if needed)
        
        Args:
            lead_data: Dictionary with lead information (must contain 'country' and 'city')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            country = lead_data.get("country", "")
            
            if not country:
                print(f"Error: Country is required in lead_data")
                return False
            
            # Get or create worksheet for this country (country-wise sheets)
            worksheet_name = self._get_or_create_worksheet(country)
            if not worksheet_name:
                print(f"Error: Failed to get or create worksheet for {country}")
                return False
            
            # Ensure headers exist
            self._ensure_headers(worksheet_name)
            
            row = [
                lead_data.get("country", ""),
                lead_data.get("city", ""),
                lead_data.get("category", ""),
                lead_data.get("business_name", ""),
                lead_data.get("phone", ""),
                lead_data.get("email", ""),
                lead_data.get("website", ""),
                lead_data.get("address", ""),
                lead_data.get("rating", ""),
                lead_data.get("review_count", ""),
                lead_data.get("run_id", ""),
                lead_data.get("timestamp", ""),
            ]
            
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{worksheet_name}!A:A",
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={'values': [row]}
            ).execute()
            
            # Update cache after successful append to avoid duplicate checks
            phone = lead_data.get("phone", "").strip()
            website = lead_data.get("website", "").strip()
            if phone:
                self._duplicate_cache[f"{country}:phone:{phone}"] = True
            if website:
                self._duplicate_cache[f"{country}:website:{website}"] = True
            
            return True
            
        except Exception as e:
            print(f"Error appending lead to sheet: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def append_leads(self, leads: List[Dict]) -> int:
        """
        Append multiple leads to the sheet (groups by country - country-wise sheets)
        
        Args:
            leads: List of lead dictionaries
            
        Returns:
            Number of successfully appended leads
        """
        if not leads:
            return 0
        
        # Group leads by country (each country gets its own worksheet)
        success_count = 0
        for lead_data in leads:
            if self.append_lead(lead_data):
                success_count += 1
        
        return success_count
    
    def check_duplicate(self, phone: Optional[str], website: Optional[str], country: str, city: str) -> bool:
        """
        Check if a lead already exists in the country worksheet (by phone or website)
        Uses caching to avoid repeated API calls for the same values.
        
        Args:
            phone: Phone number to check
            website: Website URL to check
            country: Country name (to identify worksheet)
            city: City name (not used for worksheet identification, but kept for compatibility)
        
        Returns:
            True if duplicate exists, False otherwise
        """
        try:
            # Check cache first (fast lookup)
            phone_key = f"{country}:phone:{phone}" if phone and phone.strip() else None
            website_key = f"{country}:website:{website}" if website and website.strip() else None
            
            if phone_key and phone_key in self._duplicate_cache:
                return self._duplicate_cache[phone_key]
            if website_key and website_key in self._duplicate_cache:
                return self._duplicate_cache[website_key]
            
            # Get worksheet name for this country (country-wise sheets)
            worksheet_name = self._get_or_create_worksheet(country)
            if not worksheet_name:
                return False  # If worksheet doesn't exist, no duplicates
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{worksheet_name}!E:F"  # Phone and Website columns
            ).execute()
            
            values = result.get('values', [])
            if len(values) <= 1:  # Only headers or empty
                return False
            
            # Build cache of existing phones/websites from this call
            existing_phones = set()
            existing_websites = set()
            
            # Skip header row
            for row in values[1:]:
                existing_phone = row[0] if len(row) > 0 else ""
                existing_website = row[1] if len(row) > 1 else ""
                
                if existing_phone and existing_phone.strip():
                    existing_phones.add(existing_phone.strip())
                if existing_website and existing_website.strip():
                    existing_websites.add(existing_website.strip())
            
            # Check if current lead is duplicate
            is_duplicate = False
            if phone and phone.strip():
                phone_clean = phone.strip()
                if phone_clean in existing_phones:
                    is_duplicate = True
                # Cache result
                if phone_key:
                    self._duplicate_cache[phone_key] = is_duplicate
            
            if not is_duplicate and website and website.strip():
                website_clean = website.strip()
                if website_clean in existing_websites:
                    is_duplicate = True
                # Cache result
                if website_key:
                    self._duplicate_cache[website_key] = is_duplicate
            
            # Cache all existing phones/websites to avoid future API calls
            for existing_phone in existing_phones:
                key = f"{country}:phone:{existing_phone}"
                self._duplicate_cache[key] = True
            for existing_website in existing_websites:
                key = f"{country}:website:{existing_website}"
                self._duplicate_cache[key] = True
            
            return is_duplicate
            
        except Exception as e:
            print(f"Error checking duplicate: {e}")
            return False  # On error, assume not duplicate to be safe
