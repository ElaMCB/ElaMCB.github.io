# Job Search Automation - Backend

## Quick Start

### 1. Install Dependencies

```bash
cd job-search-automation/backend
pip install -r requirements.txt
```

### 2. Download spaCy Model (for NLP)

```bash
python -m spacy download en_core_web_sm
```

### 3. Run the API Server

```bash
python main.py
```

The API will start at `http://localhost:8000`

### 4. Test the API

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## API Endpoints

### Upload Resume
```bash
POST /upload-resume
Content-Type: multipart/form-data

# Upload your resume (PDF, DOCX, or TXT)
curl -X POST "http://localhost:8000/upload-resume" \
  -F "file=@your-resume.pdf"
```

### Search Jobs
```bash
POST /search-jobs
Content-Type: application/json

{
  "keywords": "QA automation python",
  "location": "Remote",
  "experience_level": "senior",
  "remote": true,
  "max_results": 20
}
```

### Match Jobs to Your Profile
```bash
POST /match-jobs
Content-Type: application/json

{
  "skills": ["Python", "Playwright", "CI/CD"],
  "experience_years": 8,
  "preferred_roles": ["QA Engineer", "SDET"],
  "preferred_locations": ["Remote", "San Francisco"]
}
```

## Testing Your Resume

1. **Upload your resume:**
```bash
curl -X POST "http://localhost:8000/upload-resume" \
  -F "file=@Elena_Mereanu_Resume.pdf"
```

2. **Use the extracted profile** to search for matching jobs:
```bash
curl -X POST "http://localhost:8000/match-jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["Python", "Playwright", "Selenium", "CI/CD", "AWS"],
    "experience_years": 8,
    "preferred_roles": ["QA Engineer", "SDET", "Test Automation Engineer"],
    "preferred_locations": ["Remote"]
  }'
```

3. **Review matches** - jobs ranked by AI with match scores and reasons

## Components

- `main.py` - FastAPI application with API endpoints
- `resume_parser.py` - Extract skills from PDF/DOCX/TXT resumes
- `job_matcher.py` - AI-powered job ranking using TF-IDF and cosine similarity
- `job_scraper.py` - Ethical job scraping (currently demo data, extensible to real scraping)

## Ethical Automation Notes

This implementation:
- ✅ Uses sample data for demonstration (no actual scraping yet)
- ✅ Implements rate limiting and delays
- ✅ Designed to use official APIs when available
- ✅ Respects platform ToS and robots.txt
- ✅ Focuses on quality matching over quantity

## Next Steps

To make this production-ready:
1. Integrate LinkedIn Jobs API (requires API key)
2. Add Indeed Publisher API integration
3. Implement proper caching with Redis
4. Add database for tracking applications
5. Build authentication for multi-user support

