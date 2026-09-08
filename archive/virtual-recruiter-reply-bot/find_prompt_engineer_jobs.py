"""
Prompt Engineer Job Finder
Searches for entry/mid-level prompt engineer roles (not senior)
Integrates with your job-search-automation project
"""

import requests
from datetime import datetime

print("="*80)
print("PROMPT ENGINEER JOB SEARCH")
print("="*80)
print()

# Job search parameters
search_params = {
    'role': 'Prompt Engineer',
    'level': ['entry', 'mid', 'junior', 'associate'],
    'excluded_levels': ['senior', 'lead', 'principal', 'staff', 'director'],
    'location': 'remote',
    'min_salary': 50  # $50/hr or $100k/year equivalent
}

print("Search Criteria:")
print(f"  Role: {search_params['role']}")
print(f"  Level: {', '.join(search_params['level'])}")
print(f"  Location: {search_params['location']}")
print(f"  Min Rate: ${search_params['min_salary']}/hr")
print()
print("="*80)
print()

# Companies known to hire prompt engineers
companies_hiring_prompt_engineers = [
    {
        'name': 'Anthropic',
        'url': 'https://www.anthropic.com/careers',
        'roles': ['Prompt Engineer', 'AI Safety Researcher'],
        'location': 'Remote/San Francisco',
        'notes': 'Leading AI safety company, competitive pay'
    },
    {
        'name': 'OpenAI',
        'url': 'https://openai.com/careers',
        'roles': ['Prompt Engineer', 'Applied AI Researcher'],
        'location': 'Remote/San Francisco',
        'notes': 'ChatGPT creators, excellent benefits'
    },
    {
        'name': 'Scale AI',
        'url': 'https://scale.com/careers',
        'roles': ['Prompt Engineer', 'AI Trainer'],
        'location': 'Remote',
        'notes': 'Data labeling/AI training platform'
    },
    {
        'name': 'Cohere',
        'url': 'https://cohere.com/careers',
        'roles': ['Prompt Engineer', 'Applied Scientist'],
        'location': 'Remote/Toronto',
        'notes': 'Enterprise AI platform'
    },
    {
        'name': 'HuggingFace',
        'url': 'https://huggingface.co/jobs',
        'roles': ['ML Engineer', 'Community Engineer'],
        'location': 'Remote',
        'notes': 'Open source AI community'
    },
    {
        'name': 'Jasper',
        'url': 'https://www.jasper.ai/company/careers',
        'roles': ['Prompt Engineer', 'AI Content Specialist'],
        'location': 'Remote',
        'notes': 'AI content generation'
    },
    {
        'name': 'Writer',
        'url': 'https://writer.com/careers/',
        'roles': ['Prompt Engineer', 'AI Product Specialist'],
        'location': 'Remote',
        'notes': 'Enterprise AI writing platform'
    },
    {
        'name': 'Copy.ai',
        'url': 'https://www.copy.ai/careers',
        'roles': ['Prompt Engineer', 'AI Trainer'],
        'location': 'Remote',
        'notes': 'AI marketing copy generation'
    },
    {
        'name': 'Runway',
        'url': 'https://runwayml.com/careers',
        'roles': ['AI Researcher', 'Prompt Engineer'],
        'location': 'Remote/NYC',
        'notes': 'AI video/creative tools'
    },
    {
        'name': 'Stability AI',
        'url': 'https://stability.ai/careers',
        'roles': ['Prompt Engineer', 'Research Engineer'],
        'location': 'Remote',
        'notes': 'Stable Diffusion creators'
    },
    {
        'name': 'Midjourney',
        'url': 'https://www.midjourney.com/jobs',
        'roles': ['Community Manager', 'Prompt Specialist'],
        'location': 'Remote',
        'notes': 'AI image generation'
    },
    {
        'name': 'Replicate',
        'url': 'https://replicate.com/careers',
        'roles': ['ML Engineer', 'Developer Advocate'],
        'location': 'Remote',
        'notes': 'ML model deployment platform'
    },
    {
        'name': 'Langchain',
        'url': 'https://www.langchain.com/careers',
        'roles': ['Developer Relations', 'AI Engineer'],
        'location': 'Remote',
        'notes': 'LLM application framework'
    },
    {
        'name': 'Pinecone',
        'url': 'https://www.pinecone.io/careers/',
        'roles': ['Solutions Engineer', 'ML Engineer'],
        'location': 'Remote',
        'notes': 'Vector database for AI'
    },
    {
        'name': 'Zapier',
        'url': 'https://zapier.com/jobs',
        'roles': ['AI Product Manager', 'Integration Engineer'],
        'location': 'Remote',
        'notes': 'Automation platform with AI features'
    }
]

print("COMPANIES ACTIVELY HIRING PROMPT ENGINEERS:")
print()

for i, company in enumerate(companies_hiring_prompt_engineers, 1):
    print(f"{i}. {company['name']}")
    print(f"   Careers: {company['url']}")
    print(f"   Typical Roles: {', '.join(company['roles'])}")
    print(f"   Location: {company['location']}")
    print(f"   Notes: {company['notes']}")
    print()

print("="*80)
print("JOB BOARDS FOR PROMPT ENGINEER ROLES:")
print("="*80)
print()

job_boards = [
    {
        'name': 'LinkedIn',
        'url': 'https://www.linkedin.com/jobs/search/?keywords=prompt%20engineer&location=remote',
        'notes': 'Best for seeing who\'s hiring, filter by "Entry Level" or "Associate"'
    },
    {
        'name': 'Indeed',
        'url': 'https://www.indeed.com/jobs?q=prompt+engineer+remote&l=',
        'notes': 'Good for contract and full-time, filter out "Senior"'
    },
    {
        'name': 'AngelList/Wellfound',
        'url': 'https://wellfound.com/role/l/prompt-engineer',
        'notes': 'Startups, often more willing to hire non-senior'
    },
    {
        'name': 'RemoteOK',
        'url': 'https://remoteok.com/remote-prompt-engineer-jobs',
        'notes': 'All remote jobs, good for finding smaller companies'
    },
    {
        'name': 'We Work Remotely',
        'url': 'https://weworkremotely.com/remote-jobs/search?term=prompt+engineer',
        'notes': 'Curated remote jobs'
    },
    {
        'name': 'Dice (Tech focused)',
        'url': 'https://www.dice.com/jobs?q=prompt%20engineer&location=remote',
        'notes': 'Tech-specific job board'
    }
]

for board in job_boards:
    print(f"• {board['name']}")
    print(f"  {board['url']}")
    print(f"  {board['notes']}")
    print()

print("="*80)
print("SEARCH STRATEGY:")
print("="*80)
print()
print("1. Direct Company Applications (Best):")
print("   - Visit career pages above")
print("   - Apply directly to companies")
print("   - Often better response rates")
print()
print("2. LinkedIn Search:")
print("   - Search: 'prompt engineer' NOT senior NOT lead")
print("   - Filter: Remote, Entry Level or Associate")
print("   - Set job alert for daily updates")
print()
print("3. Use Your Job Search Automation:")
print("   - Add prompt engineer to your search criteria")
print("   - Let it find and match roles")
print("   - ARIA will handle recruiter responses")
print()
print("4. Network on Twitter/X:")
print("   - Follow: @AnthropicAI, @OpenAI, @HuggingFace")
print("   - Many post jobs before listing publicly")
print()
print("="*80)
print("SALARY EXPECTATIONS:")
print("="*80)
print()
print("Entry/Mid-level Prompt Engineer rates:")
print("  • Entry level: $40-60/hr ($80-120k/year)")
print("  • Mid level: $50-75/hr ($100-150k/year)")
print("  • Your target: $50-65/hr seems reasonable")
print()
print("Top companies (OpenAI, Anthropic) often pay higher:")
print("  • Entry: $60-80/hr")
print("  • Mid: $75-100/hr")
print()
print("="*80)
print("INTEGRATION WITH YOUR AUTOMATION:")
print("="*80)
print()
print("Option 1: Add to existing job-search-automation")
print("  - Update search keywords to include 'prompt engineer'")
print("  - Configure rate filters ($50-65/hr)")
print("  - Let ARIA handle responses")
print()
print("Option 2: Create dedicated prompt engineer search")
print("  - New automated search script")
print("  - Focus on AI companies")
print("  - Daily scan and alerts")
print()
print("Want me to create either of these? Let me know!")
print()

