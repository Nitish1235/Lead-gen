# Google Places API Setup Guide

## Fix "REQUEST_DENIED" Error

If you're seeing `Places API error: REQUEST_DENIED`, follow these steps:

### Step 1: Enable Places API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create a new one)
3. Go to **APIs & Services** > **Library**
4. Search for "Places API"
5. Click on **Places API (New)** or **Places API**
6. Click **Enable**

### Step 2: Create API Key

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **API Key**
3. Copy the API key that appears

### Step 3: Configure API Key

**Option A: Using .env file (Recommended)**

Create or edit `.env` file in your project root:
```env
GOOGLE_MAPS_API_KEY=your_api_key_here
```

**Option B: Edit config.py**

Edit `config.py` and set:
```python
GOOGLE_MAPS_API_KEY = "your_api_key_here"
```

### Step 4: Restrict API Key (Recommended for Security)

1. In Google Cloud Console, go to **APIs & Services** > **Credentials**
2. Click on your API key
3. Under **API restrictions**, select **Restrict key**
4. Check only **Places API (New)** or **Places API**
5. Click **Save**

### Step 5: Set Billing (Required for Places API)

Google Places API requires billing to be enabled:

1. Go to **Billing** in Google Cloud Console
2. Link a billing account (or create one)
3. **Note**: Google provides $200 free credit per month, which is usually enough for personal use

### Common Issues

**"REQUEST_DENIED" Error:**
- ✅ API key is missing or incorrect
- ✅ Places API is not enabled
- ✅ API key restrictions are too strict
- ✅ Billing is not enabled

**Check if API key is set:**
```python
# In Python console or add to your code temporarily
import config
print(f"API Key set: {bool(config.GOOGLE_MAPS_API_KEY)}")
print(f"API Key: {config.GOOGLE_MAPS_API_KEY[:10]}..." if config.GOOGLE_MAPS_API_KEY else "Not set")
```

**Test API Key:**
```bash
# Test in browser (replace YOUR_API_KEY)
https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurant+in+New+York&key=YOUR_API_KEY
```

### Alternative: Use Without API Key (Less Reliable)

If you don't want to use Places API, the system will attempt HTML scraping, but:
- ❌ Less reliable
- ❌ May get blocked by Google
- ❌ Slower
- ⚠️ Not recommended for production use

To disable API usage, simply don't set `GOOGLE_MAPS_API_KEY` in your `.env` or `config.py`.

### Cost Information

- **Places API Text Search**: $32 per 1,000 requests
- **Places API Details**: $17 per 1,000 requests
- **Free Tier**: $200 credit/month (approximately 6,000 searches/month)

For personal use with reasonable limits, you should stay within the free tier.

### Verify Setup

After setting up, restart your application:

```bash
# Stop current process (Ctrl+C)
# Then restart
python run_ui.py
# or
python main.py
```

Check the console output - you should NOT see "REQUEST_DENIED" errors anymore.

