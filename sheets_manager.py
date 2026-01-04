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
        self.drive_service = None  # Drive API service for searching/creating spreadsheets
        self.worksheet_name = config.GOOGLE_SHEETS_WORKSHEET_NAME
        self._spreadsheet_cache = {}  # Cache spreadsheet IDs by country-city
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
                        'https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive.file'  # Need Drive API to search/create spreadsheets
                    ]
                )
                self.service = build('sheets', 'v4', credentials=creds)
                self.drive_service = build('drive', 'v3', credentials=creds)
                print(f"✓ Google Sheets & Drive services initialized from: {creds_path}")
            else:
                raise FileNotFoundError(
                    f"Credentials file not found: {creds_path}\n"
                    "Please download credentials.json from Google Cloud Console or set GOOGLE_SHEETS_CREDENTIALS_PATH"
                )
        except Exception as e:
            raise Exception(f"Failed to initialize Google Sheets service: {e}")
    
    def _get_spreadsheet_name(self, country: str, city: str) -> str:
        """Generate spreadsheet name in format: country-city"""
        # Clean name: remove special characters, replace spaces with hyphens
        clean_country = re.sub(r'[^\w\s-]', '', country).strip().replace(' ', '-')
        clean_city = re.sub(r'[^\w\s-]', '', city).strip().replace(' ', '-')
        return f"{clean_country}-{clean_city}"
    
    def _find_spreadsheet_by_title(self, title: str) -> Optional[str]:
        """
        Search for spreadsheet by title using Google Drive API
        
        Args:
            title: Spreadsheet title to search for
            
        Returns:
            Spreadsheet ID if found, None otherwise
        """
        try:
            # Search for spreadsheets with matching title
            # mimeType='application/vnd.google-apps.spreadsheet' filters to only Google Sheets
            query = f"name='{title}' and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
            
            results = self.drive_service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                pageSize=10
            ).execute()
            
            files = results.get('files', [])
            
            # Return first exact match
            for file in files:
                if file.get('name') == title:
                    print(f"✓ Found existing spreadsheet: {title} (ID: {file.get('id')})")
                    return file.get('id')
            
            return None
            
        except HttpError as e:
            print(f"Error searching for spreadsheet '{title}': {e}")
            return None
        except Exception as e:
            print(f"Unexpected error searching for spreadsheet: {e}")
            return None
    
    def _create_spreadsheet(self, title: str) -> Optional[str]:
        """
        Create a new spreadsheet with given title
        
        Args:
            title: Spreadsheet title
            
        Returns:
            Spreadsheet ID if successful, None otherwise
        """
        try:
            # Create spreadsheet using Sheets API
            spreadsheet = {
                'properties': {
                    'title': title
                },
                'sheets': [{
                    'properties': {
                        'title': self.worksheet_name
                    }
                }]
            }
            
            spreadsheet = self.service.spreadsheets().create(
                body=spreadsheet,
                fields='spreadsheetId'
            ).execute()
            
            spreadsheet_id = spreadsheet.get('spreadsheetId')
            print(f"✓ Created new spreadsheet: {title} (ID: {spreadsheet_id})")
            return spreadsheet_id
            
        except HttpError as e:
            print(f"Error creating spreadsheet '{title}': {e}")
            return None
        except Exception as e:
            print(f"Unexpected error creating spreadsheet: {e}")
            return None
    
    def _get_or_create_spreadsheet(self, country: str, city: str) -> Optional[str]:
        """
        Get existing spreadsheet ID or create new one for country-city
        
        Args:
            country: Country name
            city: City name
            
        Returns:
            Spreadsheet ID if successful, None otherwise
        """
        # Check cache first
        cache_key = f"{country}-{city}"
        if cache_key in self._spreadsheet_cache:
            return self._spreadsheet_cache[cache_key]
        
        # Generate spreadsheet name
        spreadsheet_name = self._get_spreadsheet_name(country, city)
        
        # Try to find existing spreadsheet
        spreadsheet_id = self._find_spreadsheet_by_title(spreadsheet_name)
        
        # If not found, create new one
        if not spreadsheet_id:
            spreadsheet_id = self._create_spreadsheet(spreadsheet_name)
        
        # Cache the result
        if spreadsheet_id:
            self._spreadsheet_cache[cache_key] = spreadsheet_id
        
        return spreadsheet_id
    
    def _ensure_headers(self, spreadsheet_id: str):
        """Ensure worksheet exists with proper headers"""
        try:
            # Check if worksheet exists
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()
            
            worksheet_exists = False
            for sheet in spreadsheet.get('sheets', []):
                if sheet['properties']['title'] == self.worksheet_name:
                    worksheet_exists = True
                    break
            
            if not worksheet_exists:
                # Create worksheet
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={
                        'requests': [{
                            'addSheet': {
                                'properties': {
                                    'title': self.worksheet_name
                                }
                            }
                        }]
                    }
                ).execute()
                print(f"✓ Created worksheet '{self.worksheet_name}' in spreadsheet")
            
            # Check if headers exist
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=f"{self.worksheet_name}!A1:Z1"
            ).execute()
            
            values = result.get('values', [])
            if not values or len(values) == 0:
                # Add headers
                headers = [
                    "Country", "City", "Category", "Business Name",
                    "Phone", "Email", "Website", "Address",
                    "Rating", "Review Count", "Lead Score",
                    "Run ID", "Timestamp"
                ]
                self.service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range=f"{self.worksheet_name}!A1",
                    valueInputOption='RAW',
                    body={'values': [headers]}
                ).execute()
                print(f"✓ Added headers to worksheet '{self.worksheet_name}'")
            
        except HttpError as e:
            raise Exception(f"Google Sheets API error: {e}")
    
    def append_lead(self, lead_data: Dict) -> bool:
        """
        Append a single lead to the sheet (creates spreadsheet if needed)
        
        Args:
            lead_data: Dictionary with lead information (must contain 'country' and 'city')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            country = lead_data.get("country", "")
            city = lead_data.get("city", "")
            
            if not country or not city:
                print(f"Error: Country and city are required in lead_data")
                return False
            
            # Get or create spreadsheet for this country-city
            spreadsheet_id = self._get_or_create_spreadsheet(country, city)
            if not spreadsheet_id:
                print(f"Error: Failed to get or create spreadsheet for {country}-{city}")
                return False
            
            # Ensure headers exist
            self._ensure_headers(spreadsheet_id)
            
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
                lead_data.get("lead_score", ""),
                lead_data.get("run_id", ""),
                lead_data.get("timestamp", ""),
            ]
            
            self.service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=f"{self.worksheet_name}!A:A",
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={'values': [row]}
            ).execute()
            
            return True
            
        except Exception as e:
            print(f"Error appending lead to sheet: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def append_leads(self, leads: List[Dict]) -> int:
        """
        Append multiple leads to the sheet (groups by country-city)
        
        Args:
            leads: List of lead dictionaries
            
        Returns:
            Number of successfully appended leads
        """
        if not leads:
            return 0
        
        # Group leads by country-city (each gets its own spreadsheet)
        success_count = 0
        for lead_data in leads:
            if self.append_lead(lead_data):
                success_count += 1
        
        return success_count
    
    def check_duplicate(self, phone: Optional[str], website: Optional[str], country: str, city: str) -> bool:
        """
        Check if a lead already exists in the country-city spreadsheet (by phone or website)
        
        Args:
            phone: Phone number to check
            website: Website URL to check
            country: Country name (to identify spreadsheet)
            city: City name (to identify spreadsheet)
        
        Returns:
            True if duplicate exists, False otherwise
        """
        try:
            # Get spreadsheet ID for this country-city
            spreadsheet_id = self._get_or_create_spreadsheet(country, city)
            if not spreadsheet_id:
                return False  # If spreadsheet doesn't exist, no duplicates
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=f"{self.worksheet_name}!E:F"  # Phone and Website columns
            ).execute()
            
            values = result.get('values', [])
            if len(values) <= 1:  # Only headers or empty
                return False
            
            # Skip header row
            for row in values[1:]:
                existing_phone = row[0] if len(row) > 0 else ""
                existing_website = row[1] if len(row) > 1 else ""
                
                if phone and phone.strip() and existing_phone == phone:
                    return True
                if website and website.strip() and existing_website == website:
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error checking duplicate: {e}")
            return False  # On error, assume not duplicate to be safe

