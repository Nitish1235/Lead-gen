# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Google Sheets Credentials

1. Go to https://console.cloud.google.com/
2. Create a project
3. Enable **Google Sheets API** and **Google Drive API**
4. Create Service Account (IAM & Admin > Service Accounts)
5. Create JSON key for the service account
6. Save as `credentials.json` in project root

### Step 3: Create & Share Google Sheet

1. Create a new Google Sheet
2. Copy Sheet ID from URL: `https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit`
3. Share sheet with service account email (found in `credentials.json`)
4. Give "Editor" permissions

### Step 4: Configure

Create `.env` file:
```env
GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id_here
```

Or edit `config.py` directly.

### Step 5: Run!

```bash
python main.py
```

Then type:
```
> start United States New York
```

## Google Places API Setup (Required for Best Results)

**If you see "REQUEST_DENIED" errors, you need to set up the Places API key.**

1. In Google Cloud Console, enable **Places API (New)**
2. Create an API key
3. Enable billing (required, but $200 free credit/month covers personal use)
4. Add to `.env`: `GOOGLE_MAPS_API_KEY=your_key_here`

**See [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) for detailed step-by-step instructions.**

Without this, the system will attempt HTML scraping (less reliable and may fail).

## First Run Tips

### Using Web UI (Recommended)
```bash
python run_ui.py
```
- Select country and city in the sidebar
- Choose categories (or use all defaults)
- Click "Start" button
- Watch leads appear in real-time
- View statistics and filter leads

### Using Command Line
```bash
python main.py
```
- Start with one category: `start United States New York barber shop`
- Or try multiple: `start United States New York hair salon nail salon spa`
- Check your Google Sheet - leads appear in real-time
- Use `stop` command to halt anytime
- Use `status` to see progress

## Troubleshooting

**"Credentials file not found"**
- Make sure `credentials.json` is in project root

**"Permission denied" on Sheets**
- Share sheet with service account email
- Give "Editor" permissions

**"No leads found"**
- Set `GOOGLE_MAPS_API_KEY` for reliable results
- Try different cities/categories

