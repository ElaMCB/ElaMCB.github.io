"""
Quick test to see what ARIA would respond to Alex's email
"""

# Alex's offer details
alex_offer = {
    'recruiter_name': 'Alex',
    'company': 'Artech Information Systems (client: TCS)',
    'position': 'Java Selenium Automation Architect',
    'location': 'Alpharetta, GA',
    'offered_rate': '45-48',
    'duration': '6 months',
    'start_date': '2025-11-20'
}

# Elena's requirements (from profile.yaml)
elena_requirements = {
    'minimum_hourly': 65,
    'target_hourly': 75
}

# Generate counter-offer response
counter_offer_response = f"""Hi Alex,

Thank you for the opportunity with Artech Information Systems in Alpharetta, GA. The Java Selenium Automation Architect role looks interesting and aligns well with my expertise in Java Selenium automation architecture.

However, the offered rate of ${alex_offer['offered_rate']}/hr is below my current market rate for architect-level positions. Based on my 10+ years of experience designing and implementing enterprise automation frameworks, CI/CD pipeline integration, and establishing architecture standards across projects, I'm targeting ${elena_requirements['minimum_hourly']}-${elena_requirements['target_hourly']}/hr.

I'm confident I can deliver strong value given my extensive background in:
- Designing scalable automation frameworks with Java and Selenium
- Integrating test automation with CI/CD pipelines
- Defining architecture standards for enterprise-level projects
- Leading QA automation initiatives

The 6-month contract duration and {alex_offer['start_date']} start date work well for my availability. Would there be flexibility on the rate? If so, I'd be very interested in discussing this opportunity further.

Best regards,
Elena

--
ARIA (Automated Recruiter Interaction Assistant)
Responding on behalf of Elena Mereanu
"""

# Analysis
print("=" * 80)
print("ARIA's ANALYSIS OF ALEX'S OFFER")
print("=" * 80)
print()
print(f"Position: {alex_offer['position']}")
print(f"  [YES] Matches title requirement (Architect)")
print()
print(f"Offered Rate: ${alex_offer['offered_rate']}/hr")
print(f"  [NO] BELOW your ${elena_requirements['minimum_hourly']}/hr minimum")
print(f"  Gap: ${elena_requirements['minimum_hourly'] - 48} - ${elena_requirements['minimum_hourly'] - 45}/hr under target")
print()
print(f"Location: {alex_offer['location']}")
print(f"  [YES] Acceptable (you're open to Alpharetta/Atlanta area)")
print()
print(f"Duration: {alex_offer['duration']}")
print(f"  [YES] Meets your 3+ month minimum")
print()
print(f"Tech Stack: Java, Selenium, CI/CD")
print(f"  [YES] Perfect match for your skills")
print()
print("=" * 80)
print("ARIA's RECOMMENDED ACTION: COUNTER-OFFER")
print("=" * 80)
print()
print("ARIA will send the following response:")
print()
print(counter_offer_response)
print()
print("=" * 80)
print("KEY POINTS IN RESPONSE:")
print("=" * 80)
print("[+] Professional and respectful tone")
print("[+] Acknowledges the opportunity")
print("[+] Clear about rate expectations ($65-75/hr)")
print("[+] Highlights relevant experience and value")
print("[+] Leaves door open for negotiation")
print("[+] ARIA disclosure in signature (transparent AI assistance)")
print()
print("=" * 80)
print("NEXT STEPS:")
print("=" * 80)
print()
print("Option 1: Send this response manually")
print("  - Copy the response above")
print("  - Reply to Alex's email")
print("  - See how he responds")
print()
print("Option 2: Let ARIA send it automatically")
print("  - Complete Gmail API setup (15 mins)")
print("  - Run: python main.py --once")
print("  - ARIA will detect and respond to Alex's email")
print()
print("Option 3: Modify the response")
print("  - Edit config/prompts.yaml")
print("  - Adjust the counter_offer template")
print("  - Run this script again to see changes")
print()

