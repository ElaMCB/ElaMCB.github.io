# LLM & Gen AI Research Discovery System

Automated weekly scans to discover:
- New LLM releases (like KMI K2, GPT-4, Claude, etc.)
- Groundbreaking Gen AI research papers
- Model releases on Hugging Face
- GitHub repositories for new LLMs
- Papers with Code updates

## How It Works

1. **Weekly Automated Scans** - Runs every Monday via GitHub Actions
2. **Multiple Sources**:
   - GitHub (new LLM repositories)
   - ArXiv (latest research papers)
   - Hugging Face (new model releases)
   - Papers with Code (SOTA updates)
   - Twitter/X (AI announcements)
   - Perplexity (AI news)

3. **Smart Filtering**:
   - Filters for significant releases (not every small update)
   - Focuses on models with notable capabilities
   - Prioritizes papers with high impact

4. **Display Page** - Shows all discoveries in one place

## Usage

The discovery system runs automatically. Results are displayed on the main page.

Manual trigger: Run `node auto-discover-llms.js` locally

## Sources Monitored

- **GitHub**: New repositories tagged with LLM/AI keywords
- **ArXiv**: Latest papers in cs.CL, cs.AI, cs.LG
- **Hugging Face**: New model releases
- **Papers with Code**: State-of-the-art updates
- **Twitter/X**: AI researcher announcements
- **Perplexity**: AI news aggregator

