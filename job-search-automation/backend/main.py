#!/usr/bin/env python3
"""
Job Search Automation - FastAPI Backend
Ethical automation for intelligent job matching
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
import json

from job_matcher import JobMatcher
from resume_parser import ResumeParser
from job_scraper import JobScraper

app = FastAPI(title="Job Search Automation API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
job_matcher = JobMatcher()
resume_parser = ResumeParser()
job_scraper = JobScraper()

# Data models
class JobSearchRequest(BaseModel):
    keywords: str
    location: str
    experience_level: str
    remote: bool = False
    max_results: int = 20

class JobMatch(BaseModel):
    title: str
    company: str
    location: str
    description: str
    url: str
    match_score: float
    match_reasons: List[str]
    salary_range: Optional[str] = None
    posted_date: Optional[str] = None

class UserProfile(BaseModel):
    skills: List[str]
    experience_years: int
    preferred_roles: List[str]
    preferred_locations: List[str]
    salary_expectation: Optional[int] = None

# API Endpoints

@app.get("/")
async def root():
    return {
        "message": "Job Search Automation API",
        "status": "active",
        "version": "1.0.0"
    }

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse resume to extract skills and experience"""
    try:
        contents = await file.read()
        
        # Parse resume
        profile = resume_parser.parse_resume(contents, file.filename)
        
        return {
            "success": True,
            "profile": profile,
            "message": f"Resume parsed successfully. Found {len(profile['skills'])} skills."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume parsing failed: {str(e)}")

@app.post("/search-jobs")
async def search_jobs(request: JobSearchRequest):
    """Search for jobs across multiple platforms"""
    try:
        # Scrape jobs from platforms (respecting rate limits)
        jobs = await job_scraper.search_jobs(
            keywords=request.keywords,
            location=request.location,
            remote=request.remote,
            max_results=request.max_results
        )
        
        return {
            "success": True,
            "total_jobs": len(jobs),
            "jobs": jobs,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")

@app.post("/match-jobs")
async def match_jobs(profile: UserProfile):
    """Match jobs against user profile using AI"""
    try:
        # Get recent jobs from cache/database
        # For demo, we'll search based on profile
        search_keywords = ", ".join(profile.preferred_roles[:3])
        
        jobs = await job_scraper.search_jobs(
            keywords=search_keywords,
            location=profile.preferred_locations[0] if profile.preferred_locations else "Remote",
            remote=True,
            max_results=50
        )
        
        # Use AI to match jobs
        matched_jobs = job_matcher.rank_jobs(jobs, profile.dict())
        
        # Return top matches
        top_matches = matched_jobs[:20]
        
        return {
            "success": True,
            "total_analyzed": len(jobs),
            "top_matches": len(top_matches),
            "matches": top_matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job matching failed: {str(e)}")

@app.get("/analytics")
async def get_analytics():
    """Get job search analytics and insights"""
    # This would pull from database in production
    return {
        "applications_sent": 0,
        "interviews_scheduled": 0,
        "offers_received": 0,
        "avg_match_score": 0.0,
        "top_companies": [],
        "trending_skills": []
    }

if __name__ == "__main__":
    print("🚀 Starting Job Search Automation API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

