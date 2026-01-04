# Permissions Setup Guide

## Complete Permissions Setup for Lead Discovery System

This guide explains all the permissions you need to configure for the application to work properly.

---

## 1. Google Cloud Console Setup

### Step 1: Enable Required APIs

Your application needs access to these Google APIs:

1. **Google Sheets API**
   - Go to: [APIs & Services > Library](https://console.cloud.google.com/apis/library)
   - Search for "Google Sheets API"
   - Click on it and click **Enable**

### Step 2: Create Service Account

1. Go to: [IAM & Admin > Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Click **Create Service Account**
3. Fill in:
   - **Service account name**: `lead-discovery` (or any name you prefer)
   - **Service account ID**: Auto-generated (you can change it)
   - **Description**: (Optional) "Service account for lead discovery automation"
4. Click **Create and Continue**

### Step 3: Grant IAM Role (Optional but Recommended)

On the "Grant this service account access to project" screen:

- **Role**: Select **Editor** (or you can skip this - it's not strictly required for API access)
- Click **Continue**
- Click **Done**

**Note**: IAM roles at the project level are not strictly required because API access is controlled by:
1. Which APIs are enabled in the project
2. The OAuth scopes in your credentials.json
3. Individual file sharing permissions

### Step 4: Create JSON Key (Credentials)

1. Click on your newly created service account
2. Go to the **Keys** tab
3. Click **Add Key** > **Create new key**
4. Select **JSON** format
5. Click **Create**
6. The JSON file will download automatically
7. **Rename it to `credentials.json`** and save it in your project root

**Important**: 
- Keep this file secure - don't commit it to Git
- The file contains your service account's private key
- If lost, you can delete the key and create a new one

---

## 2. API Scopes (Already Configured in Code)

Your application requests these OAuth scopes (already configured in `sheets_manager.py`):

- ✅ `https://www.googleapis.com/auth/spreadsheets`
  - Allows read/write access to Google Sheets
  - Allows creating new worksheets (tabs) within existing spreadsheets using addSheet request

**You don't need to configure these manually** - they're automatically requested when your app uses the credentials.

---

## 3. Spreadsheet Permissions (IMPORTANT!)

Since your application now **creates spreadsheets automatically**, you have two scenarios:

### Using a Single Spreadsheet with Multiple Worksheets (Current Behavior)

The application uses **one spreadsheet** and creates **multiple worksheets (tabs)** for each country-city combination.

**Setup Steps:**

1. **Create a Google Sheet**:
   - Go to [Google Sheets](https://sheets.google.com)
   - Create a new spreadsheet (or use an existing one)
   - Copy the Spreadsheet ID from the URL: `https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`
   - Set this ID in your `.env` file or `config.py` as `GOOGLE_SHEETS_SPREADSHEET_ID`

2. **Find your service account email**:
   - Open `credentials.json`
   - Look for the `"client_email"` field
   - It looks like: `lead-gen@your-project-id.iam.gserviceaccount.com`

3. **Share the spreadsheet with the service account**:
   - Open your Google Sheet
   - Click the **Share** button (top right)
   - Paste the service account email in the "Add people and groups" field
   - Select **Editor** permission
   - Uncheck "Notify people" (service accounts don't receive emails)
   - Click **Share**

4. **The application will automatically**:
   - Create new worksheets (tabs) for each country-city combination
   - Name them in format: `Country-City` (e.g., "France-Lyon", "United-States-New-York")
   - Add headers and save leads to the appropriate worksheet

---

## 4. Permission Summary

### What the Service Account Can Do:

✅ **Create new worksheets (tabs)** in the shared spreadsheet (automatic)  
✅ **Read from worksheets** in the spreadsheet  
✅ **Write to worksheets** in the spreadsheet  
✅ **Access the spreadsheet** that's explicitly shared with it  

### What You Need to Do:

1. ✅ **Enable Google Sheets API** in Google Cloud Console
2. ✅ **Create service account** and download JSON key
3. ✅ **Save credentials.json** in project root
4. ✅ **Create a Google Sheet** and copy its ID to `GOOGLE_SHEETS_SPREADSHEET_ID` in config
5. ✅ **Share the spreadsheet** with service account email (Editor permission)

---

## 5. Troubleshooting Permission Issues

### Error: "API not enabled"

**Fix**: Enable Google Sheets API in Google Cloud Console

### Error: "Permission denied" or "Insufficient permissions" / "The caller does not have permission" (403)

**Possible causes**:
- Service account doesn't have access to the spreadsheet
- If spreadsheet is not shared: Share it with service account email (Editor permission)
- Make sure `GOOGLE_SHEETS_SPREADSHEET_ID` is set correctly in config
- The application creates worksheets (tabs) automatically, but the main spreadsheet must be shared first

### Error: "Invalid credentials"

**Fix**: 
- Check that `credentials.json` is valid JSON
- Verify the file path in `GOOGLE_SHEETS_CREDENTIALS_PATH`
- Make sure you downloaded the JSON key correctly

### Error: "Scope not authorized"

**Fix**: 
- The scopes are hardcoded in the application (no action needed)
- If you see this error, it might be an API quota/billing issue
- Check that APIs are enabled in your project

---

## 6. Security Best Practices

1. **Don't commit credentials.json to Git**
   - Add `credentials.json` to `.gitignore`
   - Use environment variables in production (Cloud Run secrets)

2. **Scope considerations**
   - The application uses `drive` scope (full Drive access) which is required for creating spreadsheets
   - This allows the service account to create and manage files it creates
   - Files created by the service account are owned by the service account

3. **Rotate keys periodically**
   - Delete old keys in Google Cloud Console
   - Generate new keys if credentials are compromised

4. **Restrict API key usage** (for Places API, if used)
   - Restrict API keys to specific APIs
   - Set up IP/HTTP referrer restrictions if needed

---

## Quick Checklist

- [ ] Google Sheets API enabled
- [ ] Service account created
- [ ] JSON key downloaded and saved as `credentials.json`
- [ ] `credentials.json` in project root (or path set in `.env`)
- [ ] Google Sheet created and ID copied
- [ ] `GOOGLE_SHEETS_SPREADSHEET_ID` set in config or `.env`
- [ ] Spreadsheet shared with service account email (Editor permission)

---

## Need Help?

If you encounter permission errors:

1. Check the error message in the application logs
2. Verify APIs are enabled in [Google Cloud Console](https://console.cloud.google.com/apis/dashboard)
3. Verify service account exists in [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
4. Check that `credentials.json` is valid JSON and in the correct location

