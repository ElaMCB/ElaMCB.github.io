# Google Analytics 4 Setup Guide (Free)

Google Analytics 4 is completely free and perfect for weekly analytics reports.

## Step 1: Create Google Analytics Account

1. Go to https://analytics.google.com
2. Click **"Start measuring"**
3. Create an account (free)
4. Set up a property for `elamcb.github.io`
5. Note your **Measurement ID** (format: `G-XXXXXXXXXX`)

## Step 2: Add Tracking Code to Your Site

1. In GA4, go to **Admin** → **Data Streams** → Click your stream
2. Copy the **Global Site Tag (gtag.js)** code
3. Add it to your `index.html` in the `<head>` section (I can help with this)

The code looks like:
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

## Step 3: Exclude Your IP Address

1. In GA4, go to **Admin** → **Data Settings** → **Data Filters**
2. Click **"Create filter"**
3. Choose **"Internal traffic"**
4. Add your IP addresses
5. Set filter state to **"Active"**

## Step 4: Set Up API Access

1. Go to https://console.cloud.google.com
2. Create a new project (or use existing)
3. Enable **Google Analytics Reporting API**
4. Create credentials:
   - Go to **APIs & Services** → **Credentials**
   - Click **"Create Credentials"** → **"Service Account"**
   - Give it a name (e.g., "Analytics Reports")
   - Grant it **"Viewer"** role for your GA4 property
5. Create a key:
   - Click on the service account
   - Go to **Keys** tab
   - Click **"Add Key"** → **"JSON"**
   - Download the JSON file

## Step 5: Add GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Add these secrets:

**Required:**
- **Name**: `GA4_PROPERTY_ID`
- **Value**: Your GA4 Property ID (format: `123456789`)

- **Name**: `GA4_CREDENTIALS`
- **Value**: Paste the entire contents of the JSON credentials file you downloaded

**Optional (for filtering):**
- **Name**: `OWN_IP_ADDRESSES`
- **Value**: Your IP addresses (comma-separated)

## Step 6: Test the Workflow

1. Go to **Actions** → **Weekly Analytics Report**
2. Click **Run workflow** → **Run workflow**
3. Check the logs to see if it successfully fetches data
4. Check your email for the report!

## Benefits of Google Analytics 4

- ✅ **Completely free** - No limits
- ✅ **Powerful features** - Comprehensive analytics
- ✅ **Easy IP exclusion** - Built-in filters
- ✅ **API access** - Free tier: 25,000 requests/day
- ✅ **Industry standard** - Widely used

## Note on Privacy

Google Analytics uses cookies and collects data. If you're in the EU, you may need a GDPR consent banner. However, for personal portfolios, this is usually acceptable.

## Troubleshooting

### "GA4_PROPERTY_ID is required" error
- Make sure you've added the secret to GitHub
- Verify the Property ID is correct (numbers only, no `G-` prefix)

### API errors
- Check that the service account has Viewer access to your GA4 property
- Verify the credentials JSON is correct
- Check GitHub Actions logs for detailed errors

### No data in report
- Make sure the tracking code is on your site
- Verify your site is receiving traffic
- Check that data filters aren't excluding all traffic

