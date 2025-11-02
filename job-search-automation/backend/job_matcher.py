"""
Job Matcher - AI-powered job matching algorithm
"""

from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JobMatcher:
    """Match jobs to candidate profile using NLP and ML"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2)
        )
    
    def rank_jobs(self, jobs: List[Dict], profile: Dict) -> List[Dict]:
        """Rank jobs by match score"""
        
        if not jobs:
            return []
        
        # Build candidate profile text
        profile_text = self._build_profile_text(profile)
        
        # Build job description texts
        job_texts = [self._build_job_text(job) for job in jobs]
        
        # Calculate similarity scores
        try:
            # Fit vectorizer on all texts
            all_texts = [profile_text] + job_texts
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            
            # Calculate cosine similarity
            profile_vector = tfidf_matrix[0:1]
            job_vectors = tfidf_matrix[1:]
            
            similarities = cosine_similarity(profile_vector, job_vectors)[0]
            
            # Add scores and reasons to jobs
            ranked_jobs = []
            for job, score in zip(jobs, similarities):
                match_reasons = self._generate_match_reasons(job, profile, score)
                
                ranked_jobs.append({
                    **job,
                    'match_score': float(score),
                    'match_reasons': match_reasons
                })
            
            # Sort by match score descending
            ranked_jobs.sort(key=lambda x: x['match_score'], reverse=True)
            
            return ranked_jobs
            
        except Exception as e:
            print(f"Matching error: {e}")
            # Fallback: return jobs with neutral scores
            return [{**job, 'match_score': 0.5, 'match_reasons': ['Analysis pending']} 
                    for job in jobs]
    
    def _build_profile_text(self, profile: Dict) -> str:
        """Build searchable text from profile"""
        parts = []
        
        # Add skills multiple times for weight
        if 'skills' in profile:
            skills_text = " ".join(profile['skills']) * 3
            parts.append(skills_text)
        
        # Add preferred roles
        if 'preferred_roles' in profile:
            roles_text = " ".join(profile['preferred_roles']) * 2
            parts.append(roles_text)
        
        # Add experience level
        if 'experience_years' in profile:
            exp_text = f"senior experienced professional {profile['experience_years']} years"
            parts.append(exp_text)
        
        return " ".join(parts)
    
    def _build_job_text(self, job: Dict) -> str:
        """Build searchable text from job posting"""
        parts = [
            job.get('title', ''),
            job.get('company', ''),
            job.get('description', ''),
            job.get('location', '')
        ]
        return " ".join(parts)
    
    def _generate_match_reasons(self, job: Dict, profile: Dict, score: float) -> List[str]:
        """Generate human-readable match reasons"""
        reasons = []
        
        # Skill matching
        if 'skills' in profile:
            job_text_lower = self._build_job_text(job).lower()
            matched_skills = [s for s in profile['skills'] 
                            if s.lower() in job_text_lower]
            
            if len(matched_skills) >= 3:
                reasons.append(f"Strong skill match: {', '.join(matched_skills[:3])}")
        
        # Role matching
        if 'preferred_roles' in profile:
            for role in profile['preferred_roles']:
                if role.lower() in job.get('title', '').lower():
                    reasons.append(f"Matches preferred role: {role}")
                    break
        
        # Location match
        if 'preferred_locations' in profile:
            job_location = job.get('location', '').lower()
            for pref_loc in profile['preferred_locations']:
                if pref_loc.lower() in job_location or 'remote' in job_location:
                    reasons.append(f"Location match: {job.get('location', 'Remote')}")
                    break
        
        # Overall score interpretation
        if score > 0.7:
            reasons.append("Excellent overall match")
        elif score > 0.5:
            reasons.append("Good potential fit")
        else:
            reasons.append("Moderate match")
        
        return reasons[:4]  # Top 4 reasons

# Test the matcher
if __name__ == "__main__":
    matcher = JobMatcher()
    
    # Sample data
    profile = {
        'skills': ['Python', 'Playwright', 'Selenium', 'CI/CD', 'AWS'],
        'experience_years': 8,
        'preferred_roles': ['QA Engineer', 'SDET', 'Test Automation Engineer'],
        'preferred_locations': ['Remote', 'San Francisco']
    }
    
    jobs = [
        {
            'title': 'Senior SDET - Test Automation',
            'company': 'Tech Corp',
            'location': 'Remote',
            'description': 'Looking for SDET with Python, Playwright, and CI/CD experience. AWS knowledge required.',
            'url': 'https://example.com/job1'
        },
        {
            'title': 'Backend Developer',
            'company': 'StartupXYZ',
            'location': 'New York',
            'description': 'Node.js developer needed for API development',
            'url': 'https://example.com/job2'
        }
    ]
    
    ranked = matcher.rank_jobs(jobs, profile)
    
    print("\n🎯 Job Matching Results:")
    for i, job in enumerate(ranked, 1):
        print(f"\n{i}. {job['title']} at {job['company']}")
        print(f"   Match Score: {job['match_score']:.2%}")
        print(f"   Reasons: {', '.join(job['match_reasons'])}")

