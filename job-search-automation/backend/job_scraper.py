"""
Job Scraper - Ethical web scraping for job postings
"""

from typing import List, Dict
import asyncio
from datetime import datetime
import random
import os

# Try to import real API
try:
    from adzuna_api import AdzunaAPI
    REAL_API_AVAILABLE = True
except:
    REAL_API_AVAILABLE = False

class JobScraper:
    """
    Ethical job scraping with rate limiting and respectful practices
    
    NOTE: This is a demonstration. In production:
    - Use official APIs when available (LinkedIn API, Indeed API)
    - Respect robots.txt and rate limits
    - Implement exponential backoff
    - Cache results to minimize requests
    """
    
    def __init__(self):
        self.rate_limit_delay = 2  # seconds between requests
        self.cache = {}
        
        # Try to use real API if available
        self.use_real_api = REAL_API_AVAILABLE and os.getenv('ADZUNA_APP_ID')
        
        if self.use_real_api:
            try:
                self.adzuna_api = AdzunaAPI()
                print("✅ Using REAL Adzuna API for job search!")
            except:
                self.use_real_api = False
                print("⚠️  Adzuna API not configured, using demo data")
        else:
            print("⚠️  Using demo data (add Adzuna credentials for real jobs)")
    
    async def search_jobs(self, keywords: str, location: str, 
                         remote: bool = False, max_results: int = 20) -> List[Dict]:
        """
        Search for jobs across platforms
        """
        
        # Check cache first
        cache_key = f"{keywords}_{location}_{remote}"
        if cache_key in self.cache:
            print(f"📦 Returning {len(self.cache[cache_key][:max_results])} cached results")
            return self.cache[cache_key][:max_results]
        
        print(f"🔍 Searching for: {keywords} in {location}")
        
        # Use real API if available
        if self.use_real_api:
            print("   ✅ Fetching REAL jobs from Adzuna API...")
            try:
                jobs = self.adzuna_api.search_jobs(
                    keywords=keywords,
                    location=location,
                    results_per_page=max_results
                )
                
                if jobs:
                    self.cache[cache_key] = jobs
                    print(f"   ✅ Found {len(jobs)} REAL job postings!")
                    return jobs
                else:
                    print("   ⚠️  No jobs found, falling back to demo data")
            except Exception as e:
                print(f"   ❌ API error: {e}")
                print("   Falling back to demo data")
        
        # Fallback to demo data
        print("   Using demo data (configure Adzuna API for real jobs)")
        await asyncio.sleep(0.5)
        jobs = self._generate_sample_jobs(keywords, location, remote, max_results)
        self.cache[cache_key] = jobs
        
        return jobs
    
    def _generate_sample_jobs(self, keywords: str, location: str, 
                             remote: bool, count: int) -> List[Dict]:
        """
        Generate sample job postings for demonstration
        
        In production, replace this with actual scraping:
        - LinkedIn Jobs API
        - Indeed API
        - Glassdoor (if available)
        - Company career pages
        """
        
        companies = [
            'TechCorp', 'InnovateLabs', 'CloudScale', 'DataDriven Inc',
            'AgileWorks', 'QuantumSoft', 'NexGen Systems', 'DevOps Pro',
            'QualityFirst', 'AutomateX', 'TestMasters', 'CodeCraft'
        ]
        
        job_titles = [
            'Senior QA Engineer',
            'SDET - Test Automation',
            'Quality Automation Engineer',
            'Test Automation Architect',
            'QA Lead - Automation',
            'Software Engineer in Test',
            'DevOps QA Engineer',
            'Automation Framework Engineer'
        ]
        
        jobs = []
        
        for i in range(min(count, 50)):
            company = random.choice(companies)
            title = random.choice(job_titles)
            
            # Build description based on keywords
            description = f"""
We are seeking a {title} to join our quality engineering team.

Requirements:
- {random.randint(3, 8)}+ years of experience in test automation
- Strong proficiency in Python and test frameworks
- Experience with Playwright, Selenium, or Cypress
- CI/CD pipeline experience (Jenkins, GitHub Actions)
- Excellent communication and collaboration skills

Nice to have:
- Cloud platform experience (AWS, Azure, GCP)
- API testing and performance testing
- Agile/Scrum methodology
- Test strategy and framework design

Keywords: {keywords}
"""
            
            jobs.append({
                'title': title,
                'company': company,
                'location': location if not remote else 'Remote',
                'description': description.strip(),
                'url': f'https://example.com/jobs/{company.lower()}-{i}',
                'salary_range': f'${random.randint(100, 180)}K - ${random.randint(130, 220)}K',
                'posted_date': f'{random.randint(1, 14)} days ago',
                'job_type': 'Full-time',
                'experience_level': random.choice(['Mid-Level', 'Senior', 'Lead'])
            })
        
        return jobs

# Test the scraper
if __name__ == "__main__":
    async def test_scraper():
        scraper = JobScraper()
        jobs = await scraper.search_jobs(
            keywords="QA automation python",
            location="Remote",
            remote=True,
            max_results=5
        )
        
        print(f"\n✓ Found {len(jobs)} jobs:")
        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job['title']} at {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   Salary: {job['salary_range']}")
    
    asyncio.run(test_scraper())

