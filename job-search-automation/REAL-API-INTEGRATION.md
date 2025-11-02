# Real Job API Integration Guide

## Get Started Finding REAL Jobs

This guide will help you integrate actual job board APIs to find real job postings.

---

## Option 1: Indeed Publisher API (Easiest - Recommended)

### Step 1: Get Your Indeed Publisher API Key

1. **Visit:** https://ads.indeed.com/jobroll/xmlfeed
2. **Sign up** for Indeed Publisher Program (free)
3. **Get your Publisher ID** - looks like: `1234567890123456`
4. **Save it** - you'll need this

### Step 2: Create `.env` File

Create `job-search-automation/backend/.env`:

```bash
INDEED_PUBLISHER_ID=your_publisher_id_here
```

### Step 3: Install Additional Package

```bash
cd job-search-automation/backend
pip install python-dotenv requests
```

### Step 4: Update job_scraper.py

I'll create a new file with Indeed integration.

---

## Option 2: Adzuna API (Also Free)

### Step 1: Get API Credentials

1. **Visit:** https://developer.adzuna.com/
2. **Sign up** for free account
3. **Get:** App ID and App Key
4. **Free tier:** 5,000 calls/month

### Step 2: Add to `.env`

```bash
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

---

## Option 3: LinkedIn Jobs (Harder - Requires Partnership)

LinkedIn doesn't have a public jobs API. You have two options:

**A. Use RapidAPI LinkedIn Scraper**
- Visit: https://rapidapi.com/rockapis-rockapis-default/api/linkedin-data-api
- Free tier: 100 requests/month
- Costs: $10/month for 1000 requests

**B. Web Scraping (Use Cautiously)**
- Against LinkedIn ToS
- Can get account banned
- Not recommended

---

## Quick Start: Indeed Publisher API

### Implementation (I'll create this for you)

File: `job-search-automation/backend/indeed_api.py`

```python
import os
import requests
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

class IndeedAPI:
    def __init__(self):
        self.publisher_id = os.getenv('INDEED_PUBLISHER_ID')
        if not self.publisher_id:
            raise ValueError("INDEED_PUBLISHER_ID not found in .env file")
        
        self.base_url = "http://api.indeed.com/ads/apisearch"
    
    def search_jobs(self, keywords: str, location: str, 
                   limit: int = 25, sort: str = 'relevance') -> List[Dict]:
        """Search Indeed jobs"""
        
        params = {
            'publisher': self.publisher_id,
            'q': keywords,
            'l': location,
            'sort': sort,
            'limit': limit,
            'format': 'json',
            'v': '2'
        }
        
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return self._format_results(data.get('results', []))
        else:
            raise Exception(f"Indeed API error: {response.status_code}")
    
    def _format_results(self, results: List[Dict]) -> List[Dict]:
        """Format Indeed results to our standard format"""
        formatted = []
        
        for job in results:
            formatted.append({
                'title': job.get('jobtitle'),
                'company': job.get('company'),
                'location': job.get('formattedLocation'),
                'description': job.get('snippet'),
                'url': job.get('url'),
                'posted_date': job.get('formattedRelativeTime'),
                'salary_range': None,  # Indeed doesn't always provide
                'job_type': job.get('jobtype'),
                'source': 'Indeed'
            })
        
        return formatted
```

---

## Testing Your API Integration

### Step 1: Test Indeed API Directly

```bash
cd job-search-automation/backend
python

>>> from indeed_api import IndeedAPI
>>> api = IndeedAPI()
>>> jobs = api.search_jobs("QA automation python", "Remote", limit=10)
>>> print(f"Found {len(jobs)} real jobs!")
>>> print(jobs[0])  # See first job
```

### Step 2: Update main.py to Use Real API

Change line in `job_scraper.py` or create a switch:

```python
USE_REAL_API = True  # Set to True once you have API key

if USE_REAL_API:
    from indeed_api import IndeedAPI
    self.indeed_api = IndeedAPI()
```

---

## Cost Comparison

| API | Free Tier | Cost | Best For |
|-----|-----------|------|----------|
| **Indeed Publisher** | Yes | Free | US jobs, large coverage |
| **Adzuna** | 5,000/month | Free | UK/EU jobs |
| **RapidAPI LinkedIn** | 100/month | $10/mo for 1000 | LinkedIn-specific |
| **The Muse** | Yes | Free | Startup/tech jobs |

---

## Recommended Approach

**Start with Indeed Publisher API:**
1. Free and easy to get approved
2. Largest US job database
3. Good API documentation
4. No rate limit issues for personal use

**Then add Adzuna** for more coverage.

---

## Next Steps

1. Sign up for Indeed Publisher: https://ads.indeed.com/jobroll/xmlfeed
2. Get your Publisher ID
3. I'll create the integration code
4. Test with your resume
5. Find real jobs!

Ready to get your Indeed Publisher ID? It takes ~5 minutes to sign up! 🚀

