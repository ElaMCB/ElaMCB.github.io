# Quick Start Guide - Test It With Your Resume!

## Prerequisites

- Python 3.8+ installed
- Your resume in PDF, DOCX, or TXT format

## Step-by-Step Setup

### 1. Install Dependencies

```bash
cd job-search-automation/backend
pip install -r requirements.txt
```

### 2. Download NLP Model (One-time setup)

```bash
python -m spacy download en_core_web_sm
```

### 3. Start the API Server

```bash
python main.py
```

You should see:
```
🚀 Starting Job Search Automation API...
📍 API will be available at: http://localhost:8000
📚 Documentation: http://localhost:8000/docs
```

### 4. Open the Dashboard

In a **new terminal/browser**, open:
```
job-search-automation/dashboard.html
```

Or visit: `file:///path/to/job-search-automation/dashboard.html`

## Using the Dashboard

### Option 1: With Your Resume (Recommended)

1. **Click "Click to upload your resume"**
2. **Select your resume file** (Elena_Mereanu_Resume.pdf)
3. **Wait for parsing** - it will extract your skills automatically
4. **Click "Find Matching Jobs"**
5. **Review AI-matched results** ranked by relevance

### Option 2: Without Resume

1. **Enter keywords** (e.g., "QA automation python")
2. **Enter location** (e.g., "Remote")
3. **Click "Find Matching Jobs"**
4. **Get results** (without personalized matching)

## What You'll See

- **Match Scores:** 0-100% how well each job fits your profile
- **Match Reasons:** Why the AI thinks it's a good fit
- **Job Details:** Title, company, location, salary, posting date
- **Direct Links:** Click to apply on the actual job board

## Testing With Your Resume

```bash
# Test the resume parser directly
cd backend
python resume_parser.py

# Test the job matcher
python job_matcher.py

# Test the scraper
python job_scraper.py
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API docs (Swagger UI)

## Troubleshooting

**Issue:** "Connection refused" or "Failed to fetch"  
**Fix:** Make sure the API server is running (`python main.py`)

**Issue:** "Resume parsing failed"  
**Fix:** Check that your resume is a valid PDF/DOCX file

**Issue:** "No jobs found"  
**Fix:** Try broader keywords like "software engineer" or "quality assurance"

## Current Capabilities

✅ **Working Now:**
- Resume parsing (PDF, DOCX, TXT)
- Skill extraction from your resume
- AI-powered job matching with TF-IDF and cosine similarity
- Match score calculation with explanations
- Sample job data for testing

⚠️ **Demo Mode:**
- Currently using sample job data (not real scraping)
- To add real scraping: See `backend/job_scraper.py` comments

## Next Steps

To make this production-ready with real job data:

1. **Add LinkedIn API:** Get API key and integrate
2. **Add Indeed API:** Sign up for Indeed Publisher API
3. **Add Caching:** Use Redis to store results
4. **Add Database:** Track applications and history

But you can **test the matching algorithm RIGHT NOW** with your actual resume! 🎯

