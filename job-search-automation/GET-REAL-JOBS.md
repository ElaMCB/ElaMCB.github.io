# How to Find REAL Jobs (Not Demo Data)

## Current Status

⚠️ **You're seeing FAKE demo data** - synthetic job postings I generated for testing the algorithm.

To find **REAL jobs**, you need to integrate with actual job board APIs.

---

## Quick Setup: Indeed Publisher API (5 Minutes)

### Step 1: Get Free API Access

1. **Go to:** https://ads.indeed.com/jobroll/xmlfeed
2. **Fill out the form:**
   - Name: Elena Mereanu
   - Email: Your email
   - Website: https://elamcb.github.io
   - How you'll use it: "Personal job search automation tool"
3. **Submit and wait** for approval email (usually within 24 hours)
4. **Get your Publisher ID** from the email (16-digit number)

### Step 2: Configure Your System

Create `.env` file in `job-search-automation/backend/`:

```bash
# job-search-automation/backend/.env
INDEED_PUBLISHER_ID=1234567890123456
```

Replace `1234567890123456` with your actual Publisher ID.

### Step 3: Install Dependencies

```bash
cd job-search-automation/backend
pip install python-dotenv requests
```

### Step 4: Update job_scraper.py

Replace the demo mode with real API calls. I've created `indeed_api.py` for you.

Update `job_scraper.py`:

```python
from indeed_api import IndeedAPI

class JobScraper:
    def __init__(self):
        self.use_real_api = os.getenv('INDEED_PUBLISHER_ID') is not None
        
        if self.use_real_api:
            self.indeed_api = IndeedAPI()
            print("✅ Using REAL Indeed API")
        else:
            print("⚠️  Using demo data (set INDEED_PUBLISHER_ID for real jobs)")
    
    async def search_jobs(self, keywords, location, remote, max_results):
        if self.use_real_api:
            # Get REAL jobs from Indeed
            return self.indeed_api.search_jobs(keywords, location, limit=max_results)
        else:
            # Demo data (current behavior)
            return self._generate_sample_jobs(...)
```

### Step 5: Test It!

```bash
cd job-search-automation/backend
python indeed_api.py
```

If your API key is valid, you'll see:
```
✅ SUCCESS! Found 10 REAL jobs:

1. Senior QA Engineer - Test Automation
   Company: Google
   Location: Remote
   Posted: 2 days ago
   URL: https://www.indeed.com/viewjob?jk=...
```

### Step 6: Use Dashboard with Real Jobs

1. Restart your API server: `python main.py`
2. Refresh dashboard: `http://localhost:8080/dashboard.html`
3. Upload your resume
4. Click "Find Matching Jobs"
5. **Get REAL job matches!** 🎯

---

## Alternative: Adzuna API (No Approval Needed)

### Instant Setup (5 Minutes)

1. **Sign up:** https://developer.adzuna.com/signup
2. **Get instant API credentials** (no approval wait)
3. **Add to .env:**
   ```bash
   ADZUNA_APP_ID=your_app_id
   ADZUNA_APP_KEY=your_app_key
   ```

### Use Multiple APIs for Better Coverage

```python
# Get jobs from both Indeed AND Adzuna
indeed_jobs = indeed_api.search_jobs(keywords, location, 25)
adzuna_jobs = adzuna_api.search_jobs(keywords, location, 25)

all_jobs = indeed_jobs + adzuna_jobs
# Remove duplicates and rank by match score
```

---

## Cost-Free Options Summary

| API | Approval Time | Free Tier | Coverage |
|-----|--------------|-----------|----------|
| **Indeed Publisher** | 24-48 hours | Unlimited (reasonable use) | Best US coverage |
| **Adzuna** | Instant | 5,000 calls/month | Good UK/US coverage |
| **The Muse** | Instant | Limited | Startup/tech focus |
| **GitHub Jobs** | None (shut down 2021) | - | - |

---

## Recommended Workflow

**Day 1 (Today):**
1. Sign up for Indeed Publisher API
2. Sign up for Adzuna API (instant access)
3. Use Adzuna while waiting for Indeed approval
4. Test with your resume

**Day 2-3:**
1. Get Indeed approval
2. Add Indeed API key
3. Now you have REAL jobs from 2 sources!

---

## What You'll Get

Once APIs are integrated:

✅ **Real job postings** from Indeed, Adzuna  
✅ **Real company names** (Google, Microsoft, startups)  
✅ **Real salaries** (when available)  
✅ **Real URLs** to apply directly  
✅ **Up-to-date postings** (posted today, yesterday)  
✅ **Better match scores** (60-90% for good fits)  

Your AI will analyze THOUSANDS of real jobs and show you the best matches for YOUR skills!

---

## Next Step: Sign Up Now

**Go here right now:** https://ads.indeed.com/jobroll/xmlfeed

Fill out the form, then while you wait for approval, sign up for Adzuna too: https://developer.adzuna.com/signup

I'll help you integrate both APIs once you have your credentials! 🚀

