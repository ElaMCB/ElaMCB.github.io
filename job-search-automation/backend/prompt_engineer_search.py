"""
Prompt Engineer Job Search Automation
Integrates with existing job-search-automation and ARIA

Searches for entry/mid-level prompt engineer roles
Filters by remote and salary requirements
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()


class PromptEngineerJobSearch:
    """Automated search for prompt engineer positions"""
    
    def __init__(self):
        self.adzuna_app_id = os.getenv('ADZUNA_APP_ID')
        self.adzuna_app_key = os.getenv('ADZUNA_APP_KEY')
        self.min_salary = 100000  # $50/hr equivalent annually
        self.max_salary = 150000  # $75/hr equivalent
        
    def search_adzuna(self, role='prompt engineer', location='remote'):
        """Search Adzuna API for prompt engineer jobs"""
        
        if not self.adzuna_app_id or not self.adzuna_app_key:
            print("Adzuna API credentials not configured!")
            print("Get free API access at: https://developer.adzuna.com/signup")
            return []
        
        base_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
        
        params = {
            'app_id': self.adzuna_app_id,
            'app_key': self.adzuna_app_key,
            'what': role,
            'where': location,
            'salary_min': self.min_salary,
            'max_days_old': 14,  # Last 2 weeks
            'results_per_page': 50
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            jobs = data.get('results', [])
            
            # Filter out senior roles
            filtered_jobs = []
            excluded_keywords = ['senior', 'lead', 'principal', 'staff', 'director', 'head of']
            
            for job in jobs:
                title = job.get('title', '').lower()
                
                # Skip if has senior keywords
                if any(keyword in title for keyword in excluded_keywords):
                    continue
                
                filtered_jobs.append({
                    'title': job.get('title'),
                    'company': job.get('company', {}).get('display_name', 'Unknown'),
                    'location': job.get('location', {}).get('display_name', 'Remote'),
                    'salary_min': job.get('salary_min'),
                    'salary_max': job.get('salary_max'),
                    'description': job.get('description', '')[:500],
                    'url': job.get('redirect_url'),
                    'created': job.get('created'),
                    'category': job.get('category', {}).get('label', '')
                })
            
            return filtered_jobs
            
        except Exception as e:
            print(f"Error searching Adzuna: {e}")
            return []
    
    def search_all_sources(self):
        """Search all available job sources"""
        all_jobs = []
        
        print("Searching for Prompt Engineer roles...")
        print()
        
        # Search Adzuna
        print("1. Searching Adzuna API...")
        adzuna_jobs = self.search_adzuna()
        all_jobs.extend(adzuna_jobs)
        print(f"   Found {len(adzuna_jobs)} jobs")
        
        # Could add more sources here (Indeed API, LinkedIn, etc.)
        
        return all_jobs
    
    def display_results(self, jobs):
        """Display job search results"""
        
        if not jobs:
            print("\nNo jobs found matching criteria.")
            print("Try:")
            print("  - Lowering salary filter")
            print("  - Broader search terms")
            print("  - Checking job boards manually")
            return
        
        print("\n" + "="*80)
        print(f"FOUND {len(jobs)} PROMPT ENGINEER JOBS")
        print("="*80)
        print()
        
        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Location: {job['location']}")
            
            if job.get('salary_min') and job.get('salary_max'):
                annual_min = job['salary_min']
                annual_max = job['salary_max']
                hourly_min = annual_min / 2080  # Convert to hourly (assumes 40hrs/week)
                hourly_max = annual_max / 2080
                
                print(f"   Salary: ${annual_min:,.0f}-${annual_max:,.0f}/year (${hourly_min:.0f}-${hourly_max:.0f}/hr)")
            
            print(f"   Category: {job['category']}")
            print(f"   Posted: {job['created']}")
            print(f"   URL: {job['url']}")
            print()
        
        print("="*80)
    
    def export_to_csv(self, jobs, filename='prompt_engineer_jobs.csv'):
        """Export jobs to CSV for review"""
        import csv
        
        if not jobs:
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
            writer.writeheader()
            writer.writerows(jobs)
        
        print(f"\nExported {len(jobs)} jobs to {filename}")


def main():
    """Main search function"""
    searcher = PromptEngineerJobSearch()
    
    print("="*80)
    print("PROMPT ENGINEER JOB SEARCH - AUTOMATED")
    print("="*80)
    print()
    print("Criteria:")
    print(f"  - Role: Prompt Engineer (entry/mid level)")
    print(f"  - Location: Remote")
    print(f"  - Min Salary: ${searcher.min_salary:,}/year (~$50/hr)")
    print(f"  - Max Salary: ${searcher.max_salary:,}/year (~$75/hr)")
    print(f"  - Excludes: Senior, Lead, Principal roles")
    print()
    print("="*80)
    print()
    
    # Search
    jobs = searcher.search_all_sources()
    
    # Display
    searcher.display_results(jobs)
    
    # Export
    if jobs:
        searcher.export_to_csv(jobs)
    
    print()
    print("NEXT STEPS:")
    print("-"*80)
    print("1. Review the jobs above")
    print("2. Visit company career pages directly")
    print("3. Set up LinkedIn job alerts")
    print("4. Let ARIA handle any recruiter responses!")
    print()


if __name__ == "__main__":
    main()

