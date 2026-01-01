"""
Test script to verify Google Sheets connection and save dummy data
"""
import os
from datetime import datetime
import config
from sheets_manager import SheetsManager

def test_sheets_connection():
    """Test Google Sheets connection and save dummy data"""
    
    print("=" * 60)
    print("Google Sheets Connection Test")
    print("=" * 60)
    print()
    
    # Step 1: Check credentials file
    print("Step 1: Checking credentials file...")
    creds_path = config.GOOGLE_SHEETS_CREDENTIALS_PATH
    if os.path.exists(creds_path):
        print(f"  [OK] Credentials file found: {creds_path}")
    else:
        print(f"  [ERROR] Credentials file NOT found: {creds_path}")
        print(f"  Please ensure credentials.json exists in the project root")
        return False
    print()
    
    # Step 2: Check spreadsheet ID
    print("Step 2: Checking spreadsheet ID...")
    spreadsheet_id = config.GOOGLE_SHEETS_SPREADSHEET_ID
    if spreadsheet_id:
        print(f"  [OK] Spreadsheet ID configured: {spreadsheet_id[:20]}...")
    else:
        print(f"  [ERROR] Spreadsheet ID NOT configured")
        print(f"  Please set GOOGLE_SHEETS_SPREADSHEET_ID in .env or config.py")
        return False
    print()
    
    # Step 3: Initialize SheetsManager
    print("Step 3: Initializing Google Sheets service...")
    try:
        sheets_manager = SheetsManager()
        print("  [OK] Google Sheets service initialized successfully")
    except Exception as e:
        print(f"  [ERROR] Failed to initialize Google Sheets service: {e}")
        print()
        print("Common issues:")
        print("  1. Credentials file is invalid or corrupted")
        print("  2. Service account doesn't have proper permissions")
        print("  3. Google Sheets API not enabled in Google Cloud Console")
        return False
    print()
    
    # Step 4: Test connection by reading spreadsheet
    print("Step 4: Testing connection to spreadsheet...")
    try:
        spreadsheet = sheets_manager.service.spreadsheets().get(
            spreadsheetId=spreadsheet_id
        ).execute()
        spreadsheet_title = spreadsheet.get('properties', {}).get('title', 'Unknown')
        print(f"  [OK] Successfully connected to spreadsheet: '{spreadsheet_title}'")
    except Exception as e:
        print(f"  [ERROR] Failed to connect to spreadsheet: {e}")
        print()
        print("Common issues:")
        print("  1. Spreadsheet ID is incorrect")
        print("  2. Service account doesn't have access to the spreadsheet")
        print("  3. Share the spreadsheet with the service account email (from credentials.json)")
        return False
    print()
    
    # Step 5: Ensure worksheet exists
    print("Step 5: Ensuring worksheet exists...")
    try:
        sheets_manager._ensure_headers()
        print(f"  [OK] Worksheet '{config.GOOGLE_SHEETS_WORKSHEET_NAME}' is ready")
    except Exception as e:
        print(f"  [ERROR] Failed to ensure worksheet: {e}")
        return False
    print()
    
    # Step 6: Save dummy data
    print("Step 6: Saving dummy test data...")
    try:
        dummy_lead = {
            "country": "Test Country",
            "city": "Test City",
            "category": "Test Category",
            "business_name": f"TEST BUSINESS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "phone": "+1-555-123-4567",
            "email": "test@example.com",
            "website": "https://example.com",
            "address": "123 Test Street, Test City, Test Country",
            "rating": 4.5,
            "review_count": 100,
            "lead_score": 85,
            "value_justification": "This is a test lead to verify Google Sheets connection",
            "run_id": "TEST-001",
            "timestamp": datetime.now().isoformat(),
        }
        
        success = sheets_manager.append_lead(dummy_lead)
        if success:
            print(f"  [OK] Dummy data saved successfully!")
            print(f"    Business: {dummy_lead['business_name']}")
            print(f"    Check your Google Sheet to see the test entry")
        else:
            print(f"  [ERROR] Failed to save dummy data")
            return False
    except Exception as e:
        print(f"  [ERROR] Error saving dummy data: {e}")
        import traceback
        traceback.print_exc()
        return False
    print()
    
    # Step 7: Verify data was saved
    print("Step 7: Verifying saved data...")
    try:
        result = sheets_manager.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{config.GOOGLE_SHEETS_WORKSHEET_NAME}!A:A"
        ).execute()
        values = result.get('values', [])
        row_count = len(values) - 1  # Exclude header
        print(f"  [OK] Found {row_count} row(s) in the sheet (including headers)")
        if row_count > 0:
            print(f"    Latest entry should be the test data we just saved")
    except Exception as e:
        print(f"  [WARNING] Could not verify data (but save was successful): {e}")
    print()
    
    print("=" * 60)
    print("[SUCCESS] All tests passed! Google Sheets connection is working.")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Open your Google Sheet to verify the test data")
    print("  2. You can delete the test row if you want")
    print("  3. Your application is ready to save real leads!")
    
    return True

if __name__ == "__main__":
    try:
        success = test_sheets_connection()
        if not success:
            print()
            print("Please fix the issues above and try again.")
            exit(1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

