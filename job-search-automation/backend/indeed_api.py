"""
Indeed Publisher API Integration
Get your Publisher ID: https://ads.indeed.com/jobroll/xmlfeed
"""

import os
import requests
from dotenv import load_dotenv
from typing import List, Dict
import time

load_dotenv()

class IndeedAPI:
    """
    Indeed Publisher API Integration
    
    Setup:
    1. Sign up at https://ads.indeed.com/jobroll/xmlfeed
    2. Get your Publisher ID
    3. Add to .env file: INDEED_PUBLISHER_ID=your_id_here
    """
    
    def __init__(self):
        self.publisher_id = os.getenv('INDEED_PUBLISHER_ID')
        if not self.publisher_id:
            print("⚠️  WARNING: INDEED_PUBLISHER_ID not found in .env file")
            print("   Sign up at: https://ads.indeed.com/jobroll/xmlfeed")
            print("   Then create .env file with: INDEED_PUBLISHER_ID=your_id")
            raise ValueError("INDEED_PUBLISHER_ID required")
        
        self.base_url = "http://api.indeed.com/ads/apisearch"
        self.rate_limit_delay = 1  # Respectful 1 second between calls
    
    def search_jobs(self, keywords: str, location: str = "", 
                   limit: int = 25, sort: str = 'relevance',
                   job_type: str = 'fulltime', radius: int = 25) -> List[Dict]:
        """
        Search Indeed for real job postings
        
        Args:
            keywords: Search terms (e.g., "QA automation python")
            location: City, state, or "remote"
            limit: Max results (25 max per request)
            sort: 'relevance' or 'date'
            job_type: 'fulltime', 'parttime', 'contract', 'internship', 'temporary'
            radius: Search radius in miles
        
        Returns:
            List of job postings in standard format
        """
        
        # Respect rate limiting
        time.sleep(self.rate_limit_delay)
        
        params = {
            'publisher': self.publisher_id,
            'q': keywords,
            'l': location,
            'sort': sort,
            'limit': min(limit, 25),  # Indeed max is 25 per request
            'format': 'json',
            'v': '2',
            'jt': job_type,
            'radius': radius,
            'useragent': 'Mozilla/5.0'  # Required by Indeed
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                total_results = data.get('totalResults', 0)
                results = data.get('results', [])
                
                print(f"✓ Indeed API: Found {total_results} total jobs, returning {len(results)}")
                
                return self._format_results(results)
            else:
                print(f"❌ Indeed API error: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return []
                
        except Exception as e:
            print(f"❌ Indeed API request failed: {e}")
            return []
    
    def _format_results(self, results: List[Dict]) -> List[Dict]:
        """Format Indeed results to our standard format"""
        formatted = []
        
        for job in results:
            # Extract full description (snippet is truncated)
            full_description = f"{job.get('snippet', '')} {job.get('formattedLocationFull', '')}"
            
            formatted.append({
                'title': job.get('jobtitle', 'Unknown Title'),
                'company': job.get('company', 'Unknown Company'),
                'location': job.get('formattedLocation', location),
                'description': full_description,
                'url': job.get('url', '#'),
                'posted_date': job.get('formattedRelativeTime', 'Recently posted'),
                'salary_range': None,  # Indeed API doesn't provide salary in free tier
                'job_type': job.get('formattedJobType', 'Full-time'),
                'source': 'Indeed',
                'job_key': job.get('jobkey')  # Unique identifier
            })
        
        return formatted

# Test the API
if __name__ == "__main__":
    try:
        api = IndeedAPI()
        
        print("\n🔍 Testing Indeed API...")
        print("Searching for: QA automation python engineer")
        print("Location: Remote\n")
        
        jobs = api.search_jobs(
            keywords="QA automation python engineer",
            location="Remote",
            limit=10
        )
        
        if jobs:
            print(f"\n✅ SUCCESS! Found {len(jobs)} REAL jobs:\n")
            
            for i, job in enumerate(jobs[:5], 1):
                print(f"{i}. {job['title']}")
                print(f"   Company: {job['company']}")
                print(f"   Location: {job['location']}")
                print(f"   Posted: {job['posted_date']}")
                print(f"   URL: {job['url'][:60]}...")
                print()
        else:
            print("No jobs found. Check your API key.")
            
    except ValueError as e:
        print(f"\n❌ {e}")
        print("\nTo get started:")
        print("1. Sign up at: https://ads.indeed.com/jobroll/xmlfeed")
        print("2. Get your Publisher ID")
        print("3. Create .env file with: INDEED_PUBLISHER_ID=your_id")

