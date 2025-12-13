# Weekly Analytics Report Setup Guide

This guide will help you set up weekly email reports that show your portfolio traffic **excluding your own visits**.

## Quick Start (Simplest Approach)

Since your analytics are currently client-side only (localStorage), we need to add server-side collection. Here are the options:

### Option 1: Use Plausible Analytics (Recommended - Free & Privacy-Friendly)

1. **Sign up for Plausible**: https://plausible.io (free for personal sites)
2. **Add Plausible script** to your `index.html`:
   ```html
   <script defer data-domain="elamcb.github.io" src="https://plausible.io/js/script.js"></script>
   ```
3. **Get your API token** from Plausible dashboard
4. **Update the weekly workflow** to use Plausible API instead of local data
5. **Set up IP exclusion** in Plausible dashboard (Settings → Exclusions)

This is the easiest option and gives you a nice dashboard too!

### Option 2: Use Google Analytics (Free)

1. **Create a Google Analytics account**
2. **Add tracking code** to your `index.html`
3. **Set up IP exclusion** in GA dashboard
4. **Update the weekly workflow** to query GA API

### Option 3: Build Your Own Collection (More Work)

If you want to keep everything self-hosted:

1. **Set up a serverless function** (Vercel/Netlify) to collect visits
2. **Store data** in a JSON file or database
3. **Update client-side code** to send visits to your endpoint
4. **Configure the weekly workflow** to process the data

## Configuration Steps

### Step 1: Add GitHub Secrets

Go to your repository → **Settings** → **Secrets and variables** → **Actions** and add:

#### Required for Filtering:
- `OWN_IP_ADDRESSES`: Comma-separated list of your IP addresses
  - Find your IP: https://whatismyipaddress.com/
  - Example: `123.45.67.89,98.76.54.32`
  
- `OWN_USER_AGENTS` (Optional): Comma-separated user agent strings
  - Helps identify your visits even if IP changes
  - Example: `Mozilla/5.0 (Windows NT 10.0; Win64; x64)`

#### Required for Email:
- `MAIL_SERVER`: Your SMTP server (e.g., `smtp.gmail.com`)
- `MAIL_PORT`: SMTP port (e.g., `587`)
- `MAIL_USERNAME`: Your email address
- `MAIL_PASSWORD`: Your email password or app password
- `MAIL_TO`: Recipient email (your email)
- `MAIL_FROM`: Sender email (your email)

See `.github/PLAYWRIGHT_EMAIL_SETUP.md` for detailed email setup.

### Step 2: Test the Workflow

1. Go to **Actions** → **Weekly Analytics Report**
2. Click **Run workflow** → **Run workflow**
3. Check your email for the report

### Step 3: Verify Schedule

The workflow runs every **Monday at 9 AM UTC** by default. You can change this in `.github/workflows/weekly-analytics-report.yml`:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Monday 9 AM UTC
```

## What the Report Includes

- **Visits (Excluding Yours)**: Main metric you care about
- **Unique Visitors**: Distinct visitors (excluding you)
- **Total Visits (Including Yours)**: For reference
- **Your Visits**: How many times you visited
- **Last 7 Days Trend**: Daily visit chart
- **Top Traffic Sources**: Where visitors came from
- **Top Browsers**: Browser breakdown

## Troubleshooting

### "No visits found" in report?
- Make sure `analytics/visits.json` exists and has data
- Check that visit collection is working
- Verify your IP/user agent filters aren't too strict

### Email not sending?
- Check all email secrets are set correctly
- Verify SMTP settings match your email provider
- Check GitHub Actions logs for errors

### Want to change report format?
- Edit `analytics/generate-weekly-report.js`
- Modify the HTML template in the `generateEmailHTML()` function

## Next Steps

1. Choose your collection method (Plausible recommended)
2. Set up GitHub Secrets
3. Test the workflow manually
4. Wait for your first weekly email!

