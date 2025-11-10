"""
ARIA's response to Alex's screening questionnaire
"""

# Your details (update these as needed)
your_details = {
    'total_experience': '10+ years',
    'current_location_zip': '30004',  # Update with your actual zip
    'preferred_location_zip': '30004 (Remote preferred, open to Alpharetta/Atlanta area)',
    'us_authorization': 'Yes',
    'sponsorship_needed': 'No',
    'w2_or_c2c': 'W2',
    'notice_period': '2 weeks',
    'interview_availability': 'Flexible - evenings and weekends preferred'
}

# Generate response
response = f"""Hi Alex,

Thank you for following up. I'd be happy to provide the requested information.

**Professional Summary:**
- **Total Experience:** {your_details['total_experience']} in test automation and QA architecture

**Technical Competencies:**

**Automation Frameworks with Java and Selenium WebDriver:**
I have extensive experience designing and implementing scalable automation frameworks from scratch using Java and Selenium WebDriver. This includes:
- Architecting Page Object Model (POM) and hybrid frameworks
- Implementing data-driven and keyword-driven approaches
- Building reusable component libraries and utility classes
- Optimizing test execution for parallel and distributed testing
- Establishing coding standards and best practices for test automation teams

**Integration with CI/CD Pipelines and Test Management Tools:**
Strong background in integrating test automation with enterprise CI/CD ecosystems:
- Jenkins pipeline integration with automated test execution and reporting
- GitHub Actions and GitLab CI/CD workflow implementation
- Integration with test management tools (TestRail, Zephyr, qTest)
- Automated reporting and notifications (Slack, email, dashboards)
- Docker containerization for test environments
- Cloud-based test execution (AWS, Azure)

**Logistics:**
- **Current Location:** {your_details['current_location_zip']}
- **Preferred Location:** {your_details['preferred_location_zip']}
- **US Work Authorization:** {your_details['us_authorization']}
- **Sponsorship Needed:** {your_details['sponsorship_needed']}
- **W2 or C2C:** {your_details['w2_or_c2c']} preferred
- **Notice Period:** {your_details['notice_period']}
- **Interview Availability:** {your_details['interview_availability']}

**Important Note on Compensation:**
As mentioned in my previous email, I'm targeting **$65-75/hr** for architect-level contract positions based on my experience and the market rate for this level of expertise. I'd appreciate if you could confirm whether opportunities in this range are available before we proceed further with the interview process.

I'm excited about the possibility of working with quality automation opportunities that align with my experience level and compensation expectations. Please let me know if you have positions that meet these criteria.

Looking forward to your response.

Best regards,
Elena

--
ARIA (Automated Recruiter Interaction Assistant)
Responding on behalf of Elena Mereanu
"""

print("=" * 80)
print("ARIA'S RESPONSE TO ALEX'S SCREENING QUESTIONS")
print("=" * 80)
print()
print(response)
print()
print("=" * 80)
print("KEY POINTS:")
print("=" * 80)
print("[+] Provides all requested information professionally")
print("[+] Details technical experience with specific examples")
print("[+] RE-EMPHASIZES the $65-75/hr requirement (important!)")
print("[+] Asks for confirmation on rate before proceeding")
print("[+] Maintains professional but firm stance on compensation")
print("[+] ARIA disclosure included")
print()
print("=" * 80)
print("STRATEGY:")
print("=" * 80)
print()
print("Notice that Alex didn't address your rate concern in his response.")
print("He's collecting info to 'get back with the most relevant opportunity.'")
print()
print("This could mean:")
print("1. He's looking for other clients who can pay $65-75/hr")
print("2. He's hoping you'll forget about the rate and accept $45-48")
print("3. He needs your info to present to the client for rate negotiation")
print()
print("ARIA's response:")
print("- Provides all the info he needs")
print("- CLEARLY re-states the $65-75/hr requirement")
print("- Asks him to confirm rate availability BEFORE interviews")
print("- Saves your time if he can't meet the rate")
print()
print("=" * 80)
print("UPDATE YOUR DETAILS:")
print("=" * 80)
print()
print("Before sending, update these in the script:")
print(f"  - current_location_zip: '{your_details['current_location_zip']}'")
print(f"  - preferred_location_zip: '{your_details['preferred_location_zip']}'")
print(f"  - interview_availability: '{your_details['interview_availability']}'")
print()
print("Then run: python alex_screening_response.py")
print()


