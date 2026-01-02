"""
Google Sheets integration for storing leads
"""
import os
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
        self.worksheet_name = config.GOOGLE_SHEETS_WORKSHEET_NAME
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
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
                self.service = build('sheets', 'v4', credentials=creds)
                print(f"✓ Google Sheets service initialized from: {creds_path}")
            else:
                raise FileNotFoundError(
                    f"Credentials file not found: {creds_path}\n"
                    "Please download credentials.json from Google Cloud Console or set GOOGLE_SHEETS_CREDENTIALS_PATH"
                )
        except Exception as e:
            raise Exception(f"Failed to initialize Google Sheets service: {e}")
    
    def _ensure_headers(self):
        """Ensure worksheet exists with proper headers"""
        try:
            # Check if worksheet exists
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            worksheet_exists = False
            for sheet in spreadsheet.get('sheets', []):
                if sheet['properties']['title'] == self.worksheet_name:
                    worksheet_exists = True
                    break
            
            if not worksheet_exists:
                # Create worksheet
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
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
            
            # Check if headers exist
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.worksheet_name}!A1:Z1"
            ).execute()
            
            values = result.get('values', [])
            if not values or len(values) == 0:
                # Add headers
                headers = [
                    "Country", "City", "Category", "Business Name",
                    "Phone", "Email", "Website", "Address",
                    "Rating", "Review Count", "Lead Score",
                    "Value Justification", "Run ID", "Timestamp"
                ]
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=f"{self.worksheet_name}!A1",
                    valueInputOption='RAW',
                    body={'values': [headers]}
                ).execute()
            
        except HttpError as e:
            raise Exception(f"Google Sheets API error: {e}")
    
    def append_lead(self, lead_data: Dict) -> bool:
        """
        Append a single lead to the sheet
        
        Args:
            lead_data: Dictionary with lead information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_headers()
            
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
                lead_data.get("value_justification", ""),
                lead_data.get("run_id", ""),
                lead_data.get("timestamp", ""),
            ]
            
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.worksheet_name}!A:A",
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={'values': [row]}
            ).execute()
            
            return True
            
        except Exception as e:
            print(f"Error appending lead to sheet: {e}")
            return False
    
    def append_leads(self, leads: List[Dict]) -> int:
        """
        Append multiple leads to the sheet
        
        Args:
            leads: List of lead dictionaries
            
        Returns:
            Number of successfully appended leads
        """
        if not leads:
            return 0
        
        try:
            self._ensure_headers()
            
            rows = []
            for lead_data in leads:
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
                    lead_data.get("value_justification", ""),
                    lead_data.get("run_id", ""),
                    lead_data.get("timestamp", ""),
                ]
                rows.append(row)
            
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.worksheet_name}!A:A",
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={'values': rows}
            ).execute()
            
            return len(rows)
            
        except Exception as e:
            print(f"Error appending leads to sheet: {e}")
            return 0
    
    def check_duplicate(self, phone: Optional[str], website: Optional[str]) -> bool:
        """
        Check if a lead already exists (by phone or website)
        
        Args:
            phone: Phone number to check
            website: Website URL to check
            
        Returns:
            True if duplicate exists, False otherwise
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
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

