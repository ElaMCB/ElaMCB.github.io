/**
 * AI Innovations in QA Testing - Weekly Discovery System
 * 
 * This script monitors GitHub, Hacker News, and research papers for new AI innovations
 * applicable to QA testing. Run weekly via GitHub Actions to track the latest developments.
 * 
 * Usage: node research/ai-innovations-discover.js
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Search keywords for AI innovations in QA/testing
const SEARCH_KEYWORDS = [
    'AI testing innovation',
    'LLM testing framework',
    'AI quality assurance',
    'automated test generation AI',
    'AI test automation',
    'ML testing tools',
    'AI debugging assistant',
    'test generation AI',
    'intelligent testing',
    'AI test coverage',
    'agentic testing',
    'MCP testing',
    'AI test maintenance',
    'self-healing tests',
    'context-aware testing'
];

// Data sources
const SOURCES = {
    github: {
        url: 'https://api.github.com/search/repositories',
        params: (keyword) => `?q=${encodeURIComponent(keyword + ' testing')}&sort=updated&order=desc&per_page=10`,
        headers: {
            'User-Agent': 'AI-Innovations-Tracker',
            'Accept': 'application/vnd.github.v3+json'
        }
    },
    hackerNews: {
        algolia: 'https://hn.algolia.com/api/v1/search',
        params: (keyword) => `?query=${encodeURIComponent(keyword)}&tags=story&hitsPerPage=10&numericFilters=created_at_i>${Math.floor(Date.now() / 1000) - 7 * 24 * 60 * 60}`
    }
};

// Categories for organizing innovations
const CATEGORIES = {
    'test-generation': ['test generation', 'test creation', 'test synthesis'],
    'test-execution': ['test execution', 'test runner', 'test automation'],
    'test-maintenance': ['test maintenance', 'self-healing', 'test repair'],
    'test-debugging': ['test debugging', 'failure analysis', 'test analysis'],
    'test-coverage': ['test coverage', 'coverage analysis', 'coverage optimization'],
    'ai-agents': ['ai agent', 'autonomous testing', 'agentic testing'],
    'mcp-integration': ['mcp', 'model context protocol', 'mcp server'],
    'llm-testing': ['llm testing', 'model testing', 'prompt testing']
};

// Existing innovations to avoid duplicates
const EXISTING_INNOVATIONS = [
    'playwright',
    'selenium',
    'cypress',
    'jest',
    'pytest',
    'mcp testing servers',
    'llm-guardian',
    'cursor',
    'continue.dev'
];

/**
 * Fetch data from a URL
 */
function fetchData(url, headers = {}) {
    return new Promise((resolve, reject) => {
        https.get(url, { headers }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    reject(e);
                }
            });
        }).on('error', reject);
    });
}

/**
 * Search GitHub for AI testing innovations
 */
async function searchGitHub(keyword) {
    try {
        const url = SOURCES.github.url + SOURCES.github.params(keyword);
        const data = await fetchData(url, SOURCES.github.headers);
        
        return data.items
            .filter(repo => {
                const name = repo.name.toLowerCase();
                const desc = (repo.description || '').toLowerCase();
                
                // Check if it's relevant to QA/testing
                const isTestingRelated = desc.includes('test') || desc.includes('qa') || 
                                       desc.includes('quality') || desc.includes('testing') ||
                                       name.includes('test') || name.includes('qa');
                
                // Check if it's not already tracked
                const isNew = !EXISTING_INNOVATIONS.some(existing => 
                    name.includes(existing) || desc.includes(existing)
                );
                
                return isTestingRelated && isNew;
            })
            .map(repo => ({
                name: repo.name,
                description: repo.description,
                url: repo.html_url,
                stars: repo.stargazers_count,
                language: repo.language,
                updated: repo.updated_at,
                source: 'GitHub',
                category: categorizeInnovation(repo.description || repo.name)
            }));
    } catch (error) {
        console.error(`GitHub search error for "${keyword}":`, error.message);
        return [];
    }
}

/**
 * Search Hacker News for AI testing innovations
 */
async function searchHackerNews(keyword) {
    try {
        const url = SOURCES.hackerNews.algolia + SOURCES.hackerNews.params(keyword);
        const data = await fetchData(url);
        
        return data.hits
            .filter(hit => {
                const title = (hit.title || '').toLowerCase();
                const url = (hit.url || '').toLowerCase();
                
                // Check if relevant to testing/QA
                const isRelevant = title.includes('test') || title.includes('qa') || 
                                 title.includes('testing') || title.includes('quality') ||
                                 url.includes('test') || url.includes('testing');
                
                return isRelevant && hit.points > 5; // Filter low-quality posts
            })
            .map(hit => ({
                name: hit.title,
                description: hit.title,
                url: hit.url || `https://news.ycombinator.com/item?id=${hit.objectID}`,
                points: hit.points,
                source: 'Hacker News',
                category: categorizeInnovation(hit.title),
                created: new Date(hit.created_at_i * 1000).toISOString()
            }));
    } catch (error) {
        console.error(`Hacker News search error for "${keyword}":`, error.message);
        return [];
    }
}

/**
 * Categorize innovation based on keywords
 */
function categorizeInnovation(text) {
    const lowerText = text.toLowerCase();
    
    for (const [category, keywords] of Object.entries(CATEGORIES)) {
        if (keywords.some(keyword => lowerText.includes(keyword))) {
            return category;
        }
    }
    
    return 'general';
}

/**
 * Main discovery function
 */
async function discoverInnovations() {
    console.log('🔍 Starting AI Innovations Discovery for QA Testing...\n');
    
    const discoveries = [];
    
    // Search across all keywords
    for (const keyword of SEARCH_KEYWORDS) {
        console.log(`Searching for: "${keyword}"`);
        
        // GitHub search
        const githubResults = await searchGitHub(keyword);
        discoveries.push(...githubResults);
        
        // Hacker News search
        const hnResults = await searchHackerNews(keyword);
        discoveries.push(...hnResults);
        
        // Rate limit protection
        await new Promise(resolve => setTimeout(resolve, 2000));
    }
    
    // Remove duplicates
    const uniqueDiscoveries = Array.from(
        new Map(discoveries.map(item => [item.url, item])).values()
    );
    
    // Sort by relevance and popularity
    uniqueDiscoveries.sort((a, b) => {
        const scoreA = (a.stars || 0) + (a.points || 0) * 10;
        const scoreB = (b.stars || 0) + (b.points || 0) * 10;
        return scoreB - scoreA;
    });
    
    return uniqueDiscoveries;
}

/**
 * Generate markdown report
 */
function generateReport(discoveries) {
    const timestamp = new Date().toISOString().split('T')[0];
    
    let report = `# AI Innovations in QA Testing - Weekly Discovery\n\n`;
    report += `**Discovery Date:** ${timestamp}\n\n`;
    report += `Found **${discoveries.length}** AI innovations applicable to QA testing:\n\n`;
    
    // Group by category
    const byCategory = {};
    discoveries.forEach(innovation => {
        const cat = innovation.category || 'general';
        if (!byCategory[cat]) byCategory[cat] = [];
        byCategory[cat].push(innovation);
    });
    
    // Generate report by category
    for (const [category, items] of Object.entries(byCategory)) {
        report += `## ${category.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}\n\n`;
        
        items.forEach((innovation, index) => {
            report += `### ${index + 1}. ${innovation.name}\n\n`;
            report += `- **Description**: ${innovation.description || 'No description'}\n`;
            report += `- **URL**: ${innovation.url}\n`;
            report += `- **Source**: ${innovation.source}\n`;
            if (innovation.stars) report += `- **GitHub Stars**: ${innovation.stars}\n`;
            if (innovation.points) report += `- **HN Points**: ${innovation.points}\n`;
            if (innovation.language) report += `- **Language**: ${innovation.language}\n`;
            report += `- **QA Testing Application**: ${getQAApplication(category)}\n`;
            report += `\n`;
        });
    }
    
    report += `---\n\n`;
    report += `**Next Steps:**\n`;
    report += `1. Review each innovation for QA testing applicability\n`;
    report += `2. Evaluate potential integration with existing testing workflows\n`;
    report += `3. Test promising innovations in proof-of-concept projects\n`;
    report += `4. Document learnings and best practices\n`;
    report += `5. Share insights with the QA community\n\n`;
    
    return report;
}

/**
 * Get QA testing application description for category
 */
function getQAApplication(category) {
    const applications = {
        'test-generation': 'Automated test case generation, test synthesis, and scenario creation',
        'test-execution': 'Intelligent test execution, parallel testing, and execution optimization',
        'test-maintenance': 'Self-healing tests, automated test repair, and maintenance automation',
        'test-debugging': 'AI-powered debugging, failure root cause analysis, and issue diagnosis',
        'test-coverage': 'Coverage analysis, gap identification, and coverage optimization',
        'ai-agents': 'Autonomous testing agents, multi-agent orchestration, and agentic workflows',
        'mcp-integration': 'Model Context Protocol integration for tool connectivity',
        'llm-testing': 'LLM validation, prompt testing, and model evaluation frameworks',
        'general': 'General AI/ML innovations with potential QA testing applications'
    };
    
    return applications[category] || applications['general'];
}

/**
 * Save discoveries to file
 */
function saveDiscoveries(discoveries) {
    const timestamp = new Date().toISOString().split('T')[0];
    // Save to research/discoveries directory (relative to repo root when run from root)
    const dir = __dirname.endsWith('research') 
        ? path.join(__dirname, 'discoveries')
        : path.join(__dirname, 'research', 'discoveries');
    
    // Create discoveries directory if it doesn't exist
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    
    const filename = path.join(dir, `innovations-${timestamp}.md`);
    const report = generateReport(discoveries);
    fs.writeFileSync(filename, report);
    
    console.log(`\n📝 Report saved to: ${filename}`);
    
    // Save JSON for programmatic processing
    const jsonFilename = path.join(dir, `innovations-${timestamp}.json`);
    const jsonData = {
        scanDate: timestamp,
        totalDiscoveries: discoveries.length,
        discoveries: discoveries.map(d => ({
            name: d.name,
            description: d.description,
            url: d.url,
            stars: d.stars || null,
            points: d.points || null,
            language: d.language || null,
            source: d.source,
            category: d.category,
            updated: d.updated || null,
            created: d.created || null
        }))
    };
    
    fs.writeFileSync(jsonFilename, JSON.stringify(jsonData, null, 2));
    console.log(`📊 JSON data saved to: ${jsonFilename}`);
    
    // Save simplified JSON (just discoveries array) for easy loading
    const simpleJsonFilename = path.join(dir, `innovations-${timestamp}-simple.json`);
    fs.writeFileSync(simpleJsonFilename, JSON.stringify(jsonData.discoveries, null, 2));
    console.log(`📊 Simple JSON saved to: ${simpleJsonFilename}`);
}

/**
 * Run the discovery
 */
(async () => {
    try {
        const discoveries = await discoverInnovations();
        
        console.log(`\n✅ Discovery complete!`);
        console.log(`📊 Found ${discoveries.length} AI innovations for QA testing\n`);
        
        if (discoveries.length > 0) {
            saveDiscoveries(discoveries);
            
            // Print top 10 for quick review
            console.log('\n🔥 Top 10 Discoveries:\n');
            discoveries.slice(0, 10).forEach((innovation, index) => {
                console.log(`${index + 1}. ${innovation.name} (${innovation.source})`);
                console.log(`   Category: ${innovation.category}`);
                console.log(`   ${innovation.url}\n`);
            });
        } else {
            console.log('No new AI innovations discovered this week.');
        }
    } catch (error) {
        console.error('❌ Discovery failed:', error);
        process.exit(1);
    }
})();

