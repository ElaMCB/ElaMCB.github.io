# Analytics Collection & Weekly Reports

This system provides weekly email reports of your portfolio traffic, excluding your own visits.

## How It Works

1. **Client-side tracking**: Your portfolio tracks visits using localStorage (existing system)
2. **Server-side collection**: Visits are also sent to a collection endpoint
3. **Weekly processing**: GitHub Actions runs weekly to generate a filtered report
4. **Email delivery**: You receive a weekly email with traffic stats (excluding your visits)

## Setup Instructions

### Step 1: Configure Your Visit Identifiers

You need to tell the system how to identify your own visits. Add these as GitHub Secrets:

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Add the following secrets:

#### `OWN_IP_ADDRESSES`
- Comma-separated list of your IP addresses
- Example: `123.45.67.89,98.76.54.32`
- To find your IP: Visit https://whatismyipaddress.com/

#### `OWN_USER_AGENTS` (Optional)
- Comma-separated list of user agent strings that identify your browser
- Example: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36`
- This helps identify your visits even if your IP changes

### Step 2: Set Up Email (If Not Already Done)

If you haven't set up email secrets for other workflows, add these:

- `MAIL_SERVER`: Your SMTP server (e.g., `smtp.gmail.com`)
- `MAIL_PORT`: SMTP port (e.g., `587`)
- `MAIL_USERNAME`: Your email address
- `MAIL_PASSWORD`: Your email password or app password
- `MAIL_TO`: Recipient email (your email)
- `MAIL_FROM`: Sender email (your email)

See `.github/PLAYWRIGHT_EMAIL_SETUP.md` for detailed instructions.

### Step 3: Set Up Serverless Endpoint (Choose One Option)

Since GitHub Pages is static, you need a serverless function to collect visits. Choose one:

#### Option A: Vercel (Recommended - Free)

1. Create a free account at https://vercel.com
2. Create a new project and connect your GitHub repo
3. Create `api/collect-visit.js`:

```javascript
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Store visit data (you can use Vercel KV, a database, or file storage)
  // For simplicity, we'll use a GitHub Gist or file in the repo
  
  const visitData = req.body;
  
  // TODO: Store visitData somewhere (database, file, etc.)
  
  res.status(200).json({ success: true });
}
```

4. Deploy and note the endpoint URL

#### Option B: Netlify Functions (Free)

Similar to Vercel, create `netlify/functions/collect-visit.js`

#### Option C: GitHub Actions Webhook (Simpler, but requires manual setup)

Use a GitHub Action that can be triggered via webhook. See `analytics/webhook-collect.yml` for an example.

### Step 4: Update Client-Side Code

Update `index.html` to send visits to your collection endpoint (see the updated analytics code).

### Step 5: Test the Workflow

1. Manually trigger the workflow: Go to **Actions** → **Weekly Analytics Report** → **Run workflow**
2. Check your email for the report

## What Gets Tracked

- **Total visits** (including yours, for reference)
- **Other visits** (excluding yours - the main metric)
- **Unique visitors** (excluding yours)
- **Daily visit trends** (last 7 days)
- **Top traffic sources** (referrers)
- **Top browsers**

## Report Frequency

- **Default**: Every Monday at 9 AM UTC
- **Manual**: You can trigger it anytime from the Actions tab

## Customization

- Edit `.github/workflows/weekly-analytics-report.yml` to change schedule
- Edit `analytics/generate-weekly-report.js` to customize report format
- Edit email template in the workflow file

## Troubleshooting

### No visits being collected?
- Check that your serverless endpoint is deployed and accessible
- Verify client-side code is sending data to the endpoint
- Check browser console for errors

### Report shows 0 visits?
- Verify `OWN_IP_ADDRESSES` secret is set correctly
- Check that visits are being stored in `analytics/visits.json`
- Manually trigger the workflow and check logs

### Email not sending?
- Verify all email secrets are set correctly
- Check GitHub Actions logs for email errors
- See `.github/PLAYWRIGHT_EMAIL_SETUP.md` for email setup help

