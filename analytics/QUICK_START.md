# Weekly Analytics Report - Quick Start

## ✅ What's Already Done

✅ **Weekly GitHub Action Workflow** (`.github/workflows/weekly-analytics-report.yml`)
- Runs every Monday at 9 AM UTC
- Supports Google Analytics 4 (free) or local analytics file
- Generates a filtered report excluding your visits
- Sends you a beautiful HTML email

✅ **Report Generation Script** (`analytics/generate-weekly-report.js`)
- Generates HTML and text email reports
- Shows: visits, unique visitors, pageviews, bounce rate, daily trends, top sources, browsers
- Works with GA4 API or local visits.json file

✅ **Setup Documentation** 
- `analytics/GOOGLE_ANALYTICS_SETUP.md` - GA4 setup guide
- `analytics/FREE_ALTERNATIVES.md` - Other free options

## Choose Your Analytics Solution

### Option 1: Google Analytics 4 (Recommended - Free)
- ✅ Completely free
- ✅ Powerful features
- ✅ Easy setup
- See `analytics/GOOGLE_ANALYTICS_SETUP.md` for full instructions

### Option 2: Local Analytics File
- ✅ Already implemented (localStorage)
- ✅ Privacy-friendly
- ✅ No external services
- Requires adding server-side collection

## Quick Setup (Google Analytics 4)

### Step 1: Set Up Google Analytics 4

1. **Create account** at https://analytics.google.com (free)
2. **Create property** for `elamcb.github.io`
3. **Get your Measurement ID** (format: `G-XXXXXXXXXX`)
4. **Add tracking code** to your `index.html` (I can help with this)
5. **Exclude your IP**: Admin → Data Settings → Data Filters → Create "Internal traffic" filter

### Step 2: Set Up API Access

1. Go to https://console.cloud.google.com
2. **Enable** Google Analytics Reporting API
3. **Create service account** with Viewer role
4. **Download JSON credentials** file

### Step 3: Add GitHub Secrets

Go to **Repository → Settings → Secrets and variables → Actions** and add:

**Required:**
- **Name**: `GA4_PROPERTY_ID`
- **Value**: Your GA4 Property ID (numbers only, e.g., `123456789`)

- **Name**: `GA4_CREDENTIALS`
- **Value**: Paste entire contents of the JSON credentials file

**Optional (for additional filtering):**
- **Name**: `OWN_IP_ADDRESSES`
- **Value**: Your IP addresses (comma-separated)

**For Email (if not already set up):**
- `MAIL_SERVER`: `smtp.gmail.com` (or your provider)
- `MAIL_PORT`: `587`
- `MAIL_USERNAME`: Your email
- `MAIL_PASSWORD`: Your email password or app password
- `MAIL_TO`: Your email (recipient)
- `MAIL_FROM`: Your email (sender)

See `.github/PLAYWRIGHT_EMAIL_SETUP.md` for detailed email setup.

### Step 4: Test It

1. Go to **Actions** → **Weekly Analytics Report**
2. Click **Run workflow** → **Run workflow**
3. Check the logs to see if it successfully fetches data
4. Check your email for the report!

**Note**: It may take a few hours for Plausible to start collecting data after you add the script. The first report might show 0 visits if you just set it up.

## What the Report Shows

- ✅ **Visits (Excluding Yours)**: The main metric (your IP is auto-excluded by Plausible)
- ✅ **Unique Visitors**: Distinct visitors
- ✅ **Pageviews**: Total page views
- ✅ **Bounce Rate**: Percentage of single-page visits
- ✅ **Last 7 Days**: Daily visit chart
- ✅ **Top Traffic Sources**: Where visitors came from
- ✅ **Top Browsers**: Browser breakdown

## Benefits of Google Analytics 4

- ✅ **Completely free** - No limits or paid tiers
- ✅ **Powerful features** - Comprehensive analytics
- ✅ **Easy IP exclusion** - Built-in data filters
- ✅ **API access** - Free tier: 25,000 requests/day
- ✅ **Industry standard** - Widely used and supported

## Need Help?

- See `analytics/GOOGLE_ANALYTICS_SETUP.md` for detailed step-by-step instructions
- See `analytics/FREE_ALTERNATIVES.md` for other free options
- See `analytics/README.md` for technical details
- Check GitHub Actions logs if something doesn't work

---

**That's it!** Once you complete the setup above, you'll start receiving weekly email reports every Monday at 9 AM UTC. 🎉

