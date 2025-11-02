"""
Resume Parser - Extract skills and experience from resumes
"""

import re
from typing import Dict, List
import PyPDF2
import docx
from io import BytesIO

class ResumeParser:
    """Parse resumes and extract structured information"""
    
    def __init__(self):
        # Common technical skills (expandable)
        self.tech_skills = {
            'python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'fastapi', 'django', 'flask',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
            'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'git', 'ci/cd', 'jenkins', 'github actions',
            'machine learning', 'nlp', 'deep learning', 'tensorflow', 'pytorch',
            'rest api', 'graphql', 'microservices', 'agile', 'scrum',
            'playwright', 'selenium', 'cypress', 'jest', 'pytest',
            'qa', 'sdet', 'test automation', 'quality assurance'
        }
    
    def parse_resume(self, file_contents: bytes, filename: str) -> Dict:
        """Parse resume and extract key information"""
        
        # Extract text based on file type
        if filename.endswith('.pdf'):
            text = self._parse_pdf(file_contents)
        elif filename.endswith('.docx'):
            text = self._parse_docx(file_contents)
        else:
            # Assume plain text
            text = file_contents.decode('utf-8')
        
        # Extract information
        skills = self._extract_skills(text)
        experience_years = self._extract_experience(text)
        education = self._extract_education(text)
        roles = self._extract_roles(text)
        
        return {
            'skills': skills,
            'experience_years': experience_years,
            'education': education,
            'preferred_roles': roles,
            'raw_text': text[:500]  # First 500 chars for context
        }
    
    def _parse_pdf(self, file_contents: bytes) -> str:
        """Extract text from PDF"""
        try:
            pdf_file = BytesIO(file_contents)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            return text
        except Exception as e:
            print(f"PDF parsing error: {e}")
            return ""
    
    def _parse_docx(self, file_contents: bytes) -> str:
        """Extract text from DOCX"""
        try:
            doc_file = BytesIO(file_contents)
            doc = docx.Document(doc_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text
        except Exception as e:
            print(f"DOCX parsing error: {e}")
            return ""
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.tech_skills:
            # Look for skill as whole word or in common variations
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill.title())
        
        return sorted(list(set(found_skills)))
    
    def _extract_experience(self, text: str) -> int:
        """Estimate years of experience"""
        # Look for patterns like "5 years", "5+ years", "2-5 years"
        patterns = [
            r'(\d+)\+?\s*years?\s*of\s*experience',
            r'(\d+)\s*years?\s*in',
            r'experience.*?(\d+)\s*years?'
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                try:
                    years.append(int(match))
                except:
                    pass
        
        # Return max found or estimate from resume length
        if years:
            return max(years)
        
        # Fallback: estimate from resume structure
        job_count = len(re.findall(r'\d{4}\s*-\s*(?:\d{4}|present)', text.lower()))
        return min(job_count * 2, 15) if job_count > 0 else 3
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education degrees"""
        degrees = []
        degree_keywords = ['bachelor', 'master', 'phd', 'mba', 'bs', 'ms', 'ba', 'ma']
        
        for keyword in degree_keywords:
            if keyword in text.lower():
                degrees.append(keyword.title())
        
        return degrees
    
    def _extract_roles(self, text: str) -> List[str]:
        """Extract job roles/titles from resume"""
        common_roles = [
            'QA Engineer', 'SDET', 'Test Automation Engineer', 'Quality Engineer',
            'Software Engineer', 'Full Stack Developer', 'Backend Developer',
            'Frontend Developer', 'DevOps Engineer', 'Data Engineer',
            'QA Lead', 'QA Manager', 'Test Manager', 'Automation Architect'
        ]
        
        found_roles = []
        text_lower = text.lower()
        
        for role in common_roles:
            if role.lower() in text_lower:
                found_roles.append(role)
        
        return found_roles[:5]  # Top 5 roles

# Test the parser
if __name__ == "__main__":
    parser = ResumeParser()
    
    # Test with sample text
    sample_text = """
    Senior QA Engineer with 8 years of experience in test automation.
    Skills: Python, Playwright, Selenium, JavaScript, React, CI/CD, AWS
    Master's degree in Computer Science
    """
    
    # Simulate parsing
    result = parser.parse_resume(sample_text.encode(), "resume.txt")
    print("Parsed Resume:")
    print(json.dumps(result, indent=2))

