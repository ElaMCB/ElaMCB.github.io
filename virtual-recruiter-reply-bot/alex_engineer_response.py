"""
ARIA's response to Alex's Automation Test Engineer offer ($38-42/hr)
"""

# Alex's new offer
offer = {
    'position': 'Automation Test Engineer',
    'level': 'mid-level',  # Not architect
    'rate': '$38-42/hr',
    'location': 'Atlanta, GA',
    'duration': '6 months',
    'start_date': '2025-11-11'
}

# Your requirements
your_rates = {
    'architect_minimum': 65,
    'architect_target': 75,
    'mid_level_minimum': 50,
    'mid_level_target': 55
}

# Analysis
print("="*80)
print("ARIA'S ANALYSIS - ALEX'S NEW OFFER")
print("="*80)
print()
print(f"Position: {offer['position']}")
print(f"  Level: Mid-level Engineer (NOT Architect)")
print()
print(f"Offered Rate: {offer['rate']}")
print(f"  [NO] BELOW your ${your_rates['mid_level_minimum']}/hr minimum for mid-level")
print(f"  Gap: $8-12/hr under your minimum")
print()
print(f"Location: {offer['location']}")
print(f"  [YES] Atlanta acceptable")
print()
print(f"Duration: {offer['duration']}")
print(f"  [YES] Meets your 3+ month minimum")
print()
print("PATTERN DETECTED:")
print("  - First offer: $45-48/hr for ARCHITECT role")
print("  - Second offer: $38-42/hr for ENGINEER role")
print("  Alex is going LOWER each time!")
print("  Strategy: Testing your rate flexibility")
print()
print("="*80)
print("ARIA'S RECOMMENDATION: POLITE DECLINE")
print("="*80)
print()
print("Why decline:")
print("  1. Rate is 20-30% below your minimum")
print("  2. Alex is pattern-testing your flexibility")
print("  3. Better to wait for $50-75/hr opportunities")
print("  4. You have 3 other good leads (Addison, ADP, Mirnal)")
print()
print("="*80)
print("ARIA'S RESPONSE:")
print("="*80)
print()

response = f"""Hi Alex,

Thank you for thinking of me for the Automation Test Engineer position.

While I have the technical skills required (Selenium, test automation frameworks, TestNG/JUnit), the offered rate of $38-42/hr is significantly below my current market rate.

For context on my rate expectations:
- **Mid-level automation engineer roles:** $50-55/hr minimum
- **Architect-level positions** (like the TCS role we previously discussed): $65-75/hr

I appreciate you keeping me in mind for opportunities. If you have positions at these rate levels, I'd be very interested in discussing them.

Thank you for your continued outreach.

Best regards,
Elena

--
ARIA (Automated Recruiter Interaction Assistant)
Responding on behalf of Elena Mereanu
"""

print(response)
print()
print("="*80)
print("KEY POINTS:")
print("="*80)
print("[+] Professional and respectful")
print("[+] Clearly states BOTH rate tiers (architect vs engineer)")
print("[+] Firm on minimums ($50/hr and $65/hr)")
print("[+] Leaves door open for future opportunities")
print("[+] Doesn't waste time explaining experience (he already knows)")
print("[+] ARIA disclosure for transparency")
print()
print("="*80)
print("WHAT HAPPENS NEXT:")
print("="*80)
print()
print("Likely outcomes:")
print("  1. Alex stops contacting you (he can't meet your rates)")
print("     Result: You saved time not interviewing for low-pay jobs")
print()
print("  2. Alex comes back with $50-75/hr opportunities")
print("     Result: You get interviews at YOUR rate")
print()
print("  3. Alex tries one more lowball offer")
print("     Result: You firmly decline again and move on")
print()
print("Either way: You've established your value and won't work below market rate!")
print()
print("="*80)
print()
print("Copy the response above and send it to Alex!")
print()

