"""
Adzuna API Integration - Get instant API access (no approval wait!)
Sign up: https://developer.adzuna.com/signup
"""

import os
import requests
from dotenv import load_dotenv
from typing import List, Dict
import time

load_dotenv()

class AdzunaAPI:
    """
    Adzuna Jobs API - Instant Access
    
    Setup:
    1. Sign up at https://developer.adzuna.com/signup
    2. Get App ID and App Key instantly
    3. Add to .env: ADZUNA_APP_ID=xxx and ADZUNA_APP_KEY=xxx
    
    Free Tier: 5,000 API calls/month
    """
    
    def __init__(self):
        self.app_id = os.getenv('ADZUNA_APP_ID')
        self.app_key = os.getenv('ADZUNA_APP_KEY')
        
        if not self.app_id or not self.app_key:
            print("⚠️  WARNING: Adzuna credentials not found in .env")
            print("   Sign up at: https://developer.adzuna.com/signup")
            print("   Add to .env: ADZUNA_APP_ID and ADZUNA_APP_KEY")
            raise ValueError("Adzuna credentials required")
        
        # API endpoints by country
        self.base_urls = {
            'us': 'https://api.adzuna.com/v1/api/jobs/us/search',
            'uk': 'https://api.adzuna.com/v1/api/jobs/gb/search',
            'ca': 'https://api.adzuna.com/v1/api/jobs/ca/search'
        }
        
        self.country = 'us'  # Default to US
        self.rate_limit_delay = 0.5
    
    def search_jobs(self, keywords: str, location: str = "", 
                   page: int = 1, results_per_page: int = 20,
                   sort_by: str = 'relevance') -> List[Dict]:
        """
        Search Adzuna for real job postings
        
        Args:
            keywords: What job to search for
            location: City or state (can be empty for all locations)
            page: Page number (starts at 1)
            results_per_page: Jobs per page (max 50)
            sort_by: 'relevance', 'date', or 'salary'
        
        Returns:
            List of real job postings
        """
        
        # Respect rate limiting
        time.sleep(self.rate_limit_delay)
        
        # Build API URL
        url = f"{self.base_urls[self.country]}/{page}"
        
        params = {
            'app_id': self.app_id,
            'app_key': self.app_key,
            'results_per_page': min(results_per_page, 50),
            'what': keywords,
            'where': location,
            'sort_by': sort_by,
            'content-type': 'application/json'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                total_results = data.get('count', 0)
                results = data.get('results', [])
                
                print(f"✓ Adzuna API: Found {total_results} total jobs, returning {len(results)}")
                
                return self._format_results(results)
            elif response.status_code == 401:
                print(f"❌ Adzuna authentication failed. Check your APP_ID and APP_KEY")
                return []
            else:
                print(f"❌ Adzuna API error: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return []
                
        except Exception as e:
            print(f"❌ Adzuna API request failed: {e}")
            return []
    
    def _format_results(self, results: List[Dict]) -> List[Dict]:
        """Format Adzuna results to our standard format"""
        formatted = []
        
        for job in results:
            # Adzuna provides detailed data
            formatted.append({
                'title': job.get('title', 'Unknown Title'),
                'company': job.get('company', {}).get('display_name', 'Unknown Company'),
                'location': job.get('location', {}).get('display_name', 'Unknown Location'),
                'description': job.get('description', ''),
                'url': job.get('redirect_url', '#'),
                'posted_date': job.get('created', 'Unknown date'),
                'salary_range': self._format_salary(job),
                'job_type': job.get('contract_type', 'Full-time'),
                'source': 'Adzuna',
                'category': job.get('category', {}).get('label', 'Unknown')
            })
        
        return formatted
    
    def _format_salary(self, job: Dict) -> str:
        """Format salary information if available"""
        salary_min = job.get('salary_min')
        salary_max = job.get('salary_max')
        
        if salary_min and salary_max:
            return f"${int(salary_min/1000)}K - ${int(salary_max/1000)}K"
        elif salary_min:
            return f"${int(salary_min/1000)}K+"
        else:
            return None

# Test the API
if __name__ == "__main__":
    try:
        api = AdzunaAPI()
        
        print("\n🔍 Testing Adzuna API...")
        print("Searching for: QA automation engineer")
        print("Location: Remote\n")
        
        jobs = api.search_jobs(
            keywords="QA automation engineer python",
            location="",  # Empty = all locations
            results_per_page=10
        )
        
        if jobs:
            print(f"\n✅ SUCCESS! Found {len(jobs)} REAL jobs from Adzuna:\n")
            
            for i, job in enumerate(jobs[:5], 1):
                print(f"{i}. {job['title']}")
                print(f"   Company: {job['company']}")
                print(f"   Location: {job['location']}")
                print(f"   Salary: {job['salary_range'] or 'Not specified'}")
                print(f"   Posted: {job['posted_date']}")
                print(f"   URL: {job['url'][:60]}...")
                print()
                
            print(f"💡 These are REAL job postings you can apply to!")
        else:
            print("No jobs found. Check your credentials.")
            
    except ValueError as e:
        print(f"\n❌ Setup Required:")
        print(f"   {e}")
        print("\n📝 Quick Setup (2 minutes):")
        print("1. Visit: https://developer.adzuna.com/signup")
        print("2. Sign up (instant approval!)")
        print("3. Copy your App ID and App Key")
        print("4. Create backend/.env file:")
        print("   ADZUNA_APP_ID=your_app_id")
        print("   ADZUNA_APP_KEY=your_app_key")
        print("5. Run: python adzuna_api.py")

