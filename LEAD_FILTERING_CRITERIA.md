# Lead Filtering Criteria

This document explains how the system filters and processes leads.

## Overview

The system uses **multiple filtering layers** to identify high-quality leads that are likely to need digital services. Leads are NOT filtered out completely - instead, they are **scored** and **prioritized** based on quality signals.

---

## 1. Exclusion Filtering (Hard Filters)

Businesses are **completely excluded** if they match any excluded terms in their name or website.

### Excluded Terms (`config.py`)

Businesses containing these terms are **skipped entirely**:
- `job portal`, `job board`, `recruitment` - Job listing sites
- `government`, `municipal` - Government entities
- `franchise`, `chain` - Large franchises/chains (less likely to need services)
- `aggregator`, `directory` - Aggregator sites
- `justdial`, `yelp` - Directory/listing sites

**Location:** `maps_discoverer.py` → `should_exclude()` method  
**When:** Applied before processing the business

---

## 2. Rating-Based Filtering (Optional)

Currently **NOT actively filtering** by rating, but ratings are used for scoring:

- `MIN_RATING_THRESHOLD = 0.0` - No minimum rating filter (all ratings accepted)
- `MAX_RATING_THRESHOLD = 4.5` - Maximum rating (currently not enforced)

**Note:** The system prioritizes businesses with **lower ratings** (3.5-4.5) as they're more likely to need improvement services.

---

## 3. Lead Scoring (Priority System)

Instead of filtering out leads, the system **scores** them (0-150 points). Higher scores = better leads.

### Scoring Criteria (`lead_scorer.py`)

#### Contact Information (23 points max)
- **Has Phone:** +10 points
- **Has Email:** +8 points  
- **Has Address:** +5 points

#### Rating Signals (25 points max)
- **Low Rating (< 3.5):** +15 points (likely needs help)
- **Medium Rating (3.5-4.0):** +10 points (potential for improvement)

#### Review Count (8 points max)
- **Few Reviews (< 50):** +8 points (newer/smaller business = potential client)

#### Website Quality Issues (47 points max)
- **Outdated Platform** (Wix, basic WordPress, GoDaddy): +12 points
- **No Online Booking:** +15 points (automation opportunity)
- **No HTTPS:** +10 points (security improvement needed)
- **Weak Website** (basic template, poor design): +10 points

**Total Maximum Score:** 103 points (capped at 150 for readability)

---

## 4. Duplicate Filtering

Leads are checked for duplicates before saving to Google Sheets.

### Duplicate Check Criteria (`sheets_manager.py`)

A lead is considered a duplicate if it matches **either**:
- Same phone number (existing in sheet)
- Same website URL (existing in sheet)

**Note:** Duplicates are **skipped** and not saved to the sheet.

---

## 5. Required Fields

A business is only converted to a lead if it has:
- **Business Name** - Required (if missing, lead is skipped)

**All other fields are optional:**
- Phone, Email, Website, Address, Rating, Reviews - All optional

---

## 6. Category-Based Targeting

The system focuses on specific business categories that benefit from digital services.

### Target Categories (`config.py` → `DEFAULT_CATEGORIES`)

#### Healthcare & Wellness (appointment-heavy)
- Dental clinics, Medical clinics, Doctor offices, Veterinary clinics
- Physiotherapy, Chiropractic, Massage therapy
- Psychology clinics, Counseling centers

#### Beauty & Personal Care (appointment-based)
- Beauty salons, Hair salons, Barber shops, Nail salons, Spas
- Estheticians, Tattoo parlors, Cosmetic clinics, Pet grooming

#### Fitness & Sports
- Gyms, Yoga studios, Pilates, Martial arts, Dance studios
- Personal trainers, Tennis clubs, Golf clubs

#### Professional Services
- Law firms, Accounting firms, Consulting firms
- Financial advisors, Insurance agencies, Real estate

#### Home Services
- Plumbers, Electricians, HVAC contractors, Handymen
- Landscaping, Cleaning services, Moving companies

#### Automotive Services
- Auto repair shops, Car mechanics, Car wash
- Tire shops, Auto detailing

#### Education & Training
- Coaching institutes, Tutoring centers, Driving schools
- Music schools, Language schools, Art schools

#### And many more... (105+ categories total)

---

## Filtering Flow Summary

```
1. Google Maps Search Results
   ↓
2. Exclusion Check (EXCLUDED_TERMS)
   → If matches excluded terms → SKIP (not processed)
   ↓
3. Process Business
   → Extract: name, phone, email, website, address, rating, reviews
   → Analyze website (if available)
   ↓
4. Calculate Lead Score (0-150)
   → Based on: contact info, rating, reviews, website quality
   ↓
5. Check Duplicates (phone or website match)
   → If duplicate → SKIP (not saved)
   ↓
6. Save to Google Sheets
   → Lead saved with score and justification
```

---

## What Gets Saved?

**All processed businesses are saved** (unless excluded or duplicate), but they are:
- **Scored** (0-150) - Higher scores appear first
- **Justified** - Explanation of why this is a good lead
- **Sorted** - By score (highest first)

**Example Lead:**
```json
{
  "business_name": "ABC Dental Clinic",
  "phone": "+1234567890",
  "email": "contact@abcdental.com",
  "website": "https://abcdental.com",
  "address": "123 Main St, City",
  "rating": 3.2,
  "review_count": 12,
  "lead_score": 68,
  "value_justification": "Low rating (3.2) suggests improvement needed, growing business with room for digital expansion, no online booking system - automation opportunity, healthcare sector needs secure, compliant digital solutions and appointment systems."
}
```

---

## Key Points

1. **No Hard Rating Filter** - All ratings are accepted, but lower ratings score higher
2. **Scoring, Not Filtering** - Leads are scored and prioritized, not filtered out
3. **Exclusion Only** - Only excluded terms (job boards, government, franchises) are completely skipped
4. **Duplicate Prevention** - Duplicates based on phone/website are skipped
5. **Category Focus** - System targets appointment-based and service businesses

---

## Customization

You can customize filtering by editing `config.py`:

- **Add/Remove Excluded Terms:** Modify `EXCLUDED_TERMS` list
- **Change Scoring Weights:** Modify `SCORE_WEIGHTS` dictionary
- **Set Rating Thresholds:** Modify `MIN_RATING_THRESHOLD` / `MAX_RATING_THRESHOLD` (requires code changes to enforce)
- **Change Categories:** Modify `DEFAULT_CATEGORIES` list

---

For more details, see:
- `config.py` - Configuration and thresholds
- `lead_scorer.py` - Scoring logic
- `maps_discoverer.py` - Exclusion filtering
- `sheets_manager.py` - Duplicate checking

